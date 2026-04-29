import shutil
import logging
from pathlib import Path
from pydub import AudioSegment

class AudioConverter:
    def __init__(self):
        bundle_path = Path("assets/bin/ffmpeg.exe")
        if bundle_path.exists():
            ffmpeg_path = str(bundle_path.resolve())
        else:
            ffmpeg_path = shutil.which("ffmpeg")

        if ffmpeg_path is None:
            raise RuntimeError(
                "FFmpeg bulunamadı. 'python scripts/download_ffmpeg.py' komutunu çalıştırın."
            )

        AudioSegment.converter = ffmpeg_path
        self.ffmpeg_available = True
        self.ffmpeg_path = ffmpeg_path

    def is_ffmpeg_installed(self) -> bool:
        return self.ffmpeg_available

    def convert_audio(self, input_path, output_path, output_format):
        if not self.ffmpeg_available:
            logging.error("Hata: FFmpeg kurulu değil.")
            return False
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=output_format.lower())
            return True
        except Exception as e:
            logging.error(f"Dönüşüm hatası: {e}")
            return False

    def convert_mp3_to_wav(self, input_path, output_path):
        return self.convert_audio(input_path, output_path, "wav")

    def convert_wav_to_mp3(self, input_path, output_path):
        return self.convert_audio(input_path, output_path, "mp3")