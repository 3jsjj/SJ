import numpy as np
import argparse
import matplotlib.pyplot as plt

def read_positions(file_path):
    # 读取粒子位置数据的函数（与原代码相同）
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
    # 计算均方位移的函数（与原代码相同）
    displacements = positions - positions[0]  # 相对初始位置的位移
    squared_displacements = np.sum(displacements**2, axis=2)  # 每个粒子的平方位移
    msd = np.mean(squared_displacements, axis=1)  # 对所有粒子求平均
    return msd

def calculate_diffusion_coefficient(msd, time_step, step_interval):
    # 计算扩散系数的函数（与原代码相同）

    time = np.arange(0, len(msd)) * time_step * step_interval  # 生成对应的时间点
    slope, _ = np.polyfit(time, msd, 1)
    diffusion_coefficient = slope / 4  # 扩散系数为 MSD 的斜率除以 4
    return diffusion_coefficient

# 使用之前定义的 calculate_msd 和 read_positions 函数
def plot_msd_vs_time(positions, time_step, step_interval):

    # 绘制 MSD 随时间的变化图
    plt.figure(figsize=(8, 6))
    plt.plot(time, msd, 'o-', label='MSD vs Time')
    plt.xlabel('Time')
    plt.ylabel('Mean Squared Displacement (MSD)')
    plt.title('MSD vs Time')
    plt.grid(True)
    plt.legend()
    plt.show()

plot_msd_vs_time(positions, time_step, step_interval)

if __name__ == "__main__":
    # 使用 argparse 模块接受命令行参数
    parser = argparse.ArgumentParser(description='Calculate diffusion coefficient from particle positions.')
    parser.add_argument('--file', type=str, required=True, help='Path to the dump file containing particle positions')
    parser.add_argument('--time_step', type=int, default=500, help='Time step interval between outputs')
    parser.add_argument('--step_interval', type=float, default=0.001, help='Time interval for each step')

    args = parser.parse_args()

    # 读取位置数据
    positions = read_positions(args.file)

    # 计算均方位移（MSD）
    msd = calculate_msd(positions)

    # 计算扩散系数
    diffusion_coefficient = calculate_diffusion_coefficient(msd, args.time_step, args.step_interval)

    # 输出扩散系数
    print(f"{diffusion_coefficient:.6f}")

