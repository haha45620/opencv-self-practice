import cv2

def gray_save(path):
    img = cv2.imread(path,cv2.IMREAD_COLOR)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path[:-4]+'_gray.png',gray)

if __name__ == '__main__':
    gray_save('img\Chew.png')