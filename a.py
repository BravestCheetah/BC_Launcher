import customtkinter as ctk
import requests
import json
import os
import sys
from datetime import datetime

# Import functions from your script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import get_data, get_downloads_data, update_download_data, get_all_project_names, get_availble_updates, uninstall_project, save_download_data


# Create the main window
app = ctk.CTk()

# Set the window size and title
app.title("Project Manager GUI")
app.geometry("600x400")

# Frame for inputs
frame_inputs = ctk.CTkFrame(app)
frame_inputs.pack(padx=20, pady=20, fill="both", expand=True)

# Label for Command
label_command = ctk.CTkLabel(frame_inputs, text="Enter Command (e.g. new_download|mc-modmanager|1.0.1):")
label_command.pack(pady=10)

# Command input field
entry_command = ctk.CTkEntry(frame_inputs)
entry_command.pack(pady=10)

# Label for Result
label_result = ctk.CTkLabel(frame_inputs, text="Result:")
label_result.pack(pady=10)

# Result text box
text_result = ctk.CTkTextbox(frame_inputs, height=5, width=50)
text_result.pack(pady=10)

# Frame for actions (buttons)
frame_actions = ctk.CTkFrame(app)
frame_actions.pack(padx=20, pady=20, fill="both", expand=True)

# Button functions
def add_download():
    command = entry_command.get()
    result = update_download_data(command)
    text_result.delete(1.0, "end")
    text_result.insert("end", result)

def view_projects():
    projects = get_all_project_names()
    text_result.delete(1.0, "end")
    text_result.insert("end", "\n".join(projects))

def check_updates():
    updates = get_availble_updates()
    text_result.delete(1.0, "end")
    if updates:
        text_result.insert("end", f"Projects with available updates: \n{', '.join(updates)}")
    else:
        text_result.insert("end", "All projects are up-to-date!")

def uninstall():
    project_name = entry_command.get().strip()
    if project_name:
        uninstall_project(project_name)
        text_result.delete(1.0, "end")
        text_result.insert("end", f"Project {project_name} uninstalled.")
    else:
        text_result.delete(1.0, "end")
        text_result.insert("end", "Please specify the project name.")

# Buttons
button_add_download = ctk.CTkButton(frame_actions, text="Add/Update Download", command=add_download)
button_add_download.pack(pady=10)

button_view_projects = ctk.CTkButton(frame_actions, text="View All Projects", command=view_projects)
button_view_projects.pack(pady=10)

button_check_updates = ctk.CTkButton(frame_actions, text="Check Available Updates", command=check_updates)
button_check_updates.pack(pady=10)

button_uninstall = ctk.CTkButton(frame_actions, text="Uninstall Project", command=uninstall)
button_uninstall.pack(pady=10)

# Start the application
app.mainloop()
