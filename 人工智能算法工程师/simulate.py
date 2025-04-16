import numpy as np
import matplotlib.pyplot as plt
import math
import random

# ================ 1. 定义目标函数 ================
def target_function(x):
    return x**2 + 10 * np.sin(x)

# ================ 2. 模拟退火算法实现 ================
def simulated_annealing(target_func, initial_temp=1000, cooling_rate=0.95, max_iter=1000, x_range=(-10, 10)):
    # 初始解（随机生成）
    current_x = random.uniform(*x_range)
    current_value = target_func(current_x)
    best_x = current_x
    best_value = current_value
    
    temp = initial_temp
    history = []  # 记录搜索过程
    
    for i in range(max_iter):
        # 生成新解：在当前解附近随机扰动
        new_x = current_x + random.uniform(-1, 1)
        new_x = np.clip(new_x, *x_range)  # 限制在定义域内
        new_value = target_func(new_x)
        
        # 计算能量差
        delta_e = new_value - current_value
        
        # 接受准则
        if delta_e < 0 or random.random() < math.exp(-delta_e / temp):
            current_x = new_x
            current_value = new_value
            
            # 更新全局最优解
            if current_value < best_value:
                best_x = current_x
                best_value = current_value
        
        # 降温
        temp *= cooling_rate
        history.append((current_x, current_value))
        
        # 打印进度
        if i % 100 == 0:
            print(f"Iteration {i}: Temp={temp:.2f}, x={current_x:.3f}, f(x)={current_value:.3f}")
    
    return best_x, best_value, history

# ================ 3. 运行算法 ================
best_x, best_value, history = simulated_annealing(target_function, 
                                                 initial_temp=1000, 
                                                 cooling_rate=0.95, 
                                                 max_iter=1000)

# ================ 4. 可视化结果 ================
# 绘制函数曲线
plt.ion()  # 开启交互模式
fig, ax = plt.subplots()

x_vals = np.linspace(-10, 10, 400)
y_vals = target_function(x_vals)
plt.plot(x_vals, y_vals, 'b-', label="f(x) = x² + 10sin(x)")


# 绘制搜索过程
search_x = [h[0] for h in history]
search_y = [h[1] for h in history]

for i in range(len(search_x)):
    plt.scatter(search_x[i], search_y[i], c='red', s=10, alpha=0.3, label="Search Path")
    plt.draw()  # 重绘
    plt.pause(0.1)  # 暂停0.1秒（控制帧率）

# 标注最优解
plt.scatter(best_x, best_value, c='red', s=100, label=f"Global Min: x={best_x:.3f}, f(x)={best_value:.3f}")

plt.ioff()  # 关闭交互模式
plt.show()