from tkinter import filedialog, messagebox
import os
import shutil

def collect_jpg_pts():
    src_folder = filedialog.askdirectory(title="选择源文件夹")
    if not src_folder:
        messagebox.showinfo("提示", "未选择文件夹，操作取消。")
        return

    collected_folder = os.path.join(src_folder, "调色前全景照片")
    os.makedirs(collected_folder, exist_ok=True)

    skipped, processed = [], 0

    for subfolder in os.listdir(src_folder):
        subfolder_path = os.path.join(src_folder, subfolder)
        if not os.path.isdir(subfolder_path) or subfolder == "调色前全景照片":
            continue

        jpg_file, pts_file = None, None
        for file in os.listdir(subfolder_path):
            if file.lower().endswith(".jpg"):
                jpg_file = file
            elif file.lower().endswith(".pts"):
                pts_file = file

        if not jpg_file or not pts_file:
            skipped.append(subfolder)
            continue

        shutil.move(os.path.join(subfolder_path, jpg_file), os.path.join(collected_folder, f"{subfolder}.jpg"))
        shutil.move(os.path.join(subfolder_path, pts_file), os.path.join(collected_folder, f"{subfolder}.pts"))
        processed += 1

    msg = f"处理完成！\n成功移动 {processed} 个子文件夹的文件。"
    if skipped:
        msg += f"\n\n以下子文件夹缺少文件，已跳过：\n" + "\n".join(skipped)
    messagebox.showinfo("完成", msg)
