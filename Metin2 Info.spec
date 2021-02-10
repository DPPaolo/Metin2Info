# -*- mode: python -*-

a = Analysis(['C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\Metin2 Info.py'],
             pathex=['C:\\Python34\\Scripts'],
             binaries=None,
             datas= [
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\item_proto_dump.xml', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\mob_proto_dump.xml', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\itemdesc.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\item_list.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\mob_list.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\item_proto_dump_en.xml', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\mob_proto_dump_en.xml', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\itemdesc_en.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\item_list_en.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\mob_list_en.txt', 'file'),
			   ('C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\Metin2.ico', 'file'),
			   
			   ],
             hiddenimports=["os", "sys", "platform", "shutil", "re", "threading", "webbrowser", "datetime", "logging", "string", "time", "urllib"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Metin2 Info',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='C:\\Users\\Paolo\\OneDrive\\Miei Tool\\Metin\\file\\Metin2.ico')