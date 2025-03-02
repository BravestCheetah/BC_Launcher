import sys
import os

def get_main_app_path():

    main_app_path = sys.argv[0]

    if not getattr(sys, 'frozen', False):  # Running as a Python script
        main_app_path = os.path.abspath(main_app_path)

    main_app_folder = os.path.dirname(main_app_path)

    return main_app_folder

def get_downloads_folder():

    main_app_folder = get_main_app_path()

    downloads_folder = os.path.join(main_app_folder, 'downloads')

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



from app import App
app = App()
app.mainloop()