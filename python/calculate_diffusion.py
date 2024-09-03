import numpy as np

def read_positions(file_path):
    """
    从文件中读取粒子位置数据
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 提取出每个时间步的数据
    positions = []
    current_positions = []
    for line in lines:
        if line.startswith("ITEM: ATOMS"):
            current_positions = []
        elif line.startswith("ITEM: TIMESTEP"):
            if current_positions:
                positions.append(current_positions)
        elif not line.startswith("ITEM"):
            parts = line.split()
            x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
            current_positions.append([x, y, z])
    if current_positions:
        positions.append(current_positions)
    
    return np.array(positions)

def calculate_msd(positions):
    """
    计算均方位移（MSD）
    """
    displacements = positions - positions[0]  # 相对初始位置的位移
    squared_displacements = np.sum(displacements**2, axis=2)  # 每个粒子的平方位移
    msd = np.mean(squared_displacements, axis=1)  # 对所有粒子求平均
    return msd

def calculate_diffusion_coefficient(msd, time_step, step_interval):
    """
    根据 MSD 计算扩散系数
    """
    t = time_step * step_interval
    diffusion_coefficient = msd[-1] / (4 * t)
    return diffusion_coefficient

# 设置文件路径和时间步长信息
file_path = '/mnt/data/custom_dump(2).txt'  # 文件路径
step_interval = 0.001  # 每个时间步的时间间隔
time_step = 500  # 每500步输出一次

# 读取位置数据
positions = read_positions(file_path)

# 计算均方位移（MSD）
msd = calculate_msd(positions)

# 计算扩散系数
diffusion_coefficient = calculate_diffusion_coefficient(msd, time_step, step_interval)

print(f"Diffusion Coefficient: {diffusion_coefficient} units^2/time")
