import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": [ "tkinter", "customtkinter", "requests", "pathlib","threading", "shutil", "PIL", "keyboard", "cv2"], 'include_files':["icon.ico"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="PontoOnline",
    version="0.1",
    description="Minha 1° Aplicação!",
    options={"build_exe":  build_exe_options},
    executables=[Executable("main.py", base=base, icon="icon.ico")]
)