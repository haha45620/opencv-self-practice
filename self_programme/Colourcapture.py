import cv2
import numpy as np
 
if __name__=="__main__":
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    # 循环读取摄像头帧
    while cap.isOpened():
        # 读取一帧图像
        ret, frame = cap.read()
        if ret:
            # 将图像从BGR颜色空间转换到HSV颜色空间
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # 定义蓝色的HSV阈值范围，这个是需要自己调试的
            lower_blue = np.array([90,50,50])
            upper_blue = np.array([140,255,255])
            # 创建掩码以识别蓝色区域，在蓝色区间的像素值为255，其他区域为0
            mask=cv2.inRange(frame, lower_blue, upper_blue)
            # 应用掩码以提取蓝色区域，按像素点每通道与操作
            res=cv2.bitwise_and(frame, frame, mask=mask)
            # 创建窗口以显示HSV图像
            cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
            cv2.imshow("frame", frame)
            # 创建窗口以显示掩码
            cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
            cv2.imshow("mask", mask)
            # 创建窗口以显示结果图像
            cv2.namedWindow("res", cv2.WINDOW_NORMAL)
            cv2.imshow("res", res)
            # 按下ESC键退出循环
            if cv2.waitKey(1) & 0xFF == 27:
                break
    # 释放摄像头资源
    cap.release()
    # 关闭所有OpenCV窗口
    cv2.destroyAllWindows()