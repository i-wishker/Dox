# Packet Sender

A simple script to send UDP packets using Scapy.

## Installation

```sh
pip install scapy
```

## Usage

Edit `pax.py` to set your target IP and port:

```python
target_ip = "192.168.1.1"  # Your router or test device IP
target_port = 443          # Target port
```

Run the script:

```sh
python pax.py
```

## Warning

Sending large amounts of packets may disrupt your network or target device. Use responsibly and at your own risk.