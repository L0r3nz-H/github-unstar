import requests
import json

# --- CONFIGURATION ---
GITHUB_USERNAME = "your_github_username"
GITHUB_TOKEN = "your_personal_access_token"
# ---------------------

starred_data = []
page = 1

print("Exporting stars with timestamps...")

while True:
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/starred?per_page=100&page={page}"
    # This specific header is REQUIRED to get the 'starred_at' timestamp
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.star+json" 
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    data = response.json()
    if not data:
        break

    starred_data.extend(data)
    print(f"Page {page} done...")
    page += 1

# Save to a new file
with open("starred_with_dates.json", "w") as f:
    json.dump(starred_data, f, indent=4)

print(f"Exported {len(starred_data)} entries to starred_with_dates.json")