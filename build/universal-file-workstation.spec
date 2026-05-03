# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

spec_dir = Path(__file__).resolve().parent
project_root = spec_dir.parent

exe_script = str(project_root / "launcher.py")

a = Analysis(
    [exe_script],
    pathex=[str(project_root)],
    binaries=[
        (str(project_root / "assets" / "bin" / "ffmpeg.exe"), "assets/bin"),
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="universal-file-workstation",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
)
