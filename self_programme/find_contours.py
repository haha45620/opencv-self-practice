import cv2

if __name__ == '__main__':
    img_color=cv2.imread("img/Portrait.jpg",cv2.IMREAD_COLOR)
    img_color=cv2.resize(img_color,(500,500))
    img=cv2.imread("img/Portrait_gray.jpg",cv2.IMREAD_GRAYSCALE)
    img=cv2.resize(img,(500,500))
    canny=cv2.Canny(img,100,200)
    cv2.imshow("canny",canny)
    #contours,hierarchy=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours,hierarchy=cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contour=cv2.drawContours(img_color,contours,-1,(0,255,0),3)
    cv2.imshow("contour",contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()