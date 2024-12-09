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
    schedule.every().monday.at("11:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("11:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("11:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("11:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("12:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("12:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("12:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("12:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("13:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("13:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("13:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("13:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("14:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("14:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("14:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("14:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("15:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("15:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("15:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("15:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("16:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("16:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("16:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("16:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("17:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("17:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("17:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("17:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("18:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("18:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("18:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("18:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("19:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("19:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("19:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("19:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("20:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("20:15").do(run_script, script="75sm.py")
    schedule.every().monday.at("20:30").do(run_script, script="75fm.py")
    schedule.every().monday.at("20:45").do(run_script, script="75fm.py")
    schedule.every().monday.at("21:00").do(run_script, script="75sm.py")
    schedule.every().monday.at("21:30").do(run_script, script="75sm.py")
    schedule.every().monday.at("21:45").do(run_script, script="75sm.py")
    schedule.every().monday.at("22:00").do(run_script, script="75sm.py")
    schedule.every().monday.at("22:30").do(run_script, script="75sm.py")
    schedule.every().monday.at("23:00").do(run_script, script="75fm.py")
    schedule.every().monday.at("23:30").do(run_script, script="75sm.py")
    schedule.every().monday.at("23:59").do(run_script, script="pause.py")
    
    # Tuesday
    schedule.every().tuesday.at("11:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("11:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("11:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("11:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("12:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("12:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("12:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("12:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("13:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("13:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("13:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("13:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("14:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("14:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("14:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("14:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("15:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("15:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("15:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("15:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("16:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("16:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("16:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("16:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("17:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("17:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("17:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("17:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("18:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("18:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("18:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("18:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("19:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("19:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("19:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("19:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("20:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("20:15").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("20:30").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("20:45").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("21:00").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("21:30").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("21:45").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("22:00").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("22:30").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("23:00").do(run_script, script="75fm.py")
    schedule.every().tuesday.at("23:30").do(run_script, script="75sm.py")
    schedule.every().tuesday.at("23:59").do(run_script, script="pause.py")
    
    
    # Wednesday
    schedule.every().wednesday.at("11:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("11:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("11:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("11:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("12:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("12:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("12:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("12:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("13:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("13:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("13:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("13:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("14:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("14:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("14:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("14:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("15:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("15:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("15:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("15:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("16:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("16:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("16:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("16:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("17:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("17:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("17:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("17:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("18:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("18:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("18:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("18:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("19:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("19:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("19:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("19:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("20:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("20:15").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("20:30").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("20:45").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("21:00").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("21:30").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("21:45").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("22:00").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("22:30").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("23:00").do(run_script, script="75fm.py")
    schedule.every().wednesday.at("23:30").do(run_script, script="75sm.py")
    schedule.every().wednesday.at("23:59").do(run_script, script="pause.py")
    
    
    # Thursday
    schedule.every().thursday.at("14:00").do(run_script, script="thursday_script.py")
    
    # Friday
    schedule.every().friday.at("15:00").do(run_script, script="friday_script.py")
    
    # Saturday
    schedule.every().saturday.at("16:00").do(run_script, script="saturday_script.py")
    
    # Sunday
    schedule.every().sunday.at("17:00").do(run_script, script="sunday_script.py")

# Call the scheduling function
schedule_tasks()

# Run the scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)