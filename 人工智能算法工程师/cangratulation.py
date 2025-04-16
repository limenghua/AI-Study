import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 设置画布
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# 添加文字
text = ax.text(5, 8, "Happy Birthday!", fontsize=24, color='purple', ha='center', va='center', alpha=0)

# 气球数据
num_balloons = 20
balloons = {
    "x": np.random.uniform(1, 9, num_balloons),
    "y": np.random.uniform(0, 2, num_balloons),
    "colors": np.random.choice(['red', 'blue', 'green', 'yellow', 'pink', 'orange'], num_balloons),
    "sizes": np.random.uniform(50, 200, num_balloons),
    "speeds": np.random.uniform(0.02, 0.1, num_balloons)
}
scat = ax.scatter(balloons["x"], balloons["y"], s=balloons["sizes"], c=balloons["colors"], alpha=0.6)

# 更新函数
def update(frame):
    # 让文字逐渐出现
    if frame < 30:
        text.set_alpha(frame / 30)
    # 气球上升
    balloons["y"] += balloons["speeds"]
    balloons["y"] = np.where(balloons["y"] > 10, 0, balloons["y"])  # 循环回到底部
    scat.set_offsets(np.c_[balloons["x"], balloons["y"]])

# 动画
ani = animation.FuncAnimation(fig, update, frames=200, interval=50)

# 保存或展示动画
plt.show()