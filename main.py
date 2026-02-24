import customtkinter as ctk

# Diğer modülleri import etme provaları (Takım arkadaşlarına örnek göstermek için)
from config.settings import Config
from ui.dashboard import MainDashboard
from core.ai_engine import AIEngine
from core.converter import FileConverter
from core.viewer import FileViewer
from core.player import MediaPlayer

class App(ctk.CTk):
    """Projenin Başlatıcı (Main) Motoru"""
    def __init__(self):
        super().__init__()
        
        # 1. Config'den ayarları çekelim
        self.title(Config.APP_NAME)
        self.geometry("900x600")
        ctk.set_appearance_mode(Config.DEFAULT_THEME)

        # 2. Arka Plan Sınıflarını (Core Modüllerini) Başlatıyoruz
        self.ai = AIEngine()
        self.converter = FileConverter()
        self.viewer = FileViewer()
        self.player = MediaPlayer()

        # 3. Kullanıcı Arayüzünü (UI - Dashboard) Sisteme Entegre Ediyoruz
        # Master olarak 'self' (Yani bu ana pencereyi) veriyoruz ki UI bunun içine otursun.
        self.dashboard = MainDashboard(master=self)
        self.dashboard.pack(expand=True, fill="both")

        # 4. Modülleri birbirine bağlama (Mimarın Asıl Görevi)
        # Örnek: dashboard.py'da tıklandığında, converter.py çalışsın v.b.

if __name__ == "__main__":
    app = App()
    app.mainloop()
