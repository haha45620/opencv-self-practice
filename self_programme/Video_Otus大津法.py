import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

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

        self.fig, ax = plt.subplots(2,3, figsize=(12, 5))
        (self.ax_cam, self.ax_cam_gray,self.ax_cam_threshBIO,self.ax_cam_threshOtus,self.ax_hist,self.ax_thresh)=ax.flatten()

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
                                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.1),
                                          animated=True)
        
        self.threshtext = self.ax_hist.text(0.02, 0.98, '', 
                                          transform=self.ax_thresh.transAxes, 
                                          verticalalignment='top',
                                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                                          animated=True)

        self.ax_thresh.set_title('Real-time Single Line Plot', fontsize=14)
        self.ax_thresh.set_xlabel('Time')
        self.ax_thresh.set_ylabel('Value')
        self.ax_thresh.grid(True, alpha=0.3)
        self.line, = self.ax_thresh.plot([], [], label='Live Data', color='blue', linewidth=2)
        
        self.current_frame = None

        self.max_points = 100
        self.data_queue = deque(maxlen=self.max_points)

    def update_frame(self, frame_num):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img_display.set_array(rgb_frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.img_display_gray.set_array(gray)
            self.img_display_gray.set_clim(vmin=gray.min(), vmax=gray.max())
            '''
                self.img_display_gray.set_clim(vmin=gray.min(), vmax=gray.max())必须有，不然灰度图黑屏
                该函数用来设置每帧的亮度-数据映射范围，vmin和vmax分别表示最小值和最大值，如果设置为None，则会自动计算
                如果不设置clims，imshow会根据当前数据的最小值和最大值自动缩放颜色映射，这可能导致不同帧之间的亮度显示不一致，甚至出现黑屏的情况。
            '''
            
            _, threshBIO = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
            self.img_display_threshBIO.set_array(threshBIO)
            self.img_display_threshBIO.set_clim(vmin=threshBIO.min(), vmax=threshBIO.max())

            thresh, threshOtus = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
            #print(f"Otsu's threshold: {thresh}")
            self.img_display_threshOtus.set_array(threshOtus)
            self.img_display_threshOtus.set_clim(vmin=threshOtus.min(), vmax=threshOtus.max())
            
            self.data_queue.append(thresh)
            x_data = list(range(len(self.data_queue)))
            y_data = list(self.data_queue)
            self.line.set_data(x_data, y_data)
            self.ax_thresh.set_ylim(-10,270)
            current_max_x = max(x_data) 
            self.ax_thresh.set_xlim(max(0, current_max_x - self.max_points), max(self.max_points, current_max_x + 1))
            self.ax_thresh.set_xticks([])
            threshstr = f'threshold: {thresh}'
            self.threshtext.set_text(threshstr)

            

            hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
            self.hist_line.set_data(range(256), hist)
            max_val = max(hist) if len(hist) > 0 else 1000
            self.ax_hist.set_ylim(0, max_val * 1.1)
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            stats_str = f'Average brightness: {mean_brightness:.1f}\nStandard deviation: {std_brightness:.1f}\nBrightness: {np.max(gray)}\nDarkest: {np.min(gray)}'
            self.stats_text.set_text(stats_str)

        return [self.img_display, self.img_display_gray,self.img_display_threshBIO,self.img_display_threshOtus,self.hist_line, self.stats_text,self.line,self.threshtext]

    def run(self):
        print("按关闭窗口或Ctrl+C停止程序")

        ani = animation.FuncAnimation(
            self.fig, self.update_frame,
            interval=20,
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
