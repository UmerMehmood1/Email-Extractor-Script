# Email Extractor

This Python script extracts email addresses from a specified webpage using Selenium and saves them to an Excel file. It leverages free proxies and random user agents to enhance the scraping process and bypass basic scraping defenses.

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (compatible with the installed Chrome version)
- `undetected-chromedriver` for bypassing detection mechanisms

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. **Install required packages:**

   ```bash
   pip install pandas selenium undetected-chromedriver```
3. **Download ChromeDriver:**

   - Download the ChromeDriver that matches your Chrome version from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   - Ensure the ChromeDriver executable is in your system's PATH or specify the path in the script.

## Usage

1. **Run the script:**

   ```bash
   python email_extractor.py```
2. **Enter the URL:**

   The script will prompt you to enter the URL from which you want to extract emails.

3. **Wait for the process:**

   The script will:

   - Fetch a list of free proxies.
   - Set a random proxy and user agent.
   - Navigate to the specified URL.
   - Extract email addresses from the webpage.
   - Save the extracted emails to an Excel file.
   - Open the directory containing the Excel file.

## Script Overview

### `fetch_free_proxies(driver)`

Fetches a list of free HTTPS proxies from `https://free-proxy-list.net/`.

### `set_proxy_and_user_agent(driver, proxy=None, user_agent=None)`

Sets a specified proxy and user agent for the Selenium driver.

### `extract_emails_from_page(driver, url)`

Navigates to the given URL, waits for the page to load, and extracts email addresses using regex.

### `save_emails_to_excel(emails)`

Saves the list of extracted email addresses to an Excel file with a timestamped filename.

### `open_directory(filename)`

Opens the directory containing the saved Excel file.

### `main(url)`

Main function that coordinates the entire email extraction process.

## Example

```bash
Enter URL to Extract Emails: https://example.com```
