import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(filename='ioc_investigator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Load Indicators of Compromise (IoCs)
def load_iocs():
    try:
        engine = create_engine(DATABASE_URI)

        # Load IoCs from the database
        query = """
        SELECT ioc_type, ioc_value, first_seen, last_seen
        FROM iocs
        """
        iocs = pd.read_sql(query, engine)

        logging.info("Successfully loaded IoCs from the database")
        return iocs
    except Exception as e:
        logging.error(f"Error occurred while loading IoCs: {str(e)}")
        raise

# Investigate IoCs and map attack path
def investigate_iocs(iocs):
    try:
        # Identify IoCs with suspicious patterns
        suspicious_iocs = iocs[(iocs['ioc_type'].str.contains('ip', case=False)) |
                               (iocs['ioc_type'].str.contains('domain', case=False)) |
                               (iocs['ioc_type'].str.contains('hash', case=False))]

        # Log suspicious IoCs
        if not suspicious_iocs.empty:
            logging.warning("Suspicious IoCs detected:")
            for _, row in suspicious_iocs.iterrows():
                logging.warning(f"IoC Type: {row['ioc_type']}, Value: {row['ioc_value']}, First Seen: {row['first_seen']}, Last Seen: {row['last_seen']}")
                print(f"Suspicious IoC detected: Type: {row['ioc_type']}, Value: {row['ioc_value']}, First Seen: {row['first_seen']}, Last Seen: {row['last_seen']}")
        else:
            logging.info("No suspicious IoCs detected.")
            print("No suspicious IoCs detected.")

        return suspicious_iocs
    except Exception as e:
        logging.error(f"Error occurred while investigating IoCs: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        iocs_data = load_iocs()

        suspicious_iocs_detected = investigate_iocs(iocs_data)

        logging.info(f"Total suspicious IoCs detected: {len(suspicious_iocs_detected)}")
        print(f"Total suspicious IoCs detected: {len(suspicious_iocs_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
