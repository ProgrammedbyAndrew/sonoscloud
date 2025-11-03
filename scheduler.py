import schedule
import time
import subprocess
import logging
import os
import signal
from pathlib import Path
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
# FIRE program only — set to -1 to start & end FIRE blocks 1 hour earlier (e.g., winter standard time);
# set to 0 to use original evening times (6:45pm start baseline).
FIRE_SHIFT_HOURS = -1   # <- -1 means start at 5:45pm instead of 6:45pm; 0 returns to normal

# Force all scheduling to use Orlando local time regardless of server timezone.
USE_LOCAL_TZ = True
LOCAL_TZ = "America/New_York"

# Author/edit times as Orlando local times. (Leave True.)
AUTHOR_TIMES_LOCAL = True

# Debug: print a preview of the next-run times after registering jobs
PRINT_LOCAL_SCHEDULE = True
PRINT_LIMIT_PER_DAY = 30

# -------------------------
# Logging & setup
# -------------------------
Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Apply local timezone to the process so the schedule library interprets times as LOCAL_TZ
if USE_LOCAL_TZ:
    try:
        os.environ['TZ'] = LOCAL_TZ
        # time.tzset is available on Unix-like systems (Heroku/Linux). On Windows it is absent.
        if hasattr(time, 'tzset'):
            time.tzset()
        logging.info(f"Timezone set to {LOCAL_TZ} for scheduling.")
    except Exception as e:
        logging.warning(f"Could not set TZ env or tzset(): {e}")

"""
===================== EASY EDIT ZONE =====================
All times below are authored in ORLANDO local time (America/New_York).
1) To move FIRE SHOW earlier/later: set FIRE_SHIFT_HOURS to -1 (earlier) or 0 (normal) above.
2) To add/edit FIRE blocks: edit FIRE_BLOCKS (LOCAL TIMES).
3) To add/edit regular programming: edit SCHEDULES (LOCAL TIMES). Use ("HH:MM", "script.py").
==========================================================
"""


# --------------------------------------
# Helpers
# --------------------------------------
def _to_ampm(hhmm: str) -> str:
    """
    Convert 'HH:MM' (24h) into a compact 'H[[:MM]]am/pm' string.
    Examples: '12:00' -> '12pm', '00:00' -> '12am', '15:30' -> '3:30pm'
    """
    try:
        h = int(hhmm[:2])
        m = int(hhmm[3:5])
    except Exception:
        # If parsing fails, just return the input
        return hhmm
    suffix = "am" if h < 12 else "pm"
    h12 = h % 12
    if h12 == 0:
        h12 = 12
    if m == 0:
        return f"{h12}{suffix}"
    else:
        return f"{h12}:{m:02d}{suffix}"

# --------------------------------------
# Runner
# --------------------------------------

def run_script(script: str, scheduled_time: str | None = None):
    try:
        label_time = scheduled_time or datetime.now().strftime('%H:%M')
        nice = _to_ampm(label_time)
        line = f"{nice} program {script} is playing now..."
        print(line)
        logging.info(line)
        subprocess.run(["python", f"scripts/{script}"], check=True)
    except subprocess.CalledProcessError as e:
        err = f"[{label_time}] ERROR running {script}: {e}"
        print(err)
        logging.error(err)
    except Exception as e:
        err = f"[{label_time}] Unexpected error running {script}: {e}"
        print(err)
        logging.error(err)

# -------------------------
# Helpers for hour-shift with day rollover
# -------------------------
DAY_ORDER = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
PREV_DAY = {d: DAY_ORDER[(i-1) % 7] for i, d in enumerate(DAY_ORDER)}
NEXT_DAY = {d: DAY_ORDER[(i+1) % 7] for i, d in enumerate(DAY_ORDER)}


def _shift_with_dayroll(hhmm: str, hours: int):
    """Return (day_delta, HH:MM) after shifting by 'hours' with 24h wrap."""
    if hours == 0:
        return 0, hhmm
    base = datetime(2000, 1, 1, int(hhmm[:2]), int(hhmm[3:5]))
    shifted = base + timedelta(hours=hours)
    day_delta = (shifted.date() - base.date()).days  # -1, 0, or +1
    return day_delta, shifted.strftime("%H:%M")


def schedule_rows_shifted(rows, anchor_day: str, hours_shift: int):
    """Schedule rows for a given anchor day, shifting by hours_shift with possible day rollover."""
    for tm, script_name in rows:
        delta, shifted_tm = _shift_with_dayroll(tm, hours_shift)
        target_day = anchor_day
        if delta == -1:
            target_day = PREV_DAY[anchor_day]
        elif delta == 1:
            target_day = NEXT_DAY[anchor_day]
        getattr(schedule.every(), target_day).at(shifted_tm).do(run_script, script=script_name, scheduled_time=shifted_tm)

