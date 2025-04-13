# -*- mode: python ; coding: utf-8 -*-

import sys
import os

from kivy_deps import sdl2, glew

from kivymd import hooks_path as kivymd_hooks_path

path = os.path.abspath(".")

a = Analysis(
    ["version2.0.py"],
    pathex=[path],
    hookspath=[kivymd_hooks_path],
    hiddenimports=[
        "kivymd.icon_definitions",
        "kivymd.uix.button",
        "kivymd.uix.label",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Include kv and DB file
a.datas += [
    ('version2.kv', 'D:\\Python PC\\KivyMD\\Archive_system\\version2.kv', 'DATA'),
    ('archive.db', 'D:\\Python PC\\KivyMD\\Archive_system\\data\\archive.db', 'DATA')
    ]

# Include entire folders
a.datas += Tree(os.path.join(path, "Image"), prefix="Image")


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    debug=False,
    strip=False,
    upx=True,
    name="xSAVE",
    icon=os.path.join(path, "Image", "Icon.ico"),
    console=False,
)