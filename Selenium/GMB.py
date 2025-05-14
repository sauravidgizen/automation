import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Load CSV file
file_path = r"C:\Users\ksaur\Downloads\market shop list.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Assuming column name is exactly "Shops"
shop_names = df["Shops"].dropna().tolist()

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or provide path: webdriver.Chrome(executable_path='path_to_chromedriver')

# Open Google and search each shop name
for shop in shop_names:
    try:
        driver.get("https://www.google.com")
        time.sleep(2)

        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(shop)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait to let results load
    except Exception as e:
        print(f"Error searching for '{shop}': {e}")

# Optional: Keep browser open or close after done
input("Press Enter to close the browser...")
driver.quit()
