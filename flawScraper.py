import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import re

# List of security headers to check
security_headers = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-XSS-Protection",
]

# Function to check for missing security headers
def check_security_headers(response, result_text):
    result_text.insert(tk.END, "\nChecking for missing security headers...\n")
    missing_headers = []
    for header in security_headers:
        if header not in response.headers:
            missing_headers.append(header)
            result_text.insert(tk.END, f"Missing header: {header}\n")
    if not missing_headers:
        result_text.insert(tk.END, "All security headers are present.\n")

# Function to check for outdated software
def check_outdated_software(response, result_text):
    result_text.insert(tk.END, "\nChecking for outdated software...\n")
    soup = BeautifulSoup(response.text, "html.parser")

    # Check for outdated jQuery
    jquery_scripts = soup.find_all("script", src=re.compile(r"jquery\.js"))
    for script in jquery_scripts:
        if "1.12.4" in script["src"]:  # Example: Check for an outdated version
            result_text.insert(tk.END, f"Outdated jQuery version detected: {script['src']}\n")

    # Check for outdated WordPress
    generator_tag = soup.find("meta", attrs={"name": "generator"})
    if generator_tag and "WordPress" in generator_tag["content"]:
        result_text.insert(tk.END, f"WordPress version detected: {generator_tag['content']}\n")
        # Add logic to check for outdated WordPress versions

# Function to check for sensitive information in HTML
def check_sensitive_information(response, result_text):
    result_text.insert(tk.END, "\nChecking for sensitive information in HTML...\n")
    soup = BeautifulSoup(response.text, "html.parser")

    # Check for comments containing sensitive information
    comments = soup.find_all(string=lambda text: isinstance(text, str) and "password" in text.lower())
    for comment in comments:
        result_text.insert(tk.END, f"Sensitive information found in comment: {comment.strip()}\n")

    # Check for internal paths or credentials in HTML
    internal_paths = re.findall(r"/var/www|/home/user|/etc", response.text)
    if internal_paths:
        result_text.insert(tk.END, f"Internal paths found in HTML: {internal_paths}\n")

# Function to check for insecure forms
def check_insecure_forms(response, result_text):
    result_text.insert(tk.END, "\nChecking for insecure forms...\n")
    soup = BeautifulSoup(response.text, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        action = form.get("action", "")
        if action.startswith("http://"):
            result_text.insert(tk.END, f"Insecure form action detected: {action}\n")

# Function to start the scan
def start_scan():
    # Clear previous results
    result_text.delete(1.0, tk.END)

    # Get target URL from the input field
    target_url = url_entry.get().strip()

    # Ensure the URL includes a scheme
    if not target_url.startswith(("http://", "https://")):
        target_url = f"https://{target_url}"
        result_text.insert(tk.END, f"Assuming HTTPS and using URL: {target_url}\n")

    result_text.insert(tk.END, f"\nScanning {target_url} for vulnerabilities...\n")

    try:
        # Send a GET request to the target URL
        response = requests.get(target_url)

        # Check for missing security headers
        check_security_headers(response, result_text)

        # Check for outdated software
        check_outdated_software(response, result_text)

        # Check for sensitive information in HTML
        check_sensitive_information(response, result_text)

        # Check for insecure forms
        check_insecure_forms(response, result_text)

    except requests.exceptions.RequestException as e:
        result_text.insert(tk.END, f"\nError scanning {target_url}: {e}\n")

# Create the main window
root = tk.Tk()
root.title("Web Vulnerability Scanner")
root.geometry("600x400")

# URL input field
url_label = tk.Label(root, text="Enter the target URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Scan button
scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

# Result display area
result_text = scrolledtext.ScrolledText(root, width=70, height=20)
result_text.pack(pady=10)

# Run the GUI
root.mainloop()