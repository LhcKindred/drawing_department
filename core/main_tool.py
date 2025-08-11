import sys
import os
import tkinter as tk
from tkinter import ttk

# # 确保子模块被 PyInstaller 收集
# import tkinter.filedialog
# import tkinter.messagebox


# # -------- 资源路径函数（支持打包和开发环境） --------
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS  # PyInstaller 解包路径
#     except AttributeError:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # -------- 导入模块目录 --------
# modules_path = resource_path("modules")
# if modules_path not in sys.path:
#     sys.path.append(modules_path)

# # 让 Python 知道去 modules 文件夹找模块
# sys.path.append(resource_path("modules"))

# -------- 导入功能模块 --------
from modules.collect_jpg_pts import collect_jpg_pts
from modules.collect_panorama import collect_panorama

# -------- 主程序 UI --------
def main():
    root = tk.Tk()
    root.title("多功能文件收集工具")
    center_window(root, 400, 280)
    root.resizable(False, False)

    # 主题样式
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("微软雅黑", 11), padding=6, relief="flat", foreground="white")
    style.map("TButton", background=[("active", "#4CAF50"), ("!active", "#2196F3")])

    style.configure("Exit.TButton", font=("微软雅黑", 11), padding=6, relief="flat",
                    foreground="white", background="#f44336")
    style.map("Exit.TButton", background=[("active", "#d32f2f"), ("!active", "#f44336")])

    # 界面布局
    tk.Label(root, text="请选择需要执行的功能：", font=("微软雅黑", 14)).pack(pady=20)
    ttk.Button(root, text="收集并重命名 JPG+PTS", width=30, command=collect_jpg_pts).pack(pady=10)
    ttk.Button(root, text="收集“全景”图片", width=30, command=collect_panorama).pack(pady=10)
    ttk.Button(root, text="退出", width=30, style="Exit.TButton", command=root.quit).pack(pady=15)

    root.mainloop()

def center_window(window, width, height):
    # 获取屏幕宽高
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # 计算居中位置
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    main()
