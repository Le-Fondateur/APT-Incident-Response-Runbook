import pandas as pd
import logging
from sklearn.ensemble import IsolationForest

# Configure logging
logging.basicConfig(filename='anomalous_behavior_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to user activity data
USER_ACTIVITY_FILE = "user_activity.csv"

# Function to load user activity data
def load_user_activity(file_path):
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Successfully loaded user activity data from {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"User activity file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading user activity data: {str(e)}")
        raise

# Function to detect anomalous user behavior
def detect_anomalous_behavior(data):
    try:
        # Select features for anomaly detection
        features = ['login_count', 'data_transfer_size', 'session_duration', 'access_location']
        df_features = data[features]

        # Handling missing values
        df_features.fillna(df_features.mean(), inplace=True)

        # Fit Isolation Forest model
        model = IsolationForest(contamination=0.05, random_state=42)
        data['anomaly'] = model.fit_predict(df_features)

        # Log anomalous user activities
        anomalies = data[data['anomaly'] == -1]
        for _, row in anomalies.iterrows():
            logging.warning(f"Anomalous user activity detected: UserID={row['user_id']}, Details={row.to_dict()}")
            print(f"Anomalous user activity detected: UserID={row['user_id']}, Details={row.to_dict()}")

        return anomalies
    except Exception as e:
        logging.error(f"Error occurred while detecting anomalous behavior: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load user activity data
        user_activity_data = load_user_activity(USER_ACTIVITY_FILE)

        # Detect anomalous user behavior
        anomalies_detected = detect_anomalous_behavior(user_activity_data)

        # Summary of anomalies detected
        logging.info(f"Total anomalies detected: {len(anomalies_detected)}")
        print(f"Total anomalies detected: {len(anomalies_detected)}")
    except Exception as e:
        print(f"Error: {str(e)}")
