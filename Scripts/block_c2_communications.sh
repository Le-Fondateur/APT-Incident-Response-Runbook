#!/bin/bash

# Script to block Command and Control (C2) communications
# This script requires superuser privileges to execute

# List of known C2 IP addresses to block
C2_IPS=("192.168.10.10" "203.0.113.15" "198.51.100.25")

# Block C2 IP addresses using iptables
for IP in "${C2_IPS[@]}"
do
  echo "Blocking C2 IP address: $IP"
  sudo iptables -A OUTPUT -d $IP -j DROP
  if [ $? -eq 0 ]; then
    echo "Successfully blocked C2 IP: $IP"
  else
    echo "Failed to block C2 IP: $IP" >&2
  fi
done

# Save iptables rules
sudo iptables-save > /etc/iptables/rules.v4

exit 0
