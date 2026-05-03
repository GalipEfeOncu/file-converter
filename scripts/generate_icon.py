import os
from PIL import Image, ImageDraw, ImageFont

def generate_icon():
    # 512x512 PNG oluştur
    size = (512, 512)
    # Koyu arka plan (Gradientimsi)
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Stylized "UFW" text
    # Not: Font dosyası olmayabilir, default font kullanalım
    try:
        # Bazı linux sistemlerde bu yollar olabilir
        font_path = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 200)
    except:
        font = ImageFont.load_default()

    text = "UFW"
    # Metni ortala
    # getbbox metodu modern Pillow versiyonlarında var
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        w, h = 300, 200 # Fallback
        
    draw.text(((size[0]-w)/2, (size[1]-h)/2 - 50), text, fill=(59, 130, 246, 255), font=font)
    
    # "Lightning" symbol (basit bir üçgen/şimşek)
    draw.polygon([(256, 350), (280, 400), (256, 400), (270, 450), (230, 380), (250, 380)], fill=(234, 179, 8, 255))

    os.makedirs("assets", exist_ok=True)
    img.save("assets/icon.png")
    print("assets/icon.png created.")
    
    # ICO'ya çevir
    img.save("assets/icon.ico", format="ICO", sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
    print("assets/icon.ico created.")

if __name__ == "__main__":
    generate_icon()
