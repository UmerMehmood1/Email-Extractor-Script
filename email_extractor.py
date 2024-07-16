import re
import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime
import os
import sys

def fetch_free_proxies(driver):
    url = "https://free-proxy-list.net/"
    driver.get(url)
    
    proxies = []
    
    # Wait until the table is loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-striped.table-bordered tbody tr'))
    )
    
    # Extract the proxy list table rows
    rows = driver.find_elements(By.CSS_SELECTOR, 'table.table-striped.table-bordered tbody tr')
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        if columns[6].text == 'yes':  # Check if the proxy supports HTTPS
            proxy = f"{columns[0].text}:{columns[1].text}"
            proxies.append(proxy)
    
    return proxies

def set_proxy_and_user_agent(driver, proxy=None, user_agent=None):
    if proxy:
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        print(f"Using proxy: {proxy}")

    if user_agent:
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        print(f"Using user agent: {user_agent}")

def extract_emails_from_page(driver, url):
    try:
        # Open the webpage
        driver.get(url)
        
        # Wait until the page is fully loaded by waiting for a specific element to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        # Wait for all JavaScript to execute
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Additional wait to ensure dynamic content is loaded
        time.sleep(random.uniform(2, 5))
        
        # Extract the page source
        page_source = driver.page_source
        
        # Use regex to find all email addresses in the page source
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_source)
        
        return emails
    except (WebDriverException, TimeoutException) as e:
        print(f"Failed to extract emails: {e}")
    
    return []

def save_emails_to_excel(emails):
    # Ensure emails are unique
    unique_emails = list(set(emails))
    
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'emails_{current_time}.xlsx'
    
    # Create a DataFrame from the list of emails
    df = pd.DataFrame(unique_emails, columns=['Email'])
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Extracted {len(unique_emails)} emails and saved to '{filename}'.")
    
    return filename

def open_directory(filename):
    directory = os.path.dirname(os.path.abspath(filename))
    os.startfile(directory)

def main(url):
    # Initialize the undetected ChromeDriver
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
    
    try:
        proxies = fetch_free_proxies(driver)
        
        if proxies:
            # Select a proxy
            proxy = random.choice(proxies)
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            ]
            user_agent = random.choice(user_agents)
            
            set_proxy_and_user_agent(driver, proxy=proxy, user_agent=user_agent)
            
            emails = extract_emails_from_page(driver, url)
            
            if emails:
                filename = save_emails_to_excel(emails)
                open_directory(filename)
            else:
                print("No emails found.")
        else:
            print("No proxies available.")
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        url = input("Enter URL to Extract Emails (Enter 'exit' to quit): ")
        if 'exit' in url.lower():
            break
        else:
            main(url)
