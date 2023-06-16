import subprocess
import time

def run_script():
    while True:
        # Start the script as a subprocess
        script_process = subprocess.Popen(['python3', 'listner.py'])
        
        # Wait for the script to finish
        script_process.wait()
        
        # If the script exited normally (return code 0), break the loop
        if script_process.returncode == 0:
            break
        
        print("Script stopped. Restarting...")
        time.sleep(5)  # Wait for 5 seconds before restarting

run_script()
