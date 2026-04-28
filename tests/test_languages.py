import json
from pathlib import Path


def _load_languages():
    path = Path("assets/languages.json")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_languages_have_tr_and_en_roots():
    languages = _load_languages()
    assert "tr" in languages
    assert "en" in languages


def test_language_keys_are_symmetric_between_tr_and_en():
    languages = _load_languages()
    tr_keys = set(languages["tr"].keys())
    en_keys = set(languages["en"].keys())
    assert tr_keys == en_keys


def test_required_runtime_keys_exist():
    languages = _load_languages()
    required_keys = {
        "app_title",
        "sidebar_title",
        "home_tab",
        "convert_tab",
        "view_tab",
        "ai_tab",
        "upload_file",
        "file_uploaded",
        "btn_convert",
        "btn_download",
        "select_target_format",
        "converting_in_progress",
        "no_file_uploaded",
        "no_conversion_available",
        "sidebar_language",
        "sidebar_navigation",
        "sidebar_upload",
        "sidebar_history",
        "sidebar_settings",
        "history_empty",
        "history_files_count",
        "settings_theme",
        "settings_theme_dark",
        "settings_theme_light",
        "settings_theme_tooltip",
        "settings_default_quality",
        "settings_clear_history",
        "settings_about",
        "loading_converting",
        "loading_rendering",
        "loading_ai_processing",
        "notify_success_default",
    }
    assert required_keys.issubset(set(languages["tr"].keys()))
    assert required_keys.issubset(set(languages["en"].keys()))
