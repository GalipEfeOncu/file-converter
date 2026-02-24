import customtkinter as ctk       # Gelişmiş, modern ve karanlık/aydınlık tema destekli arayüzler(GUI) oluşturmak için kullandığımız kütüphane.
from PIL import Image             # (Python Imaging Library - Pillow) Resim dosyalarını işlemek, açmak ve dönüştürmek için kullanılır.
import tkinter as tk              # Python'ın standart masaüstü arayüz kütüphanesidir. (CustomTkinter bunun üzerine inşa edilmiştir.)
from tkinter import filedialog, messagebox # filedialog: Dosya seçme penceresi açar. messagebox: Uyarı/Hata/Bilgi mesajı pencereleri gösterir.
import os                         # İşletim sistemiyle etkileşime girer. (Dosya yollarını bulma, uzantıları ayırma, varsayılan programı açma vb. için)
import pandas as pd               # Tablosal verileri (CSV, Excel vb.) okumak, işlemek ve dönüştürmek için veri analizi kütüphanesi.
import PyPDF2                     # PDF dosyalarından veri okumak ve metin çıkarmak için kullanılan kütüphane.
import fitz                       # PyMuPDF: PDF dosyalarını yüksek kaliteli resim(görsel) formatında render etmek(sayfa sayfa çizmek) için kullanılır.
from docx import Document         # Microsoft Word (.docx) belgelerini okuyup içindeki paragrafları/metinleri almak için kullanılır.

# Arayüzün genel görünümünü ayarlıyoruz
ctk.set_appearance_mode("System")  # Uygulamanın temasını, işletim sisteminin mevcut temasına (Karanlık veya Aydınlık) uydurur.
ctk.set_default_color_theme("blue")# Butonlar, yazılar vb. widget'ların temel renk vurgusunu belirler. (Mavi tema kullanıyoruz)

