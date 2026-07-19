# PyInstaller spec for Video Studio.
#
# Bundles the bundled ffmpeg binary (from imageio-ffmpeg), the app's fonts and
# icon, and the PySide6 Qt Multimedia backend into a single windowed app.
# Build with:  pyinstaller VideoStudio.spec

from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

datas = [("videostudio/assets", "videostudio/assets")]
# imageio-ffmpeg ships the ffmpeg executable as package data.
datas += collect_data_files("imageio_ffmpeg")
binaries = collect_dynamic_libs("imageio_ffmpeg")

block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets",
        "PySide6.Qt3DCore", "PySide6.QtCharts", "PySide6.QtDataVisualization",
        "tkinter",
    ],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Video Studio",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon="packaging/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Video Studio",
)
