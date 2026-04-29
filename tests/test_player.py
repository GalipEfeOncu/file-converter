"""
tests/test_player.py - AudioConverter birim testleri

FFmpeg kontrolu ve ses donusum davranislarini mock ile dogrular.
"""

from pathlib import Path

import pytest

from pydub.exceptions import CouldntDecodeError

from core.player import AudioConverter
from core import player as player_module


def test_is_ffmpeg_installed_reflects_shutil_which(monkeypatch):
    """Sistem ffmpeg buluyorsa helper True donmeli."""
    monkeypatch.setattr(player_module.shutil, "which", lambda name: "C:/ffmpeg.exe" if name == "ffmpeg" else None)

    converter = AudioConverter()

    assert converter.ffmpeg_available is True
    assert converter.is_ffmpeg_installed() is True


def test_convert_audio_success_exports_target_format(monkeypatch, tmp_path: Path):
    """Basarili donusumde export hedef formatla cagrilmali ve True donmeli."""
    monkeypatch.setattr(player_module.shutil, "which", lambda _name: "C:/ffmpeg.exe")
    export_calls = {}

    class FakeAudio:
        def export(self, output_path: str, format: str) -> None:
            export_calls["output_path"] = output_path
            export_calls["format"] = format
            Path(output_path).write_bytes(b"audio-bytes")

    monkeypatch.setattr(player_module.AudioSegment, "from_file", lambda input_path: FakeAudio())
    converter = AudioConverter()
    output = tmp_path / "output.ogg"

    result = converter.convert_audio(str(tmp_path / "input.mp3"), str(output), "OGG")

    assert result is True
    assert output.exists()
    assert export_calls == {"output_path": str(output), "format": "ogg"}


def test_convert_audio_decode_failure_returns_false(monkeypatch, tmp_path: Path):
    """Cozumlenemeyen ses dosyasi icin False donmeli."""
    monkeypatch.setattr(player_module.shutil, "which", lambda _name: "C:/ffmpeg.exe")

    def raise_decode_error(_input_path: str):
        raise CouldntDecodeError("bad file")

    monkeypatch.setattr(player_module.AudioSegment, "from_file", raise_decode_error)
    converter = AudioConverter()

    result = converter.convert_audio(
        str(tmp_path / "input.mp3"),
        str(tmp_path / "output.wav"),
        "wav",
    )

    assert result is False


def test_shortcut_methods_delegate_to_convert_audio(monkeypatch, tmp_path: Path):
    """Kisayol metotlar hedef formatla ana metodu cagirmali."""
    calls = []

    def fake_convert_audio(self, input_path: str, output_path: str, target_format: str) -> bool:
        calls.append((input_path, output_path, target_format))
        return True

    monkeypatch.setattr(AudioConverter, "convert_audio", fake_convert_audio)
    converter = AudioConverter.__new__(AudioConverter)
    input_path = str(tmp_path / "input")
    output_path = str(tmp_path / "output")

    assert converter.convert_mp3_to_wav(input_path, output_path) is True
    assert converter.convert_wav_to_mp3(input_path, output_path) is True
    assert calls == [
        (input_path, output_path, "wav"),
        (input_path, output_path, "mp3"),
    ]


def test_audioconverter_uses_bundle_when_exists(monkeypatch, tmp_path: Path):
    """assets/bin/ffmpeg.exe varsa AudioSegment.converter path'e set edilmeli."""
    bundle_dir = tmp_path / "assets" / "bin"
    bundle_dir.mkdir(parents=True)
    bundle_path = bundle_dir / "ffmpeg.exe"
    bundle_path.write_text("fake binary")

    monkeypatch.chdir(tmp_path)
    converter = AudioConverter()

    assert converter.ffmpeg_path == str(bundle_path)
    assert player_module.AudioSegment.converter == str(bundle_path)


def test_audioconverter_fallback_to_system(monkeypatch, tmp_path: Path):
    """assets/bin/ffmpeg.exe yoksa sistem ffmpeg yoluna donmeli."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(player_module.shutil, "which", lambda name: "C:/ffmpeg.exe" if name == "ffmpeg" else None)

    converter = AudioConverter()

    assert converter.ffmpeg_path == "C:/ffmpeg.exe"
    assert player_module.AudioSegment.converter == "C:/ffmpeg.exe"


def test_audioconverter_raises_when_no_ffmpeg(monkeypatch, tmp_path: Path):
    """Ne bundle ne sistem ffmpeg varsa RuntimeError fırlatmalı."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(player_module.shutil, "which", lambda _name: None)

    with pytest.raises(RuntimeError, match="FFmpeg bulunamadı"):
        AudioConverter()
