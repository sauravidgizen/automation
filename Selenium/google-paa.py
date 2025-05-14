import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_medium(email):
    # Launch Chrome
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = uc.Chrome(options=options)

    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Go to Medium
        driver.get("https://medium.com/")
        print("🌐 Opened Medium")

        # Step 2: Click 'Get started'
        get_started_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Get started")))
        get_started_btn.click()
        print("🟢 Clicked 'Get started'")

        # Step 3: Wait for popup and click 'Sign up with email'
        signup_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(@class, "n") and contains(@class, "o") and contains(@class, "gv")]'))
        )
        signup_button.click()
        print("✉️ Clicked 'Sign up with email'")

        # Step 4: Wait for the Gmail email input field to appear
        email_input = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "rFrNMe.X3mtXb.UOsO2.ToAxb.zKHdkd.sdJrJc.Tyc9J")
            )
        )

        # Wait until the input field is clickable and interactable
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rFrNMe.X3mtXb.UOsO2.ToAxb.zKHdkd.sdJrJc.Tyc9J")))

        # Click on the email input field before typing
        email_input.click()
        print("✋ Clicked on the email input field")

        # Wait before entering the email
        print("⏳ Waiting before entering the email...")
        time.sleep(3)  # Wait for 3 seconds before entering the email

        # Step 5: Try sending the email normally
        try:
            email_input.send_keys(email)
            email_input.send_keys(Keys.ENTER)
            print(f"📩 Email '{email}' submitted")
        except Exception as e:
            print(f"⚠️ Failed to input email using send_keys: {e}")

            # Step 6: Fallback - Use JavaScript to set the email if send_keys fails
            print("🔧 Using JavaScript to input the email...")
            driver.execute_script("arguments[0].value = arguments[1];", email_input, email)
            print(f"📩 Email '{email}' input via JavaScript")

        # Wait for the user to manually complete the Gmail authentication or click the magic link
        input("📨 Check your inbox and click the magic link. Press Enter to close the browser...")

    finally:
        print("✅ Keeping the browser open for manual interaction...")
        # Do not close the driver, waiting for user input before quitting
        # driver.quit()  # Commented out to keep the browser open

# Run the function with the email "vypzeeseo@gmail.com"
if __name__ == "__main__":
    login_medium("vypzeeseo@gmail.com")
