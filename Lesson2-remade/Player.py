import pygame
import random
from os import  path

from Env import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):  # 初始化(__init__)
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50, 30))  # 造型
        self.rect = self.image.get_rect()  # rect是rectangle(矩形)
        self.rect.centerx = x  # 中心點X座標
        self.rect.centery = y  # 中心點Y座標
        self.speedx = 8
        self.speedy = 8
        self.shield = 100

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            self.move(self.speedx, 0)
        if keystate[pygame.K_UP]:
            self.move(0, -self.speedy)
        if keystate[pygame.K_DOWN]:
            self.move(0, self.speedy)
        # TODO 01.新增上下移動

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy