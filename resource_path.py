import os
import sys
import tempfile

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        # PyInstaller创建临时文件夹,将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def extract_bg_image():
    """ 从exe中提取背景图片到临时文件 """
    try:
        # 获取背景图片路径
        bg_path = resource_path("word_bg.png")
        
        # 如果直接运行py文件，直接返回路径
        if os.path.isfile(bg_path):
            return bg_path
            
        # 如果是exe运行，复制到临时文件
        temp_dir = tempfile.gettempdir()
        temp_bg_path = os.path.join(temp_dir, "word_bg.png")
        
        # 复制文件
        with open(bg_path, 'rb') as src, open(temp_bg_path, 'wb') as dst:
            dst.write(src.read())
            
        return temp_bg_path
        
    except Exception as e:
        print(f"提取背景图片时出错: {str(e)}")
        return None 