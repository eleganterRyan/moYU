import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from resource_path import resource_path, extract_bg_image

class FakeWord:
    def __init__(self, root):
        self.root = root
        self.root.title("Word")
        
        # 移除标题栏
        self.root.overrideredirect(True)
        
        # 加载原始背景图片
        self.bg_image_path = extract_bg_image()
        if not self.bg_image_path:
            messagebox.showerror("错误", "无法加载背景图片")
            root.destroy()
            return
            
        self.original_image = Image.open(self.bg_image_path)
        self.original_width = self.original_image.width
        self.original_height = self.original_image.height
        
        # 设置初始窗口大小
        self.root.geometry(f"{self.original_width}x{self.original_height}")
        
        # 获取编辑区域的相对位置和大小比例
        self.get_editor_proportions()
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # 加载背景图片
        self.load_background()
        
        # 创建文本编辑区
        self.create_text_area()
        
        # 添加拖动功能
        self.add_drag_functionality()
        
        # 绑定窗口调整大小事件
        self.root.bind('<Configure>', self.on_resize)
        
        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        
        # 添加关闭快捷键 (Alt+F4)
        self.root.bind('<Alt-F4>', lambda e: self.root.destroy())
        
        # 添加窗口控制按钮
        self.add_window_controls()
        
        # 保存窗口原始大小和位置
        self.saved_geometry = None

    def get_editor_proportions(self):
        # 获取编辑区域的位置和大小
        img = cv2.imread(self.bg_image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 找到最大的白色区域
        max_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                x, y, w, h = cv2.boundingRect(contour)
                # 保存相对位置和大小比例
                self.editor_x_ratio = x / self.original_width
                self.editor_y_ratio = y / self.original_height
                self.editor_w_ratio = w / self.original_width
                self.editor_h_ratio = h / self.original_height
        
        # 如果没有检测到，使用默认值
        if not hasattr(self, 'editor_x_ratio'):
            self.editor_x_ratio = 0.2
            self.editor_y_ratio = 0.2
            self.editor_w_ratio = 0.6
            self.editor_h_ratio = 0.6

    def load_background(self):
        # 创建背景标签
        self.bg_label = tk.Label(self.main_frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background()

    def update_background(self):
        # 获取当前窗口大小
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 调整图片大小
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.configure(image=self.bg_image)

    def create_text_area(self):
        self.text_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            font=("仿宋", 30),
            bg='white',
            fg='black',
            insertbackground='black',
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.update_text_area_position()

    def update_text_area_position(self):
        # 获取当前窗口大小
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 计算文本区域的位置和大小
        x = int(width * self.editor_x_ratio)
        y = int(height * self.editor_y_ratio)
        w = int(width * self.editor_w_ratio)
        h = int(height * self.editor_h_ratio)
        
        # 更新文本区域位置和大小
        self.text_area.place(x=x, y=y, width=w, height=h)

    def on_resize(self, event):
        # 忽略子组件的调整大小事件
        if event.widget != self.root:
            return
            
        # 更新背景图片和文本区域
        self.update_background()
        self.update_text_area_position()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            try:
                # 保持标题为"Word"
                self.root.title("Word")
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.delete(1.0, tk.END)
                    content = file.read()
                    self.text_area.insert(1.0, content)
                    # 确保整个文本都使用仿宋字体和四号大小
                    self.text_area.tag_add("font", "1.0", tk.END)
                    self.text_area.tag_config("font", font=("仿宋", 14))
            except Exception as e:
                self.root.title("Word")  # 错误时也保持标题为"Word"
                messagebox.showerror("错误", f"无法打开文件: {str(e)}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("错误", f"无法保存文件: {str(e)}")

    def add_drag_functionality(self):
        # 绑定拖动事件到背景标签上
        self.bg_label.bind('<Button-1>', self.start_drag)
        self.bg_label.bind('<B1-Motion>', self.on_drag)
        
        # 设置鼠标样式
        self.bg_label.bind('<Enter>', lambda e: self.bg_label.configure(cursor='arrow'))

    def start_drag(self, event):
        # 只有点击顶部区域才能拖动
        if event.y < 120:  # 可以调整这个值来改变可拖动区域的高度
            self.x = event.x
            self.y = event.y
        else:
            self.x = None
            self.y = None

    def on_drag(self, event):
        if hasattr(self, 'x') and self.x is not None:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
            
            # 检查是否拖动到屏幕顶部
            if y < 10 and self.saved_geometry is None:
                self.toggle_maximize()
            # 如果已经最大化，且向下拖动，则还原窗口
            elif y > 10 and self.saved_geometry is not None:
                # 计算还原后的位置，使窗口跟随鼠标
                self.root.geometry(self.saved_geometry)
                self.saved_geometry = None
                self.max_btn.config(text='□')
                # 更新拖动起始位置
                self.x = event.x
                self.y = event.y

    def add_window_controls(self):
        # 创建窗口控制按钮框架
        control_frame = tk.Frame(self.main_frame)
        control_frame.place(x=self.original_width-120, y=0, width=120, height=30)
        
        # 设置按钮样式
        button_style = {
            'bd': 0,
            'padx': 10,
            'height': 1,
            'relief': tk.FLAT,
            'font': ('Arial', 10)
        }
        
        # 最小化按钮
        min_btn = tk.Button(control_frame, text='─', command=self.minimize_window, **button_style)
        min_btn.pack(side=tk.LEFT)
        
        # 最大化/还原按钮
        self.max_btn = tk.Button(control_frame, text='□', command=self.toggle_maximize, **button_style)
        self.max_btn.pack(side=tk.LEFT)
        
        # 关闭按钮
        close_btn = tk.Button(control_frame, text='×', command=self.root.destroy, **button_style)
        close_btn.pack(side=tk.LEFT)

    def minimize_window(self):
        self.root.iconify()

    def toggle_maximize(self):
        if self.saved_geometry is None:
            # 保存当前位置和大小
            self.saved_geometry = self.root.geometry()
            # 最大化窗口
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}+0+0")
            self.max_btn.config(text='❐')
        else:
            # 还原窗口
            self.root.geometry(self.saved_geometry)
            self.saved_geometry = None
            self.max_btn.config(text='□')

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeWord(root)
    root.mainloop() 