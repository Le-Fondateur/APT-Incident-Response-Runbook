import pandas as pd
import logging
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='anomalous_behavior_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Load user activity data from the database
def load_user_activity():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)
        query = """
        SELECT user_id, login_count, data_transfer_size, session_duration, access_location
        FROM user_activity_log
        """
        data = pd.read_sql(query, engine)
        logging.info("Successfully loaded user activity data from the database")
        return data
    except Exception as e:
        logging.error(f"Error occurred while loading user activity data: {str(e)}")
        raise

# Detect anomalous user behavior using Isolation Forest
def detect_anomalous_behavior(data):
    try:
        # Select features for anomaly detection
        features = ['login_count', 'data_transfer_size', 'session_duration', 'access_location']
        df_features = data[features]

        # Handle missing values
        df_features.fillna(df_features.mean(), inplace=True)

        # Fit Isolation Forest model
        model = IsolationForest(contamination=0.05, random_state=42)
        data['anomaly'] = model.fit_predict(df_features)

        # Log anomalous user activities
        anomalies = data[data['anomaly'] == -1]
        if not anomalies.empty:
            logging.warning("Anomalous user activities detected:")
            for _, row in anomalies.iterrows():
                logging.warning(f"UserID: {row['user_id']}, Anomalous Data: {row.to_dict()}")
                print(f"Anomalous user activity detected: UserID: {row['user_id']}, Anomalous Data: {row.to_dict()}")
        else:
            logging.info("No anomalous user activities detected.")
            print("No anomalous user activities detected.")
        return anomalies
    except Exception as e:
        logging.error(f"Error occurred while detecting anomalous behavior: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load user activity data
        user_activity_data = load_user_activity()

        # Detect anomalous user behavior
        anomalies_detected = detect_anomalous_behavior(user_activity_data)

        # Summary of anomalies detected
        logging.info(f"Total anomalies detected: {len(anomalies_detected)}")
        print(f"Total anomalies detected: {len(anomalies_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
