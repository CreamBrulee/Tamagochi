import glob
import random

import pygame
import os
import sys
from button_and_consts import WIDTH, HEIGHT, FPS, terminate, Button, earning_money
import sqlite3


all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
height = HEIGHT
screen = 0
clock = 0
score = 0


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def start_screen():
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    play = Button(325, 168, load_image('start_end/play.png'), (150, 75), screen)
    logo = pygame.transform.scale(load_image('data/game1.png'), (400, 88))
    screen.blit(logo, (200, 30))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if play.draw():
            return
        if q.draw():
            return True
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    global score
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    bestsc = cur.execute('''SELECT bestscore from bestscores WHERE game = "catch food"''').fetchone()
    if bestsc[0] >= score:
        sc_image = 'start_end/score.png'
        s = (150, 60)
        x = 0
    else:
        sc_image = 'start_end/newscore.png'
        s = (180, 60)
        x = 50
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    logo = pygame.transform.scale(load_image('start_end/gameover.png'), (250, 125))
    screen.blit(logo, (275, 30))
    scim = pygame.transform.scale(load_image(sc_image), s)
    screen.blit(scim, (250 - x, 165))
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(score), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (420, 165)
    screen.blit(string_rendered, intro_rect)
    re = Button(300, 245, load_image('start_end/replay.png'), (200, 56), screen)
    pygame.mixer.Sound('sound_data/game_over.wav').play()
    if sc_image == 'start_end/newscore.png':
        cur.execute('UPDATE bestscores SET bestscore = ? WHERE game = "catch food"', (score,))
        connect.commit()
    connect.close()
    earning_money(screen, score // 3 if score >= 3 or score == 0 else 1)
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if re.draw():
            catchfoodgamef()
        if q.draw():
            return True
        pygame.display.flip()
        clock.tick(FPS)


class Catplayer(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('data_foodcatch/cat.png'), (200, 200))
    image2 = pygame.transform.flip(image, True, False)

    def __init__(self):
        super().__init__(player)
        self.image = Catplayer.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height - 80
        self.rect.left = 300

    def go_left(self):
        if self.rect.left >= 5:
            self.rect.left -= 5
        else:
            self.rect.left = 0
        self.image = Catplayer.image
        self.mask = pygame.mask.from_surface(self.image)

    def go_right(self):
        if self.rect.right <= 795:
            self.rect.left += 5
        else:
            self.rect.right = 800
        self.image = Catplayer.image2
        self.mask = pygame.mask.from_surface(self.image)

moving = 1

class Food(pygame.sprite.Sprite):
    images = [pygame.transform.scale(load_image(i), (
        40, 40)) for i in glob.glob('data/eatings/*')]

    def __init__(self):
        super().__init__(all_sprites)
        self.images = Food.images
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(20, 740)
        self.rect.y = -40

    def update(self, cat):
        global score
        if not pygame.sprite.collide_mask(self, cat):
            self.rect = self.rect.move(0, moving)
            if self.rect.bottom >= height - 80:
                if end_screen():
                    return True
        else:
            m = pygame.mixer.Sound('sound_data/catch.wav')
            m.play()
            m.set_volume(0.5)
            score += 1
            self.kill()


class Bomb(Food):
    bomb = pygame.transform.scale(load_image('data_foodcatch/bomb.png'), (
        40, 40))

    def __init__(self):
        super().__init__()
        print('khjhj')
        self.image = Bomb.bomb
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(20, 740)
        self.rect.y = -40

    def update(self, cat):
        global score
        if not pygame.sprite.collide_mask(self, cat):
            self.rect = self.rect.move(0, moving)
            if self.rect.bottom >= height - 80:
                self.kill()
        else:
            if end_screen():
                return True



def catchfoodgamef():
    global moving
    for i in all_sprites:
        i.kill()
    for i in player:
        i.kill()
    fon = pygame.transform.scale(load_image('data_foodcatch/fonforfoodcatch.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    running = True
    pygame.mixer.music.load('sound_data/catchfood.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    cat = Catplayer()
    player.draw(screen)
    sc = pygame.transform.scale(load_image('start_end/score.png'), (100, 40))
    font = pygame.font.Font(None, 70)
    string_rendered = font.render(str(score), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (115, 5)
    k = 0
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    if start_screen():
        return True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            cat.go_left()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            cat.go_right()
        if not k % 170:
            f = random.randrange(0, 4)
            if f == 2:
                Bomb()
            else:
                Food()
            moving += 0.1
        k += 1
        screen.blit(fon, (0, 0))
        player.draw(screen)
        player.update()
        all_sprites.draw(screen)
        if all_sprites.update(cat):
            return True
        screen.blit(sc, (5, 5))
        string_rendered = font.render(str(score), 1, pygame.Color('black'))
        screen.blit(string_rendered, intro_rect)
        if q.draw():
            return True
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    catchfoodgamef()