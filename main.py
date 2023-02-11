import os
import sqlite3
import sys
import pygame

from catchfoodgame import catchfoodgamef
import catchfoodgame
from button_and_consts import Button, WIDTH, HEIGHT, FPS, terminate
import flappy_cat
import micehunt
import datetime


all_sprites = pygame.sprite.Group()
startsc_buttons = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    imagel = pygame.transform.scale(load_image('logo.png'), (400, 200))
    screen.blit(imagel, (10, 20))
    startb = Button(50, 220, load_image('start.png'), (250, 75), screen)
    quitb = Button(50, 305, load_image('quit.png'), (250, 75), screen)
    cat = AnimatedSprite(pygame.transform.scale(load_image('cat1.png'), (600, 300)), 2, 1, 460, 80)
    i = 1
    all_sprites.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if not i % 30:
            screen.blit(fon, (0, 0))
            screen.blit(imagel, (10, 20))
            cat.update()
            all_sprites.draw(screen)
        if startb.draw():
            return True
        if quitb.draw():
            terminate()

        i += 1
        pygame.display.flip()
        clock.tick(FPS)


def extra_screen():
    pygame.draw.rect(screen, (255, 255, 255), (40, 40, 720, 470))
    quitb2 = Button(720, 40, load_image('cross.png'), (40, 40), screen)
    return quitb2


def game_screen():
    q = extra_screen()
    flappycat = Button(50, 50, load_image('game3.png'), (500, 113), screen)
    micehuntb = Button(50, 183, load_image('game2.png'), (500, 113), screen)
    catchfood = Button(50, 316, load_image('game1.png'), (500, 113), screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
            return
        if flappycat.draw():
            flappy_cat.screen = screen
            flappy_cat.clock = clock
            if flappy_cat.main():
                pygame.mixer.music.load('sound_data/fon.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
                return
        if micehuntb.draw():
            micehunt.screen = screen
            micehunt.clock = clock
            if micehunt.micehunt_f():
                pygame.mixer.music.load('sound_data/fon.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
                return
        if catchfood.draw():
            catchfoodgame.screen = screen
            catchfoodgame.clock = clock
            if catchfoodgamef():
                pygame.mixer.music.load('sound_data/fon.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
                return
        pygame.display.flip()
        clock.tick(FPS)


def food_screen():
    q = extra_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
            return
        pygame.display.flip()
        clock.tick(FPS)


def clothes_screen():
    q = extra_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
            return
        pygame.display.flip()
        clock.tick(FPS)


def shop_screen():
    q = extra_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
            return
        pygame.display.flip()
        clock.tick(FPS)


clicked = False


def meow(cat, pos):
    global clicked
    r = cat.get_rect()
    r.topleft = (275, 185)
    if r.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] and not clicked:
            clicked = True
            pygame.mixer.Sound('sound_data/gameover.mp3').play()
    if not pygame.mouse.get_pressed()[0]:
        clicked = False


def draw_foodsc():
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    coins = cur.execute('''SELECT coins from money''').fetchone()[0]


if __name__ == '__main__':
    pygame.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('CatLIFE')
    pygame.mixer.music.load('sound_data/fon.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    clock = pygame.time.Clock()
    running = True
    a = start_screen()
    if a:
        food_scale = pygame.transform.scale(load_image('foodsc.png'), (90, 100))
        screen.blit(food_scale, (300, 5))
        connect = sqlite3.connect('tamagochi.db')
        cur = connect.cursor()
        coins = cur.execute('''SELECT coins from money''').fetchone()[0]
        coin = pygame.transform.scale(load_image('coin.png'), (70, 70))
        font = pygame.font.Font(None, 100)
        string_rendered = font.render(str(coins), 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.topleft = (80, 5)
        screen.blit(string_rendered, intro_rect)
        screen.blit(coin, (5, 5))
        fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        gamesb = Button(72, 450, load_image('games.png'), (110, 110), screen)
        foodb = Button(254, 440, load_image('food.png'), (110, 110), screen)
        clothesb = Button(436, 440, load_image('clothes.png'), (110, 110), screen)
        shopb = Button(618, 440, load_image('shop.png'), (110, 110), screen)
        maincat = pygame.transform.scale(load_image('maincat.png'), (250, 250))
        screen.blit(maincat, (275, 185))
        rect = maincat.get_rect()
        connect.close()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            screen.blit(fon, (0, 0))
            if gamesb.draw():
                game_screen()
            if foodb.draw():
                food_screen()
            if clothesb.draw():
                clothes_screen()
            if shopb.draw():
                shop_screen()
            screen.blit(maincat, (275, 185))
            pos = pygame.mouse.get_pos()
            screen.blit(coin, (5, 5))
            screen.blit(string_rendered, intro_rect)

            meow(maincat, pos)
            pygame.draw.rect(screen, (255, 255, 255), (300, 5, 90, 100))
            draw_foodsc()
            screen.blit(food_scale, (300, 5))
            pygame.display.flip()
            clock.tick(FPS)