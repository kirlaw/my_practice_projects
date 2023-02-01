import numpy as np
import time
import cv2
import PoseModule as pm

cap = cv2.VideoCapture(0)  # 0 打开电脑摄像头
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
success = True
point_sd = 0
while success:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (640, 480))

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # 取23 24的中点
            point = detector.midpoint(img, 24, 23)
            if point_sd == 0:
                point_sd = point
                # print(point_sd["y"])
            # 计算个数
            # print(point["y"])
            if point["y"] > point_sd["y"] + 15:

                if dir == 0:
                    count += 0.5
                    dir = 1
            if point["y"] < point_sd["y"] + 5:

                if dir == 1:
                    count += 0.5
                    dir = 0
            # print(count)
            cv2.putText(img, str(int(count)), (45, 460), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 0),
                        8)  # 图像添加文字：(照片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    if cv2.waitKey(1) == 27:  # 按下 Esc退出 (27是按键ESC对应的ASCII值)
        break

    if (cv2.getWindowProperty("Image", 0) == -1):  # 判断是否点击窗口关闭按键
        break

cap.release()
cv2.destroyAllWindows()
