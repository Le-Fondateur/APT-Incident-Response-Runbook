import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(filename='log_correlation_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

def load_logs():
    try:
        engine = create_engine(DATABASE_URI)

        # Load network logs
        network_query = """
        SELECT timestamp, ip_address, data_transfer_size, direction
        FROM network_activity_log
        """
        network_logs = pd.read_sql(network_query, engine)

        # Load system logs
        system_query = """
        SELECT timestamp, user_host, action, resource
        FROM system_activity_log
        """
        system_logs = pd.read_sql(system_query, engine)

        logging.info("Successfully loaded network and system logs from the database")
        return network_logs, system_logs
    except Exception as e:
        logging.error(f"Error occurred while loading logs: {str(e)}")
        raise

# Correlate network and system logs
def correlate_logs(network_logs, system_logs):
    try:
        network_logs['timestamp'] = pd.to_datetime(network_logs['timestamp'])
        system_logs['timestamp'] = pd.to_datetime(system_logs['timestamp'])

        # Merge logs based on timestamp proximity (within 1 minute)
        merged_logs = pd.merge_asof(
            network_logs.sort_values('timestamp'),
            system_logs.sort_values('timestamp'),
            on='timestamp',
            direction='nearest',
            tolerance=pd.Timedelta(minutes=1)
        )

        # Filter suspicious correlated activities
        suspicious_logs = merged_logs[(merged_logs['direction'] == 'outbound') & (merged_logs['action'].str.contains('login', case=False, na=False))]

        # Log suspicious correlated activities
        if not suspicious_logs.empty:
            logging.warning("Suspicious correlated activities detected:")
            for _, row in suspicious_logs.iterrows():
                logging.warning(f"Timestamp: {row['timestamp']}, IP: {row['ip_address']}, Action: {row['action']}, User: {row['user_host']}")
                print(f"Suspicious activity detected: Timestamp: {row['timestamp']}, IP: {row['ip_address']}, Action: {row['action']}, User: {row['user_host']}")
        else:
            logging.info("No suspicious correlated activities detected.")
            print("No suspicious correlated activities detected.")

        return suspicious_logs
    except Exception as e:
        logging.error(f"Error occurred while correlating logs: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        network_logs, system_logs = load_logs()

        correlated_logs = correlate_logs(network_logs, system_logs)

        logging.info(f"Total suspicious correlated activities detected: {len(correlated_logs)}")
        print(f"Total suspicious correlated activities detected: {len(correlated_logs)}")
    except Exception as e:
        print(f"Error: {str(e)}")
