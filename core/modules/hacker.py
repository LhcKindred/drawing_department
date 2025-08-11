import random
import time
import os

chars = "01*#$%&@"

try:
    while True:
        line = "".join(random.choice(chars) for _ in range(80))
        print(line)
        time.sleep(0.05)
except KeyboardInterrupt:
    os.system("cls")
    print("你...看到的，都是幻觉。")
