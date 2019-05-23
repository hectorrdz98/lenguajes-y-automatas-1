# -*- mode: python -*-

block_cipher = None


a = Analysis(['lexico.py'],
             pathex=['C:\\Users\\1ZW05LA_RS4\\Documents\\ITQ\\4 semestre\\Lenguajes y Autómatas\\lenguajes-y-automatas-1\\Unidad5\\exe'],
             binaries=[],
             datas=[],
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
          name='lexico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
