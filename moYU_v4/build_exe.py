import sys
from cx_Freeze import setup, Executable

# 构建选项
build_exe_options = {
    "packages": [
        "tkinter", 
        "PIL", 
        "cv2", 
        "numpy", 
        "pystray"
    ],
    "include_files": [
        "word_bg.png",
        "word.ico"
    ],
    "excludes": [
        "matplotlib",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "IPython",
        "jupyter"
    ],
    "optimize": 2,
}

# 可执行文件设置
executables = [
    Executable(
        "fake_word.py",
        base="Win32GUI",
        icon="word.ico",
        target_name="FakeWord.exe",
        shortcut_name="FakeWord",
        shortcut_dir="DesktopFolder"
    )
]

# 设置信息
setup(
    name="FakeWord",
    version="4.0",
    description="FakeWord Application",
    options={"build_exe": build_exe_options},
    executables=executables
) 