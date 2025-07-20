import socket
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
import struct

# Configuration
target_ip = "192.168.196.1"  # Change to your own test device's IP
target_port = 443
packet_count = 1000
batch_size = 50
delay_between_batches = 0.1
max_threads = 4
payload_size = 1024  # 1 KB payload

def create_udp_socket():
    """Create a UDP socket"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock
    except Exception as e:
        print(f"Error creating socket: {e}")
        return None

def send_udp_batch(target_ip, target_port, count, payload):
    """Send a batch of UDP packets"""
    sock = create_udp_socket()
    if not sock:
        return 0
        
    packets_sent = 0
    try:
        for i in range(count):
            sock.sendto(payload, (target_ip, target_port))
            packets_sent += 1
    except Exception as e:
        print(f"Error sending packet: {e}")
    finally:
        sock.close()
    
    return packets_sent

def main():
    print(f"Safe Packet Sender - Target: {target_ip}:{target_port}")
    print(f"Payload size: {payload_size} bytes")
    print("Using regular UDP sockets (no root required)")
    print("Press Ctrl+C to stop\n")
    
    # Create payload
    payload = b"X" * payload_size
    
    total_sent = 0
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            while True:
                print(f"Sending {packet_count} packets to {target_ip}:{target_port}...")
                
                # Submit batch jobs to thread pool
                futures = []
                for i in range(0, packet_count, batch_size):
                    batch_count = min(batch_size, packet_count - i)
                    future = executor.submit(send_udp_batch, target_ip, target_port, batch_count, payload)
                    futures.append(future)
                
                # Collect results
                batch_total = 0
                for future in futures:
                    batch_total += future.result()
                
                total_sent += batch_total
                elapsed = time.time() - start_time
                
                print(f"Batch complete: {batch_total} packets sent")
                print(f"Total sent: {total_sent} packets in {elapsed:.1f}s")
                if elapsed > 0:
                    print(f"Rate: {total_sent/elapsed:.1f} packets/second\n")
                
                time.sleep(delay_between_batches)
                
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\nStopped by user.")
        print(f"Final stats: {total_sent} packets sent in {elapsed:.1f}s")
        if elapsed > 0:
            print(f"Average rate: {total_sent/elapsed:.1f} packets/second")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Packet sender stopped.")

if __name__ == "__main__":
    main()