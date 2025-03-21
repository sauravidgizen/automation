from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import random

# Function to add human-like delays
def human_delay(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

# Define search query
search_query = "Chandni chowk"

# Set up WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (invisible)
options.add_argument("--incognito")  # Open in incognito mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Random user-agent

driver = webdriver.Chrome(options=options)

# Open Google
driver.get("https://www.google.com")
human_delay()

# Locate search box and enter query
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
search_box.send_keys(search_query)
human_delay()
search_box.send_keys(Keys.ENTER)

# Wait for search results to load
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tF2Cxc a")))
human_delay()

# Scroll down slightly to mimic human behavior
driver.execute_script("window.scrollBy(0, 300);")
human_delay()

# Locate "People also search for" section
try:
    pas_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "dg6jd"))
    )

    # Extract text content
    suggested_keywords = [element.text.strip() for element in pas_elements if element.text.strip()]
    print("📌 Extracted Text from class='dg6jd':")
    print(suggested_keywords)

    # Save to CSV
    csv_file_path = r"C:\Users\ksaur\OneDrive\Desktop\people_also_search_for.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["People Also Search For"])
        for keyword in suggested_keywords:
            writer.writerow([keyword])

    print(f"✅ Data saved successfully to: {csv_file_path}")

except Exception as e:
    print(f"⚠️ 'People also search for' section not found: {e}")

# Close browser
driver.quit()
