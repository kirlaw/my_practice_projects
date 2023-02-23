import numpy as np  # 常用数据科学包
import os
from PIL import Image  # 图像读取
import cv2  # 图像包

# 深度学习包
import paddle
import paddle.vision.transforms as T  # 数据增强

import socket

# 设置IP和端口号
ip = "127.0.0.1"
port = 9999


# 进行预测和提交
# 首先拿到预测文件的路径列表

def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def predict_model():
    # 加载训练好的模型
    pre_model = paddle.vision.models.resnet50(pretrained=True, num_classes=6)
    pre_model.set_state_dict(paddle.load('acc1.0.model'))
    pre_model.eval()

    # pre_classes = []
    normalize = T.Normalize(mean=0, std=1)
    name = ["Aprion_virescens", "clownfish", "crab", "goggles", "sea_horse", "turtle", 'null']
    # 生成预测结果
    for path in test_path:
        image_path = path

        image = np.array(Image.open(image_path))  # H, W, C
        try:
            image = image.transpose([2, 0, 1])[:3]  # C, H, W
        except:
            image = np.array([image, image, image])  # C, H, W

        # 图像变换
        features = cv2.resize(image.transpose([1, 2, 0]), (256, 256)).transpose([2, 0, 1]).astype(np.float32)
        features = normalize(features)

        features = paddle.to_tensor([features])
        pre = list(np.array(pre_model(features)[0]))
        #print(pre)
        max_item = max(pre)
        if max_item < 2.5:
            pre = 6
        else:
            pre = pre.index(max_item)
        print("图片：", path, "预测结果：", name[pre])
        # pre_classes.append(pre)


    return pre

    # print(pre_classes)


test_path = ['./test_path/image.jpg']
# test_path = []
# listdir('lego_test', test_path)
# predict_model()
# 创建一个Socket服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

# 开始监听连接
s.listen(1)

# 等待连接
#conn, addr = s.accept()
#print("Connected by", addr)

cap = cv2.VideoCapture(0)
# 接收消息
while True:
    conn, addr = s.accept()
    print("Connected by", addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        ret, frame = cap.read()
        cv2.imwrite(test_path[0], frame)
        print("Received message:", data)
        result = predict_model()
        conn.send(result.encode('utf-8'))

cap.release()

# 关闭连接
conn.close()
