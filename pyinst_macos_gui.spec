# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('/Users/cdittmar/Programming/python/pytchy/icons/*.*', 'icons'),
    ('/Users/cdittmar/Programming/python/pytchy/img/Pelican1.png', 'img')
]

a = Analysis(['gui.py'],
             pathex=['/Users/cdittmar/Programming/python/pytchy'],
             binaries=[],
             datas=added_files,
             hiddenimports=['PIL._tkinter_finder'],
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
          [],
          exclude_binaries=True,
          name='gytchy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='gytchy')