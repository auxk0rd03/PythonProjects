#WORKS GOOD
import socket
import threading
from queue import Queue

# Target IP address
target_ip = "192.168.1.188"  # Replace with your target IP (lab environment only!)

# Common ports to scan (you can customize this list)
common_ports = [
    21, 22, 23, 25, 53, 80, 110, 119, 123, 143,
    161, 194, 443, 445, 993, 995, 3306, 3389, 5900, 8080
]

# Queue for storing ports to scan
queue = Queue()

# Function to scan a single port
def scan_port(port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second

        # Attempt to connect to the port
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            print(f"Port {port} is open")
            try:
                # Attempt to grab the banner
                banner = sock.recv(1024).decode().strip()
                print(f"Banner for port {port}: {banner}")
            except:
                print(f"No banner received for port {port}")
        else:
            print(f"Port {port} is closed")

        # Close the socket
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Function to process the queue
def process_queue():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

# Main function
def main():
    print(f"Starting port scan on {target_ip}...")

    # Add ports to the queue
    for port in common_ports:
        queue.put(port)

    # Create and start threads
    threads = []
    for _ in range(10):  # Number of threads (adjust as needed)
        thread = threading.Thread(target=process_queue)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Port scan completed.")

if __name__ == "__main__":
    main()