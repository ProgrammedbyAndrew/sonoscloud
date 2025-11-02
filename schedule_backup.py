import schedule
import time
import subprocess
import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_script(script):
    """Run the specified Python script."""
    try:
        print(f"Running script: {script}")
        logging.info(f"Running script: {script}")
        subprocess.run(["python", f"scripts/{script}"], check=True)
        print(f"Script {script} ran successfully.")
        logging.info(f"Script {script} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script}: {e}")
        logging.error(f"Error running script {script}: {e}")
    except Exception as e:
        print(f"Unexpected error running script {script}: {e}")
        logging.error(f"Unexpected error running script {script}: {e}")

def schedule_tasks():
    """Schedule tasks for the week."""
    # Monday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Monday
    schedule.every().monday.at("15:00").do(run_script, script="65fm.py")  # 11:00 AM EDT
    schedule.every().monday.at("15:15").do(run_script, script="65sm.py")  # 11:15 AM EDT
    schedule.every().monday.at("15:30").do(run_script, script="65fm.py")  # 11:30 AM EDT
    schedule.every().monday.at("15:45").do(run_script, script="65sm.py")  # 11:45 AM EDT
    schedule.every().monday.at("16:00").do(run_script, script="75TIGS.py")  # 12:00 PM EDT
    schedule.every().monday.at("16:15").do(run_script, script="65sm.py")  # 12:15 PM EDT
    schedule.every().monday.at("16:30").do(run_script, script="70fm.py")  # 12:30 PM EDT
    schedule.every().monday.at("16:45").do(run_script, script="70sm.py")  # 12:45 PM EDT
    schedule.every().monday.at("17:00").do(run_script, script="70parking.py")  # 1:00 PM EDT
    schedule.every().monday.at("17:15").do(run_script, script="75TIGS.py")  # 1:15 PM EDT
    schedule.every().monday.at("17:30").do(run_script, script="70fm.py")  # 1:30 PM EDT
    schedule.every().monday.at("17:45").do(run_script, script="70sm.py")  # 1:45 PM EDT
    schedule.every().monday.at("18:00").do(run_script, script="75fm.py")  # 2:00 PM EDT
    schedule.every().monday.at("18:15").do(run_script, script="75sm.py")  # 2:15 PM EDT
    schedule.every().monday.at("18:30").do(run_script, script="75fm.py")  # 2:30 PM EDT
    schedule.every().monday.at("18:45").do(run_script, script="75TIGS.py")  # 2:45 PM EDT
    schedule.every().monday.at("19:00").do(run_script, script="75parking.py")  # 3:00 PM EDT
    schedule.every().monday.at("19:15").do(run_script, script="75sm.py")  # 3:15 PM EDT
    schedule.every().monday.at("19:30").do(run_script, script="75fm.py")  # 3:30 PM EDT
    schedule.every().monday.at("19:45").do(run_script, script="75sm.py")  # 3:45 PM EDT
    schedule.every().monday.at("20:00").do(run_script, script="parking.py")  # 4:00 PM EDT
    schedule.every().monday.at("20:15").do(run_script, script="75sm.py")  # 4:15 PM EDT
    schedule.every().monday.at("20:30").do(run_script, script="75fm.py")  # 4:30 PM EDT
    schedule.every().monday.at("20:45").do(run_script, script="75sm.py")  # 4:45 PM EDT
    schedule.every().monday.at("21:00").do(run_script, script="75parking.py")  # 5:00 PM EDT
    schedule.every().monday.at("21:15").do(run_script, script="75TIGS.py")  # 5:15 PM EDT
    schedule.every().monday.at("21:30").do(run_script, script="75fm.py")  # 5:30 PM EDT
    schedule.every().monday.at("21:45").do(run_script, script="75sm.py")  # 5:45 PM EDT
    schedule.every().monday.at("22:00").do(run_script, script="75parking.py")  # 6:00 PM EDT
    schedule.every().monday.at("22:15").do(run_script, script="75TIGS.py")  # 6:15 PM EDT

    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    schedule.every().monday.at("22:50").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().monday.at("23:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().monday.at("23:50").do(run_script, script="75adfire.py") #750
    schedule.every().tuesday.at("00:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().tuesday.at("00:50").do(run_script, script="75adfire.py") #850
    schedule.every().tuesday.at("01:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().tuesday.at("01:50").do(run_script, script="75adfire.py") #950
    schedule.every().tuesday.at("02:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().tuesday.at("02:50").do(run_script, script="75adfire.py") #1050
    schedule.every().tuesday.at("03:00").do(run_script, script="75fireparking.py") #PARKING
   
 
 
    # 12:00 AM to 2:00 AM EDT (04:00 to 06:00 UTC, next day)
   
    schedule.every().tuesday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().tuesday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().tuesday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().tuesday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().tuesday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().tuesday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().tuesday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().tuesday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().tuesday.at("06:00").do(run_script, script="pause.py")  # 2:00 AM EDT

    # Tuesday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Tuesday
    schedule.every().tuesday.at("15:00").do(run_script, script="65fm.py")  # 11:00 AM EDT
    schedule.every().tuesday.at("15:15").do(run_script, script="65sm.py")  # 11:15 AM EDT
    schedule.every().tuesday.at("15:30").do(run_script, script="65fm.py")  # 11:30 AM EDT
    schedule.every().tuesday.at("15:45").do(run_script, script="65sm.py")  # 11:45 AM EDT
    schedule.every().tuesday.at("16:00").do(run_script, script="65fm.py")  # 12:00 PM EDT
    schedule.every().tuesday.at("16:15").do(run_script, script="65sm.py")  # 12:15 PM EDT
    schedule.every().tuesday.at("16:30").do(run_script, script="65fm.py")  # 12:30 PM EDT
    schedule.every().tuesday.at("16:45").do(run_script, script="65sm.py")  # 12:45 PM EDT
    schedule.every().tuesday.at("17:00").do(run_script, script="65parking.py")  # 1:00 PM EDT
    schedule.every().tuesday.at("17:15").do(run_script, script="75TIGS.py")  # 1:15 PM EDT
    schedule.every().tuesday.at("17:30").do(run_script, script="65fm.py")  # 1:30 PM EDT
    schedule.every().tuesday.at("17:45").do(run_script, script="65sm.py")  # 1:45 PM EDT
    schedule.every().tuesday.at("18:00").do(run_script, script="65oarking.py")  # 2:00 PM EDT
    schedule.every().tuesday.at("18:15").do(run_script, script="65sm.py")  # 2:15 PM EDT
    schedule.every().tuesday.at("18:30").do(run_script, script="70fm.py")  # 2:30 PM EDT
    schedule.every().tuesday.at("18:45").do(run_script, script="70sm.py")  # 2:45 PM EDT
    schedule.every().tuesday.at("19:00").do(run_script, script="70oarking.py")  # 3:00 PM EDT
    schedule.every().tuesday.at("19:15").do(run_script, script="70sm.py")  # 3:15 PM EDT
    schedule.every().tuesday.at("19:30").do(run_script, script="75TIGS.py")  # 3:30 PM EDT
    schedule.every().tuesday.at("19:45").do(run_script, script="70sm.py")  # 3:45 PM EDT
    schedule.every().tuesday.at("20:00").do(run_script, script="75parking.py")  # 4:00 PM EDT
    schedule.every().tuesday.at("20:15").do(run_script, script="75sm.py")  # 4:15 PM EDT
    schedule.every().tuesday.at("20:30").do(run_script, script="75TIGS.py")  # 4:30 PM EDT
    schedule.every().tuesday.at("20:45").do(run_script, script="75sm.py")  # 4:45 PM EDT
    schedule.every().tuesday.at("21:00").do(run_script, script="75parking.py")  # 5:00 PM EDT
    schedule.every().tuesday.at("21:15").do(run_script, script="75sm.py")  # 5:15 PM EDT
    schedule.every().tuesday.at("21:30").do(run_script, script="75TIGS.py")  # 5:30 PM EDT
    schedule.every().tuesday.at("21:45").do(run_script, script="75sm.py")  # 5:45 PM EDT
    schedule.every().tuesday.at("22:00").do(run_script, script="75parking.py")  # 6:00 PM EDT
    schedule.every().tuesday.at("22:15").do(run_script, script="75TIGS.py")  # 6:15 PM EDT

    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    schedule.every().tuesday.at("22:50").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().tuesday.at("23:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().tuesday.at("23:50").do(run_script, script="75adfire.py") #750
    schedule.every().wednesday.at("00:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().wednesday.at("00:50").do(run_script, script="75adfire.py") #850
    schedule.every().wednesday.at("01:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().wednesday.at("01:50").do(run_script, script="75adfire.py") #950
    schedule.every().wednesday.at("02:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().wednesday.at("02:50").do(run_script, script="75adfire.py")  #1050
    schedule.every().wednesday.at("03:00").do(run_script, script="75fireparking.py")  #PARKING
    

    # 12:00 AM to 2:00 AM EDT (04:00 to 06:00 UTC, next day)

    schedule.every().wednesday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().wednesday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().wednesday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().wednesday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().wednesday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().wednesday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().wednesday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().wednesday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().wednesday.at("06:00").do(run_script, script="pause.py")  # 2:00 AM EDT

    # Wednesday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Wednesday
    schedule.every().wednesday.at("15:00").do(run_script, script="65fm.py")  # 11:00 AM EDT
    schedule.every().wednesday.at("15:15").do(run_script, script="65sm.py")  # 11:15 AM EDT
    schedule.every().wednesday.at("15:30").do(run_script, script="75TIGS.py")  # 11:30 AM EDT
    schedule.every().wednesday.at("15:45").do(run_script, script="65sm.py")  # 11:45 AM EDT
    schedule.every().wednesday.at("16:00").do(run_script, script="65fm.py")  # 12:00 PM EDT
    schedule.every().wednesday.at("16:15").do(run_script, script="65sm.py")  # 12:15 PM EDT
    schedule.every().wednesday.at("16:30").do(run_script, script="75TIGS.py")  # 12:30 PM EDT
    schedule.every().wednesday.at("16:45").do(run_script, script="65sm.py")  # 12:45 PM EDT
    schedule.every().wednesday.at("17:00").do(run_script, script="65parking.py")  # 1:00 PM EDT
    schedule.every().wednesday.at("17:15").do(run_script, script="65sm.py")  # 1:15 PM EDT
    schedule.every().wednesday.at("17:30").do(run_script, script="65fm.py")  # 1:30 PM EDT
    schedule.every().wednesday.at("17:45").do(run_script, script="65sm.py")  # 1:45 PM EDT
    schedule.every().wednesday.at("18:00").do(run_script, script="75TIGS.py")  # 2:00 PM EDT
    schedule.every().wednesday.at("18:15").do(run_script, script="65sm.py")  # 2:15 PM EDT
    schedule.every().wednesday.at("18:30").do(run_script, script="65fm.py")  # 2:30 PM EDT
    schedule.every().wednesday.at("18:45").do(run_script, script="70sm.py")  # 2:45 PM EDT
    schedule.every().wednesday.at("19:00").do(run_script, script="70parking.py")  # 3:00 PM EDT
    schedule.every().wednesday.at("19:15").do(run_script, script="70sm.py")  # 3:15 PM EDT
    schedule.every().wednesday.at("19:30").do(run_script, script="75TIGS.py")  # 3:30 PM EDT
    schedule.every().wednesday.at("19:45").do(run_script, script="70sm.py")  # 3:45 PM EDT
    schedule.every().wednesday.at("20:00").do(run_script, script="70parking.py")  # 4:00 PM EDT
    schedule.every().wednesday.at("20:15").do(run_script, script="70sm.py")  # 4:15 PM EDT
    schedule.every().wednesday.at("20:30").do(run_script, script="75TIGS.py")  # 4:30 PM EDT
    schedule.every().wednesday.at("20:45").do(run_script, script="75sm.py")  # 4:45 PM EDT
    schedule.every().wednesday.at("21:00").do(run_script, script="80parking.py")  # 5:00 PM EDT
    schedule.every().wednesday.at("21:15").do(run_script, script="80sm.py")  # 5:15 PM EDT
    schedule.every().wednesday.at("21:30").do(run_script, script="80fm.py")  # 5:30 PM EDT
    schedule.every().wednesday.at("21:45").do(run_script, script="80sm.py")  # 5:45 PM EDT
    schedule.every().wednesday.at("22:00").do(run_script, script="80parking.py")  # 6:00 PM EDT
    schedule.every().wednesday.at("22:15").do(run_script, script="80sm.py")  # 6:15 PM EDT

    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    schedule.every().wednesday.at("22:50").do(run_script, script="75parkingfire.py") #PARKING
    schedule.every().wednesday.at("23:00").do(run_script, script="75parkingfire.py") #PARKING
    schedule.every().wednesday.at("23:50").do(run_script, script="75adfire.py") #750
    schedule.every().thursday.at("00:00").do(run_script, script="75parkingfire.py") #PARKING
    schedule.every().thursday.at("00:50").do(run_script, script="75adfire.py") #850
    schedule.every().thursday.at("01:00").do(run_script, script="75parkingfire.py") #PARKING
    schedule.every().thursday.at("01:50").do(run_script, script="75adfire.py") #950
    schedule.every().thursday.at("02:00").do(run_script, script="75parkingfire.py") #PARKING
    schedule.every().thursday.at("02:50").do(run_script, script="75adfire.py")  #1050
    schedule.every().thursday.at("03:00").do(run_script, script="75parkingfire.py")  #PARKING
   


    # 12:00 AM to 2:00 AM EDT (04:00 to 06:00 UTC, next day)
   
    schedule.every().thursday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().thursday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().thursday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().thursday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().thursday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().thursday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().thursday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().thursday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().thursday.at("06:00").do(run_script, script="pause.py")  # 2:00 AM EDT

    # Thursday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Thursday
    schedule.every().thursday.at("15:00").do(run_script, script="75TIGS.py")  # 11:00 AM EDT
    schedule.every().thursday.at("15:15").do(run_script, script="75sm.py")  # 11:15 AM EDT
    schedule.every().thursday.at("15:30").do(run_script, script="75fm.py")  # 11:30 AM EDT
    schedule.every().thursday.at("15:45").do(run_script, script="75sm.py")  # 11:45 AM EDT
    schedule.every().thursday.at("16:00").do(run_script, script="75parking.py")  # 12:00 PM EDT
    schedule.every().thursday.at("16:15").do(run_script, script="75TIGS.py")  # 12:15 PM EDT
    schedule.every().thursday.at("16:30").do(run_script, script="75fm.py")  # 12:30 PM EDT
    schedule.every().thursday.at("16:45").do(run_script, script="75sm.py")  # 12:45 PM EDT
    schedule.every().thursday.at("17:00").do(run_script, script="75TIGS.py")  # 1:00 PM EDT
    schedule.every().thursday.at("17:15").do(run_script, script="75sm.py")  # 1:15 PM EDT
    schedule.every().thursday.at("17:30").do(run_script, script="75fm.py")  # 1:30 PM EDT
    schedule.every().thursday.at("17:45").do(run_script, script="75sm.py")  # 1:45 PM EDT
    schedule.every().thursday.at("18:00").do(run_script, script="75parking.py")  # 2:00 PM EDT
    schedule.every().thursday.at("18:15").do(run_script, script="75sm.py")  # 2:15 PM EDT
    schedule.every().thursday.at("18:30").do(run_script, script="75TIGS.py")  # 2:30 PM EDT
    schedule.every().thursday.at("18:45").do(run_script, script="75sm.py")  # 2:45 PM EDT
    schedule.every().thursday.at("19:00").do(run_script, script="80parking.py")  # 3:00 PM EDT
    schedule.every().thursday.at("19:15").do(run_script, script="80sm.py")  # 3:15 PM EDT
    schedule.every().thursday.at("19:30").do(run_script, script="80fm.py")  # 3:30 PM EDT
    schedule.every().thursday.at("19:45").do(run_script, script="80sm.py")  # 3:45 PM EDT
    schedule.every().thursday.at("20:00").do(run_script, script="80parking.py")  # 4:00 PM EDT
    schedule.every().thursday.at("20:15").do(run_script, script="80sm.py")  # 4:15 PM EDT
    schedule.every().thursday.at("20:30").do(run_script, script="80fm.py")  # 4:30 PM EDT
    schedule.every().thursday.at("20:45").do(run_script, script="80sm.py")  # 4:45 PM EDT
    schedule.every().thursday.at("21:00").do(run_script, script="80parking.py")  # 5:00 PM EDT
    schedule.every().thursday.at("21:15").do(run_script, script="80ad.py")  # 5:15 PM EDT
    schedule.every().thursday.at("21:30").do(run_script, script="80fm.py")  # 5:30 PM EDT
    schedule.every().thursday.at("21:45").do(run_script, script="80sm.py")  # 5:45 PM EDT
    schedule.every().thursday.at("22:00").do(run_script, script="80parking.py")  # 6:00 PM EDT
    schedule.every().thursday.at("22:15").do(run_script, script="80sm.py")  # 6:15 PM EDT

    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    schedule.every().thursday.at("22:50").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().thursday.at("23:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().thursday.at("23:50").do(run_script, script="85adfire.py") #750
    schedule.every().friday.at("00:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().friday.at("00:50").do(run_script, script="85adfire.py") #850
    schedule.every().friday.at("01:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().friday.at("01:50").do(run_script, script="75adfire.py") #950
    schedule.every().friday.at("02:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().friday.at("02:50").do(run_script, script="75adfire.py")  #1050
    schedule.every().friday.at("03:00").do(run_script, script="75fireparking.py")  #PARKING


    # 12:00 AM to 2:00 AM EDT (04:00 to 06:00 UTC, next day)
    schedule.every().friday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().friday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().friday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().friday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().friday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().friday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().friday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().friday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    # 2:00 AM to 4:00 AM EDT (06:00 to 08:00 UTC, next day, Friday only)
    schedule.every().friday.at("06:00").do(run_script, script="50parking.py")  # 2:00 AM EDT
    schedule.every().friday.at("06:15").do(run_script, script="50sm.py")  # 2:15 AM EDT
    schedule.every().friday.at("06:30").do(run_script, script="50sm.py")  # 2:30 AM EDT
    schedule.every().friday.at("06:45").do(run_script, script="50sm.py")  # 2:45 AM EDT
    schedule.every().friday.at("07:00").do(run_script, script="50parking.py")  # 3:00 AM EDT
    schedule.every().friday.at("07:15").do(run_script, script="50sm.py")  # 3:15 AM EDT
    schedule.every().friday.at("07:30").do(run_script, script="50sm.py")  # 3:30 AM EDT
    schedule.every().friday.at("07:45").do(run_script, script="50sm.py")  # 3:45 AM EDT
    schedule.every().friday.at("08:00").do(run_script, script="pause.py")  # 4:00 AM EDT

    # Friday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Friday
    schedule.every().friday.at("15:00").do(run_script, script="75fm.py")  # 11:00 AM EDT
    schedule.every().friday.at("15:15").do(run_script, script="75sm.py")  # 11:15 AM EDT
    schedule.every().friday.at("15:30").do(run_script, script="75TIGS.py")  # 11:30 AM EDT
    schedule.every().friday.at("15:45").do(run_script, script="75sm.py")  # 11:45 AM EDT
    schedule.every().friday.at("16:00").do(run_script, script="75fm.py")  # 12:00 PM EDT
    schedule.every().friday.at("16:15").do(run_script, script="75sm.py")  # 12:15 PM EDT
    schedule.every().friday.at("16:30").do(run_script, script="75fm.py")  # 12:30 PM EDT
    schedule.every().friday.at("16:45").do(run_script, script="75TIGS.py")  # 12:45 PM EDT
    schedule.every().friday.at("17:00").do(run_script, script="75parking.py")  # 1:00 PM EDT
    schedule.every().friday.at("17:15").do(run_script, script="75sm.py")  # 1:15 PM EDT
    schedule.every().friday.at("17:30").do(run_script, script="75fm.py")  # 1:30 PM EDT
    schedule.every().friday.at("17:45").do(run_script, script="75sm.py")  # 1:45 PM EDT
    schedule.every().friday.at("18:00").do(run_script, script="75parking.py")  # 2:00 PM EDT
    schedule.every().friday.at("18:15").do(run_script, script="75TIGS.py")  # 2:15 PM EDT
    schedule.every().friday.at("18:30").do(run_script, script="75fm.py")  # 2:30 PM EDT
    schedule.every().friday.at("18:45").do(run_script, script="75sm.py")  # 2:45 PM EDT
    schedule.every().friday.at("19:00").do(run_script, script="80parking.py")  # 3:00 PM EDT
    schedule.every().friday.at("19:15").do(run_script, script="80sm.py")  # 3:15 PM EDT
    schedule.every().friday.at("19:30").do(run_script, script="80fm.py")  # 3:30 PM EDT
    schedule.every().friday.at("19:45").do(run_script, script="80sm.py")  # 3:45 PM EDT
    schedule.every().friday.at("20:00").do(run_script, script="90parking.py")  # 4:00 PM EDT
    schedule.every().friday.at("20:15").do(run_script, script="90ad.py")  # 4:15 PM EDT
    schedule.every().friday.at("20:30").do(run_script, script="90fm.py")  # 4:30 PM EDT
    schedule.every().friday.at("20:45").do(run_script, script="90sm.py")  # 4:45 PM EDT
    schedule.every().friday.at("21:00").do(run_script, script="90parking.py")  # 5:00 PM EDT
    schedule.every().friday.at("21:15").do(run_script, script="90ad.py")  # 5:15 PM EDT
    schedule.every().friday.at("21:30").do(run_script, script="90fm.py")  # 5:30 PM EDT
    schedule.every().friday.at("21:45").do(run_script, script="90fm.py")  # 5:45 PM EDT
    schedule.every().friday.at("22:00").do(run_script, script="90parking.py")  # 6:00 PM EDT
    schedule.every().friday.at("22:15").do(run_script, script="90sm.py")  # 6:15 PM EDT
    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)

    schedule.every().friday.at("22:50").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().friday.at("23:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().friday.at("23:50").do(run_script, script="85adfire.py") #750
    schedule.every().saturday.at("00:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().saturday.at("00:50").do(run_script, script="85adfire.py") #850
    schedule.every().saturday.at("01:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().saturday.at("01:50").do(run_script, script="80adfire.py") #950
    schedule.every().saturday.at("02:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().saturday.at("02:50").do(run_script, script="80adfire.py")  #1050
    schedule.every().saturday.at("03:00").do(run_script, script="85fireparking.py")  #PARKING


    # 12:00 AM to 4:00 AM EDT (04:00 to 08:00 UTC, next day)

    schedule.every().saturday.at("04:00").do(run_script, script="70parking.py")  # 12:00 AM EDT
    schedule.every().saturday.at("04:00").do(run_script, script="70.py")  # 12:00 AM EDT
    schedule.every().saturday.at("04:15").do(run_script, script="70sm.py")  # 12:15 AM EDT
    schedule.every().saturday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().saturday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().saturday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().saturday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().saturday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().saturday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().saturday.at("06:00").do(run_script, script="65sm.py")  # 2:00 AM EDT
    schedule.every().saturday.at("06:15").do(run_script, script="65sm.py")  # 2:15 AM EDT
    schedule.every().saturday.at("06:30").do(run_script, script="65sm.py")  # 2:30 AM EDT
    schedule.every().saturday.at("06:45").do(run_script, script="65sm.py")  # 2:45 AM EDT
    schedule.every().saturday.at("07:00").do(run_script, script="65parking.py")  # 3:00 AM EDT
    schedule.every().saturday.at("07:15").do(run_script, script="65sm.py")  # 3:15 AM EDT
    schedule.every().saturday.at("07:30").do(run_script, script="65sm.py")  # 3:30 AM EDT
    schedule.every().saturday.at("07:45").do(run_script, script="65sm.py")  # 3:45 AM EDT
    schedule.every().saturday.at("08:00").do(run_script, script="pause.py")  # 4:00 AM EDT

    # Saturday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Saturday
    schedule.every().saturday.at("15:00").do(run_script, script="75fm.py")  # 11:00 AM EDT
    schedule.every().saturday.at("15:15").do(run_script, script="75sm.py")  # 11:15 AM EDT
    schedule.every().saturday.at("15:30").do(run_script, script="75parking.py")  # 11:30 AM EDT
    schedule.every().saturday.at("15:45").do(run_script, script="75sm.py")  # 11:45 AM EDT
    schedule.every().saturday.at("16:00").do(run_script, script="75parking.py")  # 12:00 PM EDT
    schedule.every().saturday.at("16:15").do(run_script, script="75sm.py")  # 12:15 PM EDT
    schedule.every().saturday.at("16:30").do(run_script, script="75fm.py")  # 12:30 PM EDT
    schedule.every().saturday.at("16:45").do(run_script, script="75sm.py")  # 12:45 PM EDT
    schedule.every().saturday.at("17:00").do(run_script, script="75parking.py")  # 1:00 PM EDT
    schedule.every().saturday.at("17:15").do(run_script, script="75sm.py")  # 1:15 PM EDT
    schedule.every().saturday.at("17:30").do(run_script, script="75fm.py")  # 1:30 PM EDT
    schedule.every().saturday.at("17:45").do(run_script, script="75sm.py")  # 1:45 PM EDT
    schedule.every().saturday.at("18:00").do(run_script, script="75parking.py")  # 2:00 PM EDT
    schedule.every().saturday.at("18:15").do(run_script, script="75sm.py")  # 2:15 PM EDT
    schedule.every().saturday.at("18:30").do(run_script, script="75ad.py")  # 2:30 PM EDT
    schedule.every().saturday.at("18:45").do(run_script, script="75sm.py")  # 2:45 PM EDT
    schedule.every().saturday.at("19:00").do(run_script, script="75parking.py")  # 3:00 PM EDT
    schedule.every().saturday.at("19:15").do(run_script, script="75sm.py")  # 3:15 PM EDT
    schedule.every().saturday.at("19:30").do(run_script, script="75ad.py")  # 3:30 PM EDT
    schedule.every().saturday.at("19:45").do(run_script, script="75sm.py")  # 3:45 PM EDT
    schedule.every().saturday.at("20:00").do(run_script, script="75parking.py")  # 4:00 PM EDT
    schedule.every().saturday.at("20:15").do(run_script, script="75sm.py")  # 4:15 PM EDT
    schedule.every().saturday.at("20:30").do(run_script, script="75ad.py")  # 4:30 PM EDT
    schedule.every().saturday.at("20:45").do(run_script, script="75sm.py")  # 4:45 PM EDT
    schedule.every().saturday.at("21:00").do(run_script, script="85parking.py")  # 5:00 PM EDT
    schedule.every().saturday.at("21:15").do(run_script, script="85sm.py")  # 5:15 PM EDT
    schedule.every().saturday.at("21:30").do(run_script, script="85ad.py")  # 5:30 PM EDT
    schedule.every().saturday.at("21:45").do(run_script, script="85sm.py")  # 5:45 PM EDT
    schedule.every().saturday.at("22:00").do(run_script, script="85parking.py")  # 6:00 PM EDT
    schedule.every().saturday.at("22:15").do(run_script, script="85sm.py")  # 6:15 PM EDT
    # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    
    schedule.every().saturday.at("22:50").do(run_script, script="85fireparking.py") #fire parking
    schedule.every().saturday.at("23:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().saturday.at("23:50").do(run_script, script="85adfire.py") #750
    schedule.every().sunday.at("00:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().sunday.at("00:50").do(run_script, script="85adfire.py") #850
    schedule.every().sunday.at("01:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().sunday.at("01:50").do(run_script, script="85adfire.py") #950
    schedule.every().sunday.at("02:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().sunday.at("02:50").do(run_script, script="80adfire.py")  #1050
    schedule.every().sunday.at("03:00").do(run_script, script="75fireparking.py")  #PARKING

    



    # 12:00 AM to 4:00 AM EDT (04:00 to 08:00 UTC, next day)
    
    schedule.every().sunday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().sunday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().sunday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().sunday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().sunday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().sunday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().sunday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().sunday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().sunday.at("06:00").do(run_script, script="pause.py")  # 2:00 AM EDT

    # Sunday schedule in UTC (EDT = UTC - 4 hours)
    # Start of Sunday
    schedule.every().sunday.at("15:00").do(run_script, script="70fm.py")  # 11:00 AM EDT
    schedule.every().sunday.at("15:15").do(run_script, script="70sm.py")  # 11:15 AM EDT
    schedule.every().sunday.at("15:30").do(run_script, script="70parking.py")  # 11:30 AM EDT
    schedule.every().sunday.at("15:45").do(run_script, script="70sm.py")  # 11:45 AM EDT
    schedule.every().sunday.at("16:00").do(run_script, script="70fm.py")  # 12:00 PM EDT
    schedule.every().sunday.at("16:15").do(run_script, script="70sm.py")  # 12:15 PM EDT
    schedule.every().sunday.at("16:30").do(run_script, script="70fm.py")  # 12:30 PM EDT
    schedule.every().sunday.at("16:45").do(run_script, script="70sm.py")  # 12:45 PM EDT
    schedule.every().sunday.at("17:00").do(run_script, script="70parking.py")  # 1:00 PM EDT
    schedule.every().sunday.at("17:15").do(run_script, script="75sm.py")  # 1:15 PM EDT
    schedule.every().sunday.at("17:30").do(run_script, script="75fm.py")  # 1:30 PM EDT
    schedule.every().sunday.at("17:45").do(run_script, script="75sm.py")  # 1:45 PM EDT
    schedule.every().sunday.at("18:00").do(run_script, script="75parking.py")  # 2:00 PM EDT
    schedule.every().sunday.at("18:15").do(run_script, script="80sm.py")  # 2:15 PM EDT
    schedule.every().sunday.at("18:30").do(run_script, script="80fm.py")  # 2:30 PM EDT
    schedule.every().sunday.at("18:45").do(run_script, script="80sm.py")  # 2:45 PM EDT
    schedule.every().sunday.at("19:00").do(run_script, script="85parking.py")  # 3:00 PM EDT
    schedule.every().sunday.at("19:15").do(run_script, script="85ad.py")  # 3:15 PM EDT
    schedule.every().sunday.at("19:30").do(run_script, script="85fm.py")  # 3:30 PM EDT
    schedule.every().sunday.at("19:45").do(run_script, script="85fm.py")  # 3:45 PM EDT
    schedule.every().sunday.at("20:00").do(run_script, script="85parking.py")  # 4:00 PM EDT
    schedule.every().sunday.at("20:15").do(run_script, script="85sm.py")  # 4:15 PM EDT
    schedule.every().sunday.at("20:30").do(run_script, script="85sm.py")  # 4:30 PM EDT
    schedule.every().sunday.at("20:45").do(run_script, script="85ad.py")  # 4:45 PM EDT
    schedule.every().sunday.at("21:00").do(run_script, script="85parking.py")  # 5:00 PM EDT
    schedule.every().sunday.at("21:15").do(run_script, script="85sm.py")  # 5:15 PM EDT
    schedule.every().sunday.at("21:30").do(run_script, script="85sm.py")  # 5:30 PM EDT
    schedule.every().sunday.at("21:45").do(run_script, script="85sm.py")  # 5:45 PM EDT
    schedule.every().sunday.at("22:00").do(run_script, script="85parking.py")  # 6:00 PM EDT
  

     # 7:00 PM to 11:00 PM EDT (23:00 to 03:00 UTC)
    schedule.every().sunday.at("22:50").do(run_script, script="85fireparking.py") #Fire Parking
    schedule.every().sunday.at("23:20").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().sunday.at("23:50").do(run_script, script="80adfire.py") #750
    schedule.every().monday.at("00:00").do(run_script, script="85fireparking.py") #PARKING
    schedule.every().monday.at("00:50").do(run_script, script="80adfire.py") #850
    schedule.every().monday.at("01:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().monday.at("01:50").do(run_script, script="75adfire.py") #950
    schedule.every().monday.at("02:00").do(run_script, script="75fireparking.py") #PARKING
    schedule.every().monday.at("02:50").do(run_script, script="75adfire.py") #1050
    schedule.every().monday.at("03:00").do(run_script, script="75fireparking.py") #PARKING
  

    # 12:00 AM to 2:00 AM EDT (04:00 to 06:00 UTC, next day)
  
    schedule.every().monday.at("04:00").do(run_script, script="65parking.py")  # 12:00 AM EDT
    schedule.every().monday.at("04:15").do(run_script, script="65sm.py")  # 12:15 AM EDT
    schedule.every().monday.at("04:30").do(run_script, script="65sm.py")  # 12:30 AM EDT
    schedule.every().monday.at("04:45").do(run_script, script="65sm.py")  # 12:45 AM EDT
    schedule.every().monday.at("05:00").do(run_script, script="65parking.py")  # 1:00 AM EDT
    schedule.every().monday.at("05:15").do(run_script, script="65sm.py")  # 1:15 AM EDT
    schedule.every().monday.at("05:30").do(run_script, script="65sm.py")  # 1:30 AM EDT
    schedule.every().monday.at("05:45").do(run_script, script="65sm.py")  # 1:45 AM EDT
    schedule.every().monday.at("06:00").do(run_script, script="pause.py")  # 2:00 AM EDT

# Call the scheduling function
schedule_tasks()

# Run the scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)
# -*- coding: utf-8 -*-
"""
ALL TIMES BELOW ARE AUTHORED IN ORLANDO LOCAL TIME (America/New_York).

- You can edit times exactly as you want them to happen in Orlando.
- The scheduler will convert those local times to the server's timezone automatically.
- "Fire show" blocks can be shifted earlier/later with FIRE_SHIFT_HOURS and affect ONLY fire blocks.
- The rest of the schedule runs exactly as before.

Quick edits you will commonly make:
1) To start the fire programming 1 hour earlier (e.g., 6:45 → 5:45):
   Set FIRE_SHIFT_HOURS = -1
   Set FIRE_SHIFT_ENABLED = True
   (Set FIRE_SHIFT_ENABLED = False to disable the shift quickly.)

2) To add or change a spot:
   Add/edit tuples like ("11:00", "65fm.py") under the right weekday in REGULAR.

This file replaces fixed UTC strings with Orlando-local authoring. No more manual UTC math.
"""

import schedule
import time
import subprocess
import logging
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# =========================
# CONFIG
# =========================
LOCAL_TZ = ZoneInfo("America/New_York")   # Orlando time
SERVER_TZ = datetime.now().astimezone().tzinfo  # Server's local tz (auto-detected)

# Fire-only shift (in hours). Negative = earlier, Positive = later.
FIRE_SHIFT_ENABLED = True
FIRE_SHIFT_HOURS = -1   # << set to 0 to return to normal; ONLY affects fire blocks >>

LOG_DIR = "logs"
SCRIPTS_DIR = "scripts"

# =========================
# LOGGING
# =========================
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scheduler.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_script(script: str):
    """Run the specified Python script under scripts/."""
    try:
        path = os.path.join(SCRIPTS_DIR, script)
        print(f"Running script: {path}")
        logging.info(f"Running script: {path}")
        subprocess.run(["python", path], check=True)
        print(f"Script {script} ran successfully.")
        logging.info(f"Script {script} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script}: {e}")
        logging.error(f"Error running script {script}: {e}")
    except Exception as e:
        print(f"Unexpected error running script {script}: {e}")
        logging.error(f"Unexpected error running script {script}: {e}")

# =========================
# HELPER: schedule a local Orlando time on the correct server weekday/time
# =========================
WEEKDAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def schedule_local(weekday_name: str, hhmm: str, script: str):
    """
    Schedule a job defined in Orlando local time against the server's timezone.
    - weekday_name: 'monday'..'sunday'
    - hhmm: 'HH:MM' in Orlando time
    - script: 'somefile.py'
    """
    weekday_name = weekday_name.lower()
    if weekday_name not in WEEKDAYS:
        raise ValueError(f"Bad weekday: {weekday_name}")

    # Build a LOCAL datetime (next occurrence of that weekday at hh:mm)
    now_local = datetime.now(LOCAL_TZ)
    target_time = datetime.strptime(hhmm, "%H:%M").time()
    # Start from today in local time; find next weekday match
    days_ahead = (WEEKDAYS.index(weekday_name) - now_local.weekday()) % 7
    candidate = (now_local + timedelta(days=days_ahead)).replace(hour=target_time.hour,
                                                                 minute=target_time.minute,
                                                                 second=0, microsecond=0)
    # If time already passed for that weekday today, push one week
    if candidate <= now_local:
        candidate += timedelta(days=7)

    # Convert to server time to determine the real server weekday/time string
    candidate_server = candidate.astimezone(SERVER_TZ)
    server_weekday = WEEKDAYS[candidate_server.weekday()]
    server_hhmm = candidate_server.strftime("%H:%M")

    # Schedule on server-local time/day
    getattr(schedule.every(), server_weekday).at(server_hhmm).do(run_script, script=script)

def schedule_block(day: str, items: list[tuple[str,str]]):
    """Schedule a list of (HH:MM, script) for a given day (local)."""
    for hhmm, script in items:
        schedule_local(day, hhmm, script)

def shifted(hhmm: str, hours: int) -> str:
    """Shift an HH:MM string by N hours (keep minutes)."""
    dt = datetime(2000,1,1, int(hhmm[:2]), int(hhmm[3:5]), tzinfo=LOCAL_TZ)
    dt2 = dt + timedelta(hours=hours)
    return dt2.strftime("%H:%M")

# =========================
# DATA: Orlando local times
# =========================
# NOTE: These are the same shows as before, but authored in LOCAL time
#       (we used your inline comments to map to local times).
#       If you previously started a day at "15:00  # 11:00 AM EDT", that is now "11:00".

# ---- Regular daytime/evening blocks (LOCAL Orlando time) ----
REGULAR = {
    "monday": [
        ("11:00","65fm.py"), ("11:15","65sm.py"), ("11:30","65fm.py"), ("11:45","65sm.py"),
        ("12:00","75TIGS.py"), ("12:15","65sm.py"), ("12:30","70fm.py"), ("12:45","70sm.py"),
        ("13:00","70parking.py"), ("13:15","75TIGS.py"), ("13:30","70fm.py"), ("13:45","70sm.py"),
        ("14:00","75fm.py"), ("14:15","75sm.py"), ("14:30","75fm.py"), ("14:45","75TIGS.py"),
        ("15:00","75parking.py"), ("15:15","75sm.py"), ("15:30","75fm.py"), ("15:45","75sm.py"),
        ("16:00","parking.py"), ("16:15","75sm.py"), ("16:30","75fm.py"), ("16:45","75sm.py"),
        ("17:00","75parking.py"), ("17:15","75TIGS.py"), ("17:30","75fm.py"), ("17:45","75sm.py"),
        ("18:00","75parking.py"), ("18:15","75TIGS.py"),
    ],
    "tuesday": [
        ("12:00","65parking.py"), ("12:15","65sm.py"), ("12:30","65sm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"), ("13:45","65sm.py"),
        ("14:00","pause.py"),
        ("11:00","65fm.py"), ("11:15","65sm.py"), ("11:30","65fm.py"), ("11:45","65sm.py"),
        ("12:00","65fm.py"), ("12:15","65sm.py"), ("12:30","65fm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","75TIGS.py"), ("13:30","65fm.py"), ("13:45","65sm.py"),
        ("14:00","65oarking.py"), ("14:15","65sm.py"), ("14:30","70fm.py"), ("14:45","70sm.py"),
        ("15:00","70oarking.py"), ("15:15","70sm.py"), ("15:30","75TIGS.py"), ("15:45","70sm.py"),
        ("16:00","75parking.py"), ("16:15","75sm.py"), ("16:30","75TIGS.py"), ("16:45","75sm.py"),
        ("17:00","75parking.py"), ("17:15","75sm.py"), ("17:30","75TIGS.py"), ("17:45","75sm.py"),
        ("18:00","75parking.py"), ("18:15","75TIGS.py"),
    ],
    "wednesday": [
        ("12:00","65parking.py"), ("12:15","65sm.py"), ("12:30","65sm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"), ("13:45","65sm.py"),
        ("14:00","pause.py"),
        ("11:00","65fm.py"), ("11:15","65sm.py"), ("11:30","75TIGS.py"), ("11:45","65sm.py"),
        ("12:00","65fm.py"), ("12:15","65sm.py"), ("12:30","75TIGS.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65fm.py"), ("13:45","65sm.py"),
        ("14:00","75TIGS.py"), ("14:15","65sm.py"), ("14:30","65fm.py"), ("14:45","70sm.py"),
        ("15:00","70parking.py"), ("15:15","70sm.py"), ("15:30","75TIGS.py"), ("15:45","70sm.py"),
        ("16:00","70parking.py"), ("16:15","70sm.py"), ("16:30","75TIGS.py"), ("16:45","75sm.py"),
        ("17:00","80parking.py"), ("17:15","80sm.py"), ("17:30","80fm.py"), ("17:45","80sm.py"),
        ("18:00","80parking.py"), ("18:15","80sm.py"),
    ],
    "thursday": [
        ("12:00","65parking.py"), ("12:15","65sm.py"), ("12:30","65sm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"), ("13:45","65sm.py"),
        ("14:00","pause.py"),
        ("11:00","75TIGS.py"), ("11:15","75sm.py"), ("11:30","75fm.py"), ("11:45","75sm.py"),
        ("12:00","75parking.py"), ("12:15","75TIGS.py"), ("12:30","75fm.py"), ("12:45","75sm.py"),
        ("13:00","75TIGS.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
        ("14:00","75parking.py"), ("14:15","75sm.py"), ("14:30","75TIGS.py"), ("14:45","75sm.py"),
        ("15:00","80parking.py"), ("15:15","80sm.py"), ("15:30","80fm.py"), ("15:45","80sm.py"),
        ("16:00","80parking.py"), ("16:15","80sm.py"), ("16:30","80fm.py"), ("16:45","80sm.py"),
        ("17:00","80parking.py"), ("17:15","80ad.py"), ("17:30","80fm.py"), ("17:45","80sm.py"),
        ("18:00","80parking.py"), ("18:15","80sm.py"),
    ],
    "friday": [
        ("12:00","65parking.py"), ("12:15","65sm.py"), ("12:30","65sm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"), ("13:45","65sm.py"),
        ("14:00","50parking.py"), ("14:15","50sm.py"), ("14:30","50sm.py"), ("14:45","50sm.py"),
        ("15:00","50parking.py"), ("15:15","50sm.py"), ("15:30","50sm.py"), ("15:45","50sm.py"),
        ("16:00","pause.py"),
        ("11:00","75fm.py"), ("11:15","75sm.py"), ("11:30","75TIGS.py"), ("11:45","75sm.py"),
        ("12:00","75fm.py"), ("12:15","75sm.py"), ("12:30","75fm.py"), ("12:45","75TIGS.py"),
        ("13:00","75parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
        ("14:00","75parking.py"), ("14:15","75TIGS.py"), ("14:30","75fm.py"), ("14:45","75sm.py"),
        ("15:00","80parking.py"), ("15:15","80sm.py"), ("15:30","80fm.py"), ("15:45","80sm.py"),
        ("16:00","90parking.py"), ("16:15","90ad.py"), ("16:30","90fm.py"), ("16:45","90sm.py"),
        ("17:00","90parking.py"), ("17:15","90ad.py"), ("17:30","90fm.py"), ("17:45","90fm.py"),
        ("18:00","90parking.py"), ("18:15","90sm.py"),
    ],
    "saturday": [
        ("12:00","70parking.py"), ("12:00","70.py"), ("12:15","70sm.py"), ("12:30","65sm.py"),
        ("12:45","65sm.py"), ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"),
        ("13:45","65sm.py"), ("14:00","65sm.py"), ("14:15","65sm.py"), ("14:30","65sm.py"),
        ("14:45","65sm.py"), ("15:00","65parking.py"), ("15:15","65sm.py"), ("15:30","65sm.py"),
        ("15:45","65sm.py"), ("16:00","pause.py"),
        ("11:00","75fm.py"), ("11:15","75sm.py"), ("11:30","75parking.py"), ("11:45","75sm.py"),
        ("12:00","75parking.py"), ("12:15","75sm.py"), ("12:30","75fm.py"), ("12:45","75sm.py"),
        ("13:00","75parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
        ("14:00","75parking.py"), ("14:15","75sm.py"), ("14:30","75ad.py"), ("14:45","75sm.py"),
        ("15:00","75parking.py"), ("15:15","75sm.py"), ("15:30","75ad.py"), ("15:45","75sm.py"),
        ("16:00","75parking.py"), ("16:15","75sm.py"),
        ("17:00","85parking.py"), ("17:15","85sm.py"), ("17:30","85ad.py"), ("17:45","85sm.py"),
        ("18:00","85parking.py"), ("18:15","85sm.py"),
    ],
    "sunday": [
        ("12:00","65parking.py"), ("12:15","65sm.py"), ("12:30","65sm.py"), ("12:45","65sm.py"),
        ("13:00","65parking.py"), ("13:15","65sm.py"), ("13:30","65sm.py"), ("13:45","65sm.py"),
        ("14:00","pause.py"),
        ("11:00","70fm.py"), ("11:15","70sm.py"), ("11:30","70parking.py"), ("11:45","70sm.py"),
        ("12:00","70fm.py"), ("12:15","70sm.py"), ("12:30","70fm.py"), ("12:45","70sm.py"),
        ("13:00","70parking.py"), ("13:15","75sm.py"), ("13:30","75fm.py"), ("13:45","75sm.py"),
        ("14:00","75parking.py"), ("14:15","80sm.py"), ("14:30","80fm.py"), ("14:45","80sm.py"),
        ("15:00","85parking.py"), ("15:15","85ad.py"), ("15:30","85fm.py"), ("15:45","85fm.py"),
        ("16:00","85parking.py"), ("16:15","85sm.py"), ("16:30","85sm.py"), ("16:45","85ad.py"),
        ("17:00","85parking.py"), ("17:15","85sm.py"), ("17:30","85sm.py"), ("17:45","85sm.py"),
        ("18:00","85parking.py"),
    ],
}

# ---- Fire programming (LOCAL Orlando time) ----
# Original base: fire show at 6:45 PM local.
# With FIRE_SHIFT_HOURS=-1 → it will start at 5:45 PM and end one hour earlier (FIRE ONLY).

FIRE = {
    # Mon 6:45–11:00 PM + top-of-hour parking/ad sequence into 3:00 AM (pattern preserved)
    "monday":  [
        ("18:45","75fireparking.py"), ("19:00","75fireparking.py"), ("19:50","75adfire.py"),
        ("20:00","75fireparking.py"), ("20:50","75adfire.py"), ("21:00","75fireparking.py"),
        ("21:50","75adfire.py"), ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
        ("23:00","75fireparking.py"),
        # next day (Tue) early morning wrap
        ("00:00","75fireparking.py"), ("00:50","75adfire.py"),
        ("01:00","75fireparking.py"), ("01:50","75adfire.py"),
        ("02:00","75fireparking.py"), ("02:50","75adfire.py"),
        ("03:00","75fireparking.py"),
    ],
    "tuesday": [
        ("18:45","75fireparking.py"), ("19:00","75fireparking.py"), ("19:50","75adfire.py"),
        ("20:00","75fireparking.py"), ("20:50","75adfire.py"), ("21:00","75fireparking.py"),
        ("21:50","75adfire.py"), ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
        ("23:00","75fireparking.py"),
        ("00:00","75fireparking.py"), ("00:50","75adfire.py"),
        ("01:00","75fireparking.py"), ("01:50","75adfire.py"),
        ("02:00","75fireparking.py"), ("02:50","75adfire.py"),
        ("03:00","75fireparking.py"),
    ],
    "wednesday": [
        ("18:45","75parkingfire.py"), ("19:00","75parkingfire.py"), ("19:50","75adfire.py"),
        ("20:00","75parkingfire.py"), ("20:50","75adfire.py"), ("21:00","75parkingfire.py"),
        ("21:50","75adfire.py"), ("22:00","75parkingfire.py"), ("22:50","75adfire.py"),
        ("23:00","75parkingfire.py"),
        ("00:00","75parkingfire.py"), ("00:50","75adfire.py"),
        ("01:00","75parkingfire.py"), ("01:50","75adfire.py"),
        ("02:00","75parkingfire.py"), ("02:50","75adfire.py"),
        ("03:00","75parkingfire.py"),
    ],
    "thursday": [
        ("18:45","85fireparking.py"), ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
        ("20:00","85fireparking.py"), ("20:50","85adfire.py"), ("21:00","85fireparking.py"),
        ("21:50","85adfire.py"), ("22:00","85fireparking.py"), ("22:50","85adfire.py"),
        ("23:00","85fireparking.py"),
        ("00:00","85fireparking.py"), ("00:50","85adfire.py"),
        ("01:00","85fireparking.py"), ("01:50","75adfire.py"),
        ("02:00","75fireparking.py"), ("02:50","75adfire.py"),
        ("03:00","75fireparking.py"),
    ],
    "friday": [
        ("18:45","85fireparking.py"), ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
        ("20:00","85fireparking.py"), ("20:50","85adfire.py"), ("21:00","85fireparking.py"),
        ("21:50","80adfire.py"), ("22:00","85fireparking.py"), ("22:50","80adfire.py"),
        ("23:00","85fireparking.py"),
        ("00:00","85fireparking.py"), ("00:50","85adfire.py"),
        ("01:00","85fireparking.py"), ("01:50","80adfire.py"),
        ("02:00","85fireparking.py"), ("02:50","80adfire.py"),
        ("03:00","85fireparking.py"),
    ],
    "saturday": [
        ("18:45","85fireparking.py"), ("19:00","85fireparking.py"), ("19:50","85adfire.py"),
        ("20:00","85fireparking.py"), ("20:50","85adfire.py"), ("21:00","85fireparking.py"),
        ("21:50","85adfire.py"), ("22:00","85fireparking.py"), ("22:50","80adfire.py"),
        ("23:00","75fireparking.py"),
        ("00:00","85fireparking.py"), ("00:50","85adfire.py"),
        ("01:00","85fireparking.py"), ("01:50","85adfire.py"),
        ("02:00","85fireparking.py"), ("02:50","80adfire.py"),
        ("03:00","75fireparking.py"),
    ],
    "sunday": [
        ("18:45","85fireparking.py"), ("19:15","85fireparking.py"), ("19:50","80adfire.py"),
        ("20:00","85fireparking.py"), ("20:50","80adfire.py"), ("21:00","75fireparking.py"),
        ("21:50","75adfire.py"), ("22:00","75fireparking.py"), ("22:50","75adfire.py"),
        ("23:00","75fireparking.py"),
        ("00:00","85fireparking.py"), ("00:50","80adfire.py"),
        ("01:00","75fireparking.py"), ("01:50","75adfire.py"),
        ("02:00","75fireparking.py"), ("02:50","75adfire.py"),
        ("03:00","75fireparking.py"),
    ],
}

# =========================
# SCHEDULING
# =========================
def schedule_tasks():
    # Regular (non-fire) programming
    for day, items in REGULAR.items():
        schedule_block(day, items)

    # Fire programming with optional shift
    for day, items in FIRE.items():
        if FIRE_SHIFT_ENABLED and FIRE_SHIFT_HOURS != 0:
            shifted_items = [(shifted(hhmm, FIRE_SHIFT_HOURS), script) for hhmm, script in items]
            schedule_block(day, shifted_items)
        else:
            schedule_block(day, items)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print(f"Timezone authoring: America/New_York; Server timezone detected: {SERVER_TZ}")
    if FIRE_SHIFT_ENABLED:
        print(f"FIRE blocks shifted by {FIRE_SHIFT_HOURS} hour(s). (Only fire schedule is shifted.)")
    else:
        print("FIRE shift disabled; using base fire times.")

    schedule_tasks()

    print("Scheduler started. All times listed in code are Orlando local; conversion applied at runtime.")
    while True:
        schedule.run_pending()
        time.sleep(1)