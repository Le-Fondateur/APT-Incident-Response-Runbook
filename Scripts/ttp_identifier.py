import pandas as pd
import logging
from mitreattack.navlayers import Layer, export_layer_to_file

# Configure logging
logging.basicConfig(filename='ttp_identifier.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to IOCs file
IOCS_FILE = "indicators_of_compromise.csv"
OUTPUT_FILE = "ttp_mapping_layer.json"

# Function to load IOCs data
def load_iocs(file_path):
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Successfully loaded IOCs data from {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"IOCs file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error occurred while loading IOCs data: {str(e)}")
        raise

# Function to map IOCs to MITRE ATT&CK TTPs
def map_iocs_to_ttps(iocs_data):
    try:
        layer = Layer(name="APT Threat TTPs", domain="enterprise-attack")
        # Placeholder logic for mapping IOCs to TTPs
        for _, row in iocs_data.iterrows():
            if row['type'] == 'IP Address':
                # Example mapping (not real mapping logic)
                layer.add_technique(tid="T1071", score=1)  # T1071: Application Layer Protocol
            elif row['type'] == 'Hash':
                layer.add_technique(tid="T1105", score=1)  # T1105: Ingress Tool Transfer
        return layer
    except Exception as e:
        logging.error(f"Error occurred while mapping IOCs to TTPs: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load IOCs data
        iocs_data = load_iocs(IOCS_FILE)

        # Map IOCs to MITRE ATT&CK TTPs
        ttp_layer = map_iocs_to_ttps(iocs_data)

        # Export TTP mapping to a JSON file
        export_layer_to_file(ttp_layer, OUTPUT_FILE)
        logging.info(f"TTP mapping exported to {OUTPUT_FILE}")
        print(f"TTP mapping exported to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {str(e)}")
