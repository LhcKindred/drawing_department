import os
import shutil
from tkinter import Tk, filedialog, messagebox

# 选择源文件夹
Tk().withdraw()
source_dir = filedialog.askdirectory(title="选择源文件夹")
if not source_dir:
    print("未选择文件夹，程序结束。")
    exit()

# 新文件夹名（在原目录旁边生成）
parent_dir = os.path.dirname(source_dir)
base_name = os.path.basename(source_dir)
new_dir = os.path.join(parent_dir, base_name + "_empty")

# 如果新文件夹已存在，先删除
if os.path.exists(new_dir):
    shutil.rmtree(new_dir)
os.makedirs(new_dir)

# 遍历原文件夹下的一级子文件夹
for item in os.listdir(source_dir):
    sub_path = os.path.join(source_dir, item)
    if os.path.isdir(sub_path):
        os.makedirs(os.path.join(new_dir, item))

# 生成完成弹窗提示
messagebox.showinfo("完成", f"新文件夹已生成在：\n{new_dir}")
