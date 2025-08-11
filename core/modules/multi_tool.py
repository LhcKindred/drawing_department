import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------- 功能 1：JPG + PTS 收集 ----------------
def select_folder():
    return filedialog.askdirectory(title="选择主文件夹")

def func_jpg_pts():
    main_folder = select_folder()
    if not main_folder:
        messagebox.showinfo("提示", "未选择文件夹，操作取消。")
        return

    collected_folder = os.path.join(main_folder, "调色前全景照片")
    os.makedirs(collected_folder, exist_ok=True)

    skipped, processed = [], 0

    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
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

# ---------------- 功能 2：“全景” 图片收集 ----------------
def func_panorama():
    main_folder = select_folder()
    if not main_folder:
        messagebox.showinfo("提示", "未选择文件夹，操作取消。")
        return

    collected_folder = os.path.join(main_folder, "全景文件收集")
    os.makedirs(collected_folder, exist_ok=True)

    skipped, processed = [], 0

    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
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

# ---------------- UI 主界面 ----------------
def main():
    root = tk.Tk()
    root.title("多功能文件收集工具")
    root.geometry("380x320")
    root.resizable(False, False)

    # 如果有图标文件（icon.ico），设置图标
    if os.path.exists("icon.ico"):
        root.iconbitmap("icon.ico")

    root.configure(bg="#F0F4F8")  # 背景色

    label = tk.Label(root, text="请选择需要执行的功能：", font=("微软雅黑", 13), bg="#F0F4F8", fg="#333")
    label.pack(pady=20)

    def create_button(text, command, color):
        btn = tk.Button(root, text=text, command=command, font=("微软雅黑", 11),
                        bg=color, fg="white", activebackground="#4FA3F7",
                        relief="flat", width=30, height=2, cursor="hand2")
        btn.pack(pady=5)
        return btn

    btn1 = create_button("📁 收集并重命名 JPG+PTS", func_jpg_pts, "#2196F3")
    btn2 = create_button("🖼 收集“全景”图片", func_panorama, "#4CAF50")
    btn_exit = create_button("❌ 退出", root.quit, "#E53935")

    root.mainloop()

if __name__ == "__main__":
    main()
