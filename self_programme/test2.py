import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class FixedCameraGrayScaleAnimation:
    def __init__(self):
        # 初始化摄像头捕捉对象
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("无法打开摄像头")
         
        # 设置摄像头参数
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # 预先读取一帧以确定尺寸
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            raise Exception("无法从摄像头读取帧，请检查摄像头是否被其他程序占用")
        
        height, width = frame.shape[:2]
        print(f"摄像头分辨率: {width}x{height}")  # 调试信息
        
        # 创建图形和子图
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title('Camera Grayscale', fontsize=14)
        self.ax.axis('off')  # 关闭坐标轴
        
        # 初始化灰度图像显示对象 - 使用实际尺寸的零矩阵
        initial_gray = np.zeros((height, width), dtype=np.uint8)
        self.img_display = self.ax.imshow(initial_gray, cmap='gray', animated=True)
        
        # 存储当前帧
        self.current_frame = None
    
    def update_frame(self, frame_num):
        """更新函数，被animation调用"""
        ret, frame = self.cap.read()
        if ret:
            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 更新灰度图像显示
            self.img_display.set_array(gray)
            
            # 强制更新（在某些情况下可能需要）
            self.img_display.set_clim(vmin=gray.min(), vmax=gray.max())
        else:
            print("无法读取摄像头帧")  # 调试信息
         
        return [self.img_display]
    
    def run(self):
        """运行动画"""
        print("按关闭窗口或Ctrl+C停止程序")
        
        # 创建动画对象
        ani = animation.FuncAnimation(
            self.fig, self.update_frame,
            interval=30,      # 更新间隔(毫秒)，约33FPS
            blit=True,       # 使用blitting加速更新
            cache_frame_data=False,
            repeat=False     # 防止重复播放
        )
        
        plt.tight_layout()
        plt.show()
        
        # 清理摄像头资源
        if self.cap.isOpened():
            self.cap.release()

# 运行修复后的摄像头灰度图动画
try:
    app = FixedCameraGrayScaleAnimation()
    app.run()
except Exception as e:
    print(f"程序出错: {e}")
    print("请确保已安装必要的库: pip install opencv-python matplotlib numpy")
    print("请检查:")
    print("1. 摄像头是否正常连接")
    print("2. 是否有其他程序正在使用摄像头")
    print("3. Python是否有访问摄像头的权限")