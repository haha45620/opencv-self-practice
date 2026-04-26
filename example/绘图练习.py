import numpy as np
import cv2 as cv
mode = True # 如果 True，画矩形，按下‘m’切换到曲线
ix,iy = -1,-1#初始化赋值
b,g,r,s=0,0,0,0


# 鼠标回调函数
def draw_circle(event,x,y,flags,param):
    global ix,iy,mode,b,g,r#,drawing
    if event == cv.EVENT_LBUTTONDOWN:
        ix,iy = x,y#订下左上角点
    elif event == cv.EVENT_MOUSEMOVE:
        if flags & cv.EVENT_FLAG_LBUTTON:
            if mode == True:
                cv.rectangle(img,(ix,iy),(x,y),(b,g,r),-1)
            else:
                cv.line(img,(ix,iy),(x,y),(b,g,r),2)
                ix,iy = x,y
    elif event == cv.EVENT_LBUTTONUP:        
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(b,g,r),-1)
        else:
            cv.line(img,(ix,iy),(x,y),(b,g,r),2)
    img[380:400, 0:512] = (255,255,255)        

def nothing(x):
    global r,g,b,s
    s = cv.getTrackbarPos(switch,'image')
    if s==1:
        r = cv.getTrackbarPos('R','image')
        g = cv.getTrackbarPos('G','image')
        b = cv.getTrackbarPos('B','image')
    img[400:512, 0:512] = (b, g, r)

img = np.zeros((512,512,3), np.uint8)
img[380:400, 0:512] = (255,255,255)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)
cv.createTrackbar('R','image',125,255,nothing)
cv.createTrackbar('G','image',125,255,nothing)
cv.createTrackbar('B','image',125,255,nothing)
# 创建一个用来启用和关闭功能的开关
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('r'):
        img = np.zeros((512,512,3), np.uint8)
        img[380:400, 0:512] = (255,255,255)
        img[400:512, 0:512] = (b, g, r)
    elif k == 27:
        break
cv.destroyAllWindows()