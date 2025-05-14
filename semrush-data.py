import time
import random
import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🧠 CONFIGS
SEARCH_TERM = "Chandni chowk shops"
VYPZEE_SITE = "vypzee.com"
SEARCH_URL = "https://www.google.com/"

# Setup undetected Chrome with user-agent
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

driver = uc.Chrome(options=chrome_options)

def random_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def smooth_scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(0, last_height, 300):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(random.uniform(0.5, 1.2))
    print("📜 Finished slow scroll to page bottom.")

# STEP 1: Open Google
driver.get(SEARCH_URL)
random_sleep(2, 4)

# STEP 2: Human-like typing
search_box = driver.find_element(By.NAME, "q")
for char in SEARCH_TERM:
    search_box.send_keys(char)
    time.sleep(random.uniform(0.1, 0.3))
search_box.send_keys(Keys.RETURN)
random_sleep(3, 5)

# STEP 3: Loop through Google results until Vypzee is found
found_vypzee = False
page_number = 1
while not found_vypzee and page_number <= 10:
    driver.execute_script("window.scrollBy(0, 300);")
    random_sleep(1, 2)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute('href')
        if href and VYPZEE_SITE in href:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                WebDriverWait(driver, 5).until(EC.visibility_of(link))
                link.click()
                found_vypzee = True
                break
            except Exception as e:
                print(f"❌ Couldn't click link: {e}")
                continue

    if not found_vypzee:
        next_label = f"Page {page_number + 1}"
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[aria-label="{next_label}"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            random_sleep(1, 2)
            next_button.click()
            random_sleep(2, 4)
            page_number += 1
        except Exception as e:
            print(f"❌ Error navigating to next page: {e}")
            break

# STEP 4: Interact with Vypzee page
if found_vypzee:
    try:
        print("✅ Vypzee page loaded.")

        # Scroll to "Shop Categories"
        random_sleep(2, 3)
        shop_categories = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Shop Categories')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shop_categories)
        print("🛒 Scrolled to Shop Categories")
        random_sleep(2, 3)

        # Scroll to "Directory"
        directory = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Directory')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", directory)
        print("📁 Scrolled to Directory")
        random_sleep(3, 4)

        # Simulate visible mouse scroll down after going to Directory
        pyautogui.scroll(-1000)  # Scroll down by a larger amount (adjust as needed)
        random_sleep(2, 3)  # Wait after the scroll action to make it look natural

        # Locate the "About" section and click
        try:
            # Find the "About" div by text
            about_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'About')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", about_section)
            random_sleep(1, 2)
            about_section.click()
            print("ℹ️ Clicked on the About section.")
            random_sleep(5, 6)
        except Exception as e:
            print(f"❌ Couldn't find or click the About section: {e}")

        # Slowly scroll to the bottom
        smooth_scroll_to_bottom()

    except Exception as e:
        print(f"❌ Error interacting with Vypzee page: {e}")

# 🛑 DO NOT close the browser
print("🧭 Script finished — browser remains open.")
