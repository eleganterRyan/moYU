import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# 继承v1版本的代码
from fake_word import FakeWord as FakeWordV1

from resource_path import resource_path, extract_bg_image

class FakeWord(FakeWordV1):
    def __init__(self, root):
        # 获取背景图片路径
        self.bg_image_path = extract_bg_image()
        if not self.bg_image_path:
            messagebox.showerror("错误", "无法加载背景图片")
            root.destroy()
            return
            
        super().__init__(root)
        
        # 添加大小调整功能
        self.add_resize_borders()

    def add_resize_borders(self):
        # 创建8个调整区域（四边和四角）
        self.borders = []
        
        # 四个角落
        self.add_corner('nw', 0, 0)                          # 左上
        self.add_corner('ne', self.original_width-5, 0)      # 右上
        self.add_corner('sw', 0, self.original_height-5)     # 左下
        self.add_corner('se', self.original_width-5, self.original_height-5)  # 右下
        
        # 四条边
        self.add_edge('n', 5, 0, self.original_width-10, 5)           # 上边
        self.add_edge('s', 5, self.original_height-5, self.original_width-10, 5)  # 下边
        self.add_edge('w', 0, 5, 5, self.original_height-10)          # 左边
        self.add_edge('e', self.original_width-5, 5, 5, self.original_height-10)  # 右边

    def add_corner(self, pos, x, y):
        corner = tk.Frame(self.root, bg='', width=5, height=5)
        corner.place(x=x, y=y)
        
        # 设置鼠标样式
        if pos in ['nw', 'se']:
            cursor = 'size_nw_se'
        else:
            cursor = 'size_ne_sw'
            
        corner.bind('<Enter>', lambda e: corner.configure(cursor=cursor))
        corner.bind('<Leave>', lambda e: corner.configure(cursor=''))
        corner.bind('<Button-1>', lambda e, p=pos: self.start_resize(e, p))
        corner.bind('<B1-Motion>', self.do_resize)
        
        self.borders.append(corner)

    def add_edge(self, pos, x, y, width, height):
        edge = tk.Frame(self.root, bg='', width=width, height=height)
        edge.place(x=x, y=y)
        
        # 设置鼠标样式
        if pos in ['n', 's']:
            cursor = 'sb_v_double_arrow'
        else:
            cursor = 'sb_h_double_arrow'
            
        edge.bind('<Enter>', lambda e: edge.configure(cursor=cursor))
        edge.bind('<Leave>', lambda e: edge.configure(cursor=''))
        edge.bind('<Button-1>', lambda e, p=pos: self.start_resize(e, p))
        edge.bind('<B1-Motion>', self.do_resize)
        
        self.borders.append(edge)

    def start_resize(self, event, direction):
        self.resize_direction = direction
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_width = self.root.winfo_width()
        self.start_height = self.root.winfo_height()
        self.start_pos_x = self.root.winfo_x()
        self.start_pos_y = self.root.winfo_y()

    def do_resize(self, event):
        if not hasattr(self, 'resize_direction'):
            return
            
        delta_x = event.x_root - self.start_x
        delta_y = event.y_root - self.start_y
        
        new_width = self.start_width
        new_height = self.start_height
        new_x = self.start_pos_x
        new_y = self.start_pos_y
        
        # 最小窗口大小
        min_width = 600
        min_height = 400
        
        # 根据拖动方向调整窗口大小
        if 'e' in self.resize_direction:
            new_width = max(min_width, self.start_width + delta_x)
        if 'w' in self.resize_direction:
            width_diff = min(delta_x, self.start_width - min_width)
            new_width = self.start_width - width_diff
            new_x = self.start_pos_x + width_diff
        if 's' in self.resize_direction:
            new_height = max(min_height, self.start_height + delta_y)
        if 'n' in self.resize_direction:
            height_diff = min(delta_y, self.start_height - min_height)
            new_height = self.start_height - height_diff
            new_y = self.start_pos_y + height_diff
        
        # 更新窗口大小和位置
        self.root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
        
        # 强制更新窗口
        self.root.update_idletasks()
        
        # 更新所有边框和按钮位置
        self.update_border_positions()

    def update_border_positions(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 更新边框位置和大小
        for border in self.borders:
            pos = border.winfo_x(), border.winfo_y()
            
            # 更新四个角落的位置
            if pos == (0, 0):  # 左上角
                border.place(x=0, y=0)
            elif pos[0] == 0 and pos[1] >= self.original_height-10:  # 左下角
                border.place(x=0, y=height-5)
            elif pos[0] >= self.original_width-10 and pos[1] == 0:  # 右上角
                border.place(x=width-5, y=0)
            elif pos[0] >= self.original_width-10 and pos[1] >= self.original_height-10:  # 右下角
                border.place(x=width-5, y=height-5)
            
            # 更新四条边的位置和大小
            elif pos[1] == 0:  # 上边
                border.place(x=5, y=0, width=width-10)
            elif pos[1] >= self.original_height-10:  # 下边
                border.place(x=5, y=height-5, width=width-10)
            elif pos[0] == 0:  # 左边
                border.place(x=0, y=5, height=height-10)
            elif pos[0] >= self.original_width-10:  # 右边
                border.place(x=width-5, y=5, height=height-10)
        
        # 更新控制按钮位置
        if hasattr(self, 'max_btn'):
            control_frame = self.max_btn.master
            control_frame.place(x=width-90, y=3)

    def toggle_maximize(self):
        if self.saved_geometry is None:
            # 保存当前位置和大小
            self.saved_geometry = self.root.geometry()
            
            # 最大化窗口
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}+0+0")
            self.max_btn.config(text='❐')
            
            # 更新边框位置
            self.update_border_positions()
            
            # 更新控制按钮位置
            control_frame = self.max_btn.master
            control_frame.place(x=width-90, y=3)
            
        else:
            # 还原窗口
            self.root.geometry(self.saved_geometry)
            self.saved_geometry = None
            self.max_btn.config(text='□')
            
            # 更新边框位置
            self.update_border_positions()
            
            # 还原控制按钮位置
            control_frame = self.max_btn.master
            control_frame.place(x=self.original_width-90, y=3)

    def on_resize(self, event):
        # 忽略子组件的调整大小事件
        if event.widget != self.root:
            return
        
        # 更新背景图片和文本区域
        self.update_background()
        self.update_text_area_position()
        
        # 更新控制按钮位置
        width = self.root.winfo_width()
        control_frame = self.max_btn.master
        control_frame.place(x=width-90, y=3)

    def add_window_controls(self):
        # 创建窗口控制按钮框架，调整位置和大小
        control_frame = tk.Frame(self.main_frame)
        control_frame.place(x=self.original_width-90, y=3, width=85, height=25)
        
        # 设置按钮样式
        button_style = {
            'bd': 0,
            'padx': 6,
            'height': 1,
            'relief': tk.FLAT,
            'font': ('Arial', 9),
            'bg': '#F0F0F0'
        }
        
        # 最小化按钮
        min_btn = tk.Button(control_frame, text='─', command=self.minimize_window, **button_style)
        min_btn.pack(side=tk.LEFT, padx=1)
        min_btn.bind('<Enter>', lambda e: e.widget.config(bg='#E5E5E5'))
        min_btn.bind('<Leave>', lambda e: e.widget.config(bg='#F0F0F0'))
        
        # 最大化/还原按钮
        self.max_btn = tk.Button(control_frame, text='□', command=self.toggle_maximize, **button_style)
        self.max_btn.pack(side=tk.LEFT, padx=1)
        self.max_btn.bind('<Enter>', lambda e: e.widget.config(bg='#E5E5E5'))
        self.max_btn.bind('<Leave>', lambda e: e.widget.config(bg='#F0F0F0'))
        
        # 关闭按钮
        close_btn = tk.Button(control_frame, text='×', command=self.root.destroy, **button_style)
        close_btn.pack(side=tk.LEFT, padx=1)
        close_btn.bind('<Enter>', lambda e: e.widget.config(bg='#E81123', fg='white'))
        close_btn.bind('<Leave>', lambda e: e.widget.config(bg='#F0F0F0', fg='black'))

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeWord(root)
    root.mainloop()