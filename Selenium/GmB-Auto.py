import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import math

# Load all shop names
file_path = r"C:\Users\ksaur\Downloads\shops name.xlsx"
df = pd.read_excel(file_path)
shop_list = df['Shops'].tolist()

# Define batch info
batch_size = 100
total_batches = math.ceil(len(shop_list) / batch_size)
save_folder = r"C:\Users\ksaur\Downloads"

# Check already processed batch filesnot now
existing_files = [f for f in os.listdir(save_folder) if f.startswith("gmb_with_website_info_batch_")]
existing_batches = {int(f.split("_batch_")[1].split(".")[0]) for f in existing_files}

# Setup undetected Chrome browser
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = uc.Chrome(options=options)
driver.get("https://www.google.com")
time.sleep(2)

def close_location_prompt():
    try:
        # Check if the "See results closer to you?" prompt appears
        location_prompt = driver.find_element(By.XPATH, "//button[text()='Not now']")
        location_prompt.click()
        print("⏩ Closed location prompt.")
    except:
        pass  # If the prompt doesn't appear, do nothing

for batch_num in range(1, total_batches + 1):
    if batch_num in existing_batches:
        print(f"⏩ Skipping batch {batch_num} (already processed)")
        continue

    print(f"\n🚀 Processing batch {batch_num} of {total_batches}")
    results = []
    start_index = (batch_num - 1) * batch_size
    end_index = min(batch_num * batch_size, len(shop_list))
    batch_shops = shop_list[start_index:end_index]

    for shop in batch_shops:
        print(f"🔍 Searching: {shop}")

        try:
            search_box = driver.find_element(By.NAME, "q")
        except:
            driver.get("https://www.google.com")
            time.sleep(2)
            search_box = driver.find_element(By.NAME, "q")

        search_box.clear()

        # Close the location pop-up if it appears
        close_location_prompt()

        search_box.send_keys(shop)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        gmb_status = "No"
        website_status = "Not Available"
        website_url = "N/A"

        try:
            gmb_panel = driver.find_element(By.ID, "rhs")
            gmb_status = "Yes"
            print(f"✅ GMB found for: {shop}")

            try:
                website_span = driver.find_element(By.XPATH, "//span[text()='Website']")
                website_link = website_span.find_element(By.XPATH, "./ancestor::a")
                website_url = website_link.get_attribute("href")
                website_status = "Present"
                print(f"🌐 Website: {website_url}")
            except:
                print(f"❌ Website not found for: {shop}")
        except:
            print(f"❌ No GMB profile for: {shop}")

        results.append({
            "Shop Name": shop,
            "Has GMB": gmb_status,
            "Website": website_status,
            "Website URL": website_url
        })

        time.sleep(2)

    # Save this batch
    output_path = os.path.join(save_folder, f"gmb_with_website_info_batch_{batch_num}.xlsx")
    pd.DataFrame(results).to_excel(output_path, index=False)
    print(f"✅ Batch {batch_num} saved to: {output_path}")

# Done
input("\n🎉 All batches processed. Press Enter to close browser...")
driver.quit()
