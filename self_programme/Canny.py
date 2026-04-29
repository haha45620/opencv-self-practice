import cv2

if __name__ == '__main__':
    cv2.namedWindow("Canny Edge Image",cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Threshold1","Canny Edge Image",100,255,lambda x:None)
    cv2.createTrackbar("Threshold2","Canny Edge Image",200,255,lambda x:None)
    while True:
        img=cv2.imread("img\Chew_gray.png",cv2.IMREAD_GRAYSCALE)
        cv2.imshow("Original Image",img)
        threshold1=cv2.getTrackbarPos("Threshold1","Canny Edge Image")
        threshold2=cv2.getTrackbarPos("Threshold2","Canny Edge Image")
        canny=cv2.Canny(img,threshold1,threshold2,apertureSize=3,L2gradient=False)
        cv2.imshow("Canny Edge Image",canny)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()