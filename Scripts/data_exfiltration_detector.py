import pandas as pd
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(filename='data_exfiltration_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to network activity data
NETWORK_ACTIVITY_FILE = "network_activity.csv"

# Function to load network activity data
def load_network_activity(file_path):
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Successfully loaded network activity data from {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"Network activity file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading network activity data: {str(e)}")
        raise

# Function to detect data exfiltration patterns
def detect_data_exfiltration(data):
    try:
        # Filter outbound traffic and identify potential exfiltration patterns
        outbound_traffic = data[data['direction'] == 'outbound']
        large_transfers = outbound_traffic[outbound_traffic['data_transfer_size'] > 1000000]  # Example threshold: 1MB

        # Identify slow and gradual exfiltration over time
        grouped = large_transfers.groupby('ip_address').agg({
            'timestamp': ['min', 'max'],
            'data_transfer_size': 'sum'
        })
        grouped.columns = ['first_seen', 'last_seen', 'total_transfer']
        grouped['duration'] = pd.to_datetime(grouped['last_seen']) - pd.to_datetime(grouped['first_seen'])

        # Log IPs with suspicious exfiltration patterns
        exfiltration_suspects = grouped[(grouped['total_transfer'] > 5000000) & (grouped['duration'] > timedelta(hours=1))]

        for ip, details in exfiltration_suspects.iterrows():
            logging.warning(f"Data exfiltration detected: IP={ip}, Total Transfer={details['total_transfer']}, Duration={details['duration']}")
            print(f"Data exfiltration detected: IP={ip}, Total Transfer={details['total_transfer']}, Duration={details['duration']}")

        return exfiltration_suspects
    except Exception as e:
        logging.error(f"Error occurred while detecting data exfiltration: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load network activity data
        network_activity_data = load_network_activity(NETWORK_ACTIVITY_FILE)

        # Detect data exfiltration patterns
        exfiltration_detected = detect_data_exfiltration(network_activity_data)

        # Summary of data exfiltration detected
        logging.info(f"Total data exfiltration incidents detected: {len(exfiltration_detected)}")
        print(f"Total data exfiltration incidents detected: {len(exfiltration_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
