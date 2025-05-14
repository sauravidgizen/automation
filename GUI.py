import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import glob

# === Load latest CSV from Downloads ===
downloads_path = r"C:\Users\ksaur\Downloads"
csv_files = glob.glob(os.path.join(downloads_path, "*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in the Downloads folder.")

latest_csv = max(csv_files, key=os.path.getctime)
print(f"📁 Loading latest file: {latest_csv}")  # For debug

# Load CSV
try:
    df = pd.read_csv(latest_csv)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load CSV file.\n{e}")
    raise

# Clean data
df = df.dropna(subset=['Volume', 'Keyword Difficulty', 'Intent'])
df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
df['Keyword Difficulty'] = pd.to_numeric(df['Keyword Difficulty'], errors='coerce')
df = df.dropna(subset=['Volume', 'Keyword Difficulty'])

# Unique intents
unique_intents = ['All'] + sorted(df['Intent'].dropna().unique().tolist())

# === GUI Setup ===
root = tk.Tk()
root.title("Keyword Filter + Smart Analytics")
root.geometry("1300x850")

# === FILTER SECTION ===
filter_frame = tk.Frame(root)
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

# Preset Filter Dropdown
tk.Label(filter_frame, text="Smart Filter Presets").grid(row=1, column=0, columnspan=2, pady=5)
preset_var = tk.StringVar()
preset_dropdown = ttk.Combobox(filter_frame, textvariable=preset_var, state="readonly", width=50)
preset_dropdown['values'] = [
    "None",
    "High Volume, Low Difficulty (Ranking Fast)",
    "Trending Keywords (Time-sensitive boosts)",
    "Zero Search Difficulty (Quick wins)",
    "Long-Tail with High Intent (Low comp + high conversion)",
    "Evergreen Keywords (Consistent traffic)",
    "High Click-Through Rate Keywords (Attractive SERP titles)",
    "Keywords with Featured Snippet Potential",
    "Keywords with High CPC (Monetization potential)",
    "Low Bounce Rate Keywords",
    "High Time-on-Page Keywords"
]
preset_dropdown.grid(row=1, column=2, columnspan=3, pady=5)
preset_dropdown.set("None")

# === TABLE ===
tree_frame = tk.Frame(root)
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

def update_tree(filtered_df):
    tree.delete(*tree.get_children())
    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=list(row))

# === ANALYTICS PANEL ===
stats_frame = tk.LabelFrame(root, text="Analytics Summary", padx=10, pady=10)
stats_frame.pack(fill=tk.X, pady=10)

stats_text = tk.Text(stats_frame, height=6, wrap='word')
stats_text.pack(fill=tk.X)

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

# === FILTER FUNCTION ===
def apply_filters():
    filtered = df.copy()

    vol = volume_entry.get()
    kd = kd_entry.get()
    intent = intent_var.get()
    preset = preset_var.get()

    try:
        if vol:
            filtered = filtered[filtered['Volume'] >= int(vol)]
        if kd:
            filtered = filtered[filtered['Keyword Difficulty'] <= int(kd)]
        if intent != "All":
            filtered = filtered[filtered['Intent'] == intent]
    except Exception as e:
        print("Manual Filter Error:", e)

    # Smart presets
    try:
        if preset == "High Volume, Low Difficulty (Ranking Fast)":
            filtered = filtered[(filtered['Volume'] >= 1000) & (filtered['Keyword Difficulty'] <= 20)]

        elif preset == "Zero Search Difficulty (Quick wins)":
            filtered = filtered[filtered['Keyword Difficulty'] == 0]

        elif preset == "Long-Tail with High Intent (Low comp + high conversion)":
            filtered = filtered[(filtered['Keyword'].str.count(' ') >= 3) & (filtered['Keyword Difficulty'] <= 20)]

        elif preset == "Evergreen Keywords (Consistent traffic)":
            filtered = filtered[filtered['Intent'].str.contains("Informational", case=False, na=False)]

        elif preset == "Trending Keywords (Time-sensitive boosts)":
            pass  # Requires trend data

        elif preset == "High Click-Through Rate Keywords (Attractive SERP titles)":
            pass  # CTR data needed

        elif preset == "Keywords with Featured Snippet Potential":
            filtered = filtered[filtered['Keyword'].str.startswith("how") | filtered['Keyword'].str.startswith("what")]

        elif preset == "Keywords with High CPC (Monetization potential)":
            pass  # CPC column needed

        elif preset == "Low Bounce Rate Keywords":
            pass  # Bounce rate data needed

        elif preset == "High Time-on-Page Keywords":
            pass  # Time-on-page data needed
    except Exception as e:
        print("Preset Filter Error:", e)

    update_tree(filtered)
    update_stats(filtered)

# Filter Button
tk.Button(filter_frame, text="Apply Filter", command=apply_filters).grid(row=1, column=6, padx=10)

# Initial load
update_tree(df)
update_stats(df)

# Run GUI
root.mainloop()
