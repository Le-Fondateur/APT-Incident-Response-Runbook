import pandas as pd
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='data_exfiltration_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Load network activity data
def load_network_activity():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)
        query = """
        SELECT timestamp, ip_address, direction, data_transfer_size
        FROM network_activity_log
        WHERE direction = 'outbound'
        """
        data = pd.read_sql(query, engine)
        logging.info("Successfully loaded network activity data from the database")
        return data
    except Exception as e:
        logging.error(f"Error occurred while loading network activity data: {str(e)}")
        raise

# Detect data exfiltration patterns
def detect_data_exfiltration(data):
    try:
        # Identify large outbound data transfers
        large_transfers = data[data['data_transfer_size'] > 1000000] 

        # Identify gradual exfiltration over time
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
        network_activity_data = load_network_activity()

        exfiltration_detected = detect_data_exfiltration(network_activity_data)

        logging.info(f"Total data exfiltration incidents detected: {len(exfiltration_detected)}")
        print(f"Total data exfiltration incidents detected: {len(exfiltration_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
