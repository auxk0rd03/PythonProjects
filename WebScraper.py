import requests
from bs4 import BeautifulSoup
import csv
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_headlines(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        logging.info(f"Fetching {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the webpage: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all headlines (replace with the correct tag/class)
    headlines = soup.find_all('h2', class_='article-title')
    
    # Extract text from each headline
    return [headline.get_text(strip=True) for headline in headlines]

def save_to_csv(headlines, filename):
    logging.info(f"Saving {len(headlines)} headlines to {filename}...")
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline'])  # Write header
        for title in headlines:
            writer.writerow([title])  # Write each headline

def scrape_multiple_pages(base_url, num_pages):
    all_headlines = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        headlines = fetch_headlines(url)
        all_headlines.extend(headlines)
        time.sleep(2)  # Respect rate limits
    return all_headlines

# Main
if __name__ == "__main__":
    base_url = 'https://www.scrapethissite.com/pages/simple/'  # Replace with the base URL of the website
    num_pages = 5  # Number of pages to scrape
    headlines = scrape_multiple_pages(base_url, num_pages)

    if headlines:
        save_to_csv(headlines, 'headlines.csv')
        logging.info("Scraping completed successfully!")
    else:
        logging.warning("No headlines found.")