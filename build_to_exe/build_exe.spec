# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# 專案根目錄
project_root = Path.cwd()

# 收集所有資源檔案
def collect_data_files():
    data_files = []
    assets_dir = project_root / 'assets'
    
    if assets_dir.exists():
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                source = os.path.join(root, file)
                # 計算相對於專案根目錄的路徑
                rel_path = os.path.relpath(source, project_root)
                # 目標路徑保持相同的目錄結構
                target_dir = os.path.dirname(rel_path)
                data_files.append((source, target_dir))
    
    return data_files

# 收集隱藏的模組導入
hiddenimports = [
    'pygame',
    'pygame.mixer',
    'pygame.font',
    'pygame.image',
    'pygame.transform',
    'pygame.display',
    'pygame.event',
    'pygame.key',
    'pygame.time',
    'pygame.sprite',
    'json',
    'os',
    'sys',
    'time',
    'random',
    'heapq',
    'locale',
    'webbrowser'
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=collect_data_files(),
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EscapeFromQinShiHuang',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 設為 False 隱藏控制台視窗
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # 設定應用程式圖示
)
