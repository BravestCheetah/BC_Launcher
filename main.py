import sys
import os

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