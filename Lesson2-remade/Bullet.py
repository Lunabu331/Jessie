import pygame
from os import  path
from Env import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_gun.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()