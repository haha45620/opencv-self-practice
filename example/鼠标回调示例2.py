import numpy as np
import cv2 as cv
drawing = False # 如果 True 是鼠标按下
mode = True # 如果 True，画矩形，按下‘m’切换到曲线
ix,iy = -1,-1#初始化赋值
# 鼠标回调函数
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y#订下左上角点
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv.circle(img,(x,y),5,(0,0,255),-1)

img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cv.destroyAllWindows()


'''
    初始状态：drawing = False, mode = True,ix,iy = -1,-1
    按下左键，drawing -> True, ix,iy -> x,y
    移动鼠标，drawing = True, mode = True，随鼠标的拖动与帧的不断刷新生成跟随鼠标的矩形///生成小圆点跟随鼠标
    松开鼠标，drawing -> False, mode = True，生成最终的矩形
'''