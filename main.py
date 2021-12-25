import numpy as np
import cv2

DILATE_KERNEL = np.ones((9,9), np.uint8)
CLOSING_KERNEL = np.ones((15,15), np.uint8)
ERODE_KERNEL = np.ones((11,11), np.uint8)

MIN_WIDTH = 50
MIN_HEIGHT = 50

def main():
    cap = cv2.VideoCapture()
    cap.open('./videos/visiontraffic.avi')

    backgroundImage:np.ndarray = None
    for i in range(5):
        success, backgroundImage = cap.read()
        if not success:
            print('Không thể đọc video này !!!')

    grayBackgroundImage =  cv2.cvtColor(backgroundImage, cv2.COLOR_BGR2GRAY)
    grayBackgroundImage = cv2.medianBlur(grayBackgroundImage, 5)

    while(True):
        success, frame = cap.read()
        if not success:
            break

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayImage = cv2.medianBlur(grayImage, 5)

        # Trừ ảnh
        imageProcess = cv2.absdiff(grayBackgroundImage, grayImage)

        # Phân ngưỡng
        ret, imageProcess = cv2.threshold(imageProcess, 45, 255, cv2.THRESH_BINARY)

        cv2.imshow('Truoc khi dien day anh',imageProcess)

        # Điền đầy ảnh
        imageProcess = cv2.dilate(imageProcess, kernel=DILATE_KERNEL)
        imageProcess = cv2.morphologyEx(imageProcess, cv2.MORPH_CLOSE, kernel=DILATE_KERNEL)
        imageProcess = cv2.erode(imageProcess, kernel=DILATE_KERNEL)

        cv2.imshow('Sau khi dien day anh',imageProcess)
        
        contours, _ = cv2.findContours(imageProcess, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        count = 0
        for item in contours:
            x, y ,w ,h = cv2.boundingRect(item)

            if w > MIN_WIDTH and h > MIN_HEIGHT:
                frame = cv2.rectangle(frame, pt1=(x,y), pt2=(x+w, y+h), color=(0,255,0), thickness=1)
                count += 1
        
        frame = cv2.putText(
            img=frame,
            text=f'So xe hien tai: {count}',
            org=(10,20),
            fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            fontScale=1, color=(255,255,0), thickness=1)
        
        cv2.imshow(winname='visiontraffic', mat=frame)
        if cv2.waitKey(10) == 27 or cv2.getWindowProperty(winname='visiontraffic', prop_id=cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()