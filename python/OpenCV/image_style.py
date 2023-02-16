import cv2
import numpy as np

# Load the image
# img = cv2.imread('image.jpg')
cap = cv2.VideoCapture(0)  # 0 打开电脑摄像头
success = True
while success:
    success, img = cap.read()
    # Detect the hair contours
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Segment 
    mask = np.zeros_like(img[:, :, 0])
    cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)
    
    # print(mask)
    img = cv2.bitwise_and(img, img, mask=mask)  # 改变轮廓内的颜色
    img[mask == 255] = (0, 0, 255)  # 替换为红色
    # Show the result
    cv2.imshow('Result', img)

    cv2.waitKey(1)  # 程序暂停1ms

    if cv2.waitKey(1) == 27:  # 按下 Esc退出 (27是按键ESC对应的ASCII值)
        break

    if cv2.getWindowProperty("Result", cv2.WND_PROP_AUTOSIZE) == -1:  # 判断是否点击窗口关闭按键
        break

cap.release()
cv2.destroyAllWindows()
