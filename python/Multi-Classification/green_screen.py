import cv2
import numpy as np

# 读取并转换图片格式
opencv = cv2.imread('/')
hsv = cv2.cvtColor(opencv, cv2.COLOR_RGB2HSV)

# 指定绿色范围,60表示绿色，取的范围是-+10
minGreen = np.array([50, 100, 100])
maxGreen = np.array([70, 255, 255])

# 确定绿色范围
mask = cv2.inRange(hsv, minGreen, maxGreen)

# 确定非绿色范围
mask_not = cv2.bitwise_not(mask)

# 通过掩码控制的按位与运算锁定绿色区域
green = cv2.bitwise_and(opencv, opencv, mask=mask)

# 通过掩码控制的按位与运算锁定非绿色区域
green_not = cv2.bitwise_and(opencv, opencv, mask=mask_not)

# 拆分为3通道
b, g, r = cv2.split(green_not)

# 合成四通道
bgra = cv2.merge([b, g, r, mask_not])

# 保存带有透明通道的png图片
cv2.imwrite('/', bgra)

# 显示图片验证结果
cv2.imshow('opencv', opencv)
cv2.imshow('green', green)
cv2.imshow('green_not', green_not)
cv2.waitKey()
cv2.destroyAllWindows()

