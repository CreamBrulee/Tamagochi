import os
import sqlite3
import sys
import pygame
import glob
import csv
from catchfoodgame import catchfoodgamef
import catchfoodgame
from button_and_consts import Button, WIDTH, HEIGHT, FPS, terminate
import flappy_cat
import micehunt
import button_and_consts
import datetime

all_sprites = pygame.sprite.Group()
startsc_buttons = pygame.sprite.Group()


def load_image(name, colorkey=None):
    if not name.split('/')[0] == 'data':
        fullname = os.path.join('data', name)
    else:
        fullname = name
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

    con = sqlite3.connect("clothes_and_food.db")

    # Создание курсора
    cur = con.cursor()
    con_scale_food = sqlite3.connect("tamagochi.db")

    # Создание курсора
    cur_scale_food = con_scale_food.cursor()
    result = cur.execute("""SELECT name, have FROM food""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))
    names = []
    buttons_food = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:
        kol += 1
        buttons_food.append(
            Button(85 + 110 * (kol - 1), 80, load_image('eatings/' + i + '.PNG'), (70, 70), screen, i, False))

    for i in buttons_food:
        i.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons_food:
                    print(1)
                    if i.draw():
                        pygame.mixer.Sound('sound_data/click.mp3').play()
                        print(1)
                        if int(cur_scale_food.execute("""SELECT percentage FROM scales""").fetchall()[0][0]) +5>=100:
                            cur_scale_food.execute('UPDATE scales SET percentage = ?',
                                                   (100,))
                        else:
                            cur_scale_food.execute('UPDATE scales SET percentage = ?',
                                          (int(cur_scale_food.execute("""SELECT percentage FROM scales""").fetchall()[0][0]) +
                                           +5,))
                        cur.execute('UPDATE food SET have = ? WHERE name = ?', (int(cur.execute("""SELECT have FROM food
                                    WHERE name = ?""", (i.name_for_food,)).fetchall()[0][0]) - 1, i.name_for_food))
                        con.commit()
                        con_scale_food.commit()
        if q.draw():
            food_scale = pygame.transform.scale(load_image('foodsc.png'), (90, 100))
            screen.blit(food_scale, (300, 5))

            coin = pygame.transform.scale(load_image('coin.png'), (70, 70))
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
                draw_money()
                meow(maincat, pos)
                pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
                draw_foodsc()
                screen.blit(food_scale, (300, 5))
                pygame.display.flip()
                clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)
        q = extra_screen()
        result = cur.execute("""SELECT name, have FROM food""").fetchall()
        result = list(filter(lambda item: int(item[1]), result))
        names = []
        buttons_food = []
        for i in result:
            names.append(i[0])
        kol = 0
        for i in names:
            kol += 1
            buttons_food.append(
                Button(85 + 110 * (kol - 1), 80, load_image('eatings/' + i + '.PNG'), (70, 70), screen, i, False))
        for i in buttons_food:
            i.draw()


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
    con = sqlite3.connect("clothes_and_food.db")

    # Создание курсора
    cur = con.cursor()
    con_money = sqlite3.connect("tamagochi.db")

    # Создание курсора
    cur_money = con_money.cursor()

    buttons_buy = []
    food = ['burger', 'chese', 'chicken', 'egg', 'fish', 'peach']
    buy = pygame.transform.scale(load_image('buy.PNG'), (
        70, 40))
    kol = 0
    cost_of_food = ['5', '3', '4', '2', '5', '7']
    costs_of_food_with_names = {'burger': 5, 'chese': 3, 'chicken': 4, 'egg': 2, 'fish': 5, 'peach': 7}
    costs_of_clothes_with_names = {'bant': 60, 'choker_blue': 30, 'choker_green': 30, 'fartyk': 89, 'hair': 50, 'hat': 35, 'jevelery': 40, 'nose' : 15}

    for i in range(6):
        kol += 1
        screen.blit(pygame.transform.scale(load_image('eatings/' + food[i] + '.png'), (70, 70)), (85 + 110 * (i), 80))
        buttons_buy.append(Button(75 + 110 * (kol - 1), 160, buy, (70, 40), screen, food[i]))
        screen.blit(pygame.transform.scale(load_image('costs/' + cost_of_food[i] + '.png'), (35, 35)),
                    (145 + 110 * (kol - 1), 165))
    kol = 0
    for key, volume in costs_of_clothes_with_names.items():
        if kol < 6:
            screen.blit(pygame.transform.scale(load_image('clothes/' + key + '.png'), (70, 70)), (85 + 110 * (kol), 240))
            buttons_buy.append(Button(75 + 110 * (kol), 320, buy, (70, 40), screen, key))
            #screen.blit(pygame.transform.scale(load_image('costs/' + str(volume) + '.png'), (35, 35)),
            #            (145 + 110 * (kol - 1), 165))
        kol += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
            return
        kol = 0
        for i in range(6):
            kol += 1
            screen.blit(pygame.transform.scale(load_image('eatings/' + food[i] + '.png'), (70, 70)),
                        (85 + 110 * (i), 80))
        for i in range(len(buttons_buy)):
            button = buttons_buy[i]
            index = i
            if button.draw():
                result = int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0])
                if costs_of_food_with_names[button.name_for_food] > result:
                    q = extra_screen()
                    screen.blit(pygame.transform.scale(load_image('fon_without_money.png'), (800, 550)),
                                (0, 0))
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                terminate()
                        if q.draw():
                            return
                        pygame.display.flip()
                        clock.tick(FPS)
                else:
                    result = cur.execute("""SELECT have FROM food
                                WHERE name = ?""", (food[index],)).fetchall()[0][0]
                    cur_money.execute('UPDATE money SET coins = ?',
                                      (int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0]) - costs_of_food_with_names[button.name_for_food],))

                    if int(result) != 0:
                        cur.execute('UPDATE food SET have = ? WHERE name = ?', (int(result) + 1, food[index]))
                    else:
                        cur.execute('UPDATE food SET have = ? WHERE name = ?', (1, food[index]))
                    con_money.commit()
                    con.commit()

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
    date = cur.execute('''SELECT date from scales''').fetchone()[0]
    percents = cur.execute('''SELECT percentage from scales''').fetchone()[0]
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds // 60
    x = 100 - (100 * (percents - 0.84 * time) // 100 if (percents - 0.84 * time) > 0 else 0)
    button_and_consts.perc = percents - 0.14 * time
    pygame.draw.rect(screen, (100, 100, 100), (300, 5, 90, x))
    connect.close()


def draw_money():
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    coins = cur.execute('''SELECT coins from money''').fetchone()[0]
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(coins), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (80, 5)
    screen.blit(string_rendered, intro_rect)
    connect.close()


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

        coin = pygame.transform.scale(load_image('coin.png'), (70, 70))
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
            draw_money()
            meow(maincat, pos)
            pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
            draw_foodsc()
            screen.blit(food_scale, (300, 5))
            pygame.display.flip()
            clock.tick(FPS)
