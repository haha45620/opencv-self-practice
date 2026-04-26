import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
 
class AnimatedCameraHistogram:
    def __init__(self):#创建程序主体窗口
        # 初始化摄像头捕捉对象
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("无法打开摄像头")
         
        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
         
        # 创建图形和子图用于显示摄像头画面和直方图
        '''
        plt.subplots(1, 2, figsize=(12, 5)): 
            plt.subplots 是 Matplotlib 库中的一个函数，用于创建包含一个或多个子图（Axes）的对象。
            1, 2 参数意味着创建一个包含1行2列的子图布局，即两个并排的子图。
            figsize=(12, 5) 参数指定了整个图形窗口的大小，其中12是宽度，5是高度，单位是英寸。
            返回值是一个元组，包含了图形对象和子图对象。下文赋值给 self.fig 和 (self.ax_cam, self.ax_hist)。
        self.fig: 
            self.fig 是整个图形对象的引用，包含了所有子图（Axes）。在这个类中，self.fig 被用于后续的动画创建和其他操作。
        self.ax_cam, self.ax_hist: 
            self.ax_cam 和 self.ax_hist 分别是图形窗口中的两个子图（Axes）的引用。
            self.ax_cam 用于显示摄像头捕捉的画面。
            self.ax_hist 用于绘制摄像头画面的亮度直方图   
        '''
        self.fig, (self.ax_cam, self.ax_hist) = plt.subplots(1, 2, figsize=(12, 5))#ax_cam和ax_hist分别是两个子图的Axes对象
         
        # 初始化图像显示对象以在子图上显示摄像头画面
        self.img_display = self.ax_cam.imshow(np.zeros((480, 640, 3)), animated=True)#创建imshow对象并被标志为动画，该对象用于显示子图上的图像数据。
        self.ax_cam.set_title('Camera')
        self.ax_cam.axis('off')
         
        # 初始化直方图线条对象以在子图上绘制亮度直方图
        self.hist_line, = self.ax_hist.plot([], [], 'b-', animated=True)
        '''
            []: 这是第一个参数，表示 x 轴的数据点。这里传入一个空列表，意味着我们将在后续动态更新直方图的 x 轴数据。
            []: 这是第二个参数，表示 y 轴的数据点。同样传入一个空列表，意味着我们将在后续动态更新直方图的 y 轴数据。
            'b-': 这是第三个参数，表示线条的样式和颜色。'b-' 表示使用蓝色实线。
            animated=True: 这是第四个参数，用于指定这条线条是否是动画的一部分。设置为 True 可以提高动画的更新效率。
            self.hist_line, = ...: 使用逗号将 plot 方法的返回值赋值给 self.hist_line。plot 方法会返回一个包含线条对象的元组，由于我们只绘制了一条线，
            因此元组中只有一个元素。通过在变量名后加一个逗号，可以直接将该线条对象赋值给 self.hist_line，而不是整个元组
        '''
        self.ax_hist.set_title('Brightness histogram')
        self.ax_hist.set_xlabel('pixel value')
        self.ax_hist.set_ylabel('frequency')
        self.ax_hist.set_xlim(0, 255)
        self.ax_hist.set_ylim(0, 1000)
        self.ax_hist.grid(True, alpha=0.3)#启用网格线，透明度为0.3
         
        # 初始化显示统计信息的文本对象
        self.stats_text = self.ax_hist.text(0.02, 0.98, '', 
                                          transform=self.ax_hist.transAxes, 
                                          verticalalignment='top',
                                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                                          animated=True)
         
        '''
            self.stats_text = self.ax_hist.text(...): 这行代码在 self.ax_hist 这个子图上创建了一个文本对象，并将其引用赋给 self.stats_text。
                                                      这个文本对象用于在直方图上显示统计信息。 
            0.02, 0.98: 这两个参数分别代表文本对象在子图中的位置。第一个参数表示文本对象的 x 坐标（相对于子图宽度的比例，范围是 0 到 1），
                        第二个参数表示文本对象的 y 坐标（相对于子图高度的比例，范围是 0 到 1）。
                        在这个例子中，文本对象被放置在子图的左上角，距离左侧边缘 2% 的宽度，距离顶部边缘 2% 的高度。 
            '': 这个参数是文本对象的初始文本内容。这里传入的是一个空字符串，意味着文本对象在创建时没有显示任何文字。文本内容会在后续通过 set_text 方法进行更新。 
            transform=self.ax_hist.transAxes: 这个参数指定了文本对象的位置变换方式。transAxes 是一个坐标变换对象，
                                              它将文本对象的位置参数（0.02, 0.98）从子图坐标系转换为轴坐标系。这样，即使子图的大小发生变化，
                                              文本对象的位置也会保持不变，始终位于子图的左上角。 
            verticalalignment='top': 这个参数指定了文本对象相对于其位置坐标的垂直对齐方式。'top' 表示文本对象的顶部与给定的位置坐标对齐。 
            bbox=dict(...): 这个参数用于设置文本对象的背景框。dict 函数创建了一个字典，其中包含了背景框的相关属性。
                            boxstyle='round' 表示背景框的形状是圆角矩形；facecolor='white' 表示背景框的填充颜色是白色；alpha=0.8 表示背景框的透明度是 0.8，
                            即不完全透明。
        ''' 
        self.current_frame = None#设置图像帧属性并附初值
         
    def update_frame(self, frame_num):
        """更新函数，被animation调用"""
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()#这里是深拷贝
             
            # 更新摄像头画面
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img_display.set_array(rgb_frame)#更新图像显示对象的数据为当前帧的 RGB 图像数据，以便在子图上显示最新的摄像头画面。
             
            # 计算灰度图和直方图数据
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
            '''
            cv2.calcHist(): 这是OpenCV库中的一个函数，用于计算图像的直方图。直方图是一种用于统计图像中每个像素值出现频率的工具，它可以帮助我们了解图像的亮度分布、颜色分布等信息。 
            [gray]: 这个参数指定了要计算直方图的图像。这里传入的是一个灰度图像gray。OpenCV的calcHist函数接受一个图像列表作为参数，因此需要用方括号将其包装成列表形式。 
            [0]: 这个参数指定了要计算直方图的通道。对于单通道的灰度图像，只有一个通道，所以这里传入[0]。如果是多通道的彩色图像（例如BGR图像），则可以传入不同的通道索引（0对应B通道，1对应G通道，2对应R通道）。 
            None: 这个参数用于指定掩码。掩码是一个与输入图像大小相同的图像，其中每个像素的值为0或1。对于值为1的像素，calcHist函数会计算其直方图；对于值为0的像素，则不计算直方图。这里传入None，表示不使用掩码，对整个图像计算直方图。 
            [256]: 这个参数指定了直方图的bin数量（即直方图的柱数）。对于灰度图像，像素值的范围是0到255，因此通常使用256个bin来表示每个可能的像素值。 
            [0, 256]: 这个参数指定了直方图的范围（即像素值的最小值和最大值）。对于灰度图像，像素值的范围是0到255，因此这里传入[0, 256]表示直方图的范围是从0到255。 
            .flatten(): 这个方法用于将计算得到的直方图数组展平成一维数组。cv2.calcHist函数返回的是一个多维数组，而在这里我们只需要一维数组来表示直方图，因此使用flatten()方法将多维数组展平。               
            cv2.calcHist 的返回值是一个多维数组，具体结构取决于输入图像的通道数和 histSize 参数。对于灰度图像，返回值的结构如下： 
            单通道灰度图像: 返回一个形状为 (256, 1) 的二维数组，其中每一行对应一个像素值的bin，列中的值表示该像素值在图像中出现的频率。例如，如果 histSize 为 [256]，则返回的直方图数组 hist 的形状为 (256, 1)。具体来说，hist[0] 表示像素值为0的频率，hist[1] 表示像素值为1的频率，依此类推，直到 hist[255] 表示像素值为255的频率
            '''
             
            # 更新直方图线条数据
            self.hist_line.set_data(range(256), hist)#range(256)作为x轴数据，hist作为y轴数据
             
            # 动态调整y轴范围以适应直方图的最大值
            max_val = max(hist) if len(hist) > 0 else 1000
            self.ax_hist.set_ylim(0, max_val * 1.1)
             
            # 更新统计信息文本
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)#标准差
            stats_str = f'Average brightness: {mean_brightness:.1f}\nStardard deviation: {std_brightness:.1f}\nBrightness: {np.max(gray)}\nDarkest: {np.min(gray)}'
            self.stats_text.set_text(stats_str)
         
        return [self.img_display, self.hist_line, self.stats_text]
     
    def run(self):
        """运行动画"""
        print("按关闭窗口或Ctrl+C停止程序")
         
        # 创建动画对象，设置更新函数和相关参数
        ani = animation.FuncAnimation(
            self.fig, self.update_frame, 
            interval=50,  # 更新间隔(毫秒)
            blit=True,    # 使用blitting加速更新
            cache_frame_data=False
        )
         
        '''
        self.fig：这是整个图形对象的引用，包含了所有子图（Axes）。在 AnimatedCameraHistogram 类中，self.fig 被用于创建一个包含摄像头画面和亮度直方图的图形窗口。
        self.update_frame：这是一个函数对象，用于定义动画每一帧的更新逻辑。在这个类中，self.update_frame 函数会从摄像头捕获一帧图像，更新图像显示和直方图数据，并计算和显示亮度的统计信息。
        interval=50：这是更新间隔的参数，单位是毫秒。在这个例子中，动画会每隔50毫秒更新一次，这意味着每秒有20帧图像被捕捉和显示。
        blit=True：这个参数指定了是否使用 blitting 技术来加速动画的更新。blitting 技术是一种优化方法，它只重绘图形中发生变化的部分，而不是整个图形。这样可以显著提高动画的效率，尤其是在处理复杂的图形或大量的数据时。
        cache_frame_data=False：这个参数指定了是否缓存每一帧的数据。如果设置为 True，动画对象会缓存每一帧的数据，以便在需要时快速访问。如果设置为 False，动画对象会在每一帧更新时重新计算数据，而不是缓存。在这个例子中，将其设置为 False 可能是为了确保动画能够实时更新数据，而不是使用缓存的旧数据。        
        '''
        plt.tight_layout()#自动调整子图参数，使得子图之间的间距更加紧凑
        plt.show()
         
        # 清理摄像头资源
        if self.cap.isOpened():
            self.cap.release()
 
# 运行动画版本
try:
    app = AnimatedCameraHistogram()
    app.run()
except Exception as e:
    print(f"程序出错: {e}")
    print("请确保已安装必要的库: pip install opencv-python matplotlib numpy")