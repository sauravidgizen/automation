from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time
import random

# Function to simulate typing with a delay
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Simulate human typing speed

# Function to simulate mouse movement
def random_mouse_move():
    move_x = random.randint(50, 500)
    move_y = random.randint(50, 500)
    driver.execute_script(f"window.scrollTo({move_x}, {move_y})")

# Ask for user input
query = input("Enter your Google search query: ")

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-blink-features")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--lang=en-US")
options.add_argument("window-size=1200,800")
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.{random.randint(1000,9999)}.100 Safari/537.36')

# Initialize Chrome driver
driver = webdriver.Chrome(options=options)

# Make it stealth
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# Open Google
driver.get("https://www.google.com")

# Accept cookie consent if shown
try:
    time.sleep(random.uniform(1.5, 3))
    consent = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
    consent.click()
except:
    pass

# Enter query and search with human-like typing
time.sleep(random.uniform(2, 4))
search_box = driver.find_element(By.NAME, "q")
human_typing(search_box, query)
time.sleep(random.uniform(0.5, 1.2))
search_box.send_keys(Keys.RETURN)

# Start searching for 'vypzee.com'
found = False

while not found:
    time.sleep(random.uniform(2.5, 4))

    # Simulate scrolling like a human with random mouse movements
    for scroll_y in range(0, 500, 100):
        driver.execute_script(f"window.scrollTo(0, {scroll_y})")
        random_mouse_move()
        time.sleep(random.uniform(0.3, 0.6))

    # Look for links containing 'vypzee.com'
    links = driver.find_elements(By.XPATH, "//a[contains(@href, 'vypzee.com')]")
    for link in links:
        href = link.get_attribute("href")
        if "vypzee.com" in href:
            print("Found:", href)
            time.sleep(random.uniform(1, 2))
            link.click()
            found = True
            break

    # If not found, go to next page
    if not found:
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            print("Moving to next page...")
            time.sleep(random.uniform(2, 4))
            next_button.click()
        except:
            print("No more pages. Link not found.")
            break

# Optional: Keep browser open
time.sleep(10)
driver.quit()
