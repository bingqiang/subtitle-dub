from tqdm import tqdm
import time
 
# 模拟耗时操作
for i in tqdm(range(1024)):
    # 每次循环都会更新进度条显示当前进度
    time.sleep(0.1)