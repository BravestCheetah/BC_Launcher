import tkinter as tk
import customtkinter as ctk
from backend import download_project  # Assuming the function is in backend.py

def test_download():
    # Default values for the test
    project_name = "Mc-ModManager"
    project_version = "latest"

    # Create the main window
    window = ctk.CTk()
    window.title("Download Test")
    window.geometry("400x200")
    
    # Create a progress bar
    progress_bar = ctk.CTkProgressBar(window, width=300)
    progress_bar.pack(pady=20)
    
    # Create a label to show the progress
    progress_label = ctk.CTkLabel(window, text="Waiting for download to start...")
    progress_label.pack(pady=10)

    # Add a button to trigger the download
    def on_download_button_click():
        print(f"Starting download for {project_name}, version {project_version}")
        result = download_project(project_name, project_version, progress_bar, progress_label, window)
        print(result)
    
    download_button = ctk.CTkButton(window, text="Start Download", command=on_download_button_click)
    download_button.pack(pady=10)
    
    window.mainloop()

# Call the test function to run the GUI
test_download()
