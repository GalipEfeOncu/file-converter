"""Download bundled FFmpeg for Windows.

This script downloads the FFmpeg LGPL static build ZIP, extracts
`ffmpeg.exe`, and places it under `assets/bin/ffmpeg.exe`.
"""

import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def download_ffmpeg(download_path: Path) -> Path:
    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    urllib.request.urlretrieve(FFMPEG_URL, str(download_path))
    return download_path


def extract_ffmpeg(zip_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as archive:
        ffmpeg_members = [m for m in archive.namelist() if m.lower().endswith("ffmpeg.exe")]
        if not ffmpeg_members:
            raise RuntimeError("ffmpeg.exe arşiv içinde bulunamadı.")
        with archive.open(ffmpeg_members[0]) as source, destination.open("wb") as target:
            shutil.copyfileobj(source, target)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    destination_dir = project_root / "assets" / "bin"
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_file = destination_dir / "ffmpeg.exe"

    if destination_file.exists():
        print(f"Zaten mevcut: {destination_file}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = Path(temp_dir) / "ffmpeg.zip"
        download_ffmpeg(zip_path)
        extract_ffmpeg(zip_path, destination_file)

    print(f"FFmpeg başarıyla indirildi: {destination_file}")


if __name__ == "__main__":
    main()
