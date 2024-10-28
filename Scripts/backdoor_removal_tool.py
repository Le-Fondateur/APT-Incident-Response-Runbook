import os
import logging
import subprocess

# Configure logging
logging.basicConfig(filename='backdoor_removal_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of known backdoor files and processes
KNOWN_BACKDOORS = [
    "/tmp/suspicious_backdoor.sh",
    "/var/tmp/evil_script.py"
]

# Function to remove backdoor files
def remove_backdoor_files(backdoor_files):
    try:
        for file in backdoor_files:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Backdoor file removed: {file}")
                print(f"Backdoor file removed: {file}")
            else:
                logging.info(f"Backdoor file not found: {file}")
    except Exception as e:
        logging.error(f"Error occurred while removing backdoor files: {str(e)}")
        raise

# Function to stop and remove suspicious processes
def stop_suspicious_processes(process_name):
    try:
        result = subprocess.run(["pgrep", "-f", process_name], capture_output=True, text=True)
        pids = result.stdout.splitlines()
        for pid in pids:
            subprocess.run(["kill", "-9", pid])
            logging.info(f"Suspicious process stopped: PID={pid}")
            print(f"Suspicious process stopped: PID={pid}")
    except Exception as e:
        logging.error(f"Error occurred while stopping suspicious processes: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Remove backdoor files
        remove_backdoor_files(KNOWN_BACKDOORS)

        # Stop suspicious processes (Example: process names matching backdoors)
        for backdoor in KNOWN_BACKDOORS:
            stop_suspicious_processes(backdoor)
    except Exception as e:
        print(f"Error: {str(e)}")
