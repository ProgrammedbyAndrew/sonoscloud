from fastapi import APIRouter, HTTPException
from datetime import datetime
import pytz
from ..database import database, execution_logs
from ..services.scheduler_service import scheduler_service
from ..services.sonos_api import sonos_api
from ..config import get_settings

router = APIRouter(prefix="/system", tags=["system"])
settings = get_settings()


@router.get("/status")
async def get_system_status():
    """Get overall system status"""
    try:
        # Check Sonos API connectivity
        sonos_connected = False
        try:
            await sonos_api.ensure_valid_token()
            sonos_connected = True
        except Exception:
            pass

        # Get scheduler status
        scheduler_status = scheduler_service.get_status()

        # Get current time in venue timezone
        tz = pytz.timezone(settings.timezone)
        current_time = datetime.now(tz)

        return {
            "status": "healthy" if sonos_connected else "degraded",
            "sonos_connected": sonos_connected,
            "scheduler": scheduler_status,
            "timezone": settings.timezone,
            "current_time": current_time.isoformat(),
            "current_time_display": current_time.strftime("%A %I:%M %p")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_execution_logs(limit: int = 50):
    """Get recent execution logs"""
    query = execution_logs.select().order_by(
        execution_logs.c.executed_at.desc()
    ).limit(limit)
    rows = await database.fetch_all(query)

    return {
        "logs": [
            {
                "id": row["id"],
                "program_name": row["program_name"],
                "executed_at": row["executed_at"].isoformat() if row["executed_at"] else None,
                "status": row["status"],
                "error_message": row["error_message"]
            }
            for row in rows
        ]
    }


@router.post("/restart-scheduler")
async def restart_scheduler():
    """Restart the scheduler"""
    try:
        scheduler_service.stop()
        scheduler_service.start()
        job_count = await scheduler_service.load_schedule_from_db()
        return {"message": f"Scheduler restarted with {job_count} jobs"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time")
async def get_current_time():
    """Get current time in venue timezone"""
    tz = pytz.timezone(settings.timezone)
    current_time = datetime.now(tz)

    return {
        "timezone": settings.timezone,
        "iso": current_time.isoformat(),
        "display": current_time.strftime("%A, %B %d, %Y %I:%M:%S %p"),
        "time_24h": current_time.strftime("%H:%M:%S"),
        "day_of_week": current_time.strftime("%A").lower()
    }


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# Fire Show Mode endpoints
@router.get("/fire-show-mode")
async def get_fire_show_mode():
    """Get Fire Show Mode status"""
    return scheduler_service.get_fire_show_status()


@router.post("/fire-show-mode/enable")
async def enable_fire_show_mode():
    """Enable Fire Show Mode - runs 85adfire.py every hour until midnight"""
    try:
        result = await scheduler_service.enable_fire_show_mode()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fire-show-mode/disable")
async def disable_fire_show_mode():
    """Disable Fire Show Mode - return to regular programming"""
    try:
        result = await scheduler_service.disable_fire_show_mode()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fire-show-mode/toggle")
async def toggle_fire_show_mode():
    """Toggle Fire Show Mode on/off"""
    try:
        if scheduler_service.fire_show_mode:
            result = await scheduler_service.disable_fire_show_mode()
        else:
            result = await scheduler_service.enable_fire_show_mode()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
