import random
from os import path
from Env import *
from Explosion import Explosion
from Bullet import Bullet
from Meteor import Meteor
from Player import Player
from Begin_State import Begin_State
import pygame

# TODO Refactor 將參數統一放到另外一個檔案


font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)

class Support(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(3, 8)
        self.bolt = []
        for i in range(1, 3):
            self.bolt.append(pygame.image.load(path.join(img_dir, "bolt_{0}.png".format(i))))

        self.pill = []
        for i in range(1, 4):
            self.pill.append(pygame.image.load(path.join(img_dir, "pill_{0}.png".format(i))))

        if type == 0:
            self.image = self.bolt[random.randint(0, 1)]
            self.i = 0
        if type == 1:
            self.image = self.pill[random.randint(0, 2)]
            self.i = 1

        self.image = pygame.transform.scale(self.image, (self.size * 4, self.size * 4))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(7, 15)
        self.image_origin = self.image
        self.rot_angle = 5
        self.angle = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        old_center = self.rect.center
        self.angle = self.angle + self.rot_angle
        self.image = pygame.transform.rotate(self.image_origin, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        if (self.rect.centery > HEIGHT):
            self.kill()


def newMeteor():
    global all_sprites
    m = Meteor(meteors, all_sprites)
    meteors.add(m)
    all_sprites.add(m)

def newSupport(x, y):
    global all_sprites
    if random.randint(0, 10) > 5:
        i = random.randint(0, 1)
        if i == 0:
            s = Support(x, y, i)
            bolt.add(s)
            all_sprites.add(s)
        if i == 1:
            p = Support(x, y, i)
            pill.add(p)
            all_sprites.add(p)


screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 設定寬高(畫布)
bg = pygame.image.load(path.join(img_dir, 'background.png'))  # 背景圖片
bg_rect = bg.get_rect()  # 會更新
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()  # sprite是一個角色 meteos是一對隕石的群組
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # 同上，子彈的
bolt = pygame.sprite.Group()
pill = pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)
a = 0
power = 1
lives = 3


for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
all_sprites.add(pill)

running = True
all_sprites.add(bolt)
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))


def check_meteor_hit_player():
    global running, meteors, lives,gamestate
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player")
            newMeteor()
            # TODO 修改死亡的規則，改成扣血扣到0時，遊戲才結束
            player.shield = player.shield - hit.size * 20
            if player.shield <= 0 and lives > 1:
                lives -= 1
                player.shield = 100
            elif lives <= 1 and player.shield <= 0:
                lives -= 1
                gamestate = "begin"

def check_pill_hit_player():
    global running, pill
    hits = pygame.sprite.spritecollide(player, pill, False, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            print("shield ")
            if player.shield <= 90:
                player.shield = player.shield + 10
            hit.kill()
            # print("check_meteor_hit_player")
            # TODO 修改死亡的規則，改成扣血扣到0時，遊戲才結束

def check_bolt_hit_player():
    global running, bolt,power, power_time
    hits = pygame.sprite.spritecollide(player, bolt, False, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            power_time = pygame.time.get_ticks()
            power = 2

            hit.kill()

def check_bullets_hit_meteor():
    global score
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    if hits:
        for hit in hits:
            # TODO 02.修改加分的機制

            score += round(60 / hit.size)
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            newSupport(hit.rect.centerx, hit.rect.centery)
            hit.kill()
            # print("check_bullets_hit_meteor")
            newMeteor()
            # TODO 04.增加爆炸的動畫
            # TODO 06.擊破隕石會掉出武器或是能量包 武器可以改變攻擊模式 能量包可以回血

def draw_score():
    font = pygame.font.Font(font_name, 32)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2, 20)
    screen.blit(text_surface, text_rect)
    pass

def check_power_time():
    global power,power_time
    if power == 2 and pygame.time.get_ticks() - power_time > 6000:
        power  = 1
        power_time = pygame.time.get_ticks()

def shoot():
    global power
    if power == 1:
        sound_pew.play()
        bullet = Bullet(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites.add(bullet)
    elif power == 2:
        sound_pew.play()
        bullet1 = Bullet(player.rect.centerx - 10, player.rect.centery)
        bullet2 = Bullet(player.rect.centerx + 10, player.rect.centery)
        bullets.add(bullet1)
        bullets.add(bullet2)
        all_sprites.add(bullet1)
        all_sprites.add(bullet2)

def draw_shield():
    shield_bar = pygame.rect.Rect(20, 20, player.shield, 10)
    outline_rect = pygame.rect.Rect(20, 20, 100, 10)
    pygame.draw.rect(screen, GREEN, shield_bar)
    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)
    pass

def draw_shield_score():
    fonts = pygame.font.Font(font_name, 14)
    text_surface = fonts.render(str(player.shield), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (140, 17)
    screen.blit(text_surface, text_rect)
    pass

def draw_lives(lives):
    if lives == 0:
        gamestate = "begin"
    for i in range ( lives):
        life = pygame.rect.Rect(WIDTH -100 + 30 * i, 20,10, 10)
        pygame.draw.rect(screen, (255,0,0), life)
begin =Begin_State(screen)
gamestate = "begin"


while running:
    # clocks control how fast the loop will execute

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if gamestate == "begin":
        begin.keyhandle()
        begin.show()
        gamestate = begin.updateState()
        player.shield = 100
        lives = 3


    if gamestate == "start":
        # event trigger
        a = 0
        # TODO 新增起始畫面 按下空白鍵才開始遊戲
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # 如果是FALSE，while不成立，跳出去，才會QUIT
            # if event.type == pygame.KEYDOWN:
            # TODO 03.修正成子彈可以連發
            # if event.key == pygame.K_SPACE:
            #     shoot()

        check_bolt_hit_player()
        check_power_time()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_shot > SHOT_DELAY:
                last_shot = now
                shoot()

        # update the state of sprites
        check_meteor_hit_player()
        #
        check_bullets_hit_meteor()
        check_pill_hit_player()

        all_sprites.update()

        # draw on screen

        # screen.fill(BLACK)

        screen.blit(bg, bg_rect)
        draw_shield()
        draw_shield_score()
        draw_lives(lives)
        all_sprites.draw(screen)  # 把東西畫上去
        draw_score()
        # flip to display
        pygame.display.flip()



pygame.quit()
