import sys
import os

def get_main_app_path():
    """ Returns the absolute path to the main application (EXE or Python script) """
    # Get the path to the main script or EXE that started the application
    main_app_path = sys.argv[0]  # This will give the path to the EXE or script

    # If it's an EXE, sys.argv[0] will give the path to the EXE, so no need to change it
    # If it's a script, sys.argv[0] will give the script file, and we want the folder it resides in
    if not getattr(sys, 'frozen', False):  # It's not running as an EXE, so it's a script
        main_app_path = os.path.abspath(main_app_path)  # Absolute path to the script

    # Get the folder containing the main app (EXE or script)
    main_app_folder = os.path.dirname(main_app_path)

    # Return the absolute path to the folder containing the main app (EXE or script)
    return main_app_folder

def get_downloads_folder():
    """ Returns the absolute path to the 'downloads' folder relative to the app folder """
    main_app_folder = get_main_app_path()

    # Construct the path to the 'downloads' folder
    downloads_folder = os.path.join(main_app_folder, 'downloads')

    return downloads_folder

# Test the function
if __name__ == "__main__":
    downloads_path = get_downloads_folder()
    print(f"Downloads folder path: {downloads_path}")