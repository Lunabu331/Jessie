import pygame
import random
from os import  path
from Env import *

bg = pygame.image.load(path.join(img_dir, 'background.png'))  # 背景圖片
bg_rect = bg.get_rect()  # 會更新
font_name = pygame.font.match_font('arial')
class Begin_State():

    def __init__(self, surf):
        self.surf = surf
        self.gamestate = "begin"
        pass
    def keyhandle(self):
        global  lives, keystate
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.gamestate = "start"

    def updateState(self):
        return self.gamestate
    def show(self):
        self.surf.blit(bg, bg_rect)

        font1 = pygame.font.Font(font_name, 64)
        text_surface = font1.render("JESSIE!", True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2, HEIGHT / 4)
        self.surf.blit(text_surface, text_rect)

        font2 = pygame.font.Font(font_name, 22)
        text_surface = font2.render("Arrow keys move, Space to fire", True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2, HEIGHT / 2)
        self.surf.blit(text_surface, text_rect)

        font3 = pygame.font.Font(font_name, 18)
        text_surface = font3.render("Press Space to begin", True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2, HEIGHT * 3 / 4)
        self.surf.blit(text_surface, text_rect)

        pygame.display.flip()