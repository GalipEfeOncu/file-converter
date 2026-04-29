import pytest
import json
from pathlib import Path
from config.settings import Config

@pytest.fixture
def temp_prefs_path(tmp_path, monkeypatch):
    """Monkeypatch Config.PREFS_PATH to use a temporary path for testing."""
    test_prefs_path = tmp_path / "preferences.json"
    monkeypatch.setattr(Config, "PREFS_PATH", test_prefs_path)
    return test_prefs_path

def test_load_user_prefs_file_not_exists(temp_prefs_path):
    """Dosya yokken boş dictionary dönmeli."""
    assert Config.load_user_prefs() == {}

def test_save_and_load_user_prefs(temp_prefs_path):
    """Başarılı bir şekilde yazılıp okunabilmeli."""
    test_prefs = {"language": "en", "theme": "light"}
    
    Config.save_user_prefs(test_prefs)
    assert temp_prefs_path.exists()
    
    loaded_prefs = Config.load_user_prefs()
    assert loaded_prefs == test_prefs

def test_load_user_prefs_invalid_json(temp_prefs_path):
    """JSON bozuk olduğunda exception yakalayıp boş dictionary dönmeli."""
    temp_prefs_path.parent.mkdir(parents=True, exist_ok=True)
    temp_prefs_path.write_text("{invalid json", encoding="utf-8")
    
    assert Config.load_user_prefs() == {}