# Uygulamamızın ana pencerisini temsil eden Sınıfımız (Class)
class App(ctk.CTk):
    def __init__(self):
        # Üst sınıf olan ctk.CTk'nin (Temel Pencere yeteneklerinin) çalıştırılmasını ve miras alınmasını sağlar.
        super().__init__()

        self.title("Modern File Converter & Reader") # Pencerenin en üstündeki başlık yazısı.
        self.geometry("800x600")                     # Pencerenin açılıştaki varsayılan en/boy pikselleri (800x600 piksellik bir boyut).
        
        # Ekranın düzeni (Grid Layout): Satır ve sütunlara ayrılan yapılandırılabilir alanlar yaratırız.
        # Sol taraf menü, sağ taraf ise asıl içeriğin olduğu alan olacak.
        self.grid_rowconfigure(0, weight=1)    # 0. satırın dikey(y) eksende büyümesine izin verir (weight=1).
        self.grid_columnconfigure(1, weight=1) # 1. sütunun yatay(x) eksende pencere büyüdükçe esnemesine izin verir. 0. sütunda yan menü olacak.

        # Bellekte tutulması için değişkenlerin (State) başlatılması:
        self.reader_file_path = None     # Okunacak dosyanın tam dosya yolunu tutar. (Örn: C:/Belgeler/veri.pdf)
        self.converter_file_path = None  # Dönüştürülecek dosyanın tam dosya yolunu tutar.
        
        # Tam Ekran kontrol değişkeni
        self.is_fullscreen = False       # PDF Görüntüleyicimizde tam ekran modunu takip eder.
        
        # PDF okuyucu özelliği için gerekli olan durumu (State) saklayan değişkenler:
        self.current_zoom = 1.0          # Mevcut yakınlaştırma oranı. (1.0 = %100 boyut)
        self.pdf_image_labels = []       # PDF içindeki, ekrana basılan sayfaların CTkLabel (Resim Taşıyıcısı) objelerinin listesi.
        self.base_pdf_images = []        # Görüntü bozulumunu engellemek için, ekran boyutu ne olursa olsun asıl resmi ve orijinal ebatlarını tuttuğumuz liste.

        # Klavye ve Mouse (Fare) Kısayolları İçin Event Tanımlamaları:
        # ctrl + mouse tekerleği kombinasyonunu algıladığımızda uygulamadaki "on_ctrl_scroll" fonksiyonunu tetikler.
        self.bind_all("<Control-MouseWheel>", self.on_ctrl_scroll) # Windows ve macOS için standart tekerlek etkinliği.
        self.bind_all("<Control-Button-4>", self.on_ctrl_scroll)   # Linux sistemlerde tekerleğin yukarı çevrilmesi tetikleyicisi (zoom in).
        self.bind_all("<Control-Button-5>", self.on_ctrl_scroll)   # Linux sistemlerde tekerleğin aşağı çevrilmesi tetikleyicisi (zoom out).

        # Arayüzü oluşturduğumuz yardımcı fonksiyonlarımızı (metodlarımızı) başlatıyoruz.
        self.create_sidebar()           # Sol yan menüyü (butonlar) oluşturur.
        self.create_reader_frame()      # Dosya Okuma sayfasının (içeriğinin) tasarımını oluşturur.
        self.create_converter_frame()   # Dosya Dönüştürme sayfasının (içeriğinin) tasarımını oluşturur.
        
        # Program çalıştığında varsayılan(ilk) olarak hangi sayfanın açık kalacağını belirleriz.
        self.show_frame("reader") # "reader" yani File Reader sayfası ilk açılan ekran olur.

    # ---------------------------------------------------------
    # UI TASARIM FONKSİYONLARI 
    # ---------------------------------------------------------
    def create_sidebar(self):
        """Uygulamanın solundaki navigasyon (menü) panelini tasarlayan metod."""
        # Sol taraf için bir kasa (frame) oluştururuz.
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew") # grid, öğeyi satır(row) ve sütuna(col) yerleştirir. "nsew": kuzey, güney, doğu, batı'ya yaslansın (pürüzsüz kaplasın).
        self.sidebar_frame.grid_rowconfigure(3, weight=1)       # Butonlar arasındaki boşluğu yönetmek için 3. satırı esnek hale getirir. 

        # Logo veya Başlık Metni
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="File Tools", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # "File Reader" Butonu
        self.reader_button = ctk.CTkButton(self.sidebar_frame, text="📖 File Reader",
                                           command=lambda: self.show_frame("reader")) # Tıklandığında show_frame("reader") fonksiyonunu çalıştırır.
        self.reader_button.grid(row=1, column=0, padx=20, pady=10)

        # "File Converter" Butonu
        self.converter_button = ctk.CTkButton(self.sidebar_frame, text="🔄 File Converter",
                                              command=lambda: self.show_frame("converter")) # Tıklandığında show_frame("converter") fonksiyonunu çalıştırır.
        self.converter_button.grid(row=2, column=0, padx=20, pady=10)

        # Görünüm (Aydınlık/Karanlık) Tema seçimi için açılır menü (Dropdown)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20))
        # Açılışta varsayılan olarak seçili gözükecek değeri "System" yapıyoruz, aksi halde sadece ilk değer ("Light") yazar.
        self.appearance_mode_optionemenu.set("System")

    def create_reader_frame(self):
        """Dosya Okuma ekranını (orta/sağ alan) tasarlayan metod."""
        self.reader_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.reader_frame.grid_rowconfigure(2, weight=1)      # 2. satır (görüntü alanı) ekranı kaplayacak şekilde genişlesin.
        self.reader_frame.grid_columnconfigure(0, weight=1)   # Yatayda da tüm genişliği alsın.

        # Başlık ve Dosya Seç butonu hizalamaları
        self.reader_title = ctk.CTkLabel(self.reader_frame, text="File Reader", font=ctk.CTkFont(size=24, weight="bold"))
        self.reader_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Gelişmiş Araç Çubuğu (Toolbar): İçinde zoom, fit width ve dosya seç butonu var.
        self.reader_toolbar = ctk.CTkFrame(self.reader_frame, fg_color="transparent")
        self.reader_toolbar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Okuyucu Ekranı Butonları
        self.reader_select_btn = ctk.CTkButton(self.reader_toolbar, text="Select File to Read", command=self.select_file_reader)
        self.reader_select_btn.pack(side="left", padx=(0, 10))

        # Yakınlaştırma butonlarını buradan çıkardık çünkü sağ alta yüzen(floating) buton olarak alınması istendi.
        
        # Kullanıcının hoşuna giden sayfa sığdırma(Fit Width) butonu yerinde bırakıldı
        self.fit_width_btn = ctk.CTkButton(self.reader_toolbar, text="Fit Width", command=self.fit_width)
        self.fit_width_btn.pack(side="left", padx=10)

        # Okuyucu içindeki Görüntüleme Alanı: (Örn: Birden fazla PDF sayfasını göstereceğimiz için aşağı kaydırılabilecek olan alan)
        # Sadece dikey değil, YATAY (Sağa Sola) da kaydırma yapabilmek için CustomTkinter'in basit scrollable yapısı yerine 
        # Python'un asıl güçlü aracı olan Canvas'ı (Çizim Tabağını) ve ona bağlı bağımsız iki kaydırma çubuğunu(Scrollbar) kendimiz inşa ediyoruz.
        self.reader_display_container = ctk.CTkFrame(self.reader_frame, fg_color="transparent")
        self.reader_display_container.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # İçindeki tabağın (Canvas) esnemesi için ağırlıkları %100 veriyoruz
        self.reader_display_container.grid_rowconfigure(0, weight=1)
        self.reader_display_container.grid_columnconfigure(0, weight=1)

        # 1. Asıl PDF resimlerini veya metin kutularını çizeceğimiz, x ve y yönünde kayabilen Canvas (Tuval)
        self.canvas = tk.Canvas(self.reader_display_container, bg="#2b2b2b", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # 2. Dikey (Yukarı-Aşağı) Kaydırma Çubuğu (CTkScrollbar)
        self.v_scrollbar = ctk.CTkScrollbar(self.reader_display_container, orientation="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        # 3. Yatay (Sağa-Sola) Kaydırma Çubuğu (CTkScrollbar)
        self.h_scrollbar = ctk.CTkScrollbar(self.reader_display_container, orientation="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Tuvalin (Canvas) kaydırıcıları tanıması için geri yapılandırma
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # 4. Canvas içine resim yükleyebilmek için ona bir Pencere (Frame) gömüyoruz.
        # Böylece resimler Canvas'ın üzerinde değil, bu şeffaf çerçevenin üstünde duracak, Canvas bu çerçeveyi kaydıracak.
        self.reader_display_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        
        # Ekrandaki resimleri tutacak çerçevenin (reader_display_frame) ID'sini bir değişkene kaydettik
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.reader_display_frame, anchor="nw")

        # Çerçevede (Frame) boyutsal bir büyüme vs olduğunda, Canvas'ın Tuval sınırlarını(ScrollBox) hemen güncellemesini söyleyen tetikleyici!
        self.reader_display_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Mouse'un tekerleğini Canvas üzerinde dikey ve yatay kaydırma(Scroll) yapması için bağlıyoruz:
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

        # --- YÜZEN (FLOATING) BUTONLAR ---
        # Yakınlaştırma ve uzaklaştırma için PDF okuyucusunun sağ alt köşesine konumlandırılan yarı saydam(koyu renkli) butonlar
        self.zoom_out_btn = ctk.CTkButton(self.reader_frame, text="-", width=40, height=40, corner_radius=8, fg_color="#1f1f1f", hover_color="#333333", text_color="white", font=ctk.CTkFont(size=20), command=self.zoom_out)
        # place ile grid sistemini yoksayıp serbestçe konumlandırırız. x=-85 piksel içeri çek demek (sağdan 85, alttan 40)
        self.zoom_out_btn.place(relx=1.0, rely=1.0, x=-85, y=-40, anchor="se") 

        self.zoom_in_btn = ctk.CTkButton(self.reader_frame, text="+", width=40, height=40, corner_radius=8, fg_color="#1f1f1f", hover_color="#333333", text_color="white", font=ctk.CTkFont(size=20), command=self.zoom_in)
        # Sağdan 40, aşağıdan 40 piksel içeriye (+ butonunu -'nin sağına) çivilendi
        self.zoom_in_btn.place(relx=1.0, rely=1.0, x=-40, y=-40, anchor="se")

        # Tam Ekran Modu (Fullscreen) butonu, PDF'i ekranı kaplayacak şekilde UI gizlemek için (Sağ Üstte)
        self.fullscreen_btn = ctk.CTkButton(self.reader_frame, text="⛶", width=40, height=40, corner_radius=8, fg_color="#1f1f1f", hover_color="#333333", text_color="white", font=ctk.CTkFont(size=20), command=self.toggle_fullscreen)
        # Butonu okuma alanının (PDF çerçevesinin) tam sağ üst hizasına denk gelecek şekilde y ekseninden (yukarıdan) yaklaşık 150 piksel aşağı itiyoruz.
        self.fullscreen_btn.place(relx=1.0, rely=0.0, x=-40, y=150, anchor="ne")

        # Tam Ekran moduna geçildiğinde sol üst köşede belirecek Yüzen(Floating) "Fit Width" Butonu. 
        # Diğer yüzen butonlarla aynı tasarımı kullanıyor ancak ilk başta GİZLİ olacak (.place yazarsak görünür. Toggle kısmında göstereceğiz).
        self.floating_fit_width_btn = ctk.CTkButton(self.reader_frame, text="Fit Width", width=80, height=40, corner_radius=8, fg_color="#1f1f1f", hover_color="#333333", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), command=self.fit_width)

    def create_converter_frame(self):
        """Dosya Dönüştürme ekranını (orta/sağ alan) tasarlayan metod."""
        self.converter_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.converter_frame.grid_columnconfigure(0, weight=1)

        self.converter_title = ctk.CTkLabel(self.converter_frame, text="File Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.converter_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Dosya Seç butonu
        self.converter_select_btn = ctk.CTkButton(self.converter_frame, text="Select File to Convert", command=self.select_file_converter)
        self.converter_select_btn.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Seçilen dosyanın adının gösterileceği etiket
        self.converter_selected_label = ctk.CTkLabel(self.converter_frame, text="No file selected")
        self.converter_selected_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

        # Format seçimi başlığı ve Dropdown menüsü (Combobox)
        self.format_label = ctk.CTkLabel(self.converter_frame, text="Select Target Format:")
        self.format_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.format_optionmenu = ctk.CTkOptionMenu(self.converter_frame, values=["CSV to Excel", "Excel to CSV", "TXT to PDF", "PDF to TXT"])
        self.format_optionmenu.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")

        # İşi başlatacak Buton
        self.convert_btn = ctk.CTkButton(self.converter_frame, text="Convert Now", command=self.convert_file)
        self.convert_btn.grid(row=5, column=0, padx=20, pady=20, sticky="w")

    # ---------------------------------------------------------
    # GENEL YARDIMCI METODLAR VE SCROLL (KAYDIRMA) İŞLEMLERİ
    # ---------------------------------------------------------
    def _on_mousewheel(self, event):
        """Kullanıcı farenin topunu çevirdiğinde çalışan, PDF'yi aşağı - yukarı kaydıran tuval (canvas) komutu."""
        # state = 4 -> Control tuşu / 1 -> Shift tuşu basılı demektir.
        if event.state & 0x0004:
            return # Ctrl basılıyken işlemi pas geç (Büyütme/Küçültmeye gitsin)
            
        if event.state & 0x0001:
            # İşletim sistemi MouseWheel event'ini Shift ile birleşik olarak tekil bir MouseWheel eventi gibi verirse:
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            return
            
        # Canvas'a sadece yukarı/aşağı tekerlek sinyalini gönder. Windows'ta delta -120/+120 arasıdır.
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_shift_mousewheel(self, event):
        """Saf <Shift-MouseWheel> eventi yakalanırsa doğrudan YATAY(Sağa-sola) kaydır."""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def clear_reader_display(self):
        """Uygulamada bir sayfa açıkken yeni bir dosya seçilirse, eski görsel kalıntılarını (widgetları) yok eder(siler)."""
        for widget in self.reader_display_frame.winfo_children():
            widget.destroy()

    def show_frame(self, frame_name):
        """Sol menüdeki butonlara basıldıkça "reader" veya "converter" sayfalarını gösterip diğerini ekran arka planından silmeyi(gizlemeyi) sağlar."""
        if frame_name == "reader":
            self.converter_frame.grid_forget()  # Dönüştürme ekranını görünmez yap
            self.reader_frame.grid(row=0, column=1, sticky="nsew") # Okuma ekranını görünür yap ve grid düzenine koy.
        elif frame_name == "converter":
            self.reader_frame.grid_forget()     # Okuma ekranını görünmez yap
            self.converter_frame.grid(row=0, column=1, sticky="nsew") # Dönüştürme ekranını görünür yap.

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Sol alttaki menüden tema ayarlanınca kütüphane fonksiyonuna yeni temayı gönderip görüntünün güncellenmesini sağlar."""
        ctk.set_appearance_mode(new_appearance_mode)

    # ---------------------------------------------------------
    # ZOOM İŞLEMLERİ: PDF GÖRÜNTÜLERİ YAKINLAŞTIRMA MANTIĞI
    # ---------------------------------------------------------
    def update_zoom(self):
        """Bu fonksiyon mevcut zoom oranını (self.current_zoom) dikkate alarak oluşturulmuş olan sayfaların (resimlerin) piksellerini(ebatlarını) hesaplar ve günceller."""
        # zip: İki listeyi paralel olarak (örn: birinci resim taşıyıcısı ve birinci resmin özellikleri) tek döngüde dönmemizi sağlar.
        for img_label, info in zip(self.pdf_image_labels, self.base_pdf_images):
            ctk_image, base_w, base_h = info # Bilgiyi ayıklarız. ctk formatlı resim, taban(orjinal) genişlik, taban(orjinal) yükseklik.
            
            # Yeni boyutu hesapla. Çarpan 1.5 ise; genişlik %50 büyür. Ancak en az 10 piksel (max(10, x)) olmasını sağlarız ki sistem çökmesin.
            new_w = max(10, int(base_w * self.current_zoom))
            new_h = max(10, int(base_h * self.current_zoom))
            
            # Seçili olan sayfanın CustomTkinter Resminin en/boy bilgisini yenile
            ctk_image.configure(size=(new_w, new_h))
            # Ekranda gösterilen etikete(kutuya) yeni boyutlu resmi geri ver.
            img_label.configure(image=ctk_image)
            
        # Resimler büyüyüp/küçüldükten hemen sonra çerçevenin gerçek boyutunu hesaplaması için sistemi 1 salise dürteriz.
        self.reader_display_frame.update_idletasks()
        # Canvas tuvalinin kaydırma sınırlarını, büyüyen/küçülen resimlerin yeni sınırlarına göre yeniden çizer!
        # Bunu yapmazsak yatay veya dikey Scrollbar (Kaydırma çubuğu) resimler büyüse bile çıkmaz/çalışmaz.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        if not self.pdf_image_labels: return  # Ekranda gösterilen hiçbir resim yoksa(örneğin PDF açmamışsak), hiçbir şey yapma (Kapat)
        
        # Matematiksel olarak "+ 0.2" eklemek yerine mevcudu "1.3 ile çarpmak" (%30 büyütmek) göze çok daha akıcı gelir.
        self.current_zoom *= 1.3
        self.update_zoom()                    # Resimleri tekrar hesapla
        
        # Güncelleme sonrası çerçevenin (display frame) genişleme bilgilerini anlık olarak Canvas'a iletiyoruz
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self):
        if not self.pdf_image_labels: return  # Ekranda bir şey yoksa fonksiyonu iptal et.
        if self.current_zoom > 0.3:           # Fotoğrafların gözle görülmeyecek kadar küçük olmasını engelle.
            # Küçültürken de çıkarma işlemi yerine çarpanla (örn %75'i) küçültmek harika bir akıcılık sağlar.
            self.current_zoom *= 0.75         
            self.update_zoom()
            
            # Güncelleme sonrası çerçevenin bilgilerini anlık olarak tuvale(Canvas'a) iletiyoruz (Scroll bar güncellensin diye)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fit_width(self):
        if not self.pdf_image_labels: return
        
        # Ekrana Sığdır komutunda artık hesaplamayı Canvas(Tuval) üzerinden almamız gerekiyor
        frame_width = self.canvas.winfo_width()
        
        if frame_width > 50 and self.base_pdf_images:
            # Sadece 0. indexteki (yani birinci sayfanın) genişlik bilgisini alıyoruz ki orantıyı bulalım.
            _, base_w, _ = self.base_pdf_images[0] 
            
            # Sağ taraftaki dikey Scrollbar için sistemde ortalama ortalama 30 piksel boşluk bırakılır.
            target_w = frame_width - 30 
            
            # Mantık: Orijinal resim 500 piksel ise, bizim hedef ekranımız 1000 piksel ise çarpan "1000/500" yani 2.0 (Yeni Zoom) olmalıdır.
            self.current_zoom = target_w / base_w
            self.update_zoom()

    def on_ctrl_scroll(self, event):
        """Bu fonksiyon Windows veya Mac gibi işletim sistemlerinden tekerlek hareket ettiğinde bir 'event'(olay obkesi) alır."""
        if not self.pdf_image_labels: return
        
        # event.num Linux sistemini algılamak içindir.
        # event.delta ise Windows/Mac sistemini temsil eder. (Örn: Fare bir tık ileri sürüklenince delta>0'dır, geri sürüklenince delta<0'dır)
        if event.num == 4 or getattr(event, 'delta', 0) > 0:
            self.zoom_in()   # İleri doğru tekerlek kaydırıldı = Büyüt
        elif event.num == 5 or getattr(event, 'delta', 0) < 0:
            self.zoom_out()  # Geriye doğru çekildi = Küçült

    def toggle_fullscreen(self):
        """Bu fonksiyon arayüzdeki diğer bileşenleri (Sol menü, üst başlık vb.) gizleyip sadece PDF ekranını bırakır."""
        if not self.is_fullscreen:
            # Tam ekrana geçiş (Değişkeni True yapmadan önce UI elemanlarını sakla)
            self.sidebar_frame.grid_forget()       # Sol yan menüyü kaldır
            self.reader_title.grid_forget()        # Başlığı kaldır
            self.reader_toolbar.grid_forget()      # Seçim yapma butonlarını vs. kaldır
            
            # Sağ çerçeveyi en geniş haliyle tekrar oluştur
            # columnspan=2 diyerek sol menünün alanına da taşmasını sağlarız. Ayrıca row=0 diyoruz ki en tepeye çıksın.
            self.reader_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
            
            # Okuyucu Gösterim alanının (self.reader_display_frame) grid_rowconfigure ile tanımlı "2. satırda genişleme" özelliği var.
            # Başlık ve toolbar gizlendiği için 0 ve 1. satırların yükseklikleri otomatik olarak sıfırlanır, böylece 2. satır en tepeye yükselir.
            # Okuyucu Gösterim kutusunun dış ambalajını esneteceğiz (İçindeki Canvas ve Scrolllar ona bağlı olduğu için otomatik esneyecek)
            # Bu yüzden row=2'de kalmalı! Boşlukları (padx, pady) 0 yapıp tam ekran olmasını sağlıyoruz.
            self.reader_display_container.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
            
            # Tam Ekran kapatma butonunu ekranın en sağ üstüne (padding/boşluk olmadan) yeniden konumlandırıyoruz
            self.fullscreen_btn.place(relx=1.0, rely=0.0, x=-20, y=20, anchor="ne")
            self.fullscreen_btn.configure(text="✖") # İkonu çarpı gibi "kapat" manasında değiştiririz
            
            # SADECE Tam Ekranda görünen yeni tasarım Yüzen Fit Width butonunu sol üste yerleştiriyoruz
            self.floating_fit_width_btn.place(relx=0.0, rely=0.0, x=20, y=20, anchor="nw")
            
            self.is_fullscreen = True
        else:
            # Tam ekrandan çıkış (Değişken True iken False'a döner ve sistemi eski haline uyarlar)
            # Sol menüyü geri getir
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            
            # Formu tekrar tek kolona (column=1) sıkıştır
            self.reader_frame.grid(row=0, column=1, sticky="nsew")
            
            # Başlık ve toolbar'ı sırasıyla 0 ve 1. satırlara tekrar koy
            self.reader_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
            self.reader_toolbar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
            
            # Okuma alanını (2. satır Containerı) eski kenar boşlukları ile (padx=20, pady=20) geri koy
            self.reader_display_container.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
            
            # Tam ekran açma butonunu PDF okuyucu gövdesinin sağ üstüne (eski yerine) iteliyoruz
            self.fullscreen_btn.place(relx=1.0, rely=0.0, x=-40, y=150, anchor="ne")
            self.fullscreen_btn.configure(text="⛶") # Eski haline (çerçeve) çeviriyoruz
            
            # Yüzen Fit Width butonunu gizliyoruz çünkü orijinal toolbarımız yerine var (Tam ekranda değiliz)
            self.floating_fit_width_btn.place_forget()
            
            self.is_fullscreen = False

    # ---------------------------------------------------------
    # İŞLEVSEL (MANTIK) FONKSİYONLARI - DOSYA İŞLEMLERİ
    # ---------------------------------------------------------
    def select_file_reader(self):
        """Reader (Okuyucu) bölümünde dosya seçme işlemini tetikleyen fonksiyon."""
        self.reader_file_path = filedialog.askopenfilename() # Kullanıcının klasörlerinde gezip dosya seçebileceği işletim sistemi ekranını açar.
        
        if self.reader_file_path: # Kullanıcı çarpıya basıp iptal etmediyse ve bir dosya seçtiyse...
            self.clear_reader_display() # Okuma ekranını temizle. Geleceklere yer aç.
            
            # Dosyanın uzantısını bulalım (Örn: ".pdf", ".docx", ".txt")
            _, ext = os.path.splitext(self.reader_file_path.lower()) 
            
            try:
                # EĞER DOSYA PDF İSE (Kendi okuyucumuzda sayfa sayfa resim olarak render ederek gösteriyoruz)
                if ext == ".pdf":
                    self.pdf_image_labels = []   # Temizle (yeni bir kayıt başlatıyoruz)
                    self.base_pdf_images = []    
                    self.current_zoom = 1.0      # Yakınlaştırmayı sıfırla/başlangıç haline getir.

                    doc = fitz.open(self.reader_file_path) # fitz(PyMuPDF) ile belgemizi sistem hafızasına yükleriz.
                    
                    # PERFORMANS GÜNCELLEMESİ (AKICILIK):
                    # Önceden hepsi aynı anda for döngüsüyle yüklendiği için sayfa sayısı çok olursa arayüz çöküyor (donuyor) gibi duruyordu.
                    # Artık sayfaları tek tek, arkaplanda (asenkron tarzı) yükleyen yeni bir özel metodu tetikleyeceğiz.
                    self.load_pdf_page_async(doc, current_page=0, total_pages=len(doc))
                        
                # METİN VEYA VERİ TABELASI GÖSTERİM DENEMELERİ
                elif ext in [".txt", ".csv", ".xlsx", ".xls", ".docx"]:
                    content = "" # İçeriği tutacak boş bir değişken (String metni) oluşturduk.
                    
                    # Basit düz metin (txt) okuma mantığı
                    if ext == ".txt":
                        with open(self.reader_file_path, "r", encoding="utf-8") as f: # Dosyayı karakter kodları utf-8 bozulmayacak şekilde aç.
                            content = f.read() # Tüm içeriği değişkene al.
                    
                    # CSV dosyası mantığı (Pandas kullanılır)
                    elif ext == ".csv":
                        df = pd.read_csv(self.reader_file_path) # Pandas ile dosyayı satır-sütun (Dataframe) haline dönüştürürüz...
                        content = df.head(50).to_string()       # Hafızayı boğmamak için sadece ilk 50 satırı yazdırıp text içeriğine yazarız.
                    
                    # Excel dosyası mantığı (Pandas kullanılır)
                    elif ext in [".xlsx", ".xls"]:
                        df = pd.read_excel(self.reader_file_path)
                        content = df.head(50).to_string()
                    
                    # Word Belgesi mantığı (.docx)
                    elif ext == ".docx":
                        doc_file = Document(self.reader_file_path) # Document kütüphanesi dosyayı çözer
                        for para in doc_file.paragraphs:           # Paragrafları alt alta inceler
                            content += para.text + "\n"            # Her paragrafı string değişenimize alta(yeni bir satıra) ekleyerek doldururuz.
                            
                    # Arayüzümüze sadece "Salt Okunur (Disabled)" şekilde metin gösterebileceğimiz devasa bir Textbox oluşturur ve bu "content" verisini oraya atarız.
                    tb = ctk.CTkTextbox(self.reader_display_frame, width=600, height=500)
                    tb.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
                    tb.insert(tk.END, content) # Başından (tk.END ile birleştirerek) içeriği içine süreriz
                    tb.configure(state="disabled") 
                
                # EĞER PROGRAM BİZİM Kütüphanelerimizde TANIMLI DEĞİLSE (Örneğin MP4 video veya JPG resmi)
                else: 
                    import sys        # Python'un sistem kütüphanesi
                    import subprocess # Arkaplanda görev çalıştırıcı
                    
                    # İşletim sistemini tanırız (win32 = Windows vb.)
                    if sys.platform == "win32":
                        os.startfile(self.reader_file_path)     # Win API ile dosyaya çift tıklamışız gibi davranırız! Dosyası bilgisayarda ne programı ile açılıyorsa öyle açılır.
                    elif sys.platform == "darwin":
                        subprocess.call(('open', self.reader_file_path)) # macOS'ta çift tıkla aç komutu
                    else:
                        subprocess.call(('xdg-open', self.reader_file_path)) # Linux işletim sistemlerinde çift tıkla aç komutu

                    filename = os.path.basename(self.reader_file_path) # Dosyanın sade adını bulur. (Örn: Video.mp4)
                    msg = f"Açılan Dosya: {filename}\n\nBu dosya sistemi kendi okuyucumuzda gösterilemediği için sisteminizin varsayılan programı ile açıldı."
                    
                    # UI(Arayüz) üzerinde kullanıcıya bilgi amaçlı bu metni yansıtırız.
                    tb = ctk.CTkTextbox(self.reader_display_frame, width=600, height=200)
                    tb.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
                    tb.insert(tk.END, msg)
                    tb.configure(state="disabled")

            except Exception as e:
                # Blok(try alanı) içerisinde herhangi bir okuma-izletme hatası çıkarsa Python'un çökmesi engellenir.
                # Sadece küçük bir popup ile hatanın text e'sini yazdırır.
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def load_pdf_page_async(self, doc, current_page, total_pages):
        """Performans için devasa PDF'leri aynı anda dondurarak oluşturmak yerine tek tek işler."""
        if current_page >= total_pages:
            return  # Yükleme tamamen bitmiş.

        page = doc.load_page(current_page) 
        
        # PERFORMANS VE KALİTE DENGENSİ: (5,5) bilgisayarın RAM'ini aşırı kitlediği için yavaşlamaya neden oluyordu!
        # (3,3) "Altın Orandır". Hem ekranın 3 katı çözünürlük verip yüksek kaliteli Zoom sunar, hem de takılma yaşatmaz!
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3)) 
        img_data = pix.tobytes("ppm")
        pil_image = Image.frombytes("RGB", [pix.width, pix.height], img_data)
        
        # Ekran için temel hesaplama (3 e böleriz ki doğal piksellerinde dursa bile kaliteli kalsın)
        base_w = pix.width // 3
        base_h = pix.height // 3
        
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(base_w, base_h))
        self.base_pdf_images.append((ctk_image, base_w, base_h)) 
        
        img_label = ctk.CTkLabel(self.reader_display_frame, image=ctk_image, text="", fg_color="transparent")
        img_label.grid(row=current_page, column=0, pady=10) 
        self.pdf_image_labels.append(img_label)
        
        # Yeni sayfa oluşturuldukça kaydırıcıyı(Scrollbar) durumdan haberdar et.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Can alıcı nokta: Arayüz motorunun (.after özelliği sayesinde) rahat nefes almasına izin verdik. 
        # Bir sonraki sayfayı 10 milisaniye sonra yüklemesini istiyoruz. Böylece uygulama dönüp "kullanıcı hala hareket ediyor mu?" diye bakabiliyor!
        self.after(10, self.load_pdf_page_async, doc, current_page + 1, total_pages)

    def select_file_converter(self):
        """Converter (Dönüştürücü) bölümünde dosya seçilme işlemini tetikleyen fonksiyon."""
        self.converter_file_path = filedialog.askopenfilename(
            # Gerekli uzantılara göre özel bir filtre tanımlandı
            filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")]
        )
        if self.converter_file_path:
             # Kullanıcı arayüzüne, seçilen dosyanın adını çıkarttık ki kullanıcı anlasın.
            self.converter_selected_label.configure(text=f"Selected: {os.path.basename(self.converter_file_path)}")

    def convert_file(self):
        """Dönüştürücüde Convert butonuna basıldığında format işlemini yapan en merkezi karar bloğu."""
        if not self.converter_file_path:
            # Dosya seçmemişse uyar.
            messagebox.showwarning("Warning", "Please select a file first!")
            return
            
        target_format = self.format_optionmenu.get() # Kullanıcı Dropdown'da(Combobox) tam olarak hangi dönüşümü istemiş olduğunu anlar
        dir_name = os.path.dirname(self.converter_file_path) # Dosyanın içinde bulunduğu klasörü(Dizini) tespit edip kaydı tutuyoruz.
        # base_name = Uzantısız saf ismi alır (Örn: Rapor) 
        # current_ext = Mevcut dosyanın uzantısını alır (Örn: .pdf)
        base_name, current_ext = os.path.splitext(os.path.basename(self.converter_file_path))
        current_ext = current_ext.lower() # büyük/küçük harf ayrımını eşitleyip güvene alıyoruz.
        
        try:
            # Karar mekanizmaları
            if target_format == "CSV to Excel":
                if current_ext != ".csv": # Çakallık yapıp başka format atarsa bilerek bir hata (ValueError) döndürüyoruz! Sistem çalışmasını durdursun.
                    raise ValueError("Selected file is not a CSV!")
                df = pd.read_csv(self.converter_file_path) # Pandas arkaplanda csv dosyasını geçici zihnine okur.
                save_path = os.path.join(dir_name, base_name + "_converted.xlsx") 
                df.to_excel(save_path, index=False) # Pandas hafızasındaki Excel dosyası formatlama yeteneğiyle o dosyayı .xlsx olarak dizine gönderir(kaydeder).
                messagebox.showinfo("Success", f"File successfully converted!\nSaved as: {save_path}") # Başarı ekranı

            elif target_format == "Excel to CSV":
                if current_ext not in [".xlsx", ".xls"]:
                    raise ValueError("Selected file is not an Excel format!")
                df = pd.read_excel(self.converter_file_path) # Tersi işlemi olarak Pandas bu sefer Excel formatiyle veriyi çözer.
                save_path = os.path.join(dir_name, base_name + "_converted.csv")
                df.to_csv(save_path, index=False) # df nesnesi to_csv yeteneğiyle yeni csv olarak sistemi derler.
                messagebox.showinfo("Success", f"File successfully converted!\nSaved as: {save_path}")

            elif target_format == "TXT to PDF":
                # Bu özellik için reporlab vb. grafik yaratıcı python libraryleri ile metin satırları çizgi çizgi kağıt mantığına dikilir. 
                # (Zor değil ancak bu senaryoda eklenmediği için notice / uyarı düşüyoruz.)
                messagebox.showinfo("Notice", "TXT to PDF feature requires an extra library like 'fpdf' or 'reportlab'.")
                
            elif target_format == "PDF to TXT":
                if current_ext != ".pdf":
                    raise ValueError("Selected file is not a PDF!")
                
                save_path = os.path.join(dir_name, base_name + "_converted.txt")
                
                # with open "rb" = pdf dosyamızı read binary(ikili okuma) formatında açar.
                # w "f_out" = çıktı dosyamızı ise write(yazma) formatında ve utf-8 korumalı klasörde yaratır.
                with open(self.converter_file_path, "rb") as f_in, open(save_path, "w", encoding="utf-8") as f_out:
                    pdf = PyPDF2.PdfReader(f_in) # PDF kütüphanesi açtığımız pdf hafızasından nesnemizi bir makine formatına dönüştürüp değişkenimize(pdf'ye) salar.
                    for page in pdf.pages:       # Sayfaları döngüyle tarar
                        # f_out(txt belgesi) writer'ımız(yazıcımız) extract_text fonksiyonuyla satırlara çıkarılıp txt içine enjekte edilir.
                        f_out.write(page.extract_text() + "\n") 
                messagebox.showinfo("Success", f"File successfully converted!\nSaved as: {save_path}")
                
        except Exception as e:
            # İşlem esnasındaki hataları e adlı bir yakalayıcıya atayıp messagebıox.showerror ile bildiririz.
            messagebox.showerror("Conversion Error", f"An error occurred:\n{e}")


# Dosya Eğer bağımsız çalıştırılıyorsa (Örn: Modül import değilse python main.py çalışıyorsa) Sınıflar ayağa kalkar ve sonsuz bir olay döngüsü başlatır.
if __name__ == "__main__":
    app = App()      # Yukarıda iskeletini yarattığımız sistemi (App Classını) canlandırdık (Nesne Instance oluşturduk)
    app.mainloop()   # Sonsuz olay döngüsü: İşletim sistemi kullanıcı çarpıya basına kadar programı uyanık ve dinlemede bırakır!.
