import os
from PIL import Image
from core.converter import FileConverter
from core.player import AudioConverter

print("🚀 TEST BAŞLIYOR...\n")

# --- 1. SES VE FFMPEG TESTİ ---
print("--- 1. SES SİSTEMİ (FFMPEG) TESTİ ---")
player = AudioConverter()
print(f"Sistemde FFmpeg bulundu mu?: {player.ffmpeg_available}\n")

# --- 2. GÖRSEL DÖNÜŞÜM TESTİ ---
print("--- 2. GÖRSEL DÖNÜŞÜM TESTİ ---")
converter = FileConverter()

# Test için geçici, yarı şeffaf bir PNG dosyası oluşturuyoruz (RGBA hatasını test etmek için)
dummy_png = "test_gecici.png"
dummy_jpg = "test_sonuc.jpg"

print("Geçici test görseli (PNG) oluşturuluyor...")
img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
img.save(dummy_png)

# Senin yazdığın fonksiyonu çağırıyoruz!
print("Senin fonksiyonunla PNG -> JPG dönüşümü deneniyor...")
sonuc = converter.convert_image(dummy_png, dummy_jpg, "jpg", quality=50)

print(f"Dönüşüm Başarılı mı?: {sonuc}")

# Ortalığı temizleyelim (Test dosyalarını silelim)
if os.path.exists(dummy_png):
    os.remove(dummy_png)
if os.path.exists(dummy_jpg):
    os.remove(dummy_jpg)
    
print("\n✅ TEST TAMAMLANDI.")