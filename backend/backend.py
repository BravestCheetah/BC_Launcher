import requests
import os
import json
import sys

def get_path(relative_path):
    """ Get the correct path, even when running as an EXE """
    if getattr(sys, 'frozen', False):  # If running as an EXE
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ignore_ids = [933743812, 752225491]
url = "https://api.github.com/users/BravestCheetah/repos"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    repos = response.json()
except requests.RequestException as e:
    print(f"Request failed: {e}")
    sys.exit(1)

if isinstance(repos, dict) and "message" in repos:
    print(f"GitHub API Error: {repos['message']}")
    sys.exit(1)

# Filter the repositories to only include necessary fields
filtered_repos = [
    {
        "owner": repo["owner"]["login"],
        "name": repo["name"],
        "description": repo["description"],
        "language": repo["language"],
        "repo_url": repo["html_url"],  # Main repo page
        "download_url": f"https://github.com/{repo['owner']['login']}/{repo['name']}/archive/refs/heads/{repo['default_branch']}.zip"
    }
    for repo in repos if repo['id'] not in ignore_ids
]

# Ensure the data directory exists
os.makedirs(get_path("data"), exist_ok=True)
data_path = os.path.join(get_path("data"), "data.json")

with open(data_path, "w") as f:
    json.dump(filtered_repos, f, indent=4)

print(f"Filtered data saved to {data_path}")
