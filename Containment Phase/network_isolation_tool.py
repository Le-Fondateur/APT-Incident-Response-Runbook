import logging
import os
import subprocess

logging.basicConfig(filename='network_isolation_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Isolate affected systems by disabling network adapters
def isolate_system(ip_address):
    try:
        # Disable network adapter for a given IP address
        command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
        subprocess.run(command, shell=True, check=True)
        logging.info(f"Successfully isolated system with IP: {ip_address}")
        print(f"Successfully isolated system with IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to isolate system with IP: {ip_address}. Error: {str(e)}")
        print(f"Failed to isolate system with IP: {ip_address}. Error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error occurred while isolating system with IP: {ip_address}. Error: {str(e)}")
        print(f"Unexpected error: {str(e)}")

# Read compromised IPs from a file and isolate them
def isolate_compromised_systems(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as file:
            compromised_ips = file.readlines()

        for ip in compromised_ips:
            ip = ip.strip()
            if ip:
                isolate_system(ip)

        logging.info("All compromised systems have been isolated.")
        print("All compromised systems have been isolated.")
    except FileNotFoundError as e:
        logging.error(str(e))
        print(str(e))
    except Exception as e:
        logging.error(f"Error occurred while isolating compromised systems: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        # Path to the file containing compromised IP addresses
        COMPROMISED_IPS_FILE = "compromised_ips.txt"

        isolate_compromised_systems(COMPROMISED_IPS_FILE)
    except Exception as e:
        print(f"Error: {str(e)}")
