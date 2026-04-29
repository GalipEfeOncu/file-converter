# Build & Paketi Oluşturma (PyInstaller)

Bu döküman, Universal File Workstation projesinin bağımsız çalışabilir bir Windows executable (.exe) haline getirilmesi adımlarını ve güvenlik yazılımlarıyla ilgili uyarıları içerir.

## 1. Hazırlık ve Gereksinimler
- Python ortamınızda `requirements.txt` içindeki tüm bağımlılıkların yüklü olduğundan emin olun.
- PyInstaller'ın kurulu olması gereklidir: `pip install pyinstaller`
- Proje kök dizininde komut satırını açın.

## 2. Derleme (Build) İşlemi
`build/universal-file-workstation.spec` dosyası, uygulamanın çalışması için gereken tüm klasörleri (`assets`, `config`, `core`, `ui`) ve Streamlit gibi özel kütüphanelerin `hiddenimports` ayarlarını içerir.

Derlemeyi başlatmak için şu komutu çalıştırın:
```bash
pyinstaller build/universal-file-workstation.spec
```

İşlem tamamlandığında `dist/` klasörü içerisinde uygulamanın çalıştırılabilir dosyası oluşturulacaktır. Başlatıcı olarak kodlanan `launcher.py` sayesinde, uygulama bu exe üzerinden çalıştırıldığında Streamlit sunucusunu arka planda başlatacak ve varsayılan tarayıcıda kullanıcı arayüzünü açacaktır.

## 3. Windows Defender ve Antivirüs Notları (False-Positive)
PyInstaller kullanılarak paketlenen Python uygulamaları, zaman zaman Windows Defender veya diğer üçüncü parti güvenlik yazılımları tarafından şüpheli (false-positive) olarak algılanabilir ve silinebilir. 

Bu durumu yönetmek için aşağıdaki yöntemleri uygulayabilirsiniz:

- **Çalıştırma Parametreleri:** Build işlemi sırasında yetki sorunlarını aşmak ve uyarıları kısmak için `--noconfirm --uac-admin` bayrakları kullanılabilir veya PyInstaller özellikleri spec dosyasında `uac_admin=True` olarak yapılandırılabilir.
- **Sertifikasyon (Code Signing):** En güvenilir yöntem, oluşturulan `.exe` dosyasının geçerli bir geliştirici sertifikası (Code Signing Certificate) ile imzalanmasıdır.
- **Dışlama (Exclusion):** Geliştirme ve test aşamalarında, uygulamanın bulunduğu dizini (`dist/` veya `.exe` dosyasını) Windows Defender dışlamalarına (exclusions) ekleyerek engellemeleri aşabilirsiniz.

## FFmpeg Bundling

### Windows (Sprint 5 scope)
`python scripts/download_ffmpeg.py` komutu FFmpeg LGPL static build'i
`assets/bin/ffmpeg.exe` altına indirir. Binary git'e commit edilmez.

### Linux / macOS (Sprint 6 scope)
Sistem package manager üzerinden kurulum önerilir:
- Ubuntu/Debian: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
Aynı path resolver stratejisi ilerleyen sprintte uygulanacak.
