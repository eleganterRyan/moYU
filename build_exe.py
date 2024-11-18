import PyInstaller.__main__
import sys
import os

# 确保当前目录是脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 配置打包选项
PyInstaller.__main__.run([
    'fake_word.py',     # 改为使用fake_word.py作为主程序文件
    '--name=myWord',      # exe文件的名称
    '--windowed',       # 不显示控制台窗口
    '--onefile',        # 打包成单个exe文件
    '--icon=word.ico',  # 程序图标
    '--add-data=word_bg.png;.',  # 添加背景图片
    '--clean',          # 清理临时文件
    '--noconfirm',      # 不询问确认
]) 