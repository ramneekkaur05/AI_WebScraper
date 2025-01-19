from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # For rotating User-Agent headers
import time  # For adding delays between requests

# Proxy credentials
username = "faacfc787a56427aa540324ba4250d9b388bb4615e0"
password = "render=false"
proxy_host = "proxy.scrape.do"
proxy_port = "8080"

# Configure Chrome options
def configure_chrome_options():
    ua = UserAgent()  # Initialize UserAgent instance
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server=http://{username}:{password}@{proxy_host}:{proxy_port}")
    chrome_options.add_argument(f"user-agent={ua.random}")  # Rotate User-Agent
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent Selenium detection
    return chrome_options

# Path to ChromeDriver
chrome_driver_path = "./chromedriver.exe"  # Replace with your ChromeDriver path
service = Service(chrome_driver_path)

# Scraping function
def scrape_website(url):
    chrome_options = configure_chrome_options()
    try:
        print("Initializing WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Navigating to {url}...")
        driver.get(url)

        # Adding delay to mimic human interaction
        time.sleep(5)  # Adjust as needed

        print("Scraping page content...")
        html_content = driver.page_source
        return html_content

    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

    finally:
        try:
            driver.quit()
        except NameError:
            pass  # Handle case where driver initialization failed

# Extract body content
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return ""

# Clean body content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

# Split content into chunks
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]

# Example usage
if __name__ == "__main__":
    URL = "https://httpbin.org/anything?json"  # Replace with your target website
    html_content = scrape_website(URL)

    if html_content:
        body_content = extract_body_content(html_content)
        cleaned_content = clean_body_content(body_content)
        chunks = split_dom_content(cleaned_content)

        # Print the first chunk as an example
        print("First Chunk of Cleaned Content:")
        if chunks:
            print(chunks[0])
        else:
            print("No content extracted.")
