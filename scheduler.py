import schedule
import time
import subprocess
import logging
import os
import signal
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# -----------------------------------------------------------------------------
# CONFIG: FIRE program only — set to -1 to start & end FIRE blocks 1 hour earlier (e.g., DST); set to 0 to use original times.
# -----------------------------------------------------------------------------
FIRE_SHIFT_HOURS = -1         # <- change to -1 to start at 5:45pm instead of 6:45pm

# Timezone / data-frame config
USE_LOCAL_TZ = True                 # If True, scheduler runs in LOCAL_TZ and data times below are auto-converted
LOCAL_TZ = 'America/New_York'       # Orlando time
DATA_TIMES_ARE_UTC = True           # The times in FIRE_BLOCKS and SCHEDULES below are authored in UTC

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
        time.tzset()  # works on Unix-like systems
        logging.info(f"Timezone set to {LOCAL_TZ} for scheduling.")
    except Exception as e:
        logging.warning(f"Could not set TZ env or tzset(): {e}")

"""
# ===================== EASY EDIT ZONE =====================
# 1) To move FIRE SHOW earlier/later: set FIRE_SHIFT_HOURS to -1 or 0 above.
# 2) To add/edit FIRE blocks: edit FIRE_BLOCKS below (leave times as the ORIGINAL unshifted UTC values).
# 3) To add/edit regular (non-fire) programming: edit SCHEDULES below.
#    Tip: You can copy/paste rows like ("20:15", "75sm.py").
# ==========================================================
"""

def run_script(script):
    """Run the specified Python script under scripts/."""
    try:
        msg = f"Running script: {script}"
        print(msg); logging.info(msg)
        subprocess.run(["python", f"scripts/{script}"], check=True)
        ok = f"Script {script} ran successfully."
        print(ok); logging.info(ok)
    except subprocess.CalledProcessError as e:
        err = f"Error running script {script}: {e}"
        print(err); logging.error(err)
    except Exception as e:
        err = f"Unexpected error running script {script}: {e}"
        print(err); logging.error(err)


# -------------------------
# Helpers for shifting with day rollover (UTC->local and FIRE adjustments)
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


def _utc_to_local_hours() -> int:
    """Return the integer hours offset to convert UTC times to LOCAL_TZ at runtime (handles DST)."""
    try:
        off = datetime.now(ZoneInfo(LOCAL_TZ)).utcoffset()
        return int(round(off.total_seconds() / 3600))
    except Exception as e:
        logging.warning(f"Falling back to -5h offset (EST) due to error computing tz offset: {e}")
        return -5

def schedule_rows_shifted(rows, anchor_day: str, hours_shift: int):
    """
    Schedule rows for a given anchor day, shifting by hours_shift (can be negative) with day rollover.
    This is used for BOTH regular programming (UTC->local shift only) and FIRE blocks (UTC->local + FIRE_SHIFT_HOURS).
    """
    for tm, script_name in rows:
        delta, shifted_tm = _shift_with_dayroll(tm, hours_shift)
        target_day = anchor_day
        if delta == -1:
            target_day = PREV_DAY[anchor_day]
        elif delta == 1:
            target_day = NEXT_DAY[anchor_day]
        getattr(schedule.every(), target_day).at(shifted_tm).do(run_script, script=script_name)

