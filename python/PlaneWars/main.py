#!/usr/bin/python3
# 1.封装主游戏类
# 2.创建游戏对象
# 3.启动游戏

import pygame
import sys,time,math,random
import traceback
from pygame.locals import *
from plane_sprites import *


pygame.init()
# pygame.mixer.init()
# 创建游戏窗口
screen = pygame.display.set_mode(SCREEN_RECT.size)
# 创建标题
pygame.display.set_caption ("PlaneWars")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 创建游戏时钟
clock = pygame.time.Clock()

# 创建精灵/精灵组
# 敌人组
enemy_group = pygame.sprite.Group()
# 英雄组
hero = Hero()
hero_group = pygame.sprite.Group(hero)
# 背景精灵和背景组
bg1 = BackGround()
bg2 = BackGround(True)
back_group = pygame.sprite.Group(bg1, bg2)

# 载入游戏音乐
pygame.mixer.music.load ("sound/game_music.ogg")
pygame.mixer.music.set_volume (0.2)

def main():
    # 播放背景音乐
    pygame.mixer.music.play()
    # 统计得分
    score = 0
    score_font = pygame.font.Font(None, 36)

    delay = 50
    # 游戏结束画面
    gameover_font = pygame.font.Font(None, 48)
    again_image = pygame.image.load("./images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("./images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    game_over = False
    while not game_over:
        # 定时创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,5000)
        # 定时发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT,1500)
        # 设置刷新率
        clock.tick(FRAME_PER_SEC)

        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CREATE_ENEMY_EVENT:
                enemy_group.add(Enemy())
            elif event.type ==HERO_FIRE_EVENT:
                hero.fire()

        # 按键控制英雄
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            hero.move_left()
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            hero.move_right()
        elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            hero.move_up()
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            hero.move_down()

        # 显示得分
        score_text = score_font.render ("Score : %s" % str(score), True, WHITE)
        screen.blit (score_text, (10, 5))

        # 碰撞检测
        # 子弹摧毁敌机
        if pygame.sprite.groupcollide(hero.bullets,enemy_group,True,True):
            score+=100
        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(hero,enemy_group,True)
        if len(enemies)>0:
            hero.kill()
            game_over = True

        # 更新精灵组
        for group in [back_group,enemy_group,hero.bullets]:
            group.update()
            group.draw(screen)
        hero_group.draw(screen)

        # 游戏结束
        if game_over:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 绘制结束画面
            gameover_text1 = gameover_font.render ("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect ()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (SCREEN_RECT.width - gameover_text1_rect.width) // 2, SCREEN_RECT.height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render (str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect ()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (SCREEN_RECT.width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (SCREEN_RECT.width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (SCREEN_RECT.width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit (gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main ()
                # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit ()
                    sys.exit ()

        delay -= 1
        if not delay:
            delay = 100
        # 更新屏幕显示
        pygame.display.flip ()
        clock.tick (60)


if __name__ == "__main__":
    try:
      main()
    except SystemExit:
       pass
    except:
       traceback.print_exc ()
       pygame.quit ()
       input()

