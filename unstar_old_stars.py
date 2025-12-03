import requests
import json
import time
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
GITHUB_USERNAME = "your_github_username"
# PASTE YOUR NEW CLASSIC TOKEN (starts with ghp_) BELOW:
GITHUB_TOKEN = "your_personal_access_token" 
INPUT_FILE = "starred_with_dates.json"
# ---------------------

def unstar_repository(owner, repo, token):
    url = f"https://api.github.com/user/starred/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print(f"Successfully Unstarred: {owner}/{repo}")
    else:
        # Try to get error message
        try:
            error_msg = response.json().get('message', '')
        except:
            error_msg = response.text
        print(f"FAILED: {response.status_code} - {error_msg}")

# 1. Load the data
try:
    with open(INPUT_FILE, "r") as f:
        starred_data = json.load(f)
except FileNotFoundError:
    print(f"Error: '{INPUT_FILE}' not found. Please run the export script first.")
    exit()

# 2. Set the cutoff date
current_date = datetime.now(timezone.utc)
cutoff_date = current_date - timedelta(days=365) # 1 Year

print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")
print(f"Cutoff Date:  {cutoff_date.strftime('%Y-%m-%d')}")
print("-" * 30)

# 3. Filter repositories to delete
repos_to_delete = []

for item in starred_data:
    starred_at_str = item['starred_at']
    # Handle ISO format
    starred_at_dt = datetime.fromisoformat(starred_at_str.replace("Z", "+00:00"))

    if starred_at_dt < cutoff_date:
        repos_to_delete.append(item)

# 4. Confirmation and Execution
if len(repos_to_delete) == 0:
    print("No repositories found older than 1 year.")
    exit()

print(f"Found {len(repos_to_delete)} repositories older than 1 year.")
confirm = input(f"Are you sure you want to unstar these {len(repos_to_delete)} repos? (yes/no): ")

if confirm.lower() == "yes":
    total = len(repos_to_delete)
    
    # Enumerate gives us a counter (i) starting at 1
    for i, item in enumerate(repos_to_delete, 1):
        owner = item['repo']['owner']['login']
        repo_name = item['repo']['name']
        
        # Print the counter, stay on the same line
        print(f"[{i}/{total}] ", end="")
        
        unstar_repository(owner, repo_name, GITHUB_TOKEN)
        
        # Sleep to avoid hitting API rate limits
        # time.sleep(0.5)
        
    print("\nProcess complete.")
else:
    print("Operation cancelled.")