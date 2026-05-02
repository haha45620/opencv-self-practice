import cv2

if __name__ == '__main__':
    img = cv2.imread('img/Chew.png',cv2.IMREAD_COLOR)
    img_face=cv2.imread('img/Chew_face.png',cv2.IMREAD_COLOR)
    img2=img.copy()
    ret=cv2.matchTemplate(img,img_face,cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    top_left = max_loc
    cv2.rectangle(img2,top_left, (top_left[0]+img_face.shape[1], top_left[1]+img_face.shape[0]), (0,0,255), 2)
    cv2.imshow('img_face',img_face)
    cv2.imshow('img1',img)
    cv2.imshow('img',img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    