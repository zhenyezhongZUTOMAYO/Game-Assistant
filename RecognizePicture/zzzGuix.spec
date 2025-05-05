# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['zzzGuix.py'],
    pathex=[],
    binaries=[],
    datas=[('Output.py', '.'), ('SumRecognize.py', '.'), ('AvoidStick.py', '.'), ('GanTanChat.py', '.'), ('ChooseBuff.py', '.'), ('YuanDian.py', '.'), ('EnterNextLevel.py', '.'), ('Recognize.py', '.'), ('EmptyRound.py', '.'), ('Fight.py', '.')],
    hiddenimports=['pyautogui', 'pynput.keyboard', 'winsound'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='zzzGuix',
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
    uac_admin=True,
)
