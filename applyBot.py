from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Path to your ChromeDriver
CHROME_DRIVER_PATH = "C:\\Users\\auxk0\\OneDrive\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"#path to chrome driver

# Path to your Resume PDF
RESUME_PATH = "resume2025.pdf"

# Job application URLs
JOB_URLS = [
    "https://careers-healthedge.icims.com/jobs/6320/security-intern---summer-internship-program/candidate?from=login&eem=RZ53HTK9nYvMIN1Iy0YqXRPffZ03m9XNRRUwdPjaeFL2hN8BMy8b1_2ozb7Ww3_U&code=0329cd64dddde7c30cab22e536a5f8d3a43ee861e61b2ac8ecb60466a6a6824c&ga=022e5712ce181bf7d6e2252660ca892af84518b1fad40a720c62b5f6a8688d9c&accept_gdpr=1&mobile=false&width=1410&height=1332&bga=true&needsRedirect=false&jan1offset=-300&jun1offset=-240"
]

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def apply_to_job(job_url):
    try:
        driver.get(job_url)
        time.sleep(3)  # Wait for the page to load

        # Find and fill out name field
        name_field = driver.find_element(By.NAME, "fullName")
        name_field.send_keys("Your Name")

        # Find and fill out email field
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys("your.email@example.com")

        # Upload resume
        resume_upload = driver.find_element(By.NAME, "resumeUpload")
        resume_upload.send_keys(RESUME_PATH)

        # Submit application
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Apply') or contains(text(),'Submit')]")
        submit_button.click()

        print(f"Successfully applied to {job_url}")
    except Exception as e:
        print(f"Failed to apply to {job_url}: {e}")

# Loop through job URLs and apply
for url in JOB_URLS:
    apply_to_job(url)

# Close browser
driver.quit()
