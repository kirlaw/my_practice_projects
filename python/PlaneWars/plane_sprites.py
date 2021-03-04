#!/usr/bin/python3

import pygame
import random

# 窗口
SCREEN_RECT = pygame.Rect(0,0,500,700)
# 屏幕刷新率
FRAME_PER_SEC = 15
# 敌机定时器
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 发射子弹
HERO_FIRE_EVENT = pygame.USEREVENT+1

# 游戏精灵
class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image_name,speed =1):
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed


    def update(self):
        # 垂直向上移动
        self.rect.y += self.speed


class BackGround(GameSprite):
    # is_alt判断是否是另一张图像
    # False表示第一张，需要与屏幕重合；True是另一种，在屏幕正上方
    def __init__(self,is_alt=False):
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y = -self.rect.height


    def update(self):
        super().update()
        # 判断图像是否移出屏幕，若是将图像设置到屏幕正上方，实现滚动效果
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


# 敌机精灵
class Enemy(GameSprite):
    def __init__(self):
        super().__init__('./images/enemy1.png')
        # 设置初始速度
        self.speed = random.randint(1,3)
        # 设置初始位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width-self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):
        super().update()

        # 如果飞出屏幕，删除敌机
        if self.rect.y>=SCREEN_RECT.height:
            self.kill()

# 英雄精灵
class Hero(GameSprite):
    def __init__(self):
        super().__init__('./images/me1.png',0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120
        # 创建子弹
        self.bullets  = pygame.sprite.Group()

    def update(self):
        # 水平移动
        self.rect.x +=self.speed

        # 不能超出边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    # 发射子弹
    def fire(self):
        # 生成子弹
        for i in range(3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y-i*20
            bullet.rect.centerx = self.rect.centerx
            self.bullets.add(bullet)

# 子弹精灵
class Bullet(GameSprite):
    def __init__(self):
        super().__init__('./images/bullet1.png',-2)

    def update(self):
        super().update()
        # 超出屏幕则删除
        if self.rect.bottom <0:
            self.kill()
