"""
tests/run_full_validation.py — Proje Geneli Doğrulama Scripti
PM tarafından oluşturuldu: 2026-04-21

Tüm modüllerin import edilebilirliğini, API sözleşmelerini,
i18n paritesini, converter fonksiyonelliğini ve AI Engine
davranışını test eder.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Proje kökünü path'e ekle
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

PASS = "✅ PASS"
FAIL = "❌ FAIL"
WARN = "⚠️ WARN"
results = []


def record(test_name, passed, detail=""):
    status = PASS if passed else FAIL
    results.append((test_name, status, detail))
    print(f"  {status}  {test_name}" + (f" — {detail}" if detail else ""))


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# =====================================================================
# 1. SMOKE TEST: Tüm Modüller Import Edilebilir mi?
# =====================================================================
section("1. Smoke Test — Modül Import'ları")

modules_to_import = [
    ("config.settings", "Config"),
    ("core.converter", "FileConverter"),
    ("core.player", "AudioConverter"),
    ("core.viewer", "FileViewer"),
    ("core.ai_engine", "AIEngine"),
    ("ui.styles", "apply_custom_css"),
]

for mod_path, class_name in modules_to_import:
    try:
        mod = __import__(mod_path, fromlist=[class_name])
        obj = getattr(mod, class_name, None)
        record(f"import {mod_path}.{class_name}", obj is not None)
    except Exception as e:
        record(f"import {mod_path}.{class_name}", False, str(e))

# ui.dashboard Streamlit gerektirir, importunu try ile kontrol et
try:
    from ui.dashboard import Dashboard
    record("import ui.dashboard.Dashboard", True)
except Exception as e:
    record("import ui.dashboard.Dashboard", False, str(e))


# =====================================================================
# 2. CONFIG: Settings Sözleşmesi
# =====================================================================
section("2. Config — Settings Sözleşmesi")

from config.settings import Config

record("Config.APP_NAME is str", isinstance(Config.APP_NAME, str), Config.APP_NAME)
record("Config.VERSION is str", isinstance(Config.VERSION, str), Config.VERSION)
record("Config.DEFAULT_LANGUAGE in (tr, en)", Config.DEFAULT_LANGUAGE in ("tr", "en"), Config.DEFAULT_LANGUAGE)
record("Config.GEMINI_API_KEY exists", hasattr(Config, "GEMINI_API_KEY"))
record("Config.SUPPORTED_EXTENSIONS is list", isinstance(Config.SUPPORTED_EXTENSIONS, list), f"{len(Config.SUPPORTED_EXTENSIONS)} uzantı")

# Tüm uzantılar '.' ile başlıyor mu?
all_dot = all(ext.startswith(".") for ext in Config.SUPPORTED_EXTENSIONS)
record("SUPPORTED_EXTENSIONS hepsi '.' ile başlıyor", all_dot)


# =====================================================================
# 3. AI ENGINE: API Sözleşmesi ve Davranış
# =====================================================================
section("3. AI Engine — Sözleşme ve Graceful Fallback")

from core.ai_engine import AIEngine, _SYSTEM_PROMPTS

ai = AIEngine()

# Metot varlığı
for method in ["summarize", "answer_question", "extract_keywords", "simplify", "_call_gemini"]:
    record(f"AIEngine.{method} exists", hasattr(ai, method))

# System prompts
required_prompts = {"summarize", "summarize_short", "summarize_long", "qa", "keywords", "simplify", "simplify_basic", "simplify_advanced"}
record("Tüm system prompt'lar tanımlı", required_prompts.issubset(set(_SYSTEM_PROMPTS.keys())), f"{len(_SYSTEM_PROMPTS)} prompt")

# Boş girdi graceful fallback
result = ai.summarize("")
record("summarize('') → string döner, crash yok", isinstance(result, str) and len(result) > 0)

result = ai.answer_question("", "test?")
record("answer_question('','test?') → string döner", isinstance(result, str) and len(result) > 0)

result = ai.extract_keywords("")
record("extract_keywords('') → boş liste döner", isinstance(result, list) and len(result) == 0)

result = ai.simplify("")
record("simplify('') → string döner", isinstance(result, str) and len(result) > 0)

# Length parametresi
for length in ["short", "medium", "long"]:
    result = ai.summarize("Test metni", length=length)
    record(f"summarize(length='{length}') → string döner", isinstance(result, str))

# Level parametresi
for level in ["basic", "intermediate", "advanced"]:
    result = ai.simplify("Test metni", level=level)
    record(f"simplify(level='{level}') → string döner", isinstance(result, str))


# =====================================================================
# 4. CONVERTER: Dosya Dönüştürme
# =====================================================================
section("4. Converter — Dosya Dönüştürme Testleri")

try:
    from core.converter import FileConverter
    fc = FileConverter()
    converter_available = True
except ImportError as e:
    converter_available = False
    record("FileConverter import", False, f"Eksik bağımlılık: {e} (Issue #15 kapsamı)")
    fc = None

# CSV → XLSX
if converter_available:
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "test.csv")
        xlsx_path = os.path.join(tmpdir, "test.xlsx")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("ad,yas,sehir\nAli,25,Istanbul\nVeli,30,Ankara\n")

        result = fc.convert_csv_to_xlsx(csv_path, xlsx_path)
        record("convert_csv_to_xlsx → True", result is True)
        record("convert_csv_to_xlsx → dosya oluştu", os.path.exists(xlsx_path))

    # XLSX → CSV
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "input.csv")
        xlsx_path = os.path.join(tmpdir, "input.xlsx")
        csv_out = os.path.join(tmpdir, "output.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("a,b\n1,2\n")
        fc.convert_csv_to_xlsx(csv_path, xlsx_path)
        result = fc.convert_xlsx_to_csv(xlsx_path, csv_out)
        record("convert_xlsx_to_csv → True", result is True)

    # Gorsel donusum (PNG → JPG)
    try:
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmpdir:
            png_path = os.path.join(tmpdir, "test.png")
            jpg_path = os.path.join(tmpdir, "test.jpg")
            img = Image.new("RGB", (100, 100), color="red")
            img.save(png_path)
            result = fc.convert_image(png_path, jpg_path, "jpg")
            record("convert_image PNG→JPG → True", result is True)
            record("convert_image PNG→JPG → dosya olustu", os.path.exists(jpg_path))

            # JPG → WEBP
            webp_path = os.path.join(tmpdir, "test.webp")
            result = fc.convert_image(jpg_path, webp_path, "webp")
            record("convert_image JPG→WEBP → True", result is True)

            # PNG → BMP
            bmp_path = os.path.join(tmpdir, "test.bmp")
            result = fc.convert_image(png_path, bmp_path, "bmp")
            record("convert_image PNG→BMP → True", result is True)
    except ImportError:
        record("Pillow import", False, "Pillow yuklu degil")

    # Olmayan dosya → False
    result = fc.convert_csv_to_xlsx("nonexistent.csv", "out.xlsx")
    record("convert_csv_to_xlsx(nonexistent) → False", result is False)

    # DOCX → TXT
    try:
        from docx import Document
        with tempfile.TemporaryDirectory() as tmpdir:
            docx_path = os.path.join(tmpdir, "test.docx")
            txt_path = os.path.join(tmpdir, "test.txt")
            doc = Document()
            doc.add_paragraph("Test paragraf")
            doc.save(docx_path)
            result = fc.convert_docx_to_txt(docx_path, txt_path)
            record("convert_docx_to_txt → True", result is True)
            if os.path.exists(txt_path):
                content = open(txt_path, "r", encoding="utf-8").read()
                record("convert_docx_to_txt → icerik dogru", "Test paragraf" in content)
    except ImportError:
        record("python-docx import", False, "python-docx yuklu degil")
else:
    print("  (Converter testleri atlandi — docx2pdf eksik)")


# =====================================================================
# 5. AUDIO CONVERTER: FFmpeg Kontrolü
# =====================================================================
section("5. Audio Converter — FFmpeg Durumu")

from core.player import AudioConverter

ac = AudioConverter()
record("AudioConverter oluşturuldu", ac is not None)
record(f"FFmpeg mevcut: {ac.ffmpeg_available}", True, "Bilgi amaçlı")
record("is_ffmpeg_installed() çalışıyor", isinstance(ac.is_ffmpeg_installed(), bool))

if not ac.ffmpeg_available:
    # FFmpeg yoksa False dönmeli
    result = ac.convert_audio("nonexistent.mp3", "out.wav", "wav")
    record("convert_audio(ffmpeg yok) → False", result is False)


# =====================================================================
# 6. DASHBOARD HELPERS: Format Map ve Dispatcher
# =====================================================================
section("6. Dashboard — Format Map ve Dispatcher")

try:
    from ui.dashboard import _FORMAT_MAP, Dashboard

    # Format map kontrolleri
    record("_FORMAT_MAP .pdf → docx içerir", "docx" in _FORMAT_MAP.get(".pdf", []))
    record("_FORMAT_MAP .csv → xlsx içerir", "xlsx" in _FORMAT_MAP.get(".csv", []))
    record("_FORMAT_MAP .xlsx → csv içerir", "csv" in _FORMAT_MAP.get(".xlsx", []))
    record("_FORMAT_MAP .jpg → png,webp,bmp içerir", set(["png","webp","bmp"]).issubset(set(_FORMAT_MAP.get(".jpg", []))))
    record("_FORMAT_MAP .mp3 → wav,ogg,flac içerir", set(["wav","ogg","flac"]).issubset(set(_FORMAT_MAP.get(".mp3", []))))

    # Dispatcher: desteklenmeyen format → False
    result = Dashboard._dispatch_conversion("nonexistent.file", ".xyz", "abc", "out.file")
    record("_dispatch_conversion(unsupported) → False", result is False)

except Exception as e:
    record("Dashboard import/test", False, str(e))


# =====================================================================
# 7. i18n: Dil Dosyası Parite ve Bütünlük
# =====================================================================
section("7. i18n — languages.json Parite ve Bütünlük")

with open(os.path.join(project_root, "assets", "languages.json"), "r", encoding="utf-8") as f:
    lang_data = json.load(f)

record("'tr' kökü mevcut", "tr" in lang_data)
record("'en' kökü mevcut", "en" in lang_data)

tr_keys = set(k for k in lang_data["tr"] if not k.startswith("_"))
en_keys = set(k for k in lang_data["en"] if not k.startswith("_"))

record(f"TR anahtar sayısı: {len(tr_keys)}", True)
record(f"EN anahtar sayısı: {len(en_keys)}", True)

missing_en = tr_keys - en_keys
missing_tr = en_keys - tr_keys
record("TR↔EN parite (simetri)", tr_keys == en_keys,
       f"EN'de eksik: {missing_en or 'yok'}, TR'de eksik: {missing_tr or 'yok'}")

# Kritik runtime anahtarları
critical_keys = [
    "app_title", "convert_tab", "view_tab", "ai_tab",
    "upload_file", "file_uploaded", "error_unsupported_file",
    "success_conversion", "btn_convert", "btn_download",
    "select_target_format", "converting_in_progress",
    "no_file_uploaded", "no_conversion_available",
    "error_api_key_missing", "error_ai_request_failed",
]
for key in critical_keys:
    record(f"Kritik anahtar '{key}' TR+EN'de var",
           key in tr_keys and key in en_keys)


# =====================================================================
# 8. REQUIREMENTS.TXT: Format Kontrolü
# =====================================================================
section("8. requirements.txt — Format Kontrolü")

req_path = os.path.join(project_root, "requirements.txt")
with open(req_path, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

record(f"Toplam bağımlılık sayısı: {len(lines)}", True)

all_pinned = all("~=" in line for line in lines)
record("Tüm bağımlılıklar ~= ile pinli", all_pinned,
       "Eksikler: " + str([l for l in lines if "~=" not in l]) if not all_pinned else "")

seen = set()
dupes = []
for line in lines:
    pkg = line.split("~=")[0].split("==")[0].strip().lower()
    if pkg in seen:
        dupes.append(pkg)
    seen.add(pkg)
record("Duplicate bağımlılık yok", len(dupes) == 0, f"Tekrar: {dupes}" if dupes else "")

# google-generativeai kontrolü
has_genai = any("google-generativeai" in l for l in lines)
has_openai = any("openai" in l for l in lines)
if not has_genai:
    results.append(("google-generativeai requirements.txt'de var", WARN,
                    "Ali'nin eklemesi gerekiyor"))
    print(f"  {WARN}  google-generativeai requirements.txt'de var — Ali'nin eklemesi gerekiyor")
if has_openai:
    results.append(("openai hâlâ requirements.txt'de (kullanılmıyor)", WARN,
                    "Ali ile kaldırılması koordine edilecek"))
    print(f"  {WARN}  openai hâlâ requirements.txt'de (kullanılmıyor) — Ali ile koordinasyon gerekli")


# =====================================================================
# 9. VIEWER: Temel Kontroller
# =====================================================================
section("9. Viewer — Temel API Kontrolleri")

from core.viewer import FileViewer

fv = FileViewer()
for method in ["render_pdf", "read_table", "display_pdf", "display_table",
               "display_audio", "display_video", "display_text_document"]:
    record(f"FileViewer.{method} exists", hasattr(fv, method))


# =====================================================================
# SONUÇ
# =====================================================================
section("SONUÇ ÖZETİ")

passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
warned = sum(1 for _, s, _ in results if s == WARN)

print(f"\n  Toplam: {len(results)} test")
print(f"  {PASS}  Geçen: {passed}")
print(f"  {FAIL}  Başarısız: {failed}")
print(f"  {WARN}  Uyarı: {warned}")
print()

if failed > 0:
    print("  Başarısız testler:")
    for name, status, detail in results:
        if status == FAIL:
            print(f"    {FAIL}  {name}" + (f" — {detail}" if detail else ""))

if warned > 0:
    print("\n  Uyarılar:")
    for name, status, detail in results:
        if status == WARN:
            print(f"    {WARN}  {name}" + (f" — {detail}" if detail else ""))

print(f"\n{'='*60}")
sys.exit(0 if failed == 0 else 1)
