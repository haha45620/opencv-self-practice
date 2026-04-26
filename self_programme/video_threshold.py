import cv2


if __name__=="__main__":
    cap=cv2.VideoCapture(0)
    while cap.isOpened():
        ret,frame=cap.read()
        if ret:
            cv2.imshow("original", frame)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ret,threshold=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
            mean=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
            gasssian=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            cv2.imshow("threshold", threshold)
            cv2.imshow("mean", mean)
            cv2.imshow("gasssian", gasssian)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()