import schedule
import time
import subprocess
import logging
import os
import signal
from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIG (all times are America/New_York — no UTC conversions in code)
# -----------------------------------------------------------------------------
LOCAL_TZ = "America/New_York"
USE_LOCAL_TZ = True
PRINT_LOCAL_SCHEDULE = True

# -------------------------
# Logging & setup
# -------------------------
Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Force the process timezone so the 'schedule' library interprets times as Orlando
if USE_LOCAL_TZ:
    try:
        os.environ["TZ"] = LOCAL_TZ
        if hasattr(time, "tzset"):
            time.tzset()
        logging.info(f"Timezone set to {LOCAL_TZ} for scheduling.")
    except Exception as e:
        logging.warning(f"Could not set TZ env or tzset(): {e}")

"""
===================== EASY EDIT ZONE =====================
Each day is split into simple blocks you can edit directly.

- AM      = after-midnight items (e.g., 00:00–04:00) — NOT fire show
- DAY     = day programming
- PM_FIRE = FIRE SHOW every night from 17:45 (5:45pm) to 23:00 (11:00pm)

No shifts, no rollover tricks, no UTC math. What you type is what runs in Orlando.
==========================================================
"""

# -------------------------
# Helpers
# -------------------------
def _to_ampm(hhmm: str) -> str:
    try:
        h = int(hhmm[:2]); m = int(hhmm[3:5])
    except Exception:
        return hhmm
    suffix = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}{suffix}" if m == 0 else f"{h12}:{m:02d}{suffix}"

def run_script(script: str, scheduled_time: str | None = None):
    try:
        label_time = scheduled_time or datetime.now().strftime("%H:%M")
        nice = _to_ampm(label_time)
        line = f"{nice} program {script} is playing now..."
        print(line)
        logging.info(line)
        subprocess.run(["python", f"scripts/{script}"], check=True)
    except subprocess.CalledProcessError as e:
        err = f"[{label_time}] ERROR running {script}: {e}"
        print(err); logging.error(err)
    except Exception as e:
        err = f"[{label_time}] Unexpected error running {script}: {e}"
        print(err); logging.error(err)

def schedule_rows(rows, weekday: str):
    for hhmm, script_name in rows:
        getattr(schedule.every(), weekday).at(hhmm).do(
            run_script, script=script_name, scheduled_time=hhmm
        )

# -----------------------------------------------------------------------------
# BLOCKED SCHEDULES (ALL LOCAL ORLANDO TIMES)
# -----------------------------------------------------------------------------

DAY_ORDER = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

