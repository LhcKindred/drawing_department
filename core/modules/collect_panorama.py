from tkinter import filedialog, messagebox
import os
import shutil

def collect_panorama():
    src_folder = filedialog.askdirectory(title="选择源文件夹")
    if not src_folder:
        messagebox.showinfo("提示", "未选择文件夹，操作取消。")
        return

    collected_folder = os.path.join(src_folder, "全景文件收集")
    os.makedirs(collected_folder, exist_ok=True)

    skipped, processed = [], 0

    for subfolder in os.listdir(src_folder):
        subfolder_path = os.path.join(src_folder, subfolder)
        if not os.path.isdir(subfolder_path) or subfolder == "全景文件收集":
            continue

        panorama_file = None
        for file in os.listdir(subfolder_path):
            if file.lower().endswith(".jpg") and "全景" in file:
                panorama_file = file
                break

        if not panorama_file:
            skipped.append(subfolder)
            continue

        shutil.move(os.path.join(subfolder_path, panorama_file), os.path.join(collected_folder, f"{subfolder}.jpg"))
        processed += 1

    msg = f"处理完成！\n成功移动 {processed} 个全景图片。"
    if skipped:
        msg += f"\n\n以下子文件夹未找到全景图片，已跳过：\n" + "\n".join(skipped)
    messagebox.showinfo("完成", msg)
