import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1100x600")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")

        tabs = customtkinter.CTkTabview(master=self)
        tabs.pack(padx=20, pady=20)

        tab_store = tabs.add("Store")
        tab_librabry = tabs.add("Library")


