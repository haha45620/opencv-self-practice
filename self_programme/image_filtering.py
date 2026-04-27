import cv2

if __name__=="__main__":
    img=cv2.imread("img\Chew_noisy.png",cv2.IMREAD_COLOR)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,binary=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    _,otus=cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
    cv2.imshow("Otsu",otus)
    blur=cv2.blur(otus,(5,5))
    cv2.imshow("Blur",blur)
    Gassian=cv2.GaussianBlur(otus,(5,5),0)
    cv2.imshow("Gassian",Gassian)
    median=cv2.medianBlur(otus,5)
    cv2.imshow("Median",median)
    bilateral=cv2.bilateralFilter(otus,5,75,75)
    cv2.imshow("Bilateral",bilateral)
    cv2.waitKey(0)
    cv2.destroyAllWindows()