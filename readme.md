# GitHub Star Cleaner

A set of Python scripts to manage your GitHub starred repositories. It allows you to export your stars with timestamps and bulk-remove stars that are older than a specific timeframe (default: 1 year).

Use this to declutter your profile while keeping your recent interests visible.

## Disclaimer

This script permanently removes starred repositories from your GitHub profile. **Always ensure `starred_with_dates.json` is generated correctly before running the deletion script.** Use at your own risk.


## Features

- **Export Stars:** backup all your starred repositories to a JSON file, including the date you starred them.
- **Date Filtering:** Automatically identifies repositories starred more than your specified number of days ago.
- **Bulk Unstar:** Removes stars via the GitHub API with a progress indicator.
- **Safety First:** Includes confirmation prompts and backup files to prevent accidental deletion.

## Prerequisites

- Python 3.x
- A GitHub Account
- A **Classic** Personal Access Token (PAT)  
   - A Fine-grained personal access tokens will work only for the export, but not for the deletion

## Setup

1. **Install Dependencies:**
   This project uses the `requests` library.
   ```bash
   pip install requests
   ```

2. **Generate a GitHub Token:**
   * Go to [GitHub Settings > Developer settings > Personal access tokens (classic)](https://github.com/settings/tokens).
   * Click **Generate new token (classic)**.
   * **Scopes:** Check `public_repo` (and `repo` if you want to include private repositories).
   * Copy the token (starts with `ghp_`).

3. **Configure the Scripts:**
   Open `export_stars.py` and `unstar_old_stars.py` and replace the placeholders:
   ```python
   GITHUB_USERNAME = "your_username"
   GITHUB_TOKEN = "ghp_your_token_here"
   ```

## Usage

### Step 1: Export Your Stars
Run the export script to fetch your stars and their timestamps. This serves as your backup.

```bash
python3 export_stars.py
```
*Output: `starred_with_dates.json`*

### Step 2: Unstar Old Repositories
Run the cleaning script. It will read the JSON file, calculate which stars are older than a specified number of days, and ask for confirmation before deleting anything.

```bash
python3 unstar_old_stars.py
```

## How it Works

1. **`export_stars.py`**: Uses the `application/vnd.github.star+json` header to retrieve the specific `starred_at` timestamp for every repository.
2. **`unstar_old_stars.py`**: 
   - Loads the JSON data.
   - Compares the `starred_at` date against the current date minus set number of days.
   - Iterates through the old repositories and sends `DELETE` requests to the GitHub API.
   - Includes an optional `0.5s` delay between requests to avoid API rate limiting.
