import os
import sqlite3
import sys
import pygame
from catchfoodgame import catchfoodgamef
import catchfoodgame
from button_and_consts import Button, WIDTH, HEIGHT, FPS, terminate
import flappy_cat
import micehunt
import button_and_consts
import datetime

cat1group = pygame.sprite.Group()
startsc_buttons = pygame.sprite.Group()
catgroup = pygame.sprite.Group()
coins_gr = pygame.sprite.Group()


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
        image = image
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
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

    def get_rect(self):
        return self.rect


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    imagel = pygame.transform.scale(load_image('logo.png'), (400, 200))
    screen.blit(imagel, (10, 20))
    startb = Button(50, 220, load_image('start.png'), (250, 75), screen)
    quitb = Button(50, 305, load_image('quit.png'), (250, 75), screen)
    cat = AnimatedSprite(pygame.transform.scale(load_image('cat1.png'), (600, 300)), 2, 1, 460, 80, cat1group)
    i = 1
    cat1group.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if not i % 30:
            screen.blit(fon, (0, 0))
            screen.blit(imagel, (10, 20))
            cat.update()
            cat1group.draw(screen)
        if startb.draw():
            cat.kill()
            return True
        if quitb.draw():
            terminate()

        i += 1
        pygame.display.flip()
        clock.tick(FPS)


def draw_fon():
    fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))


maincat = AnimatedSprite(pygame.transform.scale(load_image('spritesheet_maincat.png'), (1250, 750)), 5, 3, 275, 185,
                         catgroup)


