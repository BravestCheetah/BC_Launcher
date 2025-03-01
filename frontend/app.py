import customtkinter

repos = ["CheetahsExtendedSurvival", "Cool", "test"]
downloaded_products = []  # List of downloaded products

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1100x600")
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")

        # Create Tabs
        self.tabs = customtkinter.CTkTabview(master=self)
        self.tabs.pack(padx=20, pady=20)

        self.tab_store = self.tabs.add("Store")
        self.tab_library = self.tabs.add("Library")
        self.tab_product = self.tabs.add("Product")

        # Store product buttons
        for product in repos:
            repo_button = customtkinter.CTkButton(self.tab_store, text=product, 
                                                  command=lambda r=product: self.open_repo_page(r))
            repo_button.pack(pady=2)

        # Create a frame inside the library tab to hold buttons
        self.library_frame = customtkinter.CTkFrame(self.tab_library)
        self.library_frame.pack(fill="both", expand=True)

    def open_repo_page(self, product_name):
        """Simulates downloading a product and adds it to the Library."""
        if product_name not in downloaded_products:  # Prevent duplicates
            downloaded_products.append(product_name)
            self.update_library()  # Update the library UI

    def update_library(self):
        """Refreshes the Library tab to display newly downloaded products."""
        # Clear previous buttons
        for widget in self.library_frame.winfo_children():
            widget.destroy()

        # Create new buttons for downloaded products
        for product in downloaded_products:
            repo_button = customtkinter.CTkButton(self.library_frame, text=product, 
                                                  command=lambda r=product: self.launch_repo(r))
            repo_button.pack(pady=2)

    def launch_repo(self, product_name):
        """Handles launching a downloaded product."""
        print(f"Launching {product_name}...")

# Run the App
if __name__ == "__main__":
    app = App()
    app.mainloop()
