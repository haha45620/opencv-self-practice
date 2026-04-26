import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AnimatedCameraHistogram:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("无法打开摄像头")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            raise Exception("无法从摄像头读取帧，请检查摄像头是否被其他程序占用")
        
        height, width = frame.shape[:2]
        print(f"摄像头分辨率: {width}x{height}")  # 调试信息

        self.fig, (self.ax_cam, self.ax_cam_gray, self.ax_cam_threshBIO, self.ax_cam_threshOtus, self.ax_hist, self.ax_thresh) = plt.subplots(2, 3, figsize=(12, 5))
        self.img_display = self.ax_cam.imshow(np.zeros((480, 640, 3)), animated=True)
        self.ax_cam.set_title('Camera')
        self.ax_cam.axis('off')

        initial_gray = np.zeros((height, width), dtype=np.uint8)
        self.img_display_gray = self.ax_cam_gray.imshow(initial_gray, cmap='gray', animated=True)
        self.ax_cam_gray.set_title('Grayscale')
        self.ax_cam_gray.axis('off')

        initial_threshBIO = np.zeros((height, width), dtype=np.uint8)
        self.img_display_threshBIO = self.ax_cam_threshBIO.imshow(initial_threshBIO, cmap='gray', animated=True)
        self.ax_cam_threshBIO.set_title('ThresholdBIO')  

        initial_threshOtus = np.zeros((height, width), dtype=np.uint8)
        self.img_display_threshOtus = self.ax_cam_threshOtus.imshow(initial_threshOtus, cmap='gray', animated=True)
        self.ax_cam_threshOtus.set_title('ThresholdOtus')

        self.hist_line, = self.ax_hist.plot([], [], 'b-', animated=True)
        self.ax_hist.set_title('Brightness histogram')
        self.ax_hist.set_xlabel('pixel value')
        self.ax_hist.set_ylabel('frequency')
        self.ax_hist.set_xlim(0, 255)
        self.ax_hist.set_ylim(0, 1000)
        self.ax_hist.grid(True, alpha=0.3)

        self.stats_text = self.ax_hist.text(0.02, 0.98, '', 
                                          transform=self.ax_hist.transAxes, 
                                          verticalalignment='top',
                                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                                          animated=True)

        self.ax_thresh.set_title('Real-time Single Line Plot', fontsize=14)
        self.ax_thresh.set_xlabel('Time')
        self.ax_thresh.set_ylabel('Value')
        self.line, = self.ax_thresh.plot([], [], label='Live Data', color='blue', linewidth=2)  # 初始化self.line

        self.current_frame = None
        self.x_data = []  # 用于存储时间数据
        self.y_data = []  # 用于存储阈值数据


        def update_frame(self, frame_num):
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.img_display.set_array(rgb_frame)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.img_display_gray.set_array(gray)
                self.img_display_gray.set_clim(vmin=gray.min(), vmax=gray.max())
                
                _, threshBIO = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
                self.img_display_threshBIO.set_array(threshBIO)
                self.img_display_threshBIO.set_clim(vmin=threshBIO.min(), vmax=threshBIO.max())

                thresh, threshOtus = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
                print(f"Otsu's threshold: {thresh}")
                self.img_display_threshOtus.set_array(threshOtus)
                self.img_display_threshOtus.set_clim(vmin=threshOtus.min(), vmax=threshOtus.max())

                hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()

                self.hist_line.set_data(range(256), hist)

                max_val = max(hist) if len(hist) > 0 else 1000
                self.ax_hist.set_ylim(0, max_val * 1.1)

                mean_brightness = np.mean(gray)
                std_brightness = np.std(gray)
                stats_str = f'Average brightness: {mean_brightness:.1f}\nStandard deviation: {std_brightness:.1f}\nBrightness: {np.max(gray)}\nDarkest: {np.min(gray)}'
                self.stats_text.set_text(stats_str)

                # 更新阈值折线图的数据
                self.x_data.append(frame_num)  # 假设frame_num是帧索引，可以作为时间数据
                self.y_data.append(thresh)  # 大津法计算的阈值作为y轴数据
                self.line.set_data(self.x_data, self.y_data)

            return [self.img_display, self.img_display_gray, self.img_display_threshBIO, self.img_display_threshOtus, self.hist_line, self.stats_text, self.line]

    def run(self):
        print("按关闭窗口或Ctrl+C停止程序")

        ani = animation.FuncAnimation(
            self.fig, self.update_frame,
            interval=50,
            blit=True,
            cache_frame_data=False,
            repeat=False
        )

        plt.tight_layout()
        plt.show()

        if self.cap.isOpened():
            self.cap.release()

try:
    app = AnimatedCameraHistogram()
    app.run()
except Exception as e:
    print(f"程序出错: {e}")
    print("请确保已安装必要的库: pip install opencv-python matplotlib numpy")
