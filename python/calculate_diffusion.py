import numpy as np

def read_positions(file_path):
    """
    从文件中读取粒子位置数据，并将其以 numpy 数组的形式返回。
    """
    positions = []
    with open(file_path, 'r') as file:
        current_positions = []
        for line in file:
            if line.startswith("ITEM: TIMESTEP"):
                if current_positions:
                    positions.append(current_positions)  # 保存上一个时间步的数据
                current_positions = []  # 清空列表以保存新数据
            elif line.startswith("ITEM: ATOMS"):
                continue  # 跳过 ITEM: ATOMS 行
            else:
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        # 提取 x, y, z 坐标
                        x, y, z = map(float, parts[2:5])
                        current_positions.append([x, y, z])
                    except ValueError:
                        continue  # 忽略无效行
        if current_positions:
            positions.append(current_positions)  # 保存最后一个时间步的数据
    return np.array(positions)


def calculate_msd(positions):
    """
    计算均方位移（MSD）。
    """
    displacements = positions - positions[0]  # 相对初始位置的位移
    squared_displacements = np.sum(displacements**2, axis=2)  # 每个粒子的平方位移
    msd = np.mean(squared_displacements, axis=1)  # 对所有粒子求平均
    return msd


def calculate_diffusion_coefficient(msd, time_step, step_interval):
    """
    使用线性拟合计算扩散系数，避免仅依赖最后一步的 MSD。
    """
    time = np.arange(0, len(msd)) * time_step * step_interval  # 生成对应的时间点
    # 线性拟合 MSD 和时间，斜率为 MSD 的增长率
    slope, _ = np.polyfit(time, msd, 1)
    diffusion_coefficient = slope / 4  # 扩散系数为 MSD 的斜率除以 4
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

print(f"Diffusion Coefficient: {diffusion_coefficient:.6f} units^2/time")
