import sys
import pygame
from pygame.locals import *
import math

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
yellow = 255, 255, 0

pygame.init()

screen = pygame.display.set_mode((1024, 600))  # 设置窗口
pygame.display.set_caption("Pie")  # 设置标题
myfont = pygame.font.Font(None, 80)  # 设置字体
textImage = myfont.render("Welcome to Pie", True, white)  # 渲染文本 true为抗锯齿
buttonimage = pygame.image.load("开始.png")
while True:
    # 点击窗口右上角X退出
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    screen.fill(black)  # 清除屏幕
    screen.blit(textImage, (300, 150))  # 绘制
    screen.blit(buttonimage, (500, 400)) # 绘制开始按钮
    pygame.display.update()  # 刷新显示

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and \
        500<=event.pos[0]<=600 and 400<=event.pos[1]<=450:

