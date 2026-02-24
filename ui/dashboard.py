import customtkinter as ctk

class MainDashboard(ctk.CTkFrame):
    """Uygulamanın ana ekran yerleşimini içeren frame."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Buraya butonlar, sidebar ve içerik alanı tasarlanacak
        self.label = ctk.CTkLabel(self, text="Dashboard Yüklendi", font=("Arial", 20))
        self.label.pack(pady=20)

if __name__ == "__main__":
    # Tek başına çalıştırınca boş bir pencerede dashboard'u görsün diye
    root = ctk.CTk()
    root.geometry("400x300")
    dash = MainDashboard(root)
    dash.pack(expand=True, fill="both")
    root.mainloop()