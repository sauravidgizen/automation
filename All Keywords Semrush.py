import csv
import time
import random
from selenium import webdriver
import tkinter as tk
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keyword = input("Enter the Market: ").strip()

def safe_get_text(driver, by, selector):
    """Safely get text from an element or return 'N/A' if not found."""
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, selector))
        )
        return element.text.strip()
    except:
        return "N/A"

# Replace with your actual credentials
EMAIL = "tools@idigizen.com"
PASSWORD = "Vypzee@2023"
OUTPUT_FILE = r"C:\Users\ksaur\OneDrive\Desktop\RGsemrush_data.csv"

# Initialize WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keeps browser open
chrome_options.add_argument("--start-maximized")  # Opens in full-screen mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open SEO Tool Adda login page
    driver.get("https://seotooladda.com/user/login.php")

    # Log in
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email ID']"))
    )
    email_input.send_keys(EMAIL)
    time.sleep(random.uniform(1, 2))

    password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
    password_input.send_keys(PASSWORD)
    time.sleep(random.uniform(1, 2))
    password_input.send_keys("\n")

    # Wait for dashboard to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("✅ Dashboard loaded successfully!")

    # Navigate to SEMrush tool
    driver.get("https://smr.seotooladda.com/analytics/")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.srf-report-sidebar-main__link-text"))
    )

    # Wait for loader to disappear
    WebDriverWait(driver, 20).until(
          EC.invisibility_of_element_located((By.ID, "pLoader"))
)

    keyword_magic_tool_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Keyword Magic Tool')]"))
    )
    keyword_magic_tool_button.click()

    print("✅ Successfully opened Keyword Magic Tool!")

    # Enter keyword
    # keyword = "Chawri Bazar"
    
    time.sleep(random.uniform(2, 5))  # Random delay

    search_bar = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "___SValue_7h59t-kmt_._size_l_7h59t-kmt_._state_normal_7h59t-kmt_"))
    )
    search_bar.clear()
    search_bar.send_keys(keyword)
    time.sleep(random.uniform(1, 2))

    # Click the location dropdown
    location_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sm-database-selector__trigger-text"))
    )
    location_dropdown.click()
    print("✅ Opened the location dropdown")

    # Select "India"
    india_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'India')]"))
    )
    india_option.click()
    print("✅ Selected 'India'")

    # Click the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "_size_l_se82q-kmt_.___SText_se82q-kmt_"))
    )
    search_button.click()
    
    print(f"🔍 Searching for keyword: {keyword}")

    # # Wait for the report to load
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.kwo-report-header"))
    # )
    # print("✅ Report Loaded!")

    
    all_keywords_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='All Keywords']"))
        )
    all_keywords_tab.click()
    print("✅ Clicked on 'All Keywords' tab.")
    
    export_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='export-button']"))
        )
    export_button.click()
    print("✅ Clicked on Export tab.")

    csv_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='CSV']"))
        )
    csv_button.click()
    print("✅ CSV export clicked!")

except Exception as e:
    print(f"❌ Critical Error: {e}")
    driver.save_screenshot("critical_error_screenshot.png")
    with open("critical_error_log.txt", "w") as f:
        f.write(str(e))

finally:
    # Give the browser a few seconds to start the download
    print("⏳ Waiting for download to begin...")
    time.sleep(20)  # Adjust time as needed depending on your network speed

    print("✅ Process completed. Closing browser...")
    driver.quit()

def start_bot():
    keyword = keyword_entry.get().strip()
    if keyword:
        threading.Thread(target=run_selenium, args=(keyword,), daemon=True).start()
        status_label.config(text="🕵️‍♂️ Automation started...")
    else:
        status_label.config(text="❌ Please enter a keyword.")

root = tk.Tk()
root.title("SEMrush Keyword Export Tool")
root.geometry("400x200")

tk.Label(root, text="Enter Market Keyword:", font=("Arial", 12)).pack(pady=10)
keyword_entry = tk.Entry(root, width=30, font=("Arial", 12))
keyword_entry.pack(pady=5)
tk.Button(root, text="Start Automation", command=start_bot, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
status_label.pack()
