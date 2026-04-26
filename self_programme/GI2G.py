import cv2

#标准的图像显示函数
def imgshow(title,img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL) #创建一个可调整大小的窗口
    cv2.imshow(title, img)#加载图像数据在该窗口
    k =cv2.waitKey(0)#返回键码值ASCII
    #print(k)
    if k == ord("s"):
        title2 = input("请输入文件名称：")
        cv2.imwrite(title2,img)
    cv2.destroyWindow(title)#关闭特定窗口


# def imgshow(title,img):
#     cv2.namedWindow(title,cv2.WINDOW_NORMAL) #创建一个可调整大小的窗口
#     cv2.resizeWindow(title, 1844, 1040) #调整窗口大小
#     cv2.imshow(title, img)#加载图像数据在该窗口
#     cv2.waitKey(0)#返回键码值ASCII
#     cv2.destroyWindow(title)#关闭特定窗口

if __name__ == "__main__":
    title=input("请输入要打开的文件名：")

    # img=cv2.imread("Portrait.jpg",cv2.IMREAD_COLOR)#RGB
    # print(img)
    img=cv2.imread("Portrait.jpg",cv2.IMREAD_GRAYSCALE)#灰度亮度
    #print(img)
    # img=cv2.imread("Portrait.jpg",cv2.IMREAD_UNCHANGED)#所有通道信息，包括透明度A（前提是有A通道）
    # print(img)   

    imgshow(title, img)