import logging
import time
from scapy.all import sniff, IP

# Configure logging
logging.basicConfig(filename='persistent_network_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set the threshold for low-level network activity
PACKET_THRESHOLD = 100
MONITOR_DURATION = 3600  # Monitor for 1 hour

# Dictionary to store packet count per IP
packet_counts = {}

# Function to process packets and monitor low-level network activity
def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        packet_counts[src_ip] = packet_counts.get(src_ip, 0) + 1

# Function to monitor persistent network activity
def monitor_network():
    try:
        logging.info("Starting network activity monitoring...")
        sniff(prn=process_packet, timeout=MONITOR_DURATION)

        # Log IPs with persistent low-level activity
        for ip, count in packet_counts.items():
            if count > PACKET_THRESHOLD:
                logging.info(f"Persistent network activity detected: IP={ip}, Packet Count={count}")
                print(f"Persistent network activity detected: IP={ip}, Packet Count={count}")

        logging.info("Network activity monitoring completed.")
    except Exception as e:
        logging.error(f"Error occurred during network monitoring: {str(e)}")
        print(f"Error occurred during network monitoring: {str(e)}")

if __name__ == "__main__":
    monitor_network()