BLOCKS = {
    "monday": {
        "AM": [],
        "DAY": [
            ("12:00","65fm.py"), ("12:15","65sm.py"), ("12:30","65fm.py"), ("12:45","65sm.py"),
            ("13:00","75TIGS.py"), ("13:15","65sm.py"), ("13:30","70fm.py"), ("13:45","70sm.py"),
            ("14:00","70parking.py"), ("14:15","75TIGS.py"), ("14:30","70fm.py"), ("14:45","70sm.py"),
            ("15:00","75fm.py"), ("15:15","75sm.py"), ("15:30","75fm.py"), ("15:45","75TIGS.py"),
            ("16:00","75parking.py"), ("16:15","75sm.py"), ("16:30","75fm.py"), ("16:45","75sm.py"),
            ("17:00","parking.py"), ("17:15","75sm.py"), ("17:30","75fm.py"), ("17:45","75sm.py"),
            ("18:00","75parking.py"), ("18:15","75TIGS.py"), ("18:30","75fm.py"), ("18:45","75sm.py"),
            ("19:00","75parking.py"), ("19:15","75TIGS.py"),
        ],
        # FIRE SHOW: 5:45pm → 11:00pm
        "PM_FIRE": [
            ("17:45","75fireparking.py"), ("18:00","75fireparking.py"), ("18:50","75adfire.py"),
            ("19:00","75fireparking.py"), ("19:50","75adfire.py"),
            ("20:00","75fireparking.py"), ("20:50","75adfire.py"),
            ("21:00","75fireparking.py"), ("21:50","75adfire.py"),
            ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
            ("23:00","75fireparking.py"),
        ],
    },

    "tuesday": {
        "AM": [
            ("00:00","65parking.py"), ("00:15","65sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","pause.py"),
        ],
        "DAY": [
            ("11:00","65fm.py"), ("11:15","65sm.py"), ("11:30","65fm.py"), ("11:45","65sm.py"),
            ("12:00","65fm.py"), ("12:15","65sm.py"), ("12:30","65fm.py"), ("12:45","65sm.py"),
            ("13:00","65parking.py"), ("13:15","75TIGS.py"), ("13:30","65fm.py"), ("13:45","65sm.py"),
            ("14:00","65parking.py"), ("14:15","65sm.py"), ("14:30","70fm.py"), ("14:45","70sm.py"),
            ("15:00","70parking.py"), ("15:15","70sm.py"), ("15:30","75TIGS.py"), ("15:45","70sm.py"),
            ("16:00","75parking.py"), ("16:15","75sm.py"), ("16:30","75TIGS.py"), ("16:45","75sm.py"),
            ("17:00","75parking.py"), ("17:15","75sm.py"), ("17:30","75TIGS.py"), ("17:45","75sm.py"),
            ("18:00","75parking.py"), ("18:15","75TIGS.py"),
        ],
        "PM_FIRE": [
            ("17:45","75fireparking.py"), ("18:00","75fireparking.py"), ("18:50","75adfire.py"),
            ("19:00","75fireparking.py"), ("19:50","75adfire.py"),
            ("20:00","75fireparking.py"), ("20:50","75adfire.py"),
            ("21:00","75fireparking.py"), ("21:50","75adfire.py"),
            ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
            ("23:00","75fireparking.py"),
        ],
    },

    "wednesday": {
        "AM": [
            ("00:00","65parking.py"), ("00:15","65sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","pause.py"),
        ],
        "DAY": [
            ("11:00","65fm.py"), ("11:15","65sm.py"), ("11:30","75TIGS.py"), ("11:45","65sm.py"),
            ("12:00","65fm.py"), ("12:15","65sm.py"), ("12:30","75TIGS.py"), ("12:45","65sm.py"),
            ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65fm.py"), ("13:45","65sm.py"),
            ("14:00","75TIGS.py"), ("14:15","65sm.py"), ("14:30","65fm.py"), ("14:45","70sm.py"),
            ("15:00","70parking.py"), ("15:15","70sm.py"), ("15:30","75TIGS.py"), ("15:45","70sm.py"),
            ("16:00","70parking.py"), ("16:15","70sm.py"), ("16:30","75TIGS.py"), ("16:45","75sm.py"),
            ("17:00","80parking.py"), ("17:15","80sm.py"), ("17:30","80fm.py"), ("17:45","80sm.py"),
            ("18:00","80parking.py"), ("18:15","80sm.py"),
        ],
        "PM_FIRE": [
            ("17:45","75parkingfire.py"), ("18:00","75parkingfire.py"), ("18:50","75adfire.py"),
            ("19:00","75parkingfire.py"), ("19:50","75adfire.py"),
            ("20:00","75parkingfire.py"), ("20:50","75adfire.py"),
            ("21:00","75parkingfire.py"), ("21:50","75adfire.py"),
            ("22:00","75parkingfire.py"), ("22:50","75adfire.py"),
            ("23:00","75parkingfire.py"),
        ],
    },

    "thursday": {
        "AM": [
            ("00:00","65parking.py"), ("00:15","65sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","pause.py"),
        ],
        "DAY": [
            ("11:00","75TIGS.py"), ("11:15","75sm.py"), ("11:30","75fm.py"), ("11:45","75sm.py"),
            ("12:00","75parking.py"), ("12:15","75TIGS.py"), ("12:30","75fm.py"), ("12:45","75sm.py"),
            ("13:00","75TIGS.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
            ("14:00","75parking.py"), ("14:15","75sm.py"), ("14:30","75TIGS.py"), ("14:45","75sm.py"),
            ("15:00","80parking.py"), ("15:15","80sm.py"), ("15:30","80fm.py"), ("15:45","80sm.py"),
            ("16:00","80parking.py"), ("16:15","80sm.py"), ("16:30","80fm.py"), ("16:45","80sm.py"),
            ("17:00","80parking.py"), ("17:15","80ad.py"), ("17:30","80fm.py"), ("17:45","80sm.py"),
            ("18:00","80parking.py"), ("18:15","80sm.py"),
        ],
        "PM_FIRE": [
            ("17:45","85fireparking.py"), ("18:00","85fireparking.py"), ("18:50","85adfire.py"),
            ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
            ("20:00","85fireparking.py"), ("20:50","85adfire.py"),
            ("21:00","85fireparking.py"), ("21:50","85adfire.py"),
            ("22:00","85fireparking.py"), ("22:50","85adfire.py"),
            ("23:00","85fireparking.py"),
        ],
    },

    "friday": {
        "AM": [
            ("00:00","65parking.py"), ("00:15","65sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","50parking.py"), ("02:15","50sm.py"), ("02:30","50sm.py"), ("02:45","50sm.py"),
            ("03:00","50parking.py"), ("03:15","50sm.py"), ("03:30","50sm.py"), ("03:45","50sm.py"),
            ("04:00","pause.py"),
        ],
        "DAY": [
            ("11:00","75fm.py"), ("11:15","75sm.py"), ("11:30","75TIGS.py"), ("11:45","75sm.py"),
            ("12:00","75fm.py"), ("12:15","75sm.py"), ("12:30","75fm.py"), ("12:45","75TIGS.py"),
            ("13:00","75parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
            ("14:00","75parking.py"), ("14:15","75TIGS.py"), ("14:30","75fm.py"), ("14:45","75sm.py"),
            ("15:00","80parking.py"), ("15:15","80sm.py"), ("15:30","80fm.py"), ("15:45","80sm.py"),
            ("16:00","90parking.py"), ("16:15","90ad.py"), ("16:30","90fm.py"), ("16:45","90sm.py"),
            ("17:00","90parking.py"), ("17:15","90ad.py"), ("17:30","90fm.py"), ("17:45","90fm.py"),
            ("18:00","90parking.py"), ("18:15","90sm.py"),
        ],
        "PM_FIRE": [
            ("17:45","85fireparking.py"), ("18:00","85fireparking.py"), ("18:50","85adfire.py"),
            ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
            ("20:00","85fireparking.py"), ("20:50","85adfire.py"),
            ("21:00","85fireparking.py"), ("21:50","85adfire.py"),
            ("22:00","85fireparking.py"), ("22:50","85adfire.py"),
            ("23:00","85fireparking.py"),
        ],
    },

    "saturday": {
        "AM": [
            ("00:00","70parking.py"), ("00:00","70.py"),
            ("00:15","70sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","65sm.py"), ("02:15","65sm.py"), ("02:30","65sm.py"), ("02:45","65sm.py"),
            ("03:00","65parking.py"), ("03:15","65sm.py"), ("03:30","65sm.py"), ("03:45","65sm.py"),
            ("04:00","pause.py"),
        ],
        "DAY": [
            ("11:00","75fm.py"), ("11:15","75sm.py"), ("11:30","75parking.py"), ("11:45","75sm.py"),
            ("12:00","75parking.py"), ("12:15","75sm.py"), ("12:30","75fm.py"), ("12:45","75sm.py"),
            ("13:00","75parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
            ("14:00","75parking.py"), ("14:15","75sm.py"), ("14:30","75ad.py"), ("14:45","75sm.py"),
            ("15:00","75parking.py"), ("15:15","75sm.py"), ("15:30","75ad.py"), ("15:45","75sm.py"),
            ("16:00","75parking.py"), ("16:15","75sm.py"),
            ("17:00","85parking.py"), ("17:15","85sm.py"), ("17:30","85ad.py"), ("17:45","85sm.py"),
            ("18:00","85parking.py"), ("18:15","85sm.py"),
        ],
        "PM_FIRE": [
            ("17:45","85fireparking.py"), ("18:00","85fireparking.py"), ("18:50","85adfire.py"),
            ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
            ("20:00","85fireparking.py"), ("20:50","85adfire.py"),
            ("21:00","85fireparking.py"), ("21:50","85adfire.py"),
            ("22:00","85fireparking.py"), ("22:50","85adfire.py"),
            ("23:00","85fireparking.py"),
        ],
    },

    "sunday": {
        "AM": [
            ("00:00","65parking.py"), ("00:15","65sm.py"), ("00:30","65sm.py"), ("00:45","65sm.py"),
            ("01:00","65parking.py"), ("01:15","65sm.py"), ("01:30","65sm.py"), ("01:45","65sm.py"),
            ("02:00","pause.py"),
        ],
        "DAY": [
            ("11:00","70fm.py"), ("11:15","70sm.py"), ("11:30","70parking.py"), ("11:45","70sm.py"),
            ("12:00","70fm.py"), ("12:15","70sm.py"), ("12:30","70fm.py"), ("12:45","70sm.py"),
            ("13:00","70parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
            ("14:00","75parking.py"), ("14:15","80sm.py"), ("14:30","80fm.py"), ("14:45","80sm.py"),
            ("15:00","85parking.py"), ("15:15","85ad.py"), ("15:30","85fm.py"), ("15:45","85fm.py"),
            ("16:00","85parking.py"), ("16:15","85sm.py"), ("16:30","85sm.py"), ("16:45","85ad.py"),
            ("17:00","85parking.py"), ("17:15","85sm.py"), ("17:30","85sm.py"), ("17:45","85sm.py"),
            ("18:00","85parking.py"),
        ],
        # Keep Sunday’s distinct mix but still 17:45 → 23:00 only
        "PM_FIRE": [
            ("17:45","85fireparking.py"), ("18:00","85fireparking.py"), ("18:50","80adfire.py"),
            ("19:00","85fireparking.py"), ("19:50","80adfire.py"),
            ("20:00","75fireparking.py"), ("20:50","75adfire.py"),
            ("21:00","75fireparking.py"), ("21:50","75adfire.py"),
            ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
            ("23:00","75fireparking.py"),
        ],
    },
}

# -----------------------------------------------------------------------------
# Register jobs
# -----------------------------------------------------------------------------
def schedule_tasks():
    for day in DAY_ORDER:
        blocks = BLOCKS.get(day, {})
        for block_name in ("AM","DAY","PM_FIRE"):
            rows = blocks.get(block_name, [])
            schedule_rows(rows, day)

def _graceful_exit(sig, _frame):
    logging.info(f"Received signal {sig}. Exiting scheduler loop.")
    raise SystemExit(0)

signal.signal(signal.SIGINT, _graceful_exit)
signal.signal(signal.SIGTERM, _graceful_exit)

schedule_tasks()

logging.info("Scheduler started (all times interpreted in America/New_York).")
logging.info(f"Process local time now: {datetime.now()}")

# Optional quick summary
if PRINT_LOCAL_SCHEDULE:
    try:
        jobs = schedule.get_jobs()
        print(f"\nLoaded {len(jobs)} scheduled jobs in {LOCAL_TZ}.")
        next_job = None
        for j in jobs:
            if j.next_run is None: 
                continue
            if next_job is None or j.next_run < next_job.next_run:
                next_job = j
        if next_job:
            # grab script name
            name = ""
            jf = next_job.job_func
            if hasattr(jf, "keywords") and isinstance(jf.keywords, dict):
                name = jf.keywords.get("script", "")
            when_str = next_job.next_run.strftime("%A %H:%M")
            if name:
                print(f"Next run: {when_str} ({name})")
            else:
                print(f"Next run: {when_str}")
        print("Scheduler running... Press Ctrl+C to exit.")
    except Exception as e:
        logging.warning(f"Could not summarize schedule: {e}")

# Main loop
while True:
    schedule.run_pending()
    time.sleep(1)