class FileConverter:
    def convert_pdf_to_docx(self, input_path):
        """PDF'den Word'e dönüştürme mantığı"""
        pass

    def convert_csv_to_xlsx(self, input_path):
        """CSV'den Excel'e dönüştürme mantığı"""
        pass

# BU KISIM TEST ALANIDIR
if __name__ == "__main__":
    # Bu kodlar sadece converter.py çalıştırıldığında devreye girer.
    # main.py içinden çağrıldığında burası YOK sayılır.
    c = FileConverter()
    print("Converter testi yapılıyor...")