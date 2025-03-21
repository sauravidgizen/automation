from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import random

# Function to add human-like delays
def human_delay(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

# Search query
search_query = "Chandni Chowk"

# Set up Selenium WebDriver with anti-bot measures
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode (no visible browser)
options.add_argument("--incognito")  # Prevents tracking
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoids detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Rotating user-agent

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Open Google
driver.get("https://www.google.com")
human_delay()

# Locate search box and enter query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search_query)
human_delay()
search_box.send_keys(Keys.ENTER)

# Initialize data storage
questions = []
max_questions = 20
counter = 1

# Scroll down a bit to mimic user behavior
driver.execute_script("window.scrollBy(0, 300);")
human_delay()

while counter <= max_questions:
    try:
        # Locate "People Also Ask" questions
        question_elements = driver.find_elements(By.CSS_SELECTOR, 'div[jsname="N760b"] > div')

        for question_element in question_elements:
            question_text = question_element.text.strip()

            # Skip empty or unrelated questions
            if question_text and search_query.lower() in question_text.lower() and question_text not in questions:
                print(f"{counter}. {question_text}")
                questions.append([question_text])
                counter += 1

                # Random small delay after interacting
                human_delay(1, 3)

        # Scroll down to possibly load more questions
        driver.execute_script("window.scrollBy(0, 400);")
        human_delay()

    except Exception as e:
        print(f"⚠️ Error: {e}")
        break

# Save extracted questions to CSV
csv_file_path = r"C:\Users\ksaur\OneDrive\Desktop\questions.csv"
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Question"])
    writer.writerows(questions)

print(f"\n✅ Successfully extracted {len(questions)} questions and saved them to: {csv_file_path}")

# Close WebDriver
driver.quit()
