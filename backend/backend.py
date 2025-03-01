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

def update_data():
    ignore_ids = [933743812, 752225491]
    base_url = "https://api.github.com"

    try:
        # Fetch user repositories
        repo_url = f"{base_url}/users/BravestCheetah/repos"
        response = requests.get(repo_url, timeout=10)
        response.raise_for_status()
        repos = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    if isinstance(repos, dict) and "message" in repos:
        print(f"GitHub API Error: {repos['message']}")
        sys.exit(1)

    filtered_repos = []

    for repo in repos:
        if repo["id"] in ignore_ids:
            continue  # Skip ignored repositories

        # Fetch releases
        releases_url = f"{base_url}/repos/{repo['owner']['login']}/{repo['name']}/releases"
        try:
            release_response = requests.get(releases_url, timeout=10)
            release_response.raise_for_status()
            releases = release_response.json()
        except requests.RequestException:
            releases = []

        # Extract release data including assets
        releases_data = []
        for release in releases:
            if release.get("draft", False):  # Ignore draft releases
                continue

            assets = [
                {
                    "name": asset["name"],
                    "download_url": asset["browser_download_url"],
                    "size": asset["size"]
                }
                for asset in release.get("assets", [])
            ]

            releases_data.append({
                "version": release["tag_name"],
                "release_url": release["html_url"],
                "zip_download_url": release.get("zipball_url", "No zip available"),
                "pre_release": release.get("prerelease", False),
                "assets": assets  # Include downloadable files
            })

        # Add repo info
        filtered_repos.append({
            "owner": repo["owner"]["login"],
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "repo_url": repo["html_url"],
            "default_download_url": f"https://github.com/{repo['owner']['login']}/{repo['name']}/archive/refs/heads/{repo['default_branch']}.zip",
            "releases": releases_data  # Full release info with assets
        })

    # Ensure the data directory exists
    os.makedirs(get_path("data"), exist_ok=True)
    data_path = os.path.join(get_path("data"), "data.json")

    with open(data_path, "w") as f:
        json.dump(filtered_repos, f, indent=4)

    print(f"Filtered data saved to {data_path}")

update_data()
