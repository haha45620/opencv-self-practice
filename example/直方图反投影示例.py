import numpy as np
import cv2 as cv
roi = cv.imread('rose_red.png')
hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)
target = cv.imread('rose.png')
hsvt = cv.cvtColor(target,cv.COLOR_BGR2HSV)
# calculating object histogram
roihist = cv.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )#对ROI进行HS直方图统计
# normalize histogram and apply backprojection
cv.normalize(roihist,roihist,0,255,cv.NORM_MINMAX)#将集中的数值归一化到0-255之间
dst = cv.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)#得到原图像中每个像素颜色与ROI区域颜色相似的概率图
# Now convolute with circular disc 二维滤波，使用该结构元素对反向投影的结果图像进行二维滤波，从而进一步平滑图像中的颜色相似度分布，减少噪声和边缘锯齿现象，使得颜色匹配的结果更加平滑和自然。
disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
cv.filter2D(dst,-1,disc,dst)
# threshold and binary AND
ret,thresh = cv.threshold(dst,50,255,0)
thresh = cv.merge((thresh,thresh,thresh))#cv.merge((thresh,thresh,thresh))的作用是将反向投影后的概率图（经过阈值处理）从单通道灰度图像扩展为三通道彩色图像，以便后续与彩色目标图像target进行位运算，从而保留目标图像中颜色与ROI区域颜色相似的部分。
res = cv.bitwise_and(target,thresh)
res = np.vstack((target,thresh,res))
cv.imwrite('res.jpg',res)