#!/usr/bin/python3
# 1.封装主游戏类
# 2.创建游戏对象
# 3.启动游戏

import pygame
import sys
from plane_sprites import *

class PlaneGame(object):
    # 初始化
    def __init__(self):
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 创建精灵
        self.__creat_sprites()
        # 定时创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        # 定时发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT,500)

    # 创建精灵/精灵组
    def __creat_sprites(self):
        # 敌人组
        self.enemy_group = pygame.sprite.Group()
        # 英雄组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 背景精灵和背景组
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)


    # 开始游戏
    def start_game(self):
        while True:
            # 设置刷新率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新精灵组
            self.__update_sprites()
            # 更新屏幕显示
            pygame.display.update()

    # 事件监听
    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_group.add(Enemy())
            elif event.type ==HERO_FIRE_EVENT:
                self.hero.fire()

        # 按键控制英雄
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.hero.speed = -3
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.hero.speed = 3
        else:
            self.hero.speed = 0

    # 碰撞检测
    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(enemies)>0:
            self.hero.kill()
            PlaneGame.__game_over()


    # 更新精灵组
    def __update_sprites(self):
        for group in [self.back_group,self.enemy_group,self.hero_group,self.hero.bullets]:
            group.update()
            group.draw(self.screen)

    # 游戏结束
    @staticmethod
    def __game_over():
        pygame.quit()
        exit()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    game = PlaneGame()
    game.start_game()

