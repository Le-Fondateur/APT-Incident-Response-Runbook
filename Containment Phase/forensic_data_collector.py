import logging
import os
import shutil
import datetime
import subprocess

logging.basicConfig(filename='forensic_data_collector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

FORENSIC_DATA_DIR = "forensic_data"

# Create forensic data directory with timestamp
def create_forensic_directory():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    forensic_dir = f"{FORENSIC_DATA_DIR}_{timestamp}"
    os.makedirs(forensic_dir, exist_ok=True)
    return forensic_dir

# Function to collect network logs
def collect_network_logs(output_dir):
    try:
        logging.info("Collecting network logs...")
        # Example command to collect network logs using tcpdump (Linux)
        command = f"sudo tcpdump -w {output_dir}/network_logs.pcap -c 1000"
        subprocess.run(command, shell=True, check=True)
        logging.info("Network logs collected successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to collect network logs. Error: {str(e)}")
        print(f"Failed to collect network logs. Error: {str(e)}")

# Function to collect system logs
def collect_system_logs(output_dir):
    try:
        logging.info("Collecting system logs...")
        syslog_path = "/var/log/syslog"
        if os.path.exists(syslog_path):
            shutil.copy(syslog_path, os.path.join(output_dir, "syslog.log"))
            logging.info("System logs collected successfully.")
            print("System logs collected successfully.")
        else:
            logging.warning("System logs not found.")
            print("System logs not found.")
    except Exception as e:
        logging.error(f"Error occurred while collecting system logs: {str(e)}")
        print(f"Error: {str(e)}")

# Function to collect memory dump
def collect_memory_dump(output_dir):
    try:
        logging.info("Collecting memory dump...")
        # Example command to collect memory dump using Linux tool (e.g., dd)
        command = f"sudo dd if=/dev/mem of={output_dir}/memory_dump.bin bs=1M count=100"
        subprocess.run(command, shell=True, check=True)
        logging.info("Memory dump collected successfully.")
        print("Memory dump collected successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to collect memory dump. Error: {str(e)}")
        print(f"Failed to collect memory dump. Error: {str(e)}")

if __name__ == "__main__":
    try:
        forensic_directory = create_forensic_directory()

        collect_network_logs(forensic_directory)
        collect_system_logs(forensic_directory)
        collect_memory_dump(forensic_directory)

        logging.info("Forensic data collection completed.")
        print("Forensic data collection completed.")
    except Exception as e:
        logging.error(f"Unexpected error during forensic data collection: {str(e)}")
        print(f"Error: {str(e)}")
