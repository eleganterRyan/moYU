import tkinter as tk
from PIL import ImageGrab
import keyboard
import time

class ScreenshotTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True, '-alpha', 0.3)
        self.root.configure(background='grey')
        
        # 初始化坐标
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # 绑定鼠标事件
        self.root.bind('<Button-1>', self.start_selection)
        self.root.bind('<B1-Motion>', self.update_selection)
        self.root.bind('<ButtonRelease-1>', self.end_selection)
        
        # 绑定ESC键退出
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # 提示文本
        self.canvas.create_text(
            self.root.winfo_screenwidth()//2,
            30,
            text="请框选要截图的区域（按ESC退出）",
            fill='white',
            font=('Arial', 14)
        )
        
    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def update_selection(self, event):
        if self.start_x and self.start_y:
            self.current_x = event.x
            self.current_y = event.y
            self.canvas.delete('selection')
            self.canvas.create_rectangle(
                self.start_x, self.start_y,
                self.current_x, self.current_y,
                outline='red',
                width=2,
                tags='selection'
            )
            
    def end_selection(self, event):
        if self.start_x and self.start_y:
            # 确保坐标是从左上到右下
            left = min(self.start_x, self.current_x)
            top = min(self.start_y, self.current_y)
            right = max(self.start_x, self.current_x)
            bottom = max(self.start_y, self.current_y)
            
            # 隐藏窗口
            self.root.withdraw()
            
            # 等待一下让窗口完全消失
            time.sleep(0.2)
            
            # 截图
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            screenshot.save("word_bg.png")
            print("背景图片已保存为 word_bg.png")
            
            self.root.quit()

def capture_screen():
    app = ScreenshotTool()
    app.root.mainloop()

if __name__ == "__main__":
    capture_screen() 