import time
import random

print("正在启动加密连接...")
time.sleep(1)
print("尝试访问远程服务器...")
time.sleep(2)
for i in range(3):
    print(f"获取令牌[{i+1}/3]...")
    time.sleep(1)
print("验证成功！欢迎回来，特工编号：037")
time.sleep(1)
print("今日任务：买杯奶茶，犒赏一下辛苦的自己。")
input("按任意键关闭任务终端。")
