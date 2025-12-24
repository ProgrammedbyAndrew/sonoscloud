import asyncio
import logging
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz
from ..config import get_settings
from ..database import database, schedule_slots, execution_logs
from .sonos_api import sonos_api

settings = get_settings()
logger = logging.getLogger(__name__)

# Program type display names
PROGRAM_TYPE_NAMES = {
    "sm": "Social Media Ad",
    "ad": "Business Ad",
    "fm": "Flea Market Ad",
    "parking": "Parking Announcement",
    "adfire": "Fire Show Ad",
    "fireparking": "Fire Show Parking",
    "TIGS": "Gift Shop Ad",
    "pause": "Pause"
}


class SchedulerService:
    """APScheduler-based service for running scheduled programs"""

    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.timezone = pytz.timezone(settings.timezone)
        self.current_program: Optional[str] = None
        self.is_running = False
        self.fire_show_mode = False  # Fire Show Mode state
        self._fire_show_job_id = "fire_show_hourly"
        self._midnight_reset_job_id = "midnight_reset"

    def start(self):
        """Start the scheduler"""
        if self.scheduler is None:
            self.scheduler = AsyncIOScheduler(timezone=self.timezone)
        if not self.scheduler.running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")

            # Always add the midnight reset job
            self._add_midnight_reset_job()

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")

    def _add_midnight_reset_job(self):
        """Add job to reset Fire Show Mode at midnight"""
        if not self.scheduler:
            return

        # Remove existing if present
        try:
            self.scheduler.remove_job(self._midnight_reset_job_id)
        except Exception:
            pass

        # Add midnight reset job (runs at 00:00 every day)
        trigger = CronTrigger(hour=0, minute=0, timezone=self.timezone)
        self.scheduler.add_job(
            self._midnight_reset,
            trigger=trigger,
            id=self._midnight_reset_job_id,
            replace_existing=True
        )
        logger.info("Midnight reset job scheduled")

    async def _midnight_reset(self):
        """Reset Fire Show Mode at midnight"""
        if self.fire_show_mode:
            logger.info("Midnight reset: Disabling Fire Show Mode")
            await self.disable_fire_show_mode()

    async def enable_fire_show_mode(self):
        """Enable Fire Show Mode - runs 85adfire.py every hour"""
        if not self.scheduler:
            self.start()

        self.fire_show_mode = True
        logger.info("Fire Show Mode ENABLED - will run 85adfire.py hourly")

        # Remove existing fire show job if present
        try:
            self.scheduler.remove_job(self._fire_show_job_id)
        except Exception:
            pass

        # Run it immediately first
        await self.run_program("85adfire.py")

        # Add hourly job (runs at the top of each hour)
        trigger = IntervalTrigger(hours=1, timezone=self.timezone)
        self.scheduler.add_job(
            self.run_program,
            trigger=trigger,
            args=["85adfire.py"],
            id=self._fire_show_job_id,
            replace_existing=True
        )

        return {"status": "enabled", "message": "Fire Show Mode enabled - running 85adfire.py every hour"}

    async def disable_fire_show_mode(self):
        """Disable Fire Show Mode - return to regular programming"""
        self.fire_show_mode = False
        logger.info("Fire Show Mode DISABLED - returning to regular schedule")

        # Remove the hourly fire show job
        try:
            self.scheduler.remove_job(self._fire_show_job_id)
        except Exception:
            pass

        return {"status": "disabled", "message": "Fire Show Mode disabled - regular programming resumed"}

    def get_fire_show_status(self) -> dict:
        """Get Fire Show Mode status"""
        return {
            "enabled": self.fire_show_mode,
            "next_reset": "Midnight (00:00)" if self.fire_show_mode else None,
            "program": "85adfire.py",
            "interval": "Every hour"
        }

    async def load_schedule_from_db(self):
        """Load schedule from database and register jobs"""
        if not self.scheduler:
            self.start()

        # Clear existing jobs except fire show and midnight reset
        for job in self.scheduler.get_jobs():
            if job.id not in [self._fire_show_job_id, self._midnight_reset_job_id]:
                job.remove()

        # Load active schedule slots from database
        query = schedule_slots.select().where(schedule_slots.c.is_active == True)
        rows = await database.fetch_all(query)

        job_count = 0
        for row in rows:
            day_of_week = row["day_of_week"].lower()
            time_str = row["time"]
            program_name = row["program_name"]

            # Parse time
            hour, minute = map(int, time_str.split(":"))

            # Map day names to APScheduler day_of_week values
            day_map = {
                "monday": "mon",
                "tuesday": "tue",
                "wednesday": "wed",
                "thursday": "thu",
                "friday": "fri",
                "saturday": "sat",
                "sunday": "sun"
            }

            trigger = CronTrigger(
                day_of_week=day_map.get(day_of_week, day_of_week),
                hour=hour,
                minute=minute,
                timezone=self.timezone
            )

            self.scheduler.add_job(
                self.run_program,
                trigger=trigger,
                args=[program_name],
                id=f"{day_of_week}_{time_str}_{program_name}",
                replace_existing=True
            )
            job_count += 1

        logger.info(f"Loaded {job_count} scheduled jobs from database")
        return job_count

    async def run_program(self, program_name: str):
        """Execute a program"""
        self.current_program = program_name
        logger.info(f"Running program: {program_name}")

        try:
            # Handle pause specially
            if program_name == "pause.py" or program_name == "pause":
                await sonos_api.pause_all()
                await self._log_execution(program_name, "success")
                self.current_program = None
                return

            # Extract volume from program name (e.g., "75fm.py" -> 75)
            volume = self._extract_volume(program_name)
            program_type = self._extract_type(program_name)

            # Get favorite IDs based on program type
            favorite_sequence = self._get_favorite_sequence(program_type)

            # Execute the program
            group_id = await sonos_api.ensure_group()

            for favorite_id, duration, vol_override in favorite_sequence:
                use_volume = vol_override if vol_override else volume
                await sonos_api.load_favorite(group_id, favorite_id)
                await sonos_api.set_all_volumes(use_volume)
                await sonos_api.play(group_id)

                if duration > 0:
                    await asyncio.sleep(duration)

            await self._log_execution(program_name, "success")
            logger.info(f"Program {program_name} completed successfully")

        except Exception as e:
            logger.error(f"Error running program {program_name}: {e}")
            await self._log_execution(program_name, "error", str(e))

        finally:
            self.current_program = None

    def _extract_volume(self, program_name: str) -> int:
        """Extract volume level from program name"""
        # Remove .py extension
        name = program_name.replace(".py", "")
        # Extract leading digits
        digits = ""
        for char in name:
            if char.isdigit():
                digits += char
            else:
                break
        return int(digits) if digits else 75

    def _extract_type(self, program_name: str) -> str:
        """Extract program type from program name"""
        name = program_name.replace(".py", "")
        # Remove leading digits
        for i, char in enumerate(name):
            if not char.isdigit():
                return name[i:]
        return "fm"

    def get_program_display_name(self, program_name: str) -> str:
        """Get human-readable display name for a program"""
        volume = self._extract_volume(program_name)
        prog_type = self._extract_type(program_name)
        type_name = PROGRAM_TYPE_NAMES.get(prog_type, prog_type)
        return f"{type_name} @ {volume}%"

    def _get_favorite_sequence(self, program_type: str) -> list[tuple[str, int, Optional[int]]]:
        """Get the favorite playlist sequence for a program type
        Returns list of (favorite_id, sleep_duration, volume_override)
        """
        # Default sequences based on the existing scripts
        sequences = {
            "ad": [("28", 35, 85), ("29", 39, 85), ("33", 0, None)],
            "fm": [("28", 35, 85), ("29", 39, 85), ("33", 0, None)],
            "sm": [("28", 14, 85), ("35", 15, 85), ("33", 0, None)],
            "parking": [("30", 30, 85), ("33", 0, None)],
            "TIGS": [("31", 45, 85), ("33", 0, None)],
            "adfire": [("28", 35, 85), ("29", 39, 85), ("34", 0, None)],
            "fireparking": [("30", 30, 85), ("34", 0, None)],
        }
        return sequences.get(program_type, [("33", 0, None)])

    async def _log_execution(self, program_name: str, status: str, error_message: str = None):
        """Log program execution to database"""
        query = execution_logs.insert().values(
            program_name=program_name,
            executed_at=datetime.now(self.timezone),
            status=status,
            error_message=error_message
        )
        await database.execute(query)

    def get_next_job(self) -> Optional[dict]:
        """Get the next scheduled job"""
        if not self.scheduler:
            return None

        jobs = self.scheduler.get_jobs()
        if not jobs:
            return None

        # Filter out system jobs
        regular_jobs = [j for j in jobs if j.id not in [self._fire_show_job_id, self._midnight_reset_job_id]]
        if not regular_jobs:
            return None

        next_job = min(regular_jobs, key=lambda j: j.next_run_time if j.next_run_time else datetime.max.replace(tzinfo=self.timezone))
        if next_job and next_job.next_run_time:
            program = next_job.args[0] if next_job.args else "unknown"
            return {
                "program": program,
                "display_name": self.get_program_display_name(program),
                "time": next_job.next_run_time.strftime("%H:%M"),
                "day": next_job.next_run_time.strftime("%A"),
                "datetime": next_job.next_run_time.isoformat()
            }
        return None

    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            "is_running": self.is_running,
            "current_program": self.current_program,
            "current_program_display": self.get_program_display_name(self.current_program) if self.current_program else None,
            "job_count": len(self.scheduler.get_jobs()) if self.scheduler else 0,
            "next_job": self.get_next_job(),
            "fire_show_mode": self.get_fire_show_status()
        }


# Global instance
scheduler_service = SchedulerService()