def draw_acssesory():

    con = sqlite3.connect("clothes_and_food.db")

    # Создание курсора
    cur = con.cursor()
    con_scale_food = sqlite3.connect("tamagochi.db")

    # Создание курсора
    cur_scale_food = con_scale_food.cursor()
    result = cur.execute("""SELECT name, have, wearing FROM clothes""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))
    result = list(filter(lambda item: int(item[2]), result))
    names = []
    buttons_clothes = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:
        kol += 1
        screen.blit(pygame.transform.scale(load_image('clothes/for_cat/' + i + '.png'), (250, 250)), (275, 185))


def draw_maincat():
    maincat.update()
    catgroup.draw(screen)
    meow(maincat, pygame.mouse.get_pos())
    draw_acssesory()


def draw_foodsc_start():
    pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    date = cur.execute('''SELECT date from scales''').fetchone()[0]
    percents = cur.execute('''SELECT percentage from scales''').fetchone()[0]
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    button_and_consts.perc = percents - 0.01388 * time if percents - 0.01388 * time >= 0 else 0
    x = 100 - button_and_consts.perc
    if button_and_consts.perc <= 50:
        feed = pygame.transform.scale(load_image('feed.png'), (175, 50))
        screen.blit(feed, (10, 100))
    pygame.draw.rect(screen, (100, 100, 100), (300, 5, 90, x))
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "food"''', (datetime.datetime.now(), ))
    connect.commit()
    connect.close()
    food_scale = pygame.transform.scale(load_image('foodsc.png'), (90, 100))
    screen.blit(food_scale, (300, 5))


def draw_foodsc():
    pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    date = cur.execute('''SELECT date from scales''').fetchone()[0]
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    button_and_consts.perc = button_and_consts.perc - time * 0.01388 if button_and_consts.perc - time * 0.01388 >= 0 else 0
    x = 100 - button_and_consts.perc
    if button_and_consts.perc <= 50:
        feed = pygame.transform.scale(load_image('feed.png'), (175, 50))
        screen.blit(feed, (10, 100))
    pygame.draw.rect(screen, (100, 100, 100), (300, 5, 90, x))
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "food"''', (datetime.datetime.now(),))
    connect.commit()
    connect.close()
    food_scale = pygame.transform.scale(load_image('foodsc.png'), (90, 100))
    screen.blit(food_scale, (300, 5))


coin = AnimatedSprite(pygame.transform.scale(load_image('money.png'), (420, 70)), 6, 1, 5, 5, coins_gr)
k = 0


def draw_money():
    global k
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    coins = cur.execute('''SELECT coins from money''').fetchone()[0]
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(coins), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (80, 5)
    screen.blit(string_rendered, intro_rect)
    connect.close()
    if not k % 2:
        coin.update()
    coins_gr.draw(screen)
    k += 1


def extra_screen():
    pygame.draw.rect(screen, (255, 255, 255), (40, 40, 720, 470))
    quitb2 = Button(720, 40, load_image('cross.png'), (40, 40), screen)
    return quitb2


def extra_screen_food_and_clothes():
    pygame.draw.rect(screen, (255, 255, 255), (40, 400, 720, 110))
    quitb2 = Button(720, 400, load_image('cross.png'), (40, 40), screen)
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
    q = extra_screen_food_and_clothes()

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
            Button(75 + 110 * (kol - 1), 420, load_image('eatings/' + i + '.PNG'), (50, 50), screen, i, False))
        screen.blit(pygame.transform.scale(load_image('costs/' + '1' + '.png'), (25, 25)),
                    (80 + 110 * (kol - 1), 475))
    for i in buttons_food:
        i.draw()

    while True:
        draw_fon()
        draw_money()
        draw_foodsc()
        draw_maincat()
        extra_screen_food_and_clothes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons_food:
                    if i.draw():
                        pygame.mixer.Sound('sound_data/click.mp3').play()
                        button_and_consts.perc = button_and_consts.perc + 5 if button_and_consts.perc + 5 <= 100 else 100
                        cur.execute('UPDATE food SET have = ? WHERE name = ?', (int(cur.execute("""SELECT have FROM food
                                    WHERE name = ?""", (i.name_for_food_or_for_clothes,)).fetchall()[0][0]) - 1, i.name_for_food_or_for_clothes))
                        con.commit()
                        con_scale_food.commit()


        if q.draw():
            return

        result = cur.execute("""SELECT name, have FROM food""").fetchall()
        print(result)
        result = list(filter(lambda item: int(item[1]), result))
        names = {}
        buttons_food = []
        for i in result:
            names[i[0]] = int(i[1])
        kol = 0
        print(result)
        for key, volume in names.items():
            kol += 1
            buttons_food.append(
                Button(75 + 110 * (kol - 1), 420, load_image('eatings/' + key + '.PNG'), (50, 50), screen, key, False))
            if volume >= 10:
                screen.blit(pygame.transform.scale(load_image('costs/' + str(volume)[0] + '.png'), (25, 25)),
                        (80 + 110 * (kol - 1), 475))
                screen.blit(pygame.transform.scale(load_image('costs/' + str(volume)[1] + '.png'), (25, 25)),
                            (105 + 110 * (kol - 1), 475))
            else:
                screen.blit(pygame.transform.scale(load_image('costs/' + str(volume)[0] + '.png'), (25, 25)),
                            (80 + 110 * (kol - 1), 475))
        for i in buttons_food:
            i.draw()
        pygame.display.flip()
        clock.tick(FPS)


def clothes_screen():
    q = extra_screen_food_and_clothes()

    con = sqlite3.connect("clothes_and_food.db")

    # Создание курсора
    cur = con.cursor()
    con_scale_food = sqlite3.connect("tamagochi.db")

    # Создание курсора
    cur_scale_food = con_scale_food.cursor()
    result = cur.execute("""SELECT name, have FROM clothes""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))
    names = []
    buttons_clothes = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:
        kol += 1
        result = cur.execute('SELECT wearing FROM clothes WHERE name = ? AND have = 1',
                             (i,)).fetchone()[0]
        if result == 1:
            buttons_clothes.append(
                Button(85 + 110 * (kol - 1), 420, load_image('clothes/' + i + '_dark.PNG'), (70, 70), screen, i, False))
        else:
            buttons_clothes.append(
                Button(85 + 110 * (kol - 1), 420, load_image('clothes/' + i + '.PNG'), (70, 70), screen, i, False))

    for i in buttons_clothes:
        i.draw()

    while True:
        draw_fon()
        draw_money()
        draw_foodsc()
        draw_maincat()
        extra_screen_food_and_clothes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons_clothes:
                    if i.draw():
                        pygame.mixer.Sound('sound_data/click.mp3').play()
                        result = cur.execute('SELECT wearing FROM clothes WHERE name = ? AND have = 1', (i.name_for_food_or_for_clothes,)).fetchone()[0]
                        if result == 1:
                            cur.execute('UPDATE clothes SET wearing = 0 WHERE have = 1 AND name = ?', (i.name_for_food_or_for_clothes, ))
                        else:
                            cur.execute('UPDATE clothes SET wearing = 1 WHERE have = 1 AND name = ?', (i.name_for_food_or_for_clothes, ))
                        con.commit()

        if q.draw():
            return

        result = cur.execute("""SELECT name, have FROM clothes""").fetchall()
        result = list(filter(lambda item: int(item[1]), result))
        names = []
        buttons_clothes = []
        for i in result:
            names.append(i[0])
        kol = 0
        for i in names:
            kol += 1
            result = cur.execute('SELECT wearing FROM clothes WHERE name = ? AND have = 1',
                                 (i,)).fetchone()[0]
            if result == 1:
                buttons_clothes.append(
                    Button(85 + 110 * (kol - 1), 420, load_image('clothes/' + i + '_dark.PNG'), (70, 70), screen, i, False))
            else:
                buttons_clothes.append(
                    Button(85 + 110 * (kol - 1), 420, load_image('clothes/' + i + '.PNG'), (70, 70), screen, i,
                           False))

        for i in buttons_clothes:
            i.draw()
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
    costs_of_clothes_with_names = {'bant': 60, 'choker_blue': 30, 'fartyk': 89, 'hair': 50,
                                   'hat': 35, 'jevelery': 40}

    for i in range(6):
        kol += 1
        screen.blit(pygame.transform.scale(load_image('eatings/' + food[i] + '.png'), (40, 40)), (85 + 110 * (i), 80))
        buttons_buy.append(Button(75 + 110 * (kol - 1), 160, buy, (70, 40), screen, food[i], False))
        screen.blit(pygame.transform.scale(load_image('costs/' + cost_of_food[i] + '.png'), (25, 25)),
                    (80 + 110 * (kol - 1), 125))
        screen.blit(pygame.transform.scale(load_image('coin.png'), (25, 25)),
                    (105 + 110 * (kol - 1), 125))
    kol = 0
    for key, volume in costs_of_clothes_with_names.items():
        result = cur.execute('SELECT have FROM clothes WHERE name = ?',
                             (key,)).fetchone()[0]
        if result == '1':
            screen.blit(pygame.transform.scale(load_image('clothes/' + key + '_dark.png'), (50, 50)),
                        (80 + 110 * (kol), 240))
        else:
            screen.blit(pygame.transform.scale(load_image('clothes/' + key + '.png'), (50, 50)),
                        (80 + 110 * (kol), 240))
            first = str(volume)[0]
            second = str(volume)[1]
            screen.blit(pygame.transform.scale(load_image('costs/' + first + '.png'), (25, 25)),
                            (180 + 110 * (kol - 1), 285))
            screen.blit(pygame.transform.scale(load_image('costs/' + second + '.png'), (25, 25)),
                        (205 + 110 * (kol - 1), 285))
            screen.blit(pygame.transform.scale(load_image('coin.png'), (25, 25)),
                        (230 + 110 * (kol - 1), 285))
            buttons_buy.append(Button(75 + 110 * (kol), 320, buy, (70, 40), screen, key, False))
            # screen.blit(pygame.transform.scale(load_image('costs/' + str(volume) + '.png'), (35, 35)),
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
            screen.blit(pygame.transform.scale(load_image('eatings/' + food[i] + '.png'), (40, 40)),
                        (85 + 110 * (i), 80))
        for i in range(len(buttons_buy)):
            button = buttons_buy[i]
            index = i
            if button.draw():
                pygame.mixer.Sound('sound_data/click.mp3').play()
                result = int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0])
                if button.name_for_food_or_for_clothes in costs_of_food_with_names:
                    if costs_of_food_with_names[button.name_for_food_or_for_clothes] > result:
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
                                          (int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0]) -
                                           costs_of_food_with_names[button.name_for_food_or_for_clothes],))

                        if int(result) != 0:
                            cur.execute('UPDATE food SET have = ? WHERE name = ?', (int(result) + 1, food[index]))
                        else:
                            cur.execute('UPDATE food SET have = ? WHERE name = ?', (1, food[index]))
                        con_money.commit()
                        con.commit()
                else:
                    if costs_of_clothes_with_names[button.name_for_food_or_for_clothes] > result:
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
                        result = cur.execute('SELECT have FROM clothes WHERE name = ?', (button.name_for_food_or_for_clothes, )).fetchone()[0]
                        if result == '0':
                            cur_money.execute('UPDATE money SET coins = ?',
                                              (int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0]) -
                                               costs_of_clothes_with_names[button.name_for_food_or_for_clothes],))

                        cur.execute('UPDATE clothes SET have = ? WHERE name = ?', ('1', button.name_for_food_or_for_clothes,))
                        con.commit()
                        con_money.commit()
        extra_screen()
        if q.draw():
            return
        buttons_buy = []
        food = ['burger', 'chese', 'chicken', 'egg', 'fish', 'peach']
        buy = pygame.transform.scale(load_image('buy.PNG'), (
            70, 40))
        kol = 0
        cost_of_food = ['5', '3', '4', '2', '5', '7']
        costs_of_food_with_names = {'burger': 5, 'chese': 3, 'chicken': 4, 'egg': 2, 'fish': 5, 'peach': 7}
        costs_of_clothes_with_names = {'bant': 60, 'choker_blue': 30, 'fartyk': 89, 'hair': 50,
                                       'hat': 35, 'jevelery': 40}

        for i in range(6):
            kol += 1
            screen.blit(pygame.transform.scale(load_image('eatings/' + food[i] + '.png'), (40, 40)),
                        (85 + 110 * (i), 80))
            buttons_buy.append(Button(75 + 110 * (kol - 1), 160, buy, (70, 40), screen, food[i], False))
            screen.blit(pygame.transform.scale(load_image('costs/' + cost_of_food[i] + '.png'), (25, 25)),
                        (80 + 110 * (kol - 1), 125))
            screen.blit(pygame.transform.scale(load_image('coin.png'), (25, 25)),
                        (105 + 110 * (kol - 1), 125))
        kol = 0
        for key, volume in costs_of_clothes_with_names.items():
            result = cur.execute('SELECT have FROM clothes WHERE name = ?',
                                 (key,)).fetchone()[0]
            if result == '1':
                screen.blit(pygame.transform.scale(load_image('clothes/' + key + '_dark.png'), (50, 50)),
                            (80 + 110 * (kol), 240))
            else:
                screen.blit(pygame.transform.scale(load_image('clothes/' + key + '.png'), (50, 50)),
                            (80 + 110 * (kol), 240))
                first = str(volume)[0]
                second = str(volume)[1]
                screen.blit(pygame.transform.scale(load_image('costs/' + first + '.png'), (25, 25)),
                            (180 + 110 * (kol - 1), 285))
                screen.blit(pygame.transform.scale(load_image('costs/' + second + '.png'), (25, 25)),
                            (205 + 110 * (kol - 1), 285))
                screen.blit(pygame.transform.scale(load_image('coin.png'), (25, 25)),
                            (230 + 110 * (kol - 1), 285))
                buttons_buy.append(Button(75 + 110 * (kol), 320, buy, (70, 40), screen, key, False))
                # screen.blit(pygame.transform.scale(load_image('costs/' + str(volume) + '.png'), (35, 35)),
                #            (145 + 110 * (kol - 1), 165))
            kol += 1
        for i in buttons_buy:
            i.draw()
        pygame.display.flip()
        clock.tick(FPS)


clicked = False


def meow(cat, pos):
    global clicked
    smile = pygame.transform.scale(load_image('smile.png'), (250, 250))
    r = cat.get_rect()
    r.topleft = (275, 185)
    if r.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] and not clicked:
            clicked = True
            pygame.mixer.Sound('sound_data/gameover.mp3').play()
            screen.blit(smile, (275, 185))

    if not pygame.mouse.get_pressed()[0]:
        clicked = False


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
        gamesb = Button(72, 450, load_image('games.png'), (110, 110), screen)
        foodb = Button(254, 440, load_image('food.png'), (110, 110), screen)
        clothesb = Button(436, 440, load_image('clothes.png'), (110, 110), screen)
        shopb = Button(618, 440, load_image('shop.png'), (110, 110), screen)
        draw_foodsc_start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            draw_fon()
            if gamesb.draw():
                game_screen()
            if foodb.draw():
                food_screen()
            if clothesb.draw():
                clothes_screen()
            if shopb.draw():
                shop_screen()

            draw_money()

            draw_foodsc()
            draw_maincat()
            pygame.display.flip()
            clock.tick(FPS)
