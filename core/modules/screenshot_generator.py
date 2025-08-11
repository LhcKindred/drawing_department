import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# ==== 配置 ====
output_folder = '生成的朋友圈截图'
os.makedirs(output_folder, exist_ok=True)

# 基础模板图 - 关键！请将您提供的截图保存为 'template_wechat_moment.jpg'
base_template_path = "template_wechat_moment.jpg"
if not os.path.exists(base_template_path):
    print(f"错误：基础模板图 '{base_template_path}' 不存在，请确保已将真实朋友圈截图放置在此路径。")
    exit()

# 字体设置（Windows 可用微软雅黑，跨平台建议使用思源黑体等开源字体）
# 确保字体文件 'msyh.ttc' 在脚本同级目录或系统字体路径中
try:
    font_name = ImageFont.truetype("msyh.ttc", 40) # 调整字体大小，使其在1080宽度下更合适
    font_text_color = (50, 50, 50) # 微信名颜色，接近深灰色
except IOError:
    print("警告：未找到字体文件 'msyh.ttc'，请确保字体已安装或指定正确路径。")
    print("将使用默认字体和颜色，显示效果可能不佳。")
    font_name = ImageFont.load_default()
    font_text_color = (0, 0, 0) # 默认黑色

# 读取员工名单
employees_excel_path = "employees.xlsx"
if not os.path.exists(employees_excel_path):
    print(f"错误：员工名单文件 '{employees_excel_path}' 不存在。")
    exit()
df = pd.read_excel(employees_excel_path)

# ==== 元素位置和尺寸 (根据您提供的模板图估算和缩放) ====
# 这些数值是基于您的 '屏幕截图 2025-07-25 091754.jpg' 估算并按比例缩放至1080宽度后的结果
# ！！！请务必根据实际生成效果进行微调！！！
AVATAR_POS = (57, 648)  # 头像左上角坐标 (x, y)
AVATAR_SIZE = (115, 115) # 头像目标尺寸（方形）

NAME_POS = (187, 655)  # 微信名文本的左上角坐标 (x, y)

# 朋友圈背景图覆盖区域 (在整个模板图上的位置和尺寸)
# 对应模板图中上方蓝色/黑色背景区域，及其内容（如动画女孩）
BACKGROUND_COVER_AREA_ON_TEMPLATE = (0, 0, 1080, 619) # (left, top, right, bottom)
# 背景图粘贴到模板图上的目标位置，通常就是 BACKGROUND_COVER_AREA_ON_TEMPLATE 的左上角
BACKGROUND_PASTE_POS = (0, 0) 

# --- 开始批量生成 ---
for index, row in df.iterrows():
    name = row['Name']
    avatar_path = row['Avatar']
    background_path = row['Background'] # 假设员工的背景图是与模板图上方背景区尺寸一致的图片

    # 检查文件是否存在
    if not os.path.exists(avatar_path):
        print(f"警告：员工 {name} 的头像文件 '{avatar_path}' 不存在，跳过此员工或使用默认。")
        continue # 如果你希望用默认，这里可以改成 pass 并加载一个默认头像
    if not os.path.exists(background_path):
        print(f"警告：员工 {name} 的背景文件 '{background_path}' 不存在，跳过此员工或使用模板自带背景。")
        # 这里我们选择跳过，如果想使用模板自带背景，则注释掉 continue
        # continue 
        pass 


    # 1. 加载基础模板图
    # 调整模板图大小以匹配目标宽度，并确保是 RGB 模式
    base_template_img = Image.open(base_template_path)
    # 计算新的高度以保持比例
    original_template_width, original_template_height = base_template_img.size
    target_template_height = int(original_template_height * (BACKGROUND_COVER_AREA_ON_TEMPLATE[2] / original_template_width))
    img = base_template_img.resize((BACKGROUND_COVER_AREA_ON_TEMPLATE[2], target_template_height)).convert("RGB") 


    draw = ImageDraw.Draw(img)
    
    # 2. 处理并粘贴朋友圈背景图（覆盖模板上相应区域）
    if os.path.exists(background_path): # 只有当背景图存在时才进行替换
        try:
            user_background = Image.open(background_path).convert("RGB")
            # 缩放背景图以适应覆盖区域的尺寸
            user_background = user_background.resize((BACKGROUND_COVER_AREA_ON_TEMPLATE[2] - BACKGROUND_COVER_AREA_ON_TEMPLATE[0],
                                                      BACKGROUND_COVER_AREA_ON_TEMPLATE[3] - BACKGROUND_COVER_AREA_ON_TEMPLATE[1]))
            img.paste(user_background, BACKGROUND_PASTE_POS)
        except Exception as e:
            print(f"警告：处理员工 {name} 的背景图失败 ({e})，将使用模板自带背景。")
    else:
        print(f"提示：员工 {name} 未提供背景图，将使用模板自带背景。")


    # 3. 处理并粘贴头像 (方形头像，无需圆形处理)
    try:
        user_avatar = Image.open(avatar_path).convert("RGBA") # 转换为RGBA以保留透明度
        # 缩放头像到指定尺寸
        user_avatar = user_avatar.resize(AVATAR_SIZE)
        # 粘贴头像，这里不需要 mask，因为不是圆形头像
        img.paste(user_avatar, AVATAR_POS, user_avatar) # 传入 user_avatar 作为 mask 以处理可能的透明背景
    except Exception as e:
        print(f"警告：处理员工 {name} 的头像失败 ({e})，将使用模板自带头像区域。")
        # 如果头像处理失败，可以考虑在这里用一个空白区域填充或不做处理

    # 4. 写入微信名（覆盖模板上原有名称）
    # 可以先填充一个小矩形来“擦除”原有的名字，确保新名字清晰
    # 这需要精确测量原名字的区域大小
    # 这里我们简化处理，直接在指定位置写，如果新名字比旧名字短，可能会有残留
    # 最佳实践是计算文本宽度和高度，然后填充一个合适的矩形
    text_bbox = draw.textbbox(NAME_POS, name, font=font_name) # 获取文本边界框
    # 填充一个白色矩形覆盖旧名字区域（需要精确计算，这里只是示意）
    # 例如：draw.rectangle((NAME_POS[0], NAME_POS[1], NAME_POS[0] + 200, NAME_POS[1] + 50), fill=(255,255,255))
    
    draw.text(NAME_POS, name, fill=font_text_color, font=font_name)

    # 5. 保存生成的图片
    output_file_path = os.path.join(output_folder, f"{name}.jpg")
    img.save(output_file_path)
    print(f"已生成 {name} 的朋友圈截图至 {output_file_path}")

print("\n所有朋友圈截图已生成！")