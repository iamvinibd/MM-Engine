# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['MMEngine.py'],
             pathex=['C:\\Users\\vinicius.diniz\\PycharmProjects\\MM Engine'],
             binaries=[],
             datas=[],
             hiddenimports=['dblib'],
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
          name='MMEngine',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='lg_2V1_icon.ico')
