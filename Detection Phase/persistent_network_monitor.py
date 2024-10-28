import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='database_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to audit the database and restore integrity
def audit_database():
    try:
        engine = create_engine(DATABASE_URI)

        # Queries to identify suspicious changes in the database
        audit_query = """
        SELECT table_name, operation, timestamp, user_host, sql_text
        FROM mysql.audit_log
        WHERE operation IN ('DELETE', 'UPDATE', 'DROP')
        AND (
            sql_text LIKE '%DROP TABLE%'
            OR sql_text LIKE '%DELETE FROM%'
            OR sql_text LIKE '%UPDATE % SET%'
            OR user_host LIKE '%unauthorized_user%'
            OR timestamp > NOW() - INTERVAL 1 DAY
        )
        """

        # Load data from database
        audit_data = pd.read_sql(audit_query, engine)

        # Log suspicious activities
        if not audit_data.empty:
            logging.warning("Suspicious database operations detected:")
            for _, row in audit_data.iterrows():
                logging.warning(f"Table: {row['table_name']}, Operation: {row['operation']}, Time: {row['timestamp']}, User: {row['user_host']}, SQL: {row['sql_text']}")
                print(f"Suspicious operation detected: Table: {row['table_name']}, Operation: {row['operation']}, Time: {row['timestamp']}, User: {row['user_host']}, SQL: {row['sql_text']}")
        else:
            logging.info("No suspicious database operations detected.")
            print("No suspicious database operations detected.")
    except Exception as e:
        logging.error(f"Error occurred during database audit: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    audit_database()
