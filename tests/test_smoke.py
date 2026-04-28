"""
tests/test_smoke.py — Temel modül import ve sözleşme doğrulamaları

Issue #5 kapsamında uygulamanın ana modüllerinin import edilebilirliğini
ve `Config` sözleşmesinin beklenen anahtarlarını doğrular.
"""

import importlib
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest


def _import_module(module_name: str, *, shim_docx2pdf: bool = False) -> ModuleType:
    """İstenirse docx2pdf shim'i ile modülü temiz şekilde import eder."""
    sys.modules.pop(module_name, None)

    if not shim_docx2pdf:
        return importlib.import_module(module_name)

    with patch.dict(sys.modules, {"docx2pdf": MagicMock()}, clear=False):
        return importlib.import_module(module_name)


def test_main_imports():
    """Ana giriş modülü import edilebilmeli ve temel callables mevcut olmalı."""
    main_module = _import_module("main")

    assert callable(main_module.load_languages)
    assert callable(main_module.init_state)
    assert callable(main_module.main)


def test_core_modules_import():
    """Core modülleri temel sınıflarıyla birlikte import edilebilmeli."""
    converter_module = _import_module("core.converter", shim_docx2pdf=True)
    player_module = _import_module("core.player")
    viewer_module = _import_module("core.viewer")
    ai_engine_module = _import_module("core.ai_engine")

    assert hasattr(converter_module, "FileConverter")
    assert hasattr(player_module, "AudioConverter")
    assert hasattr(viewer_module, "FileViewer")
    assert hasattr(ai_engine_module, "AIEngine")


def test_ui_modules_import():
    """UI modülleri beklenen sembolleriyle import edilebilmeli."""
    styles_module = _import_module("ui.styles")
    dashboard_module = _import_module("ui.dashboard")

    assert callable(styles_module.apply_custom_css)
    assert hasattr(dashboard_module, "Dashboard")
    assert hasattr(dashboard_module, "_FORMAT_MAP")


def test_config_class_attrs():
    """Config sözleşmesindeki temel alanlar beklenen tiplerde olmalı."""
    config_module = _import_module("config.settings")
    config = config_module.Config

    assert isinstance(config.APP_NAME, str)
    assert isinstance(config.VERSION, str)
    assert config.DEFAULT_LANGUAGE in {"tr", "en"}
    assert hasattr(config, "GEMINI_API_KEY")
    assert isinstance(config.SUPPORTED_EXTENSIONS, list)
    assert config.SUPPORTED_EXTENSIONS
    assert all(ext.startswith(".") for ext in config.SUPPORTED_EXTENSIONS)


def test_import_module_raises_for_missing_module():
    """Geçersiz modül adı helper üzerinden beklenen hatayı üretmeli."""
    with pytest.raises(ModuleNotFoundError):
        _import_module("does_not_exist.anywhere")
