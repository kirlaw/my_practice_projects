import cv2
import mediapipe as mp
import numpy as np
import json
import socket


def Pose_Images():
    # 使用算法包进行姿态估计时设置的参数
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8) as pose:
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        while (True):
            # 读取摄像头图像
            hx, image = cap.read()
            if hx is False:
                # print('read video error')
                exit(0)
            image.flags.writeable = False
            # Convert the BGR image to RGB before processing.
            # 姿态估计
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # print(results.pose_landmarks)
            landmarks = []
            dict_landmarks = {}
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append(
                        {'x': landmark.x, 'y': landmark.y, 'z': landmark.z, 'visibility': landmark.visibility})
                dict_landmarks = dict(landmarks=landmarks)
            pose_data = dict_landmarks
            json_data = json.dumps(pose_data)
            # print(json_data)
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dest_addr = ('127.0.0.1', 5052)
            text = json_data.encode('utf-8')
            udp_socket.sendto(text, dest_addr)

            # cv2.imshow('image', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):  # 按q退出
                break
        cap.release()


if __name__ == '__main__':
    Pose_Images()
