import pandas as pd
import logging
import re

# Configure logging
logging.basicConfig(filename='ioc_collector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to log files
LOG_DIRECTORY = "logs/"
OUTPUT_FILE = "indicators_of_compromise.csv"

# Function to extract Indicators of Compromise (IOCs)
def extract_iocs(log_data):
    try:
        iocs = []
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        hash_pattern = re.compile(r'\b[A-Fa-f0-9]{32}\b|\b[A-Fa-f0-9]{64}\b')

        for index, row in log_data.iterrows():
            message = row['message']
            ip_matches = ip_pattern.findall(message)
            hash_matches = hash_pattern.findall(message)

            for ip in ip_matches:
                iocs.append({'type': 'IP Address', 'value': ip, 'timestamp': row['timestamp']})
                logging.info(f"Extracted IP Address IOC: {ip}")

            for file_hash in hash_matches:
                iocs.append({'type': 'Hash', 'value': file_hash, 'timestamp': row['timestamp']})
                logging.info(f"Extracted Hash IOC: {file_hash}")

        return pd.DataFrame(iocs)
    except Exception as e:
        logging.error(f"Error occurred while extracting IOCs: {str(e)}")
        raise

# Function to load log data from CSV files
def load_log_data(file_path):
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Successfully loaded log data from {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"Log file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading log data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load log data
        log_data = load_log_data(f"{LOG_DIRECTORY}/network_activity.log")

        # Extract IOCs from log data
        iocs_detected = extract_iocs(log_data)

        # Save IOCs to output file
        iocs_detected.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Indicators of Compromise saved to {OUTPUT_FILE}")
        print(f"Total IOCs extracted: {len(iocs_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
