# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:\\Users\\70060\\Documents\\DCU_Config_Tool\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/70060/AppData/Local/Programs/Python/Python310/lib/site-packages/xmlschema', 'xmlschema/'), 
            ('C:/Users/70060/AppData/Local/Programs/Python/Python310/lib/site-packages/openpyxl', 'openpyxl/'), 
            ('data/aclara.png', 'data/'),
            ('data/location_data.json', 'data/'),
            ('data/time_zone_data.json', 'data/'),
            ('data/DCU+2XLS.xsd', 'data/'),
            ('data/DCU2+XLS_TEMPLATE.xml', 'data/'),
            ('SAMPLE_IMPORT_DATA/sample_freqs.json', 'SAMPLE_IMPORT_DATA/'),
            ('SAMPLE_IMPORT_DATA/sample_wkst_entries.json', 'SAMPLE_IMPORT_DATA/'),
            ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DCU Config Tool', # Name of executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Console will not be shown
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
