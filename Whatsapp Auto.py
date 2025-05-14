from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")  # Optional: opens the browser in full screen

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for the page to load completely
time.sleep(5)

try:
    # Click on "Log in with phone number"
    login_button = driver.find_element(By.XPATH, '//*[text()="Log in with phone number"]')
    login_button.click()
    print("Clicked on 'Log in with phone number'.")

    time.sleep(2)

    # Find the phone number input field
    phone_input = driver.find_element(By.XPATH, "//input[@aria-label='Type your phone number.']")
    phone_input.send_keys("8766307535")
    print("Phone number entered.")

    # Find and click the "Next" button
    next_button = driver.find_element(By.XPATH, "//div[text()='Next']")
    next_button.click()
    print("Clicked on 'Next'. Please complete OTP manually on your phone.")

    # Wait until the new chat button appears after login
    print("Waiting for successful login and chat interface to load...")
    while True:
        try:
            new_chat_button = driver.find_element(By.XPATH, "//span[@data-icon='new-chat-outline']")
            new_chat_button.click()
            print("Clicked on the 'New chat' button.")
            break
        except:
            time.sleep(2)

    # Wait for search bar and enter phone number
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
    )
    search_input.send_keys("8076929151")
    print("Entered recipient's number.")

    # Select contact from search results using title
    profile_pic = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-selected='true']//img[contains(@class, '_ao3e')]"))
    )
    profile_pic.click()

    # Type the message
    message_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
    )
    message_input.send_keys("Hello, this is an automated message!")

    # Click the green send button with white arrow
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
    )
    send_button.click()
    print("Message sent successfully.")

except Exception as e:
    print(f"Error: {e}")

# Optional: Keep the browser open for a while
time.sleep(30)

# Close the browser
driver.quit()