import PyInstaller.__main__
from os import getcwd


PyInstaller.__main__.run(
    [
        "_signal.py",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--hide-console=hide-early",
        "--icon=common/data/style/logo_triangle.ico",
        f"--distpath={getcwd()}",
        "--log-level=INFO",
    ]
)
