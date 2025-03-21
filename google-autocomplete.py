import requests
import pandas as pd

# Function to get Google Autocomplete suggestions
def get_autocomplete_suggestions(query):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code == 200:
        suggestions = response.json()[1]  # Extract suggestions from JSON response
        return suggestions
    else:
        print("Failed to fetch suggestions.")
        return []

# Fetch autocomplete suggestions
query = "Chandni Chowk market"
suggestions = get_autocomplete_suggestions(query)

# Save results to Excel
df = pd.DataFrame(suggestions, columns=["Autocomplete Suggestions"])
df.to_excel(r"C:\\Users\\ksaur\\OneDrive\\Desktop\\chandni_chowk_autocomplete.xlsx", index=False)

print("Autocomplete suggestions saved to C:\\Users\\ksaur\\OneDrive\\Desktop\\chandni_chowk_autocomplete.xlsx")
