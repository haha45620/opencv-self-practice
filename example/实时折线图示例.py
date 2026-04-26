import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import random

'''
deque 是 Python 标准库 collections 模块中的一个双端队列（double-ended queue）类。它提供了一个高效的方式来在两端添加和删除元素。deque 的主要特点包括：
快速增删：可以在队列的两端快速地添加和删除元素，这对于需要频繁从队列两端操作数据的应用场景非常有用。
固定大小：可以通过初始化时指定 maxlen 参数来创建一个固定大小的队列。当队列中的元素数量达到 maxlen 时，新的元素会被添加到队列的末端，而最早的元素会被自动移除。这在需要保持一定数量的历史数据而不需要存储更多数据的情况下特别有用。
'''

class SingleLinePlot:
    def __init__(self, max_points=100):
        """
        单线实时折线图类
        
        参数:
        max_points: 显示的最大数据点数
        """
        self.max_points = max_points
        
        # 创建数据队列存储历史数据
        self.data_queue = deque(maxlen=max_points)#创建一个deque对象，maxlen指定队列的最大长度
        
        # 创建图形和子图
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title('Real-time Single Line Plot', fontsize=14)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        
        # 创建单条线
        self.line, = self.ax.plot([], [], label='Live Data', color='blue', linewidth=2)
        '''
        self.ax.plot: 这是 matplotlib.pyplot 库中的 plot 函数，用于在 self.ax (子图) 上绘制线条。self.ax 是在 SingleLinePlot 类的初始化方法中创建的子图对象。 
        [], []: 这两个空列表分别代表 x 轴和 y 轴的数据。在这个阶段，我们还没有实际的数据来绘制，所以传入空列表。在后续的动画更新过程中，这些数据将会被更新。 
        label='Live Data': 这个参数为绘制的线条添加了一个标签，标签内容为 ‘Live Data’。在图例中会显示这个标签，以便用户知道这条线条代表什么数据。 
        color='blue': 这个参数设置了线条的颜色为蓝色。在 matplotlib 中，颜色可以通过多种方式指定，这里使用的是色彩名称。 
        linewidth=2: 这个参数设置了线条的宽度为 2 个单位。线条宽度决定了线条在图形中的粗细程度
        '''
        
        # 添加图例，根据前面的label参数显示图例
        self.ax.legend()
        
        # 添加网格
        self.ax.grid(True, alpha=0.3)
        
        # 初始化y轴范围
        self.ax.set_ylim(-5, 5)
    
    def update_data(self, new_value):
        """
        更新数据队列
        
        参数:
        new_value: 新的y值
        """
        self.data_queue.append(new_value)
    
    def animate(self, frame):
        """
        动画更新函数
        """
        # 生成x轴数据（时间）
        x_data = list(range(len(self.data_queue)))
        y_data = list(self.data_queue)
        
        # 更新线条数据
        self.line.set_data(x_data, y_data)
        
        # 自动调整x轴范围以显示最新的数据
        if x_data:
            current_max_x = max(x_data) if x_data else 99  # 防止初始状态问题
            self.ax.set_xlim(max(0, current_max_x - self.max_points), 
                           max(self.max_points, current_max_x + 1))
            
            # 根据当前数据范围调整y轴
            if y_data:
                y_min, y_max = min(y_data), max(y_data)
                margin = (y_max - y_min) * 0.1 if y_max != y_min else 0.5
                self.ax.set_ylim(y_min - margin, y_max + margin)
        
        return [self.line]
    
    def start_animation(self, interval=100):
        """
        开始动画
        
        参数:
        interval: 更新间隔（毫秒）
        """
        self.ani = animation.FuncAnimation(
            self.fig, 
            self.animate,
            interval=interval,
            blit=True,
            cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.show()

# 示例1：随机波动数据
class RandomSingleLine(SingleLinePlot):
    def animate(self, frame):
        # 添加随机数据点
        new_value = random.uniform(-3, 3)
        self.update_data(new_value)
        
        # 生成x轴数据
        x_data = list(range(len(self.data_queue)))
        y_data = list(self.data_queue)
        
        # 更新线条
        self.line.set_data(x_data, y_data)
        
        # 自动调整范围
        if x_data:
            current_max_x = max(x_data) if x_data else 99
            self.ax.set_xlim(max(0, current_max_x - self.max_points), 
                           max(self.max_points, current_max_x + 1))
            
            if y_data:
                y_min, y_max = min(y_data), max(y_data)
                margin = (y_max - y_min) * 0.1 if y_max != y_min else 0.5
                self.ax.set_ylim(y_min - margin, y_max + margin)
        
        return [self.line]

# 示例2：正弦波数据
class SineWaveSingleLine(SingleLinePlot):
    def __init__(self, max_points=200):
        super().__init__(max_points)
        self.ax.set_title('Real-time Sine Wave')
        self.time_counter = 0
        self.frequency = 0.5  # Hz
        self.amplitude = 2
    
    def animate(self, frame):
        # 生成新的正弦波数据点
        new_value = self.amplitude * np.sin(2 * np.pi * self.frequency * self.time_counter / 10)
        self.update_data(new_value)
        self.time_counter += 1
        
        # 生成x轴数据
        x_data = list(range(len(self.data_queue)))
        y_data = list(self.data_queue)
        
        # 更新线条
        self.line.set_data(x_data, y_data)
        
        # 自动调整x轴范围
        if x_data:
            current_max_x = max(x_data) if x_data else 199
            self.ax.set_xlim(max(0, current_max_x - self.max_points), 
                           max(self.max_points, current_max_x + 1))
        
        return [self.line]

# 使用示例
def demo_random_wave():
    """演示随机波动数据"""
    print("显示随机波动数据...关闭窗口结束")
    plot = RandomSingleLine(max_points=100)
    plot.start_animation(interval=100)  # 每100毫秒更新一次

def demo_sine_wave():
    """演示正弦波数据"""
    print("显示正弦波数据...关闭窗口结束")
    plot = SineWaveSingleLine(max_points=200)
    plot.start_animation(interval=50)  # 每50毫秒更新一次

if __name__ == "__main__":
    print("选择要运行的示例:")
    print("1. 随机波动数据")
    print("2. 正弦波数据")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        demo_random_wave()
    elif choice == "2":
        demo_sine_wave()
    else:
        print("无效选择，运行随机波动数据示例...")
        demo_random_wave()