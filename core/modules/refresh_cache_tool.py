import tkinter as tk
from tkinter import messagebox, ttk
import threading
import os
import shutil
import subprocess
import time

def refresh_cache(progress_var):
    try:
        steps = [
            ("结束资源管理器进程", lambda: subprocess.run("taskkill /IM explorer.exe /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)),
            ("清理图标缓存", lambda: clear_icon_cache()),
            ("清理缩略图缓存", lambda: clear_thumb_cache()),
            ("清理临时文件", lambda: clear_temp()),
            ("重启资源管理器", lambda: subprocess.run("start explorer.exe", shell=True))
        ]

        for i, (desc, func) in enumerate(steps):
            progress_var.set(int((i / len(steps)) * 100))
            time.sleep(0.5)  # 模拟处理时间
            func()

        progress_var.set(100)
        time.sleep(0.5)
    except Exception as e:
        messagebox.showerror("错误", f"刷新缓存时出现问题：{e}")

def clear_icon_cache():
    icon_cache_paths = [
        os.path.join(os.getenv("LOCALAPPDATA"), "IconCache.db"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Windows", "Explorer")
    ]
    for path in icon_cache_paths:
        if os.path.isfile(path):
            try:
                os.remove(path)
            except:
                pass
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if f.lower().startswith("iconcache"):
                    try:
                        os.remove(os.path.join(path, f))
                    except:
                        pass

def clear_thumb_cache():
    thumb_cache_path = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Windows", "Explorer")
    for f in os.listdir(thumb_cache_path):
        if f.lower().startswith("thumbcache"):
            try:
                os.remove(os.path.join(thumb_cache_path, f))
            except:
                pass

def clear_temp():
    temp_path = os.getenv("TEMP")
    shutil.rmtree(temp_path, ignore_errors=True)
    os.makedirs(temp_path, exist_ok=True)

def start_refresh():
    status_win = tk.Toplevel(root)
    status_win.title("正在刷新缓存")
    status_win.geometry("350x150")
    status_win.resizable(False, False)

    tk.Label(status_win, text="正在刷新全部缓存，请稍候...", font=("Microsoft YaHei", 10)).pack(pady=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(status_win, variable=progress_var, maximum=100, length=300, mode="determinate")
    progress_bar.pack(pady=10)

    def run():
        refresh_cache(progress_var)
        status_win.destroy()
        messagebox.showinfo("完成", "缓存已刷新！请检查效果。")

    threading.Thread(target=run, daemon=True).start()

def center_window(window, width, height):
    # 获取屏幕宽高
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # 计算居中位置
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Windows 缓存刷新工具")
center_window(root, 400, 160)
root.resizable(False, False)

tk.Label(root, text="刷新 Windows 全部缓存", font=("Microsoft YaHei", 12)).pack(pady=20)
tk.Button(root, text="开始刷新", font=("Microsoft YaHei", 10), width=15, command=start_refresh).pack()

root.mainloop()
