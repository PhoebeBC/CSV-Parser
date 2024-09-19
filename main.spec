# -*- mode: python ; coding: utf-8 -*-

datafiles = [(r"C:\Users\phoeb\PycharmProjects\CSV-Parser\images\*", "images")]

a = Analysis(
    ['main.py'],
    pathex=["C:\\Users\\phoeb\\PycharmProjects\\CSV-Parser"],
    binaries=[],
    datas=datafiles,
    hiddenimports=['xlsxwriter', 'pandas', 'openpyxl', '_openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Accounts Formatter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
