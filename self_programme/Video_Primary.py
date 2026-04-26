import cv2

#运行代码前请确保电脑硬件已打开摄像头

if __name__=="__main__":
    title=input("请输入窗口名：")
    fourcc=cv2.VideoWriter_fourcc(*'XVID')#确立FOURCC编码器，XVID是常用的编码格式之一
    out=cv2.VideoWriter('CameraOutput.avi',fourcc,20.0,(640,480),isColor=False)#创建输出对象
    cap=cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret,frame=cap.read()
        if ret:
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            out.write(frame)#向文件写入一帧
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.imshow(title,frame)
            if (cv2.waitKey(1)) & 0xFF == 27:#这里0xff是为了兼容64位系统，确保只获取最低8位的键码值
                break
    cap.release()
    out.release()
    cv2.destroyWindow(title)