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
  
#MONDAY
    # Monday to Tuesday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().monday.at("16:00").do(run_script, script="65fm.py")  # 11:00 AM EST
    schedule.every().monday.at("16:15").do(run_script, script="65sm.py")  # 11:15 AM EST
    schedule.every().monday.at("16:30").do(run_script, script="65fm.py")  # 11:30 AM EST
    schedule.every().monday.at("16:45").do(run_script, script="65sm.py")  # 11:45 AM EST
    schedule.every().monday.at("17:00").do(run_script, script="65fm.py")  # 12:00 PM EST
    schedule.every().monday.at("17:15").do(run_script, script="65sm.py")  # 12:15 PM EST
    schedule.every().monday.at("17:30").do(run_script, script="70fm.py")  # 12:30 PM EST
    schedule.every().monday.at("17:45").do(run_script, script="70sm.py")  # 12:45 PM EST
    schedule.every().monday.at("18:00").do(run_script, script="70fm.py")  # 1:00 PM EST
    schedule.every().monday.at("18:15").do(run_script, script="70sm.py")  # 1:15 PM EST
    schedule.every().monday.at("18:30").do(run_script, script="70fm.py")  # 1:30 PM EST
    schedule.every().monday.at("18:45").do(run_script, script="70sm.py")  # 1:45 PM EST
    schedule.every().monday.at("19:00").do(run_script, script="75fm.py")  # 2:00 PM EST
    schedule.every().monday.at("19:15").do(run_script, script="75sm.py")  # 2:15 PM EST
    schedule.every().monday.at("19:30").do(run_script, script="75fm.py")  # 2:30 PM EST
    schedule.every().monday.at("19:45").do(run_script, script="75sm.py")  # 2:45 PM EST
    schedule.every().monday.at("20:00").do(run_script, script="75fm.py")  # 3:00 PM EST
    schedule.every().monday.at("20:15").do(run_script, script="75sm.py")  # 3:15 PM EST
    schedule.every().monday.at("20:30").do(run_script, script="75fm.py")  # 3:30 PM EST
    schedule.every().monday.at("20:45").do(run_script, script="75sm.py")  # 3:45 PM EST
    schedule.every().monday.at("21:00").do(run_script, script="75fm.py")  # 4:00 PM EST
    schedule.every().monday.at("21:15").do(run_script, script="75sm.py")  # 4:15 PM EST
    schedule.every().monday.at("21:30").do(run_script, script="75fm.py")  # 4:30 PM EST
    schedule.every().monday.at("21:45").do(run_script, script="75sm.py")  # 4:45 PM EST
    schedule.every().monday.at("22:00").do(run_script, script="75fm.py")  # 5:00 PM EST
    schedule.every().monday.at("22:15").do(run_script, script="75sm.py")  # 5:15 PM EST
    schedule.every().monday.at("22:30").do(run_script, script="75fm.py")  # 5:30 PM EST
    schedule.every().monday.at("22:45").do(run_script, script="75sm.py")  # 5:45 PM EST
    schedule.every().monday.at("23:00").do(run_script, script="75fm.py")  # 6:00 PM EST
    schedule.every().monday.at("23:15").do(run_script, script="75sm.py")  # 6:15 PM EST
    schedule.every().monday.at("23:30").do(run_script, script="75fm.py")  # 6:30 PM EST
    schedule.every().monday.at("23:45").do(run_script, script="75sm.py")  # 6:45 PM EST
    schedule.every().tuesday.at("00:00").do(run_script, script="75fm.py")  # 7:00 PM EST
    schedule.every().tuesday.at("00:15").do(run_script, script="75sm.py")  # 7:15 PM EST
    schedule.every().tuesday.at("00:30").do(run_script, script="75fm.py")  # 7:30 PM EST
    schedule.every().tuesday.at("00:45").do(run_script, script="75sm.py")  # 7:45 PM EST
    schedule.every().tuesday.at("01:00").do(run_script, script="75fm.py")  # 8:00 PM EST
    schedule.every().tuesday.at("01:15").do(run_script, script="75sm.py")  # 8:15 PM EST
    schedule.every().tuesday.at("01:30").do(run_script, script="75fm.py")  # 8:30 PM EST
    schedule.every().tuesday.at("01:45").do(run_script, script="75fm.py")  # 8:45 PM EST
    schedule.every().tuesday.at("02:00").do(run_script, script="75sm.py")  # 9:00 PM EST
    schedule.every().tuesday.at("02:30").do(run_script, script="75sm.py")  # 9:30 PM EST
    schedule.every().tuesday.at("02:45").do(run_script, script="75sm.py")  # 9:45 PM EST
    schedule.every().tuesday.at("03:00").do(run_script, script="75sm.py")  # 10:00 PM EST
    schedule.every().tuesday.at("03:30").do(run_script, script="75sm.py")  # 10:30 PM EST
    schedule.every().tuesday.at("04:00").do(run_script, script="70sm.py")  # 11:00 PM EST
    schedule.every().tuesday.at("04:30").do(run_script, script="65sm.py")  # 11:30 PM EST
    schedule.every().tuesday.at("05:00").do(run_script, script="65sm.py")  # 12:00 AM
    schedule.every().tuesday.at("05:30").do(run_script, script="65sm.py")  # 12:30 AM
    schedule.every().tuesday.at("06:00").do(run_script, script="65sm.py")  # 1:00 AM
    schedule.every().tuesday.at("06:59").do(run_script, script="pause.py") # 1:59 AM
    
   
    # Tuesday to Wednesday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().tuesday.at("16:00").do(run_script, script="65fm.py")  # 11:00 AM EST
    schedule.every().tuesday.at("16:15").do(run_script, script="65sm.py")  # 11:15 AM EST
    schedule.every().tuesday.at("16:30").do(run_script, script="65fm.py")  # 11:30 AM EST
    schedule.every().tuesday.at("16:45").do(run_script, script="65sm.py")  # 11:45 AM EST
    schedule.every().tuesday.at("17:00").do(run_script, script="65fm.py")  # 12:00 PM EST
    schedule.every().tuesday.at("17:15").do(run_script, script="65sm.py")  # 12:15 PM EST
    schedule.every().tuesday.at("17:30").do(run_script, script="65fm.py")  # 12:30 PM EST
    schedule.every().tuesday.at("17:45").do(run_script, script="65sm.py")  # 12:45 PM EST
    schedule.every().tuesday.at("18:00").do(run_script, script="65fm.py")  # 1:00 PM EST
    schedule.every().tuesday.at("18:15").do(run_script, script="65sm.py")  # 1:15 PM EST
    schedule.every().tuesday.at("18:30").do(run_script, script="65fm.py")  # 1:30 PM EST
    schedule.every().tuesday.at("18:45").do(run_script, script="65sm.py")  # 1:45 PM EST
    schedule.every().tuesday.at("19:00").do(run_script, script="65fm.py")  # 2:00 PM EST
    schedule.every().tuesday.at("19:15").do(run_script, script="65sm.py")  # 2:15 PM EST
    schedule.every().tuesday.at("19:30").do(run_script, script="70fm.py")  # 2:30 PM EST
    schedule.every().tuesday.at("19:45").do(run_script, script="70sm.py")  # 2:45 PM EST
    schedule.every().tuesday.at("20:00").do(run_script, script="70fm.py")  # 3:00 PM EST
    schedule.every().tuesday.at("20:15").do(run_script, script="70sm.py")  # 3:15 PM EST
    schedule.every().tuesday.at("20:30").do(run_script, script="70fm.py")  # 3:30 PM EST
    schedule.every().tuesday.at("20:45").do(run_script, script="70sm.py")  # 3:45 PM EST
    schedule.every().tuesday.at("21:00").do(run_script, script="75fm.py")  # 4:00 PM EST
    schedule.every().tuesday.at("21:15").do(run_script, script="75sm.py")  # 4:15 PM EST
    schedule.every().tuesday.at("21:30").do(run_script, script="75fm.py")  # 4:30 PM EST
    schedule.every().tuesday.at("21:45").do(run_script, script="75sm.py")  # 4:45 PM EST
    schedule.every().tuesday.at("22:00").do(run_script, script="75fm.py")  # 5:00 PM EST
    schedule.every().tuesday.at("22:15").do(run_script, script="75sm.py")  # 5:15 PM EST
    schedule.every().tuesday.at("22:30").do(run_script, script="75fm.py")  # 5:30 PM EST
    schedule.every().tuesday.at("22:45").do(run_script, script="75sm.py")  # 5:45 PM EST
    schedule.every().tuesday.at("23:00").do(run_script, script="75fm.py")  # 6:00 PM EST
    schedule.every().tuesday.at("23:15").do(run_script, script="75sm.py")  # 6:15 PM EST
    schedule.every().tuesday.at("23:30").do(run_script, script="75fm.py")  # 6:30 PM EST
    schedule.every().tuesday.at("23:45").do(run_script, script="75sm.py")  # 6:45 PM EST
    schedule.every().wednesday.at("00:00").do(run_script, script="75fm.py")  # 7:00 PM EST
    schedule.every().wednesday.at("00:15").do(run_script, script="75sm.py")  # 7:15 PM EST
    schedule.every().wednesday.at("00:30").do(run_script, script="75fm.py")  # 7:30 PM EST
    schedule.every().wednesday.at("00:45").do(run_script, script="75fm.py")  # 7:45 PM EST
    schedule.every().wednesday.at("01:00").do(run_script, script="75sm.py")  # 8:00 PM EST
    schedule.every().wednesday.at("01:30").do(run_script, script="75sm.py")  # 8:30 PM EST
    schedule.every().wednesday.at("01:45").do(run_script, script="75sm.py")  # 8:45 PM EST
    schedule.every().wednesday.at("02:00").do(run_script, script="75sm.py")  # 9:00 PM EST
    schedule.every().wednesday.at("02:30").do(run_script, script="75sm.py")  # 9:30 PM EST
    schedule.every().wednesday.at("03:00").do(run_script, script="70fm.py")  # 10:00 PM EST
    schedule.every().wednesday.at("03:30").do(run_script, script="65sm.py")  # 10:30 PM EST
    schedule.every().wednesday.at("04:00").do(run_script, script="65sm.py")  # 11:00 PM EST
    schedule.every().wednesday.at("04:30").do(run_script, script="65sm.py")  # 11:30 PM
    schedule.every().wednesday.at("05:00").do(run_script, script="65sm.py")  # 12:00 AM
    schedule.every().wednesday.at("05:30").do(run_script, script="65sm.py")  # 12:30 AM
    schedule.every().wednesday.at("06:00").do(run_script, script="65sm.py")  # 01:00 AM
    schedule.every().wednesday.at("06:59").do(run_script, script="pause.py") # 01:59 AM 

    
    # Wednesday to Thursday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().wednesday.at("16:00").do(run_script, script="65fm.py")  # 11:00 AM EST
    schedule.every().wednesday.at("16:15").do(run_script, script="65sm.py")  # 11:15 AM EST
    schedule.every().wednesday.at("16:30").do(run_script, script="65fm.py")  # 11:30 AM EST
    schedule.every().wednesday.at("16:45").do(run_script, script="65sm.py")  # 11:45 AM EST
    schedule.every().wednesday.at("17:00").do(run_script, script="65fm.py")  # 12:00 PM EST
    schedule.every().wednesday.at("17:15").do(run_script, script="65sm.py")  # 12:15 PM EST
    schedule.every().wednesday.at("17:30").do(run_script, script="65fm.py")  # 12:30 PM EST
    schedule.every().wednesday.at("17:45").do(run_script, script="65sm.py")  # 12:45 PM EST
    schedule.every().wednesday.at("18:00").do(run_script, script="65fm.py")  # 1:00 PM EST
    schedule.every().wednesday.at("18:15").do(run_script, script="65sm.py")  # 1:15 PM EST
    schedule.every().wednesday.at("18:30").do(run_script, script="65fm.py")  # 1:30 PM EST
    schedule.every().wednesday.at("18:45").do(run_script, script="65sm.py")  # 1:45 PM EST
    schedule.every().wednesday.at("19:00").do(run_script, script="65fm.py")  # 2:00 PM EST
    schedule.every().wednesday.at("19:15").do(run_script, script="65sm.py")  # 2:15 PM EST
    schedule.every().wednesday.at("19:30").do(run_script, script="65fm.py")  # 2:30 PM EST
    schedule.every().wednesday.at("19:45").do(run_script, script="70sm.py")  # 2:45 PM EST
    schedule.every().wednesday.at("20:00").do(run_script, script="70fm.py")  # 3:00 PM EST
    schedule.every().wednesday.at("20:15").do(run_script, script="70sm.py")  # 3:15 PM EST
    schedule.every().wednesday.at("20:30").do(run_script, script="70fm.py")  # 3:30 PM EST
    schedule.every().wednesday.at("20:45").do(run_script, script="70sm.py")  # 3:45 PM EST
    schedule.every().wednesday.at("21:00").do(run_script, script="70fm.py")  # 4:00 PM EST
    schedule.every().wednesday.at("21:15").do(run_script, script="70sm.py")  # 4:15 PM EST
    schedule.every().wednesday.at("21:30").do(run_script, script="70fm.py")  # 4:30 PM EST
    schedule.every().wednesday.at("21:45").do(run_script, script="75sm.py")  # 4:45 PM EST
    schedule.every().wednesday.at("22:00").do(run_script, script="75fm.py")  # 5:00 PM EST
    schedule.every().wednesday.at("22:15").do(run_script, script="75sm.py")  # 5:15 PM EST
    schedule.every().wednesday.at("22:30").do(run_script, script="75fm.py")  # 5:30 PM EST
    schedule.every().wednesday.at("22:45").do(run_script, script="75sm.py")  # 5:45 PM EST
    schedule.every().wednesday.at("23:00").do(run_script, script="75fm.py")  # 6:00 PM EST
    schedule.every().wednesday.at("23:15").do(run_script, script="75sm.py")  # 6:15 PM EST
    schedule.every().wednesday.at("23:30").do(run_script, script="75fm.py")  # 6:30 PM EST
    schedule.every().wednesday.at("23:45").do(run_script, script="75sm.py")  # 6:45 PM EST
    schedule.every().thursday.at("00:00").do(run_script, script="75fm.py")  # 7:00 PM EST
    schedule.every().thursday.at("00:15").do(run_script, script="75sm.py")  # 7:15 PM EST
    schedule.every().thursday.at("00:30").do(run_script, script="75fm.py")  # 7:30 PM EST
    schedule.every().thursday.at("00:45").do(run_script, script="75fm.py")  # 7:45 PM EST
    schedule.every().thursday.at("01:00").do(run_script, script="75sm.py")  # 8:00 PM EST
    schedule.every().thursday.at("01:30").do(run_script, script="75sm.py")  # 8:30 PM EST
    schedule.every().thursday.at("01:45").do(run_script, script="75sm.py")  # 8:45 PM EST
    schedule.every().thursday.at("02:00").do(run_script, script="75sm.py")  # 9:00 PM EST
    schedule.every().thursday.at("02:30").do(run_script, script="75sm.py")  # 9:30 PM EST
    schedule.every().thursday.at("03:00").do(run_script, script="75sm.py")  # 10:00 PM EST
    schedule.every().thursday.at("03:30").do(run_script, script="65sm.py")  # 10:30 PM EST
    schedule.every().thursday.at("04:00").do(run_script, script="65sm.py")  # 11:00 PM EST
    schedule.every().thursday.at("04:30").do(run_script, script="65sm.py")  # 11:30 PM
    schedule.every().thursday.at("05:00").do(run_script, script="65sm.py")  # 12:00 AM
    schedule.every().thursday.at("05:30").do(run_script, script="65sm.py")  # 12:30 AM
    schedule.every().thursday.at("06:00").do(run_script, script="65sm.py")  # 01:00 AM
    schedule.every().thursday.at("06:30").do(run_script, script="65sm.py")  # 01:30 AM
    schedule.every().thursday.at("06:59").do(run_script, script="pause.py") # 01:59 AM 
    
    

    # Thursday to Friday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().thursday.at("16:00").do(run_script, script="75fm.py")  # 11:00 AM EST
    schedule.every().thursday.at("16:15").do(run_script, script="75sm.py")  # 11:15 AM EST
    schedule.every().thursday.at("16:30").do(run_script, script="75fm.py")  # 11:30 AM EST
    schedule.every().thursday.at("16:45").do(run_script, script="75sm.py")  # 11:45 AM EST
    schedule.every().thursday.at("17:00").do(run_script, script="75fm.py")  # 12:00 PM EST
    schedule.every().thursday.at("17:15").do(run_script, script="75sm.py")  # 12:15 PM EST
    schedule.every().thursday.at("17:30").do(run_script, script="75fm.py")  # 12:30 PM EST
    schedule.every().thursday.at("17:45").do(run_script, script="75sm.py")  # 12:45 PM EST
    schedule.every().thursday.at("18:00").do(run_script, script="75fm.py")  # 1:00 PM EST
    schedule.every().thursday.at("18:15").do(run_script, script="75sm.py")  # 1:15 PM EST
    schedule.every().thursday.at("18:30").do(run_script, script="75fm.py")  # 1:30 PM EST
    schedule.every().thursday.at("18:45").do(run_script, script="75sm.py")  # 1:45 PM EST
    schedule.every().thursday.at("19:00").do(run_script, script="75fm.py")  # 2:00 PM EST
    schedule.every().thursday.at("19:15").do(run_script, script="75sm.py")  # 2:15 PM EST
    schedule.every().thursday.at("19:30").do(run_script, script="75fm.py")  # 2:30 PM EST
    schedule.every().thursday.at("19:45").do(run_script, script="75sm.py")  # 2:45 PM EST
    schedule.every().thursday.at("20:00").do(run_script, script="75fm.py")  # 3:00 PM EST
    schedule.every().thursday.at("20:15").do(run_script, script="75sm.py")  # 3:15 PM EST
    schedule.every().thursday.at("20:30").do(run_script, script="75fm.py")  # 3:30 PM EST
    schedule.every().thursday.at("20:45").do(run_script, script="75sm.py")  # 3:45 PM EST
    schedule.every().thursday.at("21:00").do(run_script, script="75fm.py")  # 4:00 PM EST
    schedule.every().thursday.at("21:15").do(run_script, script="75sm.py")  # 4:15 PM EST
    schedule.every().thursday.at("21:30").do(run_script, script="75fm.py")  # 4:30 PM EST
    schedule.every().thursday.at("21:45").do(run_script, script="75sm.py")  # 4:45 PM EST
    schedule.every().thursday.at("22:00").do(run_script, script="75fm.py")  # 5:00 PM EST
    schedule.every().thursday.at("22:15").do(run_script, script="75ad.py")  # 5:15 PM EST
    schedule.every().thursday.at("22:30").do(run_script, script="75fm.py")  # 5:30 PM EST
    schedule.every().thursday.at("22:45").do(run_script, script="75sm.py")  # 5:45 PM EST
    schedule.every().thursday.at("23:00").do(run_script, script="75fm.py")  # 6:00 PM EST
    schedule.every().thursday.at("23:15").do(run_script, script="75ad.py")  # 6:15 PM EST
    schedule.every().thursday.at("23:30").do(run_script, script="75fm.py")  # 6:30 PM EST
    schedule.every().thursday.at("23:45").do(run_script, script="75sm.py")  # 6:45 PM EST
    schedule.every().friday.at("00:00").do(run_script, script="75ad.py")    # 7:00 PM EST
    schedule.every().friday.at("00:15").do(run_script, script="75sm.py")    # 7:15 PM EST
    schedule.every().friday.at("00:30").do(run_script, script="75fm.py")    # 7:30 PM EST
    schedule.every().friday.at("00:45").do(run_script, script="75ad.py")    # 7:45 PM EST
    schedule.every().friday.at("01:00").do(run_script, script="75fm.py")    # 8:00 PM EST
    schedule.every().friday.at("01:30").do(run_script, script="75fm.py")    # 8:30 PM EST
    schedule.every().friday.at("01:45").do(run_script, script="75sm.py")    # 8:45 PM EST
    schedule.every().friday.at("02:00").do(run_script, script="75ad.py")    # 9:00 PM EST
    schedule.every().friday.at("02:30").do(run_script, script="75sm.py")    # 9:30 PM EST
    schedule.every().friday.at("03:00").do(run_script, script="75ad.py")    # 10:00 PM EST
    schedule.every().friday.at("03:30").do(run_script, script="65sm.py")    # 10:30 PM EST
    schedule.every().friday.at("04:00").do(run_script, script="65ad.py")    # 11:00 PM EST
    schedule.every().friday.at("04:30").do(run_script, script="65sm.py")    # 11:30 PM
    schedule.every().friday.at("05:00").do(run_script, script="65ad.py")    # 12:00 AM
    schedule.every().friday.at("05:30").do(run_script, script="65sm.py")    # 12:30 AM
    schedule.every().friday.at("06:00").do(run_script, script="65sm.py")    # 1:00 AM
    schedule.every().friday.at("06:30").do(run_script, script="65sm.py")    # 1:30 AM
    schedule.every().friday.at("06:59").do(run_script, script="pause.py")   # 1:59 AM 
    
    
    # Friday to Saturday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().friday.at("16:00").do(run_script, script="75fm.py")  # 11:00 AM EST
    schedule.every().friday.at("16:15").do(run_script, script="75sm.py")  # 11:15 AM EST
    schedule.every().friday.at("16:30").do(run_script, script="75fm.py")  # 11:30 AM EST
    schedule.every().friday.at("16:45").do(run_script, script="75sm.py")  # 11:45 AM EST
    schedule.every().friday.at("17:00").do(run_script, script="75fm.py")  # 12:00 PM EST
    schedule.every().friday.at("17:15").do(run_script, script="75sm.py")  # 12:15 PM EST
    schedule.every().friday.at("17:30").do(run_script, script="75fm.py")  # 12:30 PM EST
    schedule.every().friday.at("17:45").do(run_script, script="75sm.py")  # 12:45 PM EST
    schedule.every().friday.at("18:00").do(run_script, script="75fm.py")  # 1:00 PM EST
    schedule.every().friday.at("18:15").do(run_script, script="75sm.py")  # 1:15 PM EST
    schedule.every().friday.at("18:30").do(run_script, script="75fm.py")  # 1:30 PM EST
    schedule.every().friday.at("18:45").do(run_script, script="75sm.py")  # 1:45 PM EST
    schedule.every().friday.at("19:00").do(run_script, script="75fm.py")  # 2:00 PM EST
    schedule.every().friday.at("19:15").do(run_script, script="75sm.py")  # 2:15 PM EST
    schedule.every().friday.at("19:30").do(run_script, script="75fm.py")  # 2:30 PM EST
    schedule.every().friday.at("19:45").do(run_script, script="75sm.py")  # 2:45 PM EST
    schedule.every().friday.at("20:00").do(run_script, script="80ad.py")  # 3:00 PM EST
    schedule.every().friday.at("20:15").do(run_script, script="80sm.py")  # 3:15 PM EST
    schedule.every().friday.at("20:30").do(run_script, script="80fm.py")  # 3:30 PM EST
    schedule.every().friday.at("20:45").do(run_script, script="80sm.py")  # 3:45 PM EST
    schedule.every().friday.at("21:00").do(run_script, script="90fm.py")  # 4:00 PM EST
    schedule.every().friday.at("21:15").do(run_script, script="90ad.py")  # 4:15 PM EST
    schedule.every().friday.at("21:30").do(run_script, script="90fm.py")  # 4:30 PM EST
    schedule.every().friday.at("21:45").do(run_script, script="90sm.py")  # 4:45 PM EST
    schedule.every().friday.at("22:00").do(run_script, script="90fm.py")  # 5:00 PM EST
    schedule.every().friday.at("22:15").do(run_script, script="90ad.py")  # 5:15 PM EST
    schedule.every().friday.at("22:30").do(run_script, script="90fm.py")  # 5:30 PM EST
    schedule.every().friday.at("22:45").do(run_script, script="90fm.py")  # 5:45 PM EST
    schedule.every().friday.at("23:00").do(run_script, script="90fm.py")  # 6:00 PM EST
    schedule.every().friday.at("23:30").do(run_script, script="85ad.py")  # 6:30 PM EST
    schedule.every().friday.at("23:45").do(run_script, script="85fm.py")  # 6:45 PM EST
    schedule.every().saturday.at("00:00").do(run_script, script="85fm.py")  # 7:00 PM EST
    schedule.every().saturday.at("00:30").do(run_script, script="85fm.py")  # 7:30 PM EST
    schedule.every().saturday.at("01:00").do(run_script, script="85fm.py")  # 8:00 PM EST
    schedule.every().saturday.at("01:30").do(run_script, script="85ad.py")  # 8:30 PM EST
    schedule.every().saturday.at("02:00").do(run_script, script="85fm.py")  # 9:00 PM EST
    schedule.every().saturday.at("02:30").do(run_script, script="85fm.py")  # 9:30 PM EST
    schedule.every().saturday.at("03:00").do(run_script, script="85sm.py")  # 10:00 PM EST
    schedule.every().saturday.at("03:30").do(run_script, script="85ad.py")  # 10:30 PM EST
    schedule.every().saturday.at("04:00").do(run_script, script="80sm.py")  # 11:00 PM EST
    schedule.every().saturday.at("04:30").do(run_script, script="75sm.py")  # 11:30 PM EST
    schedule.every().saturday.at("05:00").do(run_script, script="75ad.py")  # 12:00 AM EST
    schedule.every().saturday.at("05:30").do(run_script, script="75sm.py")  # 12:30 AM EST
    schedule.every().saturday.at("06:00").do(run_script, script="65sm.py")  # 1:00 AM EST
    schedule.every().saturday.at("06:30").do(run_script, script="65ad.py")  # 1:30 AM EST
    schedule.every().saturday.at("07:00").do(run_script, script="65sm.py")  # 2:00 AM EST
    schedule.every().saturday.at("07:30").do(run_script, script="65sm.py")  # 2:30 AM EST
    schedule.every().saturday.at("08:00").do(run_script, script="pause.py")  # 3:00 AM EST
   
    
    # Saturday
    schedule.every().saturday.at("16:00").do(run_script, script="75fm.py")  # 11:00 EST
    schedule.every().saturday.at("16:15").do(run_script, script="75sm.py")  # 11:15 EST
    schedule.every().saturday.at("16:30").do(run_script, script="75fm.py")  # 11:30 EST
    schedule.every().saturday.at("16:45").do(run_script, script="75sm.py")  # 11:45 EST
    schedule.every().saturday.at("17:00").do(run_script, script="75fm.py")  # 12:00 EST
    schedule.every().saturday.at("17:15").do(run_script, script="75sm.py")  # 12:15 EST
    schedule.every().saturday.at("17:30").do(run_script, script="75fm.py")  # 12:30 EST
    schedule.every().saturday.at("17:45").do(run_script, script="75sm.py")  # 12:45 EST
    schedule.every().saturday.at("18:00").do(run_script, script="75fm.py")  # 13:00 EST
    schedule.every().saturday.at("18:15").do(run_script, script="75sm.py")  # 13:15 EST
    schedule.every().saturday.at("18:30").do(run_script, script="75fm.py")  # 13:30 EST
    schedule.every().saturday.at("18:45").do(run_script, script="75sm.py")  # 13:45 EST
    schedule.every().saturday.at("19:00").do(run_script, script="75fm.py")  # 14:00 EST
    schedule.every().saturday.at("19:15").do(run_script, script="75sm.py")  # 14:15 EST
    schedule.every().saturday.at("19:30").do(run_script, script="75ad.py")  # 14:30 EST
    schedule.every().saturday.at("19:45").do(run_script, script="75sm.py")  # 14:45 EST
    schedule.every().saturday.at("20:00").do(run_script, script="75fm.py")  # 15:00 EST
    schedule.every().saturday.at("20:15").do(run_script, script="75sm.py")  # 15:15 EST
    schedule.every().saturday.at("20:30").do(run_script, script="75ad.py")  # 15:30 EST
    schedule.every().saturday.at("20:45").do(run_script, script="75sm.py")  # 15:45 EST
    schedule.every().saturday.at("21:00").do(run_script, script="75fm.py")  # 16:00 EST
    schedule.every().saturday.at("21:15").do(run_script, script="75sm.py")  # 16:15 EST
    schedule.every().saturday.at("21:30").do(run_script, script="75ad.py")  # 16:30 EST
    schedule.every().saturday.at("21:45").do(run_script, script="75sm.py")  # 16:45 EST
    schedule.every().saturday.at("22:00").do(run_script, script="80fm.py")  # 17:00 EST
    schedule.every().saturday.at("22:15").do(run_script, script="80sm.py")  # 17:15 EST
    schedule.every().saturday.at("22:30").do(run_script, script="80ad.py")  # 17:30 EST
    schedule.every().saturday.at("22:45").do(run_script, script="80sm.py")  # 17:45 EST
    schedule.every().saturday.at("23:00").do(run_script, script="80fm.py")  # 18:00 EST
    schedule.every().saturday.at("23:15").do(run_script, script="85sm.py")  # 18:15 EST
    schedule.every().saturday.at("23:30").do(run_script, script="85ad.py")  # 18:30 EST
    schedule.every().saturday.at("23:45").do(run_script, script="85sm.py")  # 18:45 EST
    schedule.every().sunday.at("00:00").do(run_script, script="85fm.py")    # 19:00 EST
    schedule.every().sunday.at("00:15").do(run_script, script="85sm.py")    # 19:15 EST
    schedule.every().sunday.at("00:30").do(run_script, script="85ad.py")    # 19:30 EST
    schedule.every().sunday.at("00:45").do(run_script, script="85sm.py")    # 19:45 EST
    schedule.every().sunday.at("01:00").do(run_script, script="85fm.py")    # 20:00 EST
    schedule.every().sunday.at("01:30").do(run_script, script="85ad.py")    # 20:30 EST
    schedule.every().sunday.at("01:45").do(run_script, script="85fm.py")    # 20:45 EST
    schedule.every().sunday.at("02:00").do(run_script, script="85sm.py")    # 21:00 EST
    schedule.every().sunday.at("02:30").do(run_script, script="85ad.py")    # 21:30 EST
    schedule.every().sunday.at("03:00").do(run_script, script="85sm.py")    # 22:00 EST
    schedule.every().sunday.at("03:30").do(run_script, script="85sm.py")    # 22:30 EST
    schedule.every().sunday.at("04:00").do(run_script, script="85ad.py")    # 23:00 EST
    schedule.every().sunday.at("04:30").do(run_script, script="85sm.py")    # 23:30 EST
    schedule.every().sunday.at("05:00").do(run_script, script="85sm.py")    # 00:00 EST
    schedule.every().sunday.at("05:15").do(run_script, script="85ad.py")    # 00:15 EST
    schedule.every().sunday.at("05:30").do(run_script, script="85sm.py")    # 00:30 EST
    schedule.every().sunday.at("05:45").do(run_script, script="85sm.py")    # 00:45 EST
    schedule.every().sunday.at("06:00").do(run_script, script="85ad.py")    # 01:00 EST
    schedule.every().sunday.at("06:15").do(run_script, script="85sm.py")    # 01:15 EST
    schedule.every().sunday.at("06:30").do(run_script, script="85sm.py")    # 01:30 EST
    schedule.every().sunday.at("06:45").do(run_script, script="85sm.py")    # 01:45 EST
    schedule.every().sunday.at("07:00").do(run_script, script="80sm.py")    # 02:00 EST
    schedule.every().sunday.at("07:15").do(run_script, script="80sm.py")    # 02:15 EST
    schedule.every().sunday.at("07:30").do(run_script, script="75sm.py")    # 02:30 EST
    schedule.every().sunday.at("07:45").do(run_script, script="75sm.py")    # 02:45 EST
    schedule.every().sunday.at("08:00").do(run_script, script="pause.py")   # 03:00 EST
    
    
    
    # Sunday
    # Sunday schedule in UTC (EST = UTC - 5 hours)
    schedule.every().sunday.at("16:00").do(run_script, script="70fm.py")  # 11:00 AM EST
    schedule.every().sunday.at("16:15").do(run_script, script="70sm.py")  # 11:15 AM EST
    schedule.every().sunday.at("16:30").do(run_script, script="70fm.py")  # 11:30 AM EST
    schedule.every().sunday.at("16:45").do(run_script, script="70sm.py")  # 11:45 AM EST
    schedule.every().sunday.at("17:00").do(run_script, script="70fm.py")  # 12:00 PM EST
    schedule.every().sunday.at("17:15").do(run_script, script="70sm.py")  # 12:15 PM EST
    schedule.every().sunday.at("17:30").do(run_script, script="70fm.py")  # 12:30 PM EST
    schedule.every().sunday.at("17:45").do(run_script, script="70sm.py")  # 12:45 PM EST
    schedule.every().sunday.at("18:00").do(run_script, script="70fm.py")  # 1:00 PM EST
    schedule.every().sunday.at("18:15").do(run_script, script="75sm.py")  # 1:15 PM EST
    schedule.every().sunday.at("18:30").do(run_script, script="75fm.py")  # 1:30 PM EST
    schedule.every().sunday.at("18:45").do(run_script, script="75sm.py")  # 1:45 PM EST
    schedule.every().sunday.at("19:00").do(run_script, script="75fm.py")  # 2:00 PM EST
    schedule.every().sunday.at("19:15").do(run_script, script="80sm.py")  # 2:15 PM EST
    schedule.every().sunday.at("19:30").do(run_script, script="80fm.py")  # 2:30 PM EST
    schedule.every().sunday.at("19:45").do(run_script, script="80sm.py")  # 2:45 PM EST
    schedule.every().sunday.at("20:00").do(run_script, script="85fm.py")  # 3:00 PM EST
    schedule.every().sunday.at("20:15").do(run_script, script="85ad.py")  # 3:15 PM EST
    schedule.every().sunday.at("20:30").do(run_script, script="85fm.py")  # 3:30 PM EST
    schedule.every().sunday.at("20:45").do(run_script, script="85fm.py")  # 3:45 PM EST
    schedule.every().sunday.at("21:00").do(run_script, script="85sm.py")  # 4:00 PM EST
    schedule.every().sunday.at("21:30").do(run_script, script="80sm.py")  # 4:30 PM EST
    schedule.every().sunday.at("21:45").do(run_script, script="80sm.py")  # 4:45 PM EST
    schedule.every().sunday.at("22:00").do(run_script, script="80ad.py")  # 5:00 PM EST
    schedule.every().sunday.at("22:30").do(run_script, script="75sm.py")  # 5:30 PM EST
    schedule.every().sunday.at("23:00").do(run_script, script="70ad.py")  # 6:00 PM EST
    schedule.every().sunday.at("23:30").do(run_script, script="65sm.py")  # 6:30 PM EST
    schedule.every().monday.at("00:30").do(run_script, script="75fm.py")  # 7:30 PM EST
    schedule.every().monday.at("01:00").do(run_script, script="70sm.py")  # 8:00 PM EST
    schedule.every().monday.at("01:30").do(run_script, script="65ad.py")  # 8:30 PM EST
    schedule.every().monday.at("02:00").do(run_script, script="80sm.py")  # 9:00 PM EST
    schedule.every().monday.at("02:30").do(run_script, script="85fm.py")  # 9:30 PM EST
    schedule.every().monday.at("03:00").do(run_script, script="85sm.py")  # 10:00 PM EST
    schedule.every().monday.at("03:30").do(run_script, script="85ad.py")  # 10:30 PM EST
    schedule.every().monday.at("04:00").do(run_script, script="70sm.py")  # 11:00 PM EST
    schedule.every().monday.at("04:30").do(run_script, script="70ad.py")  # 11:30 PM EST
    schedule.every().monday.at("05:00").do(run_script, script="70sm.py")  # 12:00 AM EST
    schedule.every().monday.at("05:15").do(run_script, script="70ad.py")  # 12:15 AM EST
    schedule.every().monday.at("05:30").do(run_script, script="65sm.py")  # 12:30 AM EST
    schedule.every().monday.at("05:45").do(run_script, script="65ad.py")  # 12:45 AM EST
    schedule.every().monday.at("06:00").do(run_script, script="65sm.py")  # 1:00 AM EST
    schedule.every().monday.at("06:30").do(run_script, script="65sm.py")  # 1:30 AM EST
    schedule.every().monday.at("07:00").do(run_script, script="pause.py") # 2:00 AM EST
 
    

# Call the scheduling function
schedule_tasks()

# Run the scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)