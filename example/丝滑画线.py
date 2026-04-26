import cv2
import numpy as np

img = np.zeros((500, 500, 3), np.uint8)
cv2.namedWindow('Freehand Drawing')
prev_x, prev_y = None, None

def mouse_drawing(event, x, y, flags, param):
    global prev_x, prev_y, img
    
    if event == cv2.EVENT_LBUTTONDOWN:
        prev_x, prev_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:  # 检查左键是否按下
            if prev_x is not None and prev_y is not None:
                cv2.line(img, (prev_x, prev_y), (x, y), (255, 255, 255), 2)
            prev_x, prev_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        prev_x, prev_y = None, None

cv2.setMouseCallback('Freehand Drawing', mouse_drawing)

while True:
    cv2.imshow('Freehand Drawing', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        img = np.zeros((500, 500, 3), np.uint8)

cv2.destroyAllWindows()