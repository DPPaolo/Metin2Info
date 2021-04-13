# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['metin2Info\\Metin2Info.py'],
             pathex=['C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin2Info'],
             binaries=[],
             datas=[
             ('metin2Info\\file\\*.*', 'file'),
             ('metin2Info\\assets\\icon\\*.*', 'assets\\icon'),
             ('metin2Info\\assets\\image\\*.*', 'assets\\image'),
             ('metin2Info\\translation\\*.qm', 'translation'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Metin2 Info',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='metin2Info\\assets\\icon\\Metin2.ico')