import requests
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import downloads_folder

def get_path(relative_path):
    # Get the correct path, even when running as an EXE
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def update_data():
    ignore_ids = [933743812, 752225491]
    base_url = "https://api.github.com"

    try:
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
            continue

        releases_url = f"{base_url}/repos/{repo['owner']['login']}/{repo['name']}/releases"
        try:
            release_response = requests.get(releases_url, timeout=10)
            release_response.raise_for_status()
            releases = release_response.json()
        except requests.RequestException:
            releases = []

        releases_data = []
        for release in releases:
            if release.get("draft", False):
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

        filtered_repos.append({
            "owner": repo["owner"]["login"],
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "repo_url": repo["html_url"],
            "default_download_url": f"https://github.com/{repo['owner']['login']}/{repo['name']}/archive/refs/heads/{repo['default_branch']}.zip",
            "releases": releases_data
        })

    os.makedirs(get_path("data"), exist_ok=True)
    data_path = os.path.join(get_path("data"), "data.json")

    with open(data_path, "w") as f:
        json.dump(filtered_repos, f, indent=4)

    print(f"Filtered data saved to {data_path}")


def get_data(project_name, query):
    os.makedirs(get_path("data"), exist_ok=True)
    data_path = os.path.join(get_path("data"), "data.json")

    with open(data_path, "r") as f:
        data = json.load(f)

    for repo in data:
        if repo["name"].lower() == project_name.lower():
            keys = query.split("|")
            data = repo

            for key in keys:
                if key == "latest" and isinstance(data, list):  
                    data = data[0] if data else None
                elif key.isdigit() and isinstance(data, list):  
                    index = int(key)
                    data = data[index] if 0 <= index < len(data) else None
                elif isinstance(data, list) and all(isinstance(item, dict) and key in item for item in data):
                    data = [item[key] for item in data]
                else:
                    data = data.get(key) if isinstance(data, dict) else None

                if data is None:
                    return f"'{query}' not found."

            return data
    return f"Project '{project_name}' not found."

def get_size(size):
    size_kb = size/1024
    size_mb = size_kb/1024
    if size_mb < 1:
        return f"{round(size_kb)} KB"
    size_gb = size_mb/1024
    if size_gb < 1:
        return f"{round(size_mb)} MB"
    return f"{round(size_gb)} GB"

def download_file(url, filename, dest, progress_bar, window):

    response = requests.get(url, stream=True)
    response.raise_for_status()
    file_size = int(response.headers.get("Content-Length", 0))  # Get the total file size

    with open(os.path.join(dest, filename), "wb") as file:
        progress_bar.set(0)
        downloaded_size = 0

        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded_size += len(chunk)
            progress_bar.set(downloaded_size / file_size)  # Update the progress bar
            window.update_idletasks()

    return "Download Complete!"

def download_project(project_name, project_version, progress_bar, progress_label, window):
    print(f"Starting download for project: {project_name}, version: {project_version}")
    
    download_urls = get_data(project_name, f"releases|{project_version}|assets|download_url")
    download_names = get_data(project_name, f"releases|{project_version}|assets|name")
    
    print(f"Found {len(download_urls)} files to download.")

    os.makedirs(os.path.join(downloads_folder, project_name), exist_ok=True)
    
    item_num = 1
    progress_label.configure(text=f"{item_num} / {len(download_urls)}")
    
    for i in range(len(download_urls)):
        print(f"Downloading file {i + 1}: {download_names[i]} from {download_urls[i]}")
        
        download_file(download_urls[i], download_names[i], os.path.join(downloads_folder, project_name), progress_bar, window)
        
        item_num = i + 1
        progress_label.configure(text=f"{item_num} / {len(download_urls)}")
        window.update_idletasks()

        print(f"Downloaded {download_names[i]} successfully.")
    
    print("Download complete.")
    return "Download Complete!"

import json
import os


downloads_data_path = os.path.join(os.path.dirname(__file__), "data", "downloads.json")


def read_download_data():
    if os.path.exists(downloads_data_path):
        with open(downloads_data_path, "r") as f:
            return json.load(f)
    return {}

def save_download_data(data):
    with open(downloads_data_path, "w") as f:
        json.dump(data, f, indent=4)


def update_download_data(command):

    parts = command.split("|")
    if len(parts) < 2:
        return "Invalid command format."

    action = parts[0].lower()
    project_name = parts[1].lower()

    downloads_data = read_download_data()

    if action == "new_download":
        if len(parts) < 3:
            return "Version is required for new download."

        version = parts[2]

        downloads_data[project_name] = {
            "version": version,
        }
        save_download_data(downloads_data)
        return f"Added new download: {project_name}, version: {version}"

    elif action == "update":
        if len(parts) < 3:
            return "Version is required for updating download."

        version = parts[2]
        if project_name in downloads_data:
            downloads_data[project_name]["version"] = version
            save_download_data(downloads_data)
            return f"Updated download: {project_name}, version: {version}"
        else:
            return f"Project {project_name} not found in downloads."

    elif action == "delete":
        if project_name in downloads_data:
            del downloads_data[project_name]
            save_download_data(downloads_data)
            return f"Deleted download: {project_name}"
        else:
            return f"Project {project_name} not found in downloads."

    return "Invalid action."

def get_all_project_names():

    os.makedirs(get_path("data"), exist_ok=True)
    data_path = os.path.join(get_path("data"), "downloads.json")

    with open(data_path, "r") as f:
        data = json.load(f)

    return list(data.keys())

def get_downloads_data(project_name, query):

    os.makedirs(get_path("data"), exist_ok=True)
    data_path = os.path.join(get_path("data"), "downloads.json")

    with open(data_path, "r") as f:
        data = json.load(f)

    if project_name in data:
        project_data = data[project_name]

        keys = query.split("|")
        result = project_data

        for key in keys:
            if key in result:
                result = result[key]
            else:
                return f"'{key}' not found in the data for project '{project_name}'."

        return result
    else:
        return f"Project '{project_name}' not found."

def get_availble_updates():

    projects = get_all_project_names()
    not_up_to_date_projects = []

    for project in projects:
        latest_project_version = get_data(project, "releases|latest|version")
        latest_downloaded_project_version = get_downloads_data(project, "version")

        if latest_downloaded_project_version != latest_project_version:
            not_up_to_date_projects.append(project)
    
    return not_up_to_date_projects

def uninstall_project(project_name):
    project_directory = os.path.join(downloads_folder, project_name)
    os.rmdir(project_directory)
