import pygame
from Env import *

class Explosion(pygame.sprite.Sprite):
    ani_list = []
    for i in range(0, 8):
        ani_list.append(pygame.image.load(path.join(img_dir, "regularExplosion0{0}.png".format(i))))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "regularExplosion01.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.last_ani = pygame.time.get_ticks()
        self.ani_delay = 50
        self.ani_ind = 1

    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.last_ani > self.ani_delay) and (self.ani_ind < 8):
            self.image = self.ani_list[self.ani_ind]
            self.ani_ind += 1
        if self.ani_ind >= 8:
            self.kill()

    def play(self):
        pass