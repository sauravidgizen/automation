# === Part 1: Imports ===
import csv
import time
import random
import tkinter as tk
import threading
import datetime
import os
import subprocess
import glob
from tkinter import ttk, messagebox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Helper Functions ===
def safe_get_text(driver, by, selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, selector))
        )
        return element.text.strip()
    except:
        return "N/A"

def log_status(message):
    status_label.config(text=message)
    status_listbox.insert(tk.END, message)
    status_listbox.yview(tk.END)

def open_downloaded_file(keyword):
    today = datetime.date.today().strftime("%Y-%m-%d")
    formatted_keyword = keyword.lower().replace(" ", "-")
    filename_pattern = f"{formatted_keyword}_all-keywords_in_{today}"

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    files = os.listdir(downloads_folder)

    for file in files:
        if filename_pattern in file and file.endswith(".csv"):
            file_path = os.path.join(downloads_folder, file)
            log_status(f"📂 File downloaded: {file}")
            return file_path

    log_status("❌ File not found. Check if the download completed successfully.")
    return None

# === Automation Function ===
def run_selenium(keyword):
    EMAIL = "tools@idigizen.com"
    PASSWORD = "Vypzee@2023"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://seotooladda.com/user/login.php")

        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email ID']"))
        )
        email_input.send_keys(EMAIL)
        time.sleep(random.uniform(1, 2))

        password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
        password_input.send_keys(PASSWORD)
        time.sleep(random.uniform(1, 2))
        password_input.send_keys("\n")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        driver.get("https://smr.seotooladda.com/analytics/")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.srf-report-sidebar-main__link-text"))
        )
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "pLoader"))
        )

        keyword_magic_tool_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Keyword Magic Tool')]"))
        )
        keyword_magic_tool_button.click()
        log_status("✅ Successfully opened Keyword Magic Tool!")

        time.sleep(random.uniform(2, 5))

        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "___SValue_7h59t-kmt_._size_l_7h59t-kmt_._state_normal_7h59t-kmt_"))
        )
        search_bar.clear()
        search_bar.send_keys(keyword)
        time.sleep(random.uniform(1, 2))

        location_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sm-database-selector__trigger-text"))
        )
        location_dropdown.click()
        log_status("✅ Opened the location dropdown")

        india_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'India')]"))
        )
        india_option.click()
        log_status("✅ Selected 'India'")

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_size_l_se82q-kmt_.___SText_se82q-kmt_"))
        )
        search_button.click()
        log_status(f"🔍 Searching for keyword: {keyword}")

        all_keywords_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='All Keywords']"))
        )
        all_keywords_tab.click()
        log_status("✅ Clicked on 'All Keywords' tab.")

        export_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='export-button']"))
        )
        export_button.click()
        log_status("✅ Clicked on Export tab.")

        csv_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='CSV']"))
        )
        csv_button.click()
        log_status("✅ CSV export clicked!")

    except Exception as e:
        log_status(f"❌ Error: {e}")
        driver.save_screenshot("critical_error_screenshot.png")
        with open("critical_error_log.txt", "w") as f:
            f.write(str(e))

    finally:
        log_status("⏳ Waiting for download to begin...")
        time.sleep(20)
        file_path = open_downloaded_file(keyword)
        driver.quit()
        if file_path:
            main_root.after(1000, lambda: launch_analysis_gui(file_path))