# --------------------------------------
# FIRE SHOW blocks (evening through early morning)
# These are the exact blocks you highlighted and their siblings for other days.
# **Do not edit the original times here**; use FIRE_SHIFT_HOURS above.
# --------------------------------------
FIRE_BLOCKS = {
    # Mon evening -> Tue early
    "monday": [
        ("22:50", "75fireparking.py"), ("23:00", "75fireparking.py"), ("23:50", "75adfire.py"),
    ],
    "tuesday_early": [
        ("00:00", "75fireparking.py"), ("00:50", "75adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Tue evening -> Wed early
    "tuesday": [
        ("22:50", "75fireparking.py"), ("23:00", "75fireparking.py"), ("23:50", "75adfire.py"),
    ],
    "wednesday_early": [
        ("00:00", "75fireparking.py"), ("00:50", "75adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Wed evening -> Thu early
    "wednesday": [
        ("22:50", "75parkingfire.py"), ("23:00", "75parkingfire.py"), ("23:50", "75adfire.py"),
    ],
    "thursday_early": [
        ("00:00", "75parkingfire.py"), ("00:50", "75adfire.py"),
        ("01:00", "75parkingfire.py"), ("01:50", "75adfire.py"),
        ("02:00", "75parkingfire.py"), ("02:50", "75adfire.py"),
        ("03:00", "75parkingfire.py"),
    ],

    # Thu evening -> Fri early
    "thursday": [
        ("22:50", "85fireparking.py"), ("23:00", "85fireparking.py"), ("23:50", "85adfire.py"),
    ],
    "friday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Fri evening -> Sat early
    "friday": [
        ("22:50", "85fireparking.py"), ("23:00", "85fireparking.py"), ("23:50", "85adfire.py"),
    ],
    "saturday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "80adfire.py"),
        ("02:00", "85fireparking.py"), ("02:50", "80adfire.py"),
        ("03:00", "85fireparking.py"),
    ],

    # Sat evening -> Sun early
    "saturday": [
        ("22:50", "85fireparking.py"), ("23:00", "85fireparking.py"), ("23:50", "85adfire.py"),
    ],
    "sunday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "85adfire.py"),
        ("01:00", "85fireparking.py"), ("01:50", "85adfire.py"),
        ("02:00", "85fireparking.py"), ("02:50", "80adfire.py"),
        ("03:00", "75fireparking.py"),
    ],

    # Sun evening -> Mon early
    "sunday": [
        ("22:50", "85fireparking.py"), ("23:20", "85fireparking.py"), ("23:50", "80adfire.py"),
    ],
    "monday_early": [
        ("00:00", "85fireparking.py"), ("00:50", "80adfire.py"),
        ("01:00", "75fireparking.py"), ("01:50", "75adfire.py"),
        ("02:00", "75fireparking.py"), ("02:50", "75adfire.py"),
        ("03:00", "75fireparking.py"),
    ],
}

# --------------------------------------
# NON-FIRE weekly schedules (unchanged behavior)
# --------------------------------------
# You can add commercials or swap scripts by editing the tuples below; format is ("HH:MM", "script.py").
SCHEDULES = {
    "monday": [
        ("15:00", "65fm.py"), ("15:15", "65sm.py"), ("15:30", "65fm.py"), ("15:45", "65sm.py"),
        ("16:00", "75TIGS.py"), ("16:15", "65sm.py"), ("16:30", "70fm.py"), ("16:45", "70sm.py"),
        ("17:00", "70parking.py"), ("17:15", "75TIGS.py"), ("17:30", "70fm.py"), ("17:45", "70sm.py"),
        ("18:00", "75fm.py"), ("18:15", "75sm.py"), ("18:30", "75fm.py"), ("18:45", "75TIGS.py"),
        ("19:00", "75parking.py"), ("19:15", "75sm.py"), ("19:30", "75fm.py"), ("19:45", "75sm.py"),
        ("20:00", "parking.py"), ("20:15", "75sm.py"), ("20:30", "75fm.py"), ("20:45", "75sm.py"),
        ("21:00", "75parking.py"), ("21:15", "75TIGS.py"), ("21:30", "75fm.py"), ("21:45", "75sm.py"),
        ("22:00", "75parking.py"), ("22:15", "75TIGS.py"),
    ],
    "tuesday": [
        ("04:00", "65parking.py"), ("04:15", "65sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "pause.py"),
        ("15:00", "65fm.py"), ("15:15", "65sm.py"), ("15:30", "65fm.py"), ("15:45", "65sm.py"),
        ("16:00", "65fm.py"), ("16:15", "65sm.py"), ("16:30", "65fm.py"), ("16:45", "65sm.py"),
        ("17:00", "65parking.py"), ("17:15", "75TIGS.py"), ("17:30", "65fm.py"), ("17:45", "65sm.py"),
        ("18:00", "65oarking.py"), ("18:15", "65sm.py"), ("18:30", "70fm.py"), ("18:45", "70sm.py"),
        ("19:00", "70oarking.py"), ("19:15", "70sm.py"), ("19:30", "75TIGS.py"), ("19:45", "70sm.py"),
        ("20:00", "75parking.py"), ("20:15", "75sm.py"), ("20:30", "75TIGS.py"), ("20:45", "75sm.py"),
        ("21:00", "75parking.py"), ("21:15", "75sm.py"), ("21:30", "75TIGS.py"), ("21:45", "75sm.py"),
        ("22:00", "75parking.py"), ("22:15", "75TIGS.py"),
    ],
    "wednesday": [
        ("04:00", "65parking.py"), ("04:15", "65sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "pause.py"),
        ("15:00", "65fm.py"), ("15:15", "65sm.py"), ("15:30", "75TIGS.py"), ("15:45", "65sm.py"),
        ("16:00", "65fm.py"), ("16:15", "65sm.py"), ("16:30", "75TIGS.py"), ("16:45", "65sm.py"),
        ("17:00", "65parking.py"), ("17:15", "65sm.py"), ("17:30", "65fm.py"), ("17:45", "65sm.py"),
        ("18:00", "75TIGS.py"), ("18:15", "65sm.py"), ("18:30", "65fm.py"), ("18:45", "70sm.py"),
        ("19:00", "70parking.py"), ("19:15", "70sm.py"), ("19:30", "75TIGS.py"), ("19:45", "70sm.py"),
        ("20:00", "70parking.py"), ("20:15", "70sm.py"), ("20:30", "75TIGS.py"), ("20:45", "75sm.py"),
        ("21:00", "80parking.py"), ("21:15", "80sm.py"), ("21:30", "80fm.py"), ("21:45", "80sm.py"),
        ("22:00", "80parking.py"), ("22:15", "80sm.py"),
    ],
    "thursday": [
        ("04:00", "65parking.py"), ("04:15", "65sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "pause.py"),
        ("15:00", "75TIGS.py"), ("15:15", "75sm.py"), ("15:30", "75fm.py"), ("15:45", "75sm.py"),
        ("16:00", "75parking.py"), ("16:15", "75TIGS.py"), ("16:30", "75fm.py"), ("16:45", "75sm.py"),
        ("17:00", "75TIGS.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "75sm.py"), ("18:30", "75TIGS.py"), ("18:45", "75sm.py"),
        ("19:00", "80parking.py"), ("19:15", "80sm.py"), ("19:30", "80fm.py"), ("19:45", "80sm.py"),
        ("20:00", "80parking.py"), ("20:15", "80sm.py"), ("20:30", "80fm.py"), ("20:45", "80sm.py"),
        ("21:00", "80parking.py"), ("21:15", "80ad.py"), ("21:30", "80fm.py"), ("21:45", "80sm.py"),
        ("22:00", "80parking.py"), ("22:15", "80sm.py"),
    ],
    "friday": [
        ("04:00", "65parking.py"), ("04:15", "65sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "50parking.py"), ("06:15", "50sm.py"), ("06:30", "50sm.py"), ("06:45", "50sm.py"),
        ("07:00", "50parking.py"), ("07:15", "50sm.py"), ("07:30", "50sm.py"), ("07:45", "50sm.py"),
        ("08:00", "pause.py"),
        ("15:00", "75fm.py"), ("15:15", "75sm.py"), ("15:30", "75TIGS.py"), ("15:45", "75sm.py"),
        ("16:00", "75fm.py"), ("16:15", "75sm.py"), ("16:30", "75fm.py"), ("16:45", "75TIGS.py"),
        ("17:00", "75parking.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "75TIGS.py"), ("18:30", "75fm.py"), ("18:45", "75sm.py"),
        ("19:00", "80parking.py"), ("19:15", "80sm.py"), ("19:30", "80fm.py"), ("19:45", "80sm.py"),
        ("20:00", "90parking.py"), ("20:15", "90ad.py"), ("20:30", "90fm.py"), ("20:45", "90sm.py"),
        ("21:00", "90parking.py"), ("21:15", "90ad.py"), ("21:30", "90fm.py"), ("21:45", "90fm.py"),
        ("22:00", "90parking.py"), ("22:15", "90sm.py"),
    ],
    "saturday": [
        ("04:00", "70parking.py"), ("04:00", "70.py"),
        ("04:15", "70sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "65sm.py"), ("06:15", "65sm.py"), ("06:30", "65sm.py"), ("06:45", "65sm.py"),
        ("07:00", "65parking.py"), ("07:15", "65sm.py"), ("07:30", "65sm.py"), ("07:45", "65sm.py"),
        ("08:00", "pause.py"),
        ("15:00", "75fm.py"), ("15:15", "75sm.py"), ("15:30", "75parking.py"), ("15:45", "75sm.py"),
        ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75fm.py"), ("16:45", "75sm.py"),
        ("17:00", "75parking.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "75sm.py"), ("18:30", "75ad.py"), ("18:45", "75sm.py"),
        ("19:00", "75parking.py"), ("19:15", "75sm.py"), ("19:30", "75ad.py"), ("19:45", "75sm.py"),
        ("20:00", "75parking.py"), ("20:15", "75sm.py"), ("20:30", "75ad.py"), ("20:45", "75sm.py"),
        ("21:00", "85parking.py"), ("21:15", "85sm.py"), ("21:30", "85ad.py"), ("21:45", "85sm.py"),
        ("22:00", "85parking.py"), ("22:15", "85sm.py"),
    ],
    "sunday": [
        ("04:00", "65parking.py"), ("04:15", "65sm.py"), ("04:30", "65sm.py"), ("04:45", "65sm.py"),
        ("05:00", "65parking.py"), ("05:15", "65sm.py"), ("05:30", "65sm.py"), ("05:45", "65sm.py"),
        ("06:00", "pause.py"),
        ("15:00", "70fm.py"), ("15:15", "70sm.py"), ("15:30", "70parking.py"), ("15:45", "70sm.py"),
        ("16:00", "70fm.py"), ("16:15", "70sm.py"), ("16:30", "70fm.py"), ("16:45", "70sm.py"),
        ("17:00", "70parking.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"), ("17:45", "75sm.py"),
        ("18:00", "75parking.py"), ("18:15", "80sm.py"), ("18:30", "80fm.py"), ("18:45", "80sm.py"),
        ("19:00", "85parking.py"), ("19:15", "85ad.py"), ("19:30", "85fm.py"), ("19:45", "85fm.py"),
        ("20:00", "85parking.py"), ("20:15", "85sm.py"), ("20:30", "85sm.py"), ("20:45", "85ad.py"),
        ("21:00", "85parking.py"), ("21:15", "85sm.py"), ("21:30", "85sm.py"), ("21:45", "85sm.py"),
        ("22:00", "85parking.py"),
    ],
}

def schedule_tasks():
    # Determine UTC->local shift (e.g., -4 during EDT, -5 during EST). If not using local tz or data are local, shift is 0.
    utc_to_local = _utc_to_local_hours() if (USE_LOCAL_TZ and DATA_TIMES_ARE_UTC) else 0
    logging.info(f"UTC->LOCAL hour shift in effect: {utc_to_local}h (LOCAL_TZ={LOCAL_TZ}, USE_LOCAL_TZ={USE_LOCAL_TZ})")

    # 1) Regular (non-fire) weekly schedules — preserve exact behavior
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
        schedule_rows_shifted(SCHEDULES[day], day, utc_to_local)

    # 2) Fire-show blocks — apply BOTH UTC->local and FIRE_SHIFT_HOURS (fire-only adjustment)
    fire_total_shift = utc_to_local + FIRE_SHIFT_HOURS

    # Mon evening -> Tue early
    schedule_rows_shifted(FIRE_BLOCKS["monday"],        "monday",   fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["tuesday_early"], "tuesday",  fire_total_shift)

    # Tue evening -> Wed early
    schedule_rows_shifted(FIRE_BLOCKS["tuesday"],         "tuesday",   fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["wednesday_early"], "wednesday", fire_total_shift)

    # Wed evening -> Thu early
    schedule_rows_shifted(FIRE_BLOCKS["wednesday"],     "wednesday", fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["thursday_early"],"thursday",  fire_total_shift)

    # Thu evening -> Fri early
    schedule_rows_shifted(FIRE_BLOCKS["thursday"],      "thursday", fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["friday_early"],  "friday",   fire_total_shift)

    # Fri evening -> Sat early
    schedule_rows_shifted(FIRE_BLOCKS["friday"],          "friday",   fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["saturday_early"],  "saturday", fire_total_shift)

    # Sat evening -> Sun early
    schedule_rows_shifted(FIRE_BLOCKS["saturday"],      "saturday", fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["sunday_early"],  "sunday",   fire_total_shift)

    # Sun evening -> Mon early
    schedule_rows_shifted(FIRE_BLOCKS["sunday"],        "sunday",   fire_total_shift)
    schedule_rows_shifted(FIRE_BLOCKS["monday_early"],  "monday",   fire_total_shift)

def _graceful_exit(sig, _frame):
    logging.info(f"Received signal {sig}. Exiting scheduler loop.")
    raise SystemExit(0)

signal.signal(signal.SIGINT, _graceful_exit)
signal.signal(signal.SIGTERM, _graceful_exit)

# Register jobs
schedule_tasks()

logging.info(f"Scheduler started. FIRE_SHIFT_HOURS={FIRE_SHIFT_HOURS} (fire program only)")
logging.info(f"Process local time now: {datetime.now()} | UTC now: {datetime.utcnow()}")

# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)