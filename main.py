import sys
import os

def get_downloads_folder():
    # Return the absolute path to the 'downloads' folder
    base_path = os.path.abspath('.')  # Gets the current working directory
    downloads_folder = os.path.join(base_path, 'downloads')

    return downloads_folder



#Gets full path to relative folder to prevent errors when compiling to an .exe
def get_path(relative_path):
    """ Get the correct path, even when running as an EXE """
    if getattr(sys, 'frozen', False):  # If running as an EXE
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#adds both backend and frontend folders manually to not create errors when importing modules
backend_path = get_path("backend")
sys.path.append(backend_path)

frontend_path = get_path("frontend")
sys.path.append(frontend_path)


downloads_folder = get_downloads_folder()