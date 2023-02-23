# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import os.path
import copy

# 椒盐噪声
def SaltAndPepper(src,percetage):
    SP_NoiseImg=src.copy()
    SP_NoiseNum=int(percetage*src.shape[0]*src.shape[1])
    for i in range(SP_NoiseNum):
        randR=np.random.randint(0,src.shape[0]-1)
        randG=np.random.randint(0,src.shape[1]-1)
        randB=np.random.randint(0,3)
        if np.random.randint(0,1)==0:
            SP_NoiseImg[randR,randG,randB]=0
        else:
            SP_NoiseImg[randR,randG,randB]=255
    return SP_NoiseImg

# 高斯噪声
def addGaussianNoise(image,percetage):
    G_Noiseimg = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    G_NoiseNum=int(percetage*image.shape[0]*image.shape[1])
    for i in range(G_NoiseNum):
        temp_x = np.random.randint(0,h)
        temp_y = np.random.randint(0,w)
        G_Noiseimg[temp_x][temp_y][np.random.randint(3)] = np.random.randn(1)[0]
    return G_Noiseimg

# 昏暗
def darker(image,percetage=0.9):
    image_copy = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    #get darker
    for xi in range(0,w):
        for xj in range(0,h):
            image_copy[xj,xi,0] = int(image[xj,xi,0]*percetage)
            image_copy[xj,xi,1] = int(image[xj,xi,1]*percetage)
            image_copy[xj,xi,2] = int(image[xj,xi,2]*percetage)
    return image_copy

# 亮度
def brighter(image, percetage=1.5):
    image_copy = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    #get brighter
    for xi in range(0,w):
        for xj in range(0,h):
            image_copy[xj,xi,0] = np.clip(int(image[xj,xi,0]*percetage),a_max=255,a_min=0)
            image_copy[xj,xi,1] = np.clip(int(image[xj,xi,1]*percetage),a_max=255,a_min=0)
            image_copy[xj,xi,2] = np.clip(int(image[xj,xi,2]*percetage),a_max=255,a_min=0)
    return image_copy

# 旋转
def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    # If no rotation center is specified, the center of the image is set as the rotation center
    if center is None:
        center = (w / 2, h / 2)
    m = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, m, (w, h))
    return rotated

# 翻转
def flip(image):
    flipped_image = np.fliplr(image)
    return flipped_image

def save_change(file_dir):
    # 注释中的图片 数据增强直接放在了当前文件夹下，没有进行创建新的文件夹去保存
    for img_name in os.listdir(file_dir):
        #img_path = file_dir + img_name
        img_path = file_dir + '/' + img_name
        img = cv2.imread(img_path)
        # cv2.imshow("1",img)
        # cv2.waitKey(5000)
        # 旋转
        rotated_90 = rotate(img, 90)
        cv2.imwrite(file_dir +'/'+ img_name[0:-4] + '_r90.jpg', rotated_90)
        rotated_180 = rotate(img, 180)
        cv2.imwrite(file_dir +'/'+ img_name[0:-4] + '_r180.jpg', rotated_180)

    for img_name in os.listdir(file_dir):
        #img_path = file_dir + img_name
        img_path = file_dir + '/' + img_name
        img = cv2.imread(img_path)
        # 镜像
        flipped_img = flip(img)
        cv2.imwrite(file_dir +'/'+img_name[0:-4] + '_fli.jpg', flipped_img)

        # 增加噪声
        # img_salt = SaltAndPepper(img, 0.3)
        # cv2.imwrite(file_dir + img_name[0:7] + '_salt.jpg', img_salt)
        img_gauss = addGaussianNoise(img, 0.3)
        cv2.imwrite(file_dir +'/'+ img_name[0:-4] + '_noise.jpg',img_gauss)

        #变亮、变暗
        img_darker = darker(img)
        cv2.imwrite(file_dir+'/' + img_name[0:-4] + '_darker.jpg', img_darker)
        img_brighter = brighter(img)
        cv2.imwrite(file_dir+'/' + img_name[0:-4] + '_brighter.jpg', img_brighter)

        blur = cv2.GaussianBlur(img, (7, 7), 1.5)
        #      cv2.GaussianBlur(图像，卷积核，标准差）
        cv2.imwrite(file_dir+'/' + img_name[0:-4] + '_blur.jpg',blur)


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("---  OK  ---")
	else:
		print("---  There is this folder!  ---")


# 数据增强：图片翻转
# def FigRotated(path):
#     dirs=[""]
#     for dir in dirs:
#         filelist = os.listdir(dir) # 获取指定的文件夹包含的文件或文件夹的名字的列表
#         print(filelist)
#         total_num = len(filelist) #获取文件夹内所有文件个数
#         print(total_num)
    
        #c = 0 # 想看总共 重命名了多少张图片
    
        #for files in filelist:
            #figsPath = path + files + '/visual'  #原来的视觉路径信息
            #figures = os.listdir(figsPath) #原先视觉文件夹中的所有图片
        
            #total_figure = len(figures)
            #print(total_figure)
        
        
            #for fig in figures:
                # 想要去新建文件夹: 关于数据增强是翻转的，让其添加 rotated 
                #对原数据的文件夹切割，主要就是为了便于获取标签和文件夹名字
                #yearMonthDate, Hour, minute, label = files.split("-")
                #yearNewFileName = yearMonthDate + "rotated90" #翻转90
                #新的保存数据增强的视觉 文件夹名称
                #filesNew = yearNewFileName + "-" + Hour + "-" + minute + "-" + label  
                #保存数据增强的图片
                #figsPathNew = path + filesNew + '/visual'   
                #mkdir(figsPathNew)
            
            
    #             fig_path = figsPath + '/' + fig # 单个图片的完整表示，包括路径
    #             img = cv2.imread(fig_path)  # img表示一张图片的具体信息。
    #             rotated_90 = rotate(img, 90) # rotated_90表示一张图片进行数据增强后的信息
    #             #cv2.imwrite(os.path.join(figsPathNew , fig[0:-4] + '.jpg'),  rotated_90) # 保存图片到指定文件夹中
    #             cv2.imwrite(os.path.join(figsPathNew , fig[0:-4] + '.jpg'),  rotated_90)
                # print("？")
    # print("ye ！！！")


if __name__ == '__main__':
    #FigRotated(path)
    dirs=[""]
    for dir in dirs:
        save_change(dir)

