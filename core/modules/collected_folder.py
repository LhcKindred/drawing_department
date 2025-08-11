import os
import shutil
from tkinter import filedialog, Tk, messagebox

# 选择主文件夹
root = Tk()
root.withdraw()
main_folder = filedialog.askdirectory(title="选择主文件夹")
if not main_folder:
    messagebox.showinfo("提示", "未选择文件夹，程序结束。")
    exit()

# 新建收集文件夹
collected_folder = os.path.join(main_folder, "调色前全景照片")
os.makedirs(collected_folder, exist_ok=True)

skipped = []  # 记录缺少所需文件的子文件夹
processed = 0

# 遍历子文件夹
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)

    # 跳过非文件夹和调色前全景照片文件夹
    if not os.path.isdir(subfolder_path) or subfolder == "调色前全景照片":
        continue

    # 找出子文件夹中的jpg和pts文件
    jpg_file = None
    pts_file = None
    for file in os.listdir(subfolder_path):
        if file.lower().endswith(".jpg"):
            jpg_file = file
        elif file.lower().endswith(".pts"):
            pts_file = file

    if not jpg_file or not pts_file:
        skipped.append(subfolder)
        continue

    # 重命名并移动到收集文件夹
    new_jpg_name = f"{subfolder}.jpg"
    new_pts_name = f"{subfolder}.pts"
    shutil.move(os.path.join(subfolder_path, jpg_file), os.path.join(collected_folder, new_jpg_name))
    shutil.move(os.path.join(subfolder_path, pts_file), os.path.join(collected_folder, new_pts_name))
    processed += 1

# 总结提示
msg = f"处理完成！\n\n成功移动 {processed} 个子文件夹中的文件。"
if skipped:
    msg += f"\n\n以下子文件夹缺少 .jpg 或 .pts，已跳过：\n" + "\n".join(skipped)
messagebox.showinfo("完成", msg)
