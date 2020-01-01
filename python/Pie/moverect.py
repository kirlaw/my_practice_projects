import pygame
import sys
from pygame.locals import *
import random

color = 0, 0, 255  # 蓝色
width = 0
x = 250
y = 0
vel_x = 1.2
vel_y = 1

def randomcolor():
    r = lambda: random.randint(0, 255)
    return r(), r(), r()

pygame.init()

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("move rect")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                sys.exit()

    screen.fill((255, 255, 255))
    x += vel_x
    y += vel_y
    if x > 500 or x < 0:
        vel_x = -vel_x
        color = randomcolor()
    if y > 400 or y < 0:
        vel_y = -vel_y
        color = randomcolor()

    pos = x, y, 100, 100
    pygame.draw.rect(screen, color, pos, width)

    pygame.display.update()