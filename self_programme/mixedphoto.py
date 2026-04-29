import cv2 as cv
import numpy as np

A = cv.imread('img/Chew.png',cv.IMREAD_COLOR)
B=cv.cvtColor(A,cv.COLOR_BGR2RGB)

G = A.copy()#深拷贝A

#下采样，生成不断缩小的5级图像
gpA = [G]
for i in range(6):
    G = cv.pyrDown(G)
    gpA.append(G)

G = B.copy()

gpB = [G]
for i in range(6):
    G = cv.pyrDown(G)
    gpB.append(G)

 #生成Laplacian金字塔，【L0=G5（最小的图像），G4-G5，G3-G4，G2-G3，G1-G2，G0-G1的差分】   
lpA = [gpA[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gpA[i])
    #十分重要的一步，将GE的大小调整为与gpA[i-1]相同，先pyrdown再pyrup的图像不一定与原图像大小相同
    if GE.shape!= gpA[i-1].shape:
        GE = cv.resize(GE,gpA[i-1].shape[1::-1],interpolation=cv.INTER_CUBIC)#注意，.shape返回的是(height, width, depth)，而cv.resize需要的尺寸格式是(width, height)，因此使用切片[1::-1]来调整顺序）。
    L = cv.subtract(gpA[i-1],GE)#差分，gpa[i-1]-ge
    lpA.append(L)

lpB = [gpB[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gpB[i])
    if GE.shape!= gpB[i-1].shape:
        GE = cv.resize(GE,gpB[i-1].shape[1::-1],interpolation=cv.INTER_CUBIC)
    L = cv.subtract(gpB[i-1],GE)
    lpB.append(L)

LS = []
for la,lb in zip(lpA,lpB):#对应Laplacian金字塔级图像一一打包成元组迭代对象
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))#这里的前提是A、B图同大小，这里只是大略地以中间部分分开，拼在一起
    LS.append(ls)

ls_ = LS[0]
for i in range(1,6):
    ls_ = cv.pyrUp(ls_)
    if ls_.shape != LS[i].shape:
        ls_ = cv.resize(ls_, LS[i].shape[1::-1], interpolation=cv.INTER_CUBIC)
    ls_ = cv.add(ls_, LS[i])
real = np.hstack((A[:,:cols//2],B[:,cols//2:]))

cv.imshow('real',real)
cv.waitKey(0)
cv.destroyAllWindows()