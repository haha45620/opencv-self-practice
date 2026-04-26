import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":

    # img=cv2.imread("chew.png")
    # cubic=cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
    # linear=cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_LINEAR)
    # nearest=cv2.resize(img,None,fx=2,fy=2,interpolation=cv2.INTER_NEAREST)
    # cv2.imshow("original", img)
    # cv2.imshow("cubic", cubic)
    # cv2.imshow("linear", linear)
    # cv2.imshow("nearest", nearest)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img=cv2.imread("Portrait.jpg")
    # area=cv2.resize(img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
    # cv2.imshow("original", img)
    # cv2.imshow("area", area)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img=cv2.imread("chew.png")
    # translation=cv2.warpAffine(img, np.float32([[1, 0, 100], [0, 1, 50]]), (img.shape[1], img.shape[0]))
    # translation_big=cv2.warpAffine(img, np.float32([[1, 0, 100], [0, 1, 50]]), (img.shape[1]*2, img.shape[0]*2))
    # cv2.imshow("original", img)
    # cv2.imshow("translation", translation)
    # cv2.imshow("translation_big", translation_big)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img=cv2.imread("chew.png")
    # M=cv2.getRotationMatrix2D((img.shape[1]//2, img.shape[0]//2), 45, 1)
    # rotation=cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    # rotation_big=cv2.warpAffine(img, M, (img.shape[1]*2, img.shape[0]*2))
    # cv2.imshow("original", img)
    # cv2.imshow("rotation", rotation)
    # cv2.imshow("rotation_big", rotation_big)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()    

    # img = cv2.imread('chew.png')
    # rows,cols,ch = img.shape
    # pts1 = np.float32([[50,50],[200,50],[50,200]])
    # pts2 = np.float32([[10,100],[200,50],[100,250]])
    # M = cv2.getAffineTransform(pts1,pts2)
    # dst = cv2.warpAffine(img,M,(cols,rows))
    # plt.subplot(121),plt.imshow(img),plt.title('Input')
    # plt.subplot(122),plt.imshow(dst),plt.title('Output')
    # plt.show()

    img=cv2.imread("chew.png")
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,threshold=cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    ret,threshold_gray=cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("original", img)
    cv2.imshow("threshold", threshold)
    cv2.imshow("threshold_gray", threshold_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
