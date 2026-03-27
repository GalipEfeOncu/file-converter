import os
import pandas as pd
from core.converter import FileConverter
from core.player import AudioConverter

def run_tests():
    print("--- ÇEKİRDEK (CORE) MODÜL TESTLERİ BAŞLIYOR ---\n")
    
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # 1. CSV to Excel 
    print("Test 1: CSV -> Excel Dönüşümü")
    test_csv_path = "temp/test_veri.csv"
    test_xlsx_path = "temp/test_sonuc.xlsx"
    
    df = pd.DataFrame({"Ad": ["Ahmet", "Said", "Berkay"], "Puan": [100, 95, 90]})
    df.to_csv(test_csv_path, index=False)
    
    converter = FileConverter()
    basarili_mi = converter.convert_csv_to_xlsx(test_csv_path, test_xlsx_path)
    
    if basarili_mi and os.path.exists(test_xlsx_path):
        print("✅ BAŞARILI: CSV dosyası Excel'e dönüştürüldü!\n")
    else:
        print("❌ BAŞARISIZ: CSV -> Excel dönüşümünde hata!\n")

    print("Test 2: Olmayan Dosyada Çökme Kontrolü (Exception Handling)")
    basarili_mi_hata = converter.convert_pdf_to_docx("temp/olmayan_dosya.pdf", "temp/sonuc.docx")
    
    if not basarili_mi_hata:
        print("✅ BAŞARILI: Sistem çökmeyi engelledi ve düzgünce False döndürdü!\n")
    else:
        print("❌ BAŞARISIZ: Sistem hatayı yakalayamadı!\n")

if __name__ == "__main__":
    run_tests()