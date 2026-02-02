# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

sep = ';' if sys.platform.startswith('win') else ':'

added_files = [
    ("Assets/Fonts/", "Assets/Fonts"),
    ("Assets/Images/", "Assets/Images"),
    ("Assets/Icon/", "Assets/Icon")
]

a = Analysis(
    ['PriceCalc.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Kalkulacka',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Assets/Icon/calculatorICO.ico' if sys.platform.startswith('win') else 'Assets/Icon/calculatorICNS.icns'
)

app = BUNDLE(
    exe,
    name='Kalkulacka.app',
    bundle_identifier='com.Lander.Kalkulacka'
)