# === GUI Launcher Function ===
def launch_analysis_gui(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Volume', 'Keyword Difficulty', 'Intent'])
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Keyword Difficulty'] = pd.to_numeric(df['Keyword Difficulty'], errors='coerce')
    df = df.dropna(subset=['Volume', 'Keyword Difficulty'])

    unique_intents = ['All'] + sorted(df['Intent'].dropna().unique().tolist())

    root2 = tk.Toplevel()
    root2.title("Keyword Filter + Smart Analytics")
    root2.geometry("1300x850")

    filter_frame = tk.Frame(root2)
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Min Volume").grid(row=0, column=0, padx=5)
    volume_entry = tk.Entry(filter_frame, width=10)
    volume_entry.grid(row=0, column=1, padx=5)

    tk.Label(filter_frame, text="Max Keyword Difficulty").grid(row=0, column=2, padx=5)
    kd_entry = tk.Entry(filter_frame, width=10)
    kd_entry.grid(row=0, column=3, padx=5)

    tk.Label(filter_frame, text="Intent").grid(row=0, column=4, padx=5)
    intent_var = tk.StringVar()
    intent_dropdown = ttk.Combobox(filter_frame, textvariable=intent_var, values=unique_intents, state="readonly", width=20)
    intent_dropdown.grid(row=0, column=5, padx=5)
    intent_dropdown.set("All")

    tk.Label(filter_frame, text="Smart Filter Presets").grid(row=1, column=0, columnspan=2, pady=5)
    preset_var = tk.StringVar()
    preset_dropdown = ttk.Combobox(filter_frame, textvariable=preset_var, state="readonly", width=50)
    preset_dropdown['values'] = [
        "None",
        "High Volume, Low Difficulty (Ranking Fast)",
        "Zero Search Difficulty (Quick wins)",
        "Long-Tail with High Intent (Low comp + high conversion)",
        "Evergreen Keywords (Consistent traffic)",
        "Keywords with Featured Snippet Potential"
    ]
    preset_dropdown.grid(row=1, column=2, columnspan=3, pady=5)
    preset_dropdown.set("None")

    tree_frame = tk.Frame(root2)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")

    stats_frame = tk.LabelFrame(root2, text="Analytics Summary", padx=10, pady=10)
    stats_frame.pack(fill=tk.X, pady=10)
    stats_text = tk.Text(stats_frame, height=6, wrap='word')
    stats_text.pack(fill=tk.X)

    def update_tree(filtered_df):
        tree.delete(*tree.get_children())
        for _, row in filtered_df.iterrows():
            tree.insert("", "end", values=list(row))

    def update_stats(filtered_df):
        total = len(filtered_df)
        avg_vol = filtered_df['Volume'].mean()
        avg_kd = filtered_df['Keyword Difficulty'].mean()
        group_counts = filtered_df['Intent'].value_counts()

        stats_text.delete(1.0, tk.END)
        stats_text.insert(tk.END, f"Total Keywords: {total}\n")
        stats_text.insert(tk.END, f"Average Volume: {avg_vol:.2f}\n")
        stats_text.insert(tk.END, f"Average Keyword Difficulty: {avg_kd:.2f}\n\n")
        stats_text.insert(tk.END, "Keyword Count by Intent:\n")
        for intent, count in group_counts.items():
            stats_text.insert(tk.END, f" - {intent}: {count}\n")

    def apply_filters():
        filtered = df.copy()
        vol = volume_entry.get()
        kd = kd_entry.get()
        intent = intent_var.get()
        preset = preset_var.get()

        try:
            if preset != "None":
                if preset == "High Volume, Low Difficulty (Ranking Fast)":
                    filtered = filtered[(filtered['Volume'] >= 1000) & (filtered['Keyword Difficulty'] <= 20)]
                elif preset == "Zero Search Difficulty (Quick wins)":
                    filtered = filtered[filtered['Keyword Difficulty'] == 0]
                elif preset == "Long-Tail with High Intent (Low comp + high conversion)":
                    filtered = filtered[(filtered['Keyword'].str.count(' ') >= 3) & (filtered['Keyword Difficulty'] <= 20)]
                elif preset == "Evergreen Keywords (Consistent traffic)":
                    filtered = filtered[filtered['Intent'].str.contains("Informational", case=False, na=False)]
                elif preset == "Keywords with Featured Snippet Potential":
                    filtered = filtered[
                        filtered['Keyword'].str.lower().str.startswith(("how", "what", "why", "can", "does"))
                    ]
            else:
                if vol:
                    filtered = filtered[filtered['Volume'] >= int(vol)]
                if kd:
                    filtered = filtered[filtered['Keyword Difficulty'] <= int(kd)]
                if intent != "All":
                    filtered = filtered[filtered['Intent'] == intent]
        except Exception as e:
            print("Filter Error:", e)

        update_tree(filtered)
        update_stats(filtered)

    tk.Button(filter_frame, text="Apply Filter", command=apply_filters).grid(row=1, column=6, padx=10)

    update_tree(df)
    update_stats(df)

# === MAIN GUI (Automation) ===
main_root = tk.Tk()
main_root.title("SEMrush Keyword Export Tool")
main_root.geometry("500x400")

tk.Label(main_root, text="Enter Market Keyword:", font=("Arial", 12)).pack(pady=10)
keyword_entry = tk.Entry(main_root, width=35, font=("Arial", 12))
keyword_entry.pack(pady=5)
keyword_entry.bind("<Return>", lambda event: start_bot())

tk.Button(main_root, text="Start Keyword Research", command=lambda: start_bot(), font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

status_label = tk.Label(main_root, text="", font=("Arial", 10), fg="blue")
status_label.pack()

status_listbox = tk.Listbox(main_root, width=60, height=15, font=("Courier", 9))
status_listbox.pack(pady=10)

def start_bot():
    keyword = keyword_entry.get().strip()
    if keyword:
        threading.Thread(target=run_selenium, args=(keyword,), daemon=True).start()
        log_status("⚙️ Keyword Research started...")
    else:
        log_status("❌ Please enter a keyword.")

main_root.mainloop()
