class Config:
    """Uygulama genelindeki sabit ayarlar ve yapılandırmalar."""
    APP_NAME = "Universal File Workstation"
    DEFAULT_THEME = "dark"
    LANGUAGE = "tr" # languages.json ile bağlanacak

if __name__ == "__main__":
    print(f"Sistem Adı: {Config.APP_NAME}")