# --------------------------------------
# FIRE SHOW blocks (evening through early morning)
# Author at ~6:45pm baseline; FIRE_SHIFT_HOURS moves these earlier/later.
# --------------------------------------
FIRE_BLOCKS = {
    # Mon evening -> Tue early (baseline start 18:45)
    "monday": [
        ("18:45", "75fireparking.py"), ("19:00", "75fireparking.py"), ("19:50", "75adfire.py"),
    ],
    "tuesday_early": [
        ("00:00", "75fireparking.py"), ("00:50", "75adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Tue evening -> Wed early
    "tuesday": [
        ("18:45", "75fireparking.py"), ("19:00", "75fireparking.py"), ("19:50", "75adfire.py"),
    ],
    "wednesday_early": [
        ("00:00", "75fireparking.py"), ("00:50", "75adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Wed evening -> Thu early (variant script name)
    "wednesday": [
        ("18:45", "75parkingfire.py"), ("19:00", "75parkingfire.py"), ("19:50", "75adfire.py"),
    ],
    "thursday_early": [
        ("00:00", "75parkingfire.py"), ("00:50", "75adfire.py"),
        ("01:00", "75parkingfire.py"), ("01:50", "75adfire.py"),
        ("02:00", "75parkingfire.py"), ("02:50", "75adfire.py"),
        ("03:00", "75parkingfire.py"),
    ],

    # Thu evening -> Fri early (85 series)
    "thursday": [
        ("18:45", "85fireparking.py"), ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
    ],
    "friday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Fri evening -> Sat early (85 series)
    "friday": [
        ("18:45", "85fireparking.py"), ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
    ],
    "saturday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "80adfire.py"),
        ("02:00", "85fireparking.py"), ("02:50", "80adfire.py"),
        ("03:00", "85fireparking.py"),
    ],

    # Sat evening -> Sun early (85 series)
    "saturday": [
        ("18:45", "85fireparking.py"), ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
    ],
    "sunday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "85adfire.py"),
        ("02:00", "85fireparking.py"), ("02:50", "80adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Sun evening -> Mon early (85 fire + 80 ads mix)
    "sunday": [
        ("18:45", "85fireparking.py"), ("19:20", "85fireparking.py"), ("19:50", "80adfire.py"),
    ],
    "monday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "80adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],
}

# --------------------------------------
# NON-FIRE weekly schedules (LOCAL times)
# Fixed typos: '65oarking.py' -> '65parking.py', '70oarking.py' -> '70parking.py'.
# --------------------------------------
SCHEDULES = {
    "monday": [
        ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "65fm.py"), ("12:45", "65sm.py"),
        ("13:00", "75TIGS.py"), ("13:15", "65sm.py"), ("13:30", "70fm.py"), ("13:45", "70sm.py"),
        ("14:00", "70parking.py"), ("14:15", "75TIGS.py"), ("14:30", "70fm.py"), ("14:45", "70sm.py"),
        ("15:00", "75fm.py"), ("15:15", "75sm.py"), ("15:30", "75fm.py"), ("15:45", "75TIGS.py"),
        ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75fm.py"), ("16:45", "75sm.py"),
        ("17:00", "parking.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "75TIGS.py"), ("18:30", "75fm.py"), ("18:45", "75sm.py"),
        ("19:00", "75parking.py"), ("19:15", "75TIGS.py"),
    ],
    "tuesday": [
        # 12:00 AM – 2:00 AM local
        ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        ("02:00", "pause.py"),
        # Day program starting 11:00 AM local
        ("11:00", "65fm.py"), ("11:15", "65sm.py"), ("11:30", "65fm.py"), ("11:45", "65sm.py"),
        ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "65fm.py"), ("12:45", "65sm.py"),
        ("13:00", "65parking.py"), ("13:15", "75TIGS.py"), ("13:30", "65fm.py"), ("13:45", "65sm.py"),
        ("14:00", "65parking.py"), ("14:15", "65sm.py"), ("14:30", "70fm.py"), ("14:45", "70sm.py"),
        ("15:00", "70parking.py"), ("15:15", "70sm.py"), ("15:30", "75TIGS.py"), ("15:45", "70sm.py"),
        ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75TIGS.py"), ("16:45", "75sm.py"),
        ("17:00", "75parking.py"), ("17:15", "75sm.py"), ("17:30", "75TIGS.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "75TIGS.py"),
    ],
    "wednesday": [
        ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        ("02:00", "pause.py"),
        ("11:00", "65fm.py"), ("11:15", "65sm.py"), ("11:30", "75TIGS.py"), ("11:45", "65sm.py"),
        ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "75TIGS.py"), ("12:45", "65sm.py"),
        ("13:00", "65parking.py"), ("13:15", "65sm.py"), ("13:30", "65fm.py"), ("13:45", "65sm.py"),
        ("14:00", "75TIGS.py"), ("14:15", "65sm.py"), ("14:30", "65fm.py"), ("14:45", "70sm.py"),
        ("15:00", "70parking.py"), ("15:15", "70sm.py"), ("15:30", "75TIGS.py"), ("15:45", "70sm.py"),
        ("16:00", "70parking.py"), ("16:15", "70sm.py"), ("16:30", "75TIGS.py"), ("16:45", "75sm.py"),
        ("17:00", "80parking.py"), ("17:15", "80sm.py"), ("17:30", "80fm.py"), ("17:45", "80sm.py"),
        ("18:00", "80parking.py"), ("18:15", "80sm.py"),
    ],
    "thursday": [
        ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        ("02:00", "pause.py"),
        ("11:00", "75TIGS.py"), ("11:15", "75sm.py"), ("11:30", "75fm.py"), ("11:45", "75sm.py"),
        ("12:00", "75parking.py"), ("12:15", "75TIGS.py"), ("12:30", "75fm.py"), ("12:45", "75sm.py"),
        ("13:00", "75TIGS.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
        ("14:00", "75parking.py"), ("14:15", "75sm.py"), ("14:30", "75TIGS.py"), ("14:45", "75sm.py"),
        ("15:00", "80parking.py"), ("15:15", "80sm.py"), ("15:30", "80fm.py"), ("15:45", "80sm.py"),
        ("16:00", "80parking.py"), ("16:15", "80sm.py"), ("16:30", "80fm.py"), ("16:45", "80sm.py"),
        ("17:00", "80parking.py"), ("17:15", "80ad.py"), ("17:30", "80fm.py"), ("17:45", "80sm.py"),
        ("18:00", "80parking.py"), ("18:15", "80sm.py"),
    ],
    "friday": [
        # 12:00 AM – 1:45 AM local
        ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        # 2:00 AM – 4:00 AM local (50-series)
        ("02:00", "50parking.py"), ("02:15", "50sm.py"), ("02:30", "50sm.py"), ("02:45", "50sm.py"),
        ("03:00", "50parking.py"), ("03:15", "50sm.py"), ("03:30", "50sm.py"), ("03:45", "50sm.py"),
        ("04:00", "pause.py"),
        # Day program starting 11:00 AM local
        ("11:00", "75fm.py"), ("11:15", "75sm.py"), ("11:30", "75TIGS.py"), ("11:45", "75sm.py"),
        ("12:00", "75fm.py"), ("12:15", "75sm.py"), ("12:30", "75fm.py"), ("12:45", "75TIGS.py"),
        ("13:00", "75parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
        ("14:00", "75parking.py"), ("14:15", "75TIGS.py"), ("14:30", "75fm.py"), ("14:45", "75sm.py"),
        ("15:00", "80parking.py"), ("15:15", "80sm.py"), ("15:30", "80fm.py"), ("15:45", "80sm.py"),
        ("16:00", "90parking.py"), ("16:15", "90ad.py"), ("16:30", "90fm.py"), ("16:45", "90sm.py"),
        ("17:00", "90parking.py"), ("17:15", "90ad.py"), ("17:30", "90fm.py"), ("17:45", "90fm.py"),
        ("18:00", "90parking.py"), ("18:15", "90sm.py"),
    ],
    "saturday": [
        # 12:00 AM – 4:00 AM local
        ("00:00", "70parking.py"), ("00:00", "70.py"),
        ("00:15", "70sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        ("02:00", "65sm.py"), ("02:15", "65sm.py"), ("02:30", "65sm.py"), ("02:45", "65sm.py"),
        ("03:00", "65parking.py"), ("03:15", "65sm.py"), ("03:30", "65sm.py"), ("03:45", "65sm.py"),
        ("04:00", "pause.py"),
        # Day program starting 11:00 AM local
        ("11:00", "75fm.py"), ("11:15", "75sm.py"), ("11:30", "75parking.py"), ("11:45", "75sm.py"),
        ("12:00", "75parking.py"), ("12:15", "75sm.py"), ("12:30", "75fm.py"), ("12:45", "75sm.py"),
        ("13:00", "75parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
        ("14:00", "75parking.py"), ("14:15", "75sm.py"), ("14:30", "75ad.py"), ("14:45", "75sm.py"),
        ("15:00", "75parking.py"), ("15:15", "75sm.py"), ("15:30", "75ad.py"), ("15:45", "75sm.py"),
        ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75ad.py"), ("16:45", "75sm.py"),
        ("17:00", "85parking.py"), ("17:15", "85sm.py"), ("17:30", "85ad.py"), ("17:45", "85sm.py"),
        ("18:00", "85parking.py"), ("18:15", "85sm.py"),
    ],
    "sunday": [
        ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
        ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
        ("02:00", "pause.py"),
        ("11:00", "70fm.py"), ("11:15", "70sm.py"), ("11:30", "70parking.py"), ("11:45", "70sm.py"),
        ("12:00", "70fm.py"), ("12:15", "70sm.py"), ("12:30", "70fm.py"), ("12:45", "70sm.py"),
        ("13:00", "70parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
        ("14:00", "75parking.py"), ("14:15", "80sm.py"), ("14:30", "80fm.py"), ("14:45", "80sm.py"),
        ("15:00", "85parking.py"), ("15:15", "85ad.py"), ("15:30", "85fm.py"), ("15:45", "85fm.py"),
        ("16:00", "85parking.py"), ("16:15", "85sm.py"), ("16:30", "85sm.py"), ("16:45", "85ad.py"),
        ("17:00", "85parking.py"), ("17:15", "85sm.py"), ("17:30", "85sm.py"), ("17:45", "85sm.py"),
        ("18:00", "85parking.py"),
    ],
}

# --------------------------------------
# Register jobs
# --------------------------------------

def schedule_tasks():
    # 1) Regular (non-fire) — times are authored in LOCAL time; schedule directly
    for day in DAY_ORDER:
        schedule_rows_shifted(SCHEDULES.get(day, []), day, 0)

    # 2) Fire — authored in LOCAL time; apply FIRE_SHIFT_HOURS only
    schedule_rows_shifted(FIRE_BLOCKS.get("monday", []),          "monday",   FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("tuesday_early", []),   "tuesday",  FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("tuesday", []),         "tuesday",  FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("wednesday_early", []), "wednesday",FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("wednesday", []),       "wednesday",FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("thursday_early", []),  "thursday", FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("thursday", []),        "thursday", FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("friday_early", []),    "friday",   FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("friday", []),          "friday",   FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("saturday_early", []),  "saturday", FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("saturday", []),        "saturday", FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("sunday_early", []),    "sunday",   FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("sunday", []),          "sunday",   FIRE_SHIFT_HOURS)
    schedule_rows_shifted(FIRE_BLOCKS.get("monday_early", []),    "monday",   FIRE_SHIFT_HOURS)


def _graceful_exit(sig, _frame):
    logging.info(f"Received signal {sig}. Exiting scheduler loop.")
    raise SystemExit(0)

signal.signal(signal.SIGINT, _graceful_exit)
signal.signal(signal.SIGTERM, _graceful_exit)

# Register jobs
schedule_tasks()

logging.info(f"Scheduler started. FIRE_SHIFT_HOURS={FIRE_SHIFT_HOURS} (fire program only)")
logging.info(f"Process local time now: {datetime.now()} | UTC now: {datetime.utcnow()}")
logging.info(f"Authoring mode: LOCAL | TZ={LOCAL_TZ}")

# Optional: print a short summary of the schedule (local time)
if PRINT_LOCAL_SCHEDULE:
    def _job_script_name(job) -> str:
        try:
            jf = job.job_func
            # Prefer kwargs as we register jobs with keyword args
            if hasattr(jf, 'keywords') and isinstance(jf.keywords, dict):
                name = jf.keywords.get('script')
                if name:
                    return str(name)
            # Fallback to positional args
            if hasattr(jf, 'args') and jf.args:
                return str(jf.args[0])
            # Last resort: best-effort parse from repr
            r = repr(jf)
            return r
        except Exception:
            return ""
    try:
        jobs = schedule.get_jobs()
        print(f"\nLoaded {len(jobs)} scheduled jobs in {LOCAL_TZ}.")
        # Find the absolute next job to run
        next_job = None
        for j in jobs:
            if j.next_run is None:
                continue
            if next_job is None or j.next_run < next_job.next_run:
                next_job = j
        if next_job:
            script_name = _job_script_name(next_job)
            when_str = next_job.next_run.strftime('%A %H:%M')
            if script_name:
                print(f"Next run: {when_str} ({script_name})")
            else:
                print(f"Next run: {when_str}")
        print("Scheduler running... Press Ctrl+C to exit.")
    except Exception as e:
        logging.warning(f"Could not summarize schedule: {e}")

# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)