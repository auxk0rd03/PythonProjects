import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import subprocess
import socket
import os
import requests
import json
import exifread
import whois
import re
import logging
import threading

# Initialize main window
root = tk.Tk()
root.title("Pen Testing Toolbox")
root.geometry("600x600")
root.configure(bg="black")

# Configure logging
logging.basicConfig(filename="pentest_toolbox.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to validate IP address
def is_valid_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None

# Function to validate URL
def is_valid_url(url):
    return re.match(r"https?://(?:www\.)?\S+", url) is not None

# Function to perform network scan
def network_scan():
    result_text.delete(1.0, tk.END)
    target = target_entry.get()
    if not target:
        result_text.insert(tk.END, "Please enter a target IP or range.\n")
        return
    
    if not is_valid_ip(target):
        result_text.insert(tk.END, "Invalid IP address.\n")
        return
    
    logging.info(f"Starting network scan on {target}")
    try:
        result = subprocess.check_output(["nmap", "-sV", target]).decode()
        result_text.insert(tk.END, result)
        logging.info(f"Network scan completed on {target}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error during network scan: {str(e)}")

# Function to perform basic DoS attack simulation
def ddos_attack():
    result_text.delete(1.0, tk.END)
    target = target_entry.get()
    if not target:
        result_text.insert(tk.END, "Please enter a target IP.\n")
        return
    
    if not is_valid_ip(target):
        result_text.insert(tk.END, "Invalid IP address.\n")
        return
    
    result_text.insert(tk.END, f"Simulating DoS attack on {target}...\n")
    logging.info(f"Starting DoS attack simulation on {target}")
    try:
        for i in range(10):  # Simulated requests
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((target, 80))
            s.send(b"GET / HTTP/1.1\r\n\r\n")
            s.close()
        result_text.insert(tk.END, "Attack simulation complete.\n")
        logging.info(f"DoS attack simulation completed on {target}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error during DoS attack simulation: {str(e)}")

# Function to check website vulnerability using requests
def check_vulnerability():
    result_text.delete(1.0, tk.END)
    target = target_entry.get()
    if not target:
        result_text.insert(tk.END, "Please enter a target URL.\n")
        return
    
    if not is_valid_url(target):
        result_text.insert(tk.END, "Invalid URL.\n")
        return
    
    logging.info(f"Checking vulnerabilities on {target}")
    try:
        response = requests.get(target)
        potential_vulnerabilities = []
        
        if "SQL" in response.text:
            potential_vulnerabilities.append("Possible SQL injection vulnerability detected.")
            potential_vulnerabilities.append("Extracted response: \n" + response.text[:500] + "...\n")  # Show first 500 chars
        
        if potential_vulnerabilities:
            result_text.insert(tk.END, "\n".join(potential_vulnerabilities))
        else:
            result_text.insert(tk.END, "No obvious vulnerabilities detected.\n")
        logging.info(f"Vulnerability check completed on {target}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error during vulnerability check: {str(e)}")

# Function to scrape IP address information
def ip_info():
    result_text.delete(1.0, tk.END)
    target = target_entry.get()
    if not target:
        result_text.insert(tk.END, "Please enter a target IP.\n")
        return
    
    if not is_valid_ip(target):
        result_text.insert(tk.END, "Invalid IP address.\n")
        return
    
    logging.info(f"Fetching IP info for {target}")
    try:
        response = requests.get(f"http://ip-api.com/json/{target}")
        data = response.json()
        result_text.insert(tk.END, json.dumps(data, indent=4))
        logging.info(f"IP info fetched for {target}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error fetching IP info: {str(e)}")

# Function to extract metadata from an image
def extract_metadata():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return
    
    result_text.delete(1.0, tk.END)
    logging.info(f"Extracting metadata from {file_path}")
    try:
        with open(file_path, "rb") as image_file:
            tags = exifread.process_file(image_file)
            for tag, value in tags.items():
                result_text.insert(tk.END, f"{tag}: {value}\n")
        logging.info(f"Metadata extracted from {file_path}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error extracting metadata: {str(e)}")

# Function to perform WHOIS lookup
def whois_lookup():
    result_text.delete(1.0, tk.END)
    target = target_entry.get()
    if not target:
        result_text.insert(tk.END, "Please enter a domain name.\n")
        return
    
    logging.info(f"Performing WHOIS lookup for {target}")
    try:
        domain_info = whois.whois(target)
        result_text.insert(tk.END, str(domain_info))
        logging.info(f"WHOIS lookup completed for {target}")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}\n")
        logging.error(f"Error during WHOIS lookup: {str(e)}")

# Function to clear results
def clear_results():
    result_text.delete(1.0, tk.END)

# Function to show help
def show_help():
    help_text = """
    Network Scan: Scans a target IP or range using Nmap.
    DoS Attack Sim: Simulates a DoS attack on a target IP.
    Check Vulnerability: Checks a URL for common vulnerabilities.
    IP Info Scraper: Retrieves information about an IP address.
    Extract Image Metadata: Extracts metadata from an image file.
    WHOIS Lookup: Performs a WHOIS lookup on a domain.
    """
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, help_text)

# Function to toggle theme
def toggle_theme():
    if root.cget("bg") == "black":
        root.configure(bg="white")
        result_text.configure(bg="white", fg="black")
    else:
        root.configure(bg="black")
        result_text.configure(bg="black", fg="orange")

# GUI Components
target_label = tk.Label(root, text="Target IP/URL:", fg="orange", bg="black")
target_label.pack()

target_entry = tk.Entry(root, width=50)
target_entry.pack()

# Add a progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack()

# Buttons
scan_button = tk.Button(root, text="Network Scan", command=lambda: threading.Thread(target=network_scan).start(), bg="orange", fg="black")
scan_button.pack()

ddos_button = tk.Button(root, text="DoS Attack Sim", command=lambda: threading.Thread(target=ddos_attack).start(), bg="orange", fg="black")
ddos_button.pack()

vuln_button = tk.Button(root, text="Check Vulnerability", command=lambda: threading.Thread(target=check_vulnerability).start(), bg="orange", fg="black")
vuln_button.pack()

ipinfo_button = tk.Button(root, text="IP Info Scraper", command=lambda: threading.Thread(target=ip_info).start(), bg="orange", fg="black")
ipinfo_button.pack()

metadata_button = tk.Button(root, text="Extract Image Metadata", command=extract_metadata, bg="orange", fg="black")
metadata_button.pack()

whois_button = tk.Button(root, text="WHOIS Lookup", command=lambda: threading.Thread(target=whois_lookup).start(), bg="orange", fg="black")
whois_button.pack()

clear_button = tk.Button(root, text="Clear Results", command=clear_results, bg="orange", fg="black")
clear_button.pack()

help_button = tk.Button(root, text="Help", command=show_help, bg="orange", fg="black")
help_button.pack()

theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg="orange", fg="black")
theme_button.pack()

# Result display
result_text = scrolledtext.ScrolledText(root, width=70, height=20, bg="black", fg="orange")
result_text.pack()

# Run the application
root.mainloop()