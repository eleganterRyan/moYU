import requests
from PIL import Image
import io

def download_word_icon():
    # Word图标的URL
    icon_url = "https://img.icons8.com/color/48/000000/microsoft-word-2019--v2.png"
    
    try:
        # 下载图标
        response = requests.get(icon_url)
        if response.status_code == 200:
            # 将下载的内容转换为图片
            img = Image.open(io.BytesIO(response.content))
            
            # 创建不同尺寸的图标
            sizes = [(16,16), (32,32), (48,48), (64,64), (128,128)]
            
            # 保存为ico文件
            img.save('word.ico', format='ICO', sizes=sizes)
            print("Word图标已成功下载并保存为word.ico")
        else:
            print(f"下载失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == '__main__':
    download_word_icon() 