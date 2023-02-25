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

# создаем группы спрайтов
cat1group = pygame.sprite.Group()
startsc_buttons = pygame.sprite.Group()
catgroup = pygame.sprite.Group()
coins_gr = pygame.sprite.Group()


# функция для загрузки фото
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


# класс для создания анимации
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        # разрезание spritesheet
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        # смена кадра
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def get_rect(self):
        # взять размеры и положение картинки
        return self.rect


# начальный экран
def start_screen():
    fon = pygame.transform.scale(load_image('data/fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    imagel = pygame.transform.scale(load_image('data/logo.png'), (400, 200))
    screen.blit(imagel, (10, 20))
    # кнопки старта и выхода
    startb = Button(50, 220, load_image('data/start.png'), (250, 75), screen)
    quitb = Button(50, 305, load_image('data/quit.png'), (250, 75), screen)
    cat = AnimatedSprite(pygame.transform.scale(load_image('data/cat1.png'), (600, 300)), 2, 1, 460, 80, cat1group)
    # счет для скорости анимации
    i = 1
    cat1group.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        # смена кадра анимации
        if not i % 30:
            screen.blit(fon, (0, 0))
            screen.blit(imagel, (10, 20))
            cat.update()
            cat1group.draw(screen)
        # обработка нажатия кнопок старта и выхода
        if startb.draw():
            cat.kill()
            return True
        if quitb.draw():
            terminate()
        i += 1
        pygame.display.flip()
        clock.tick(FPS)


# функция отрисовки основного фона
def draw_fon():
    fon = pygame.transform.scale(load_image('data/fon2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))


# создание анимированного спрайта кота
maincat = AnimatedSprite(pygame.transform.scale(load_image('data/spritesheet_maincat.png'), (
    1250, 750)), 5, 3, 275, 185, catgroup)


# функция отрисовки одежды кота
def draw_acssesory():
    con = sqlite3.connect("clothes_and_food.db")
    # Создание курсора
    cur = con.cursor()
    result = cur.execute("""SELECT name, have, wearing FROM clothes""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))  # выбираем те аксессуары которые в наличии
    result = list(filter(lambda item: int(item[2]), result))  # выюираем те аксессуары которы надо надеть
    names = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:  # отрисовываем аксессуары
        kol += 1
        screen.blit(pygame.transform.scale(load_image('data/clothes/for_cat/' + i + '.png'), (250, 250)), (275, 185))


# отрисовка основного кота
def draw_maincat():
    if not button_and_consts.sleeping:
        maincat.update()
    catgroup.draw(screen)
    meow(maincat, pygame.mouse.get_pos())
    draw_acssesory()
    if button_and_consts.sleeping:
        screen.blit(pygame.transform.scale(load_image('data/sleepingcat.png'), (250, 250)), (275, 185))


# первая отрисовка шкалы еды с учетом времени нахождения вне игры
def draw_foodsc_start():
    pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    # взятие даты выхода и процентов шкалы при прошлом выходе из игры
    cur = connect.cursor()
    date = cur.execute('''SELECT date from scales WHERE scale = "food"''').fetchone()[0]
    percents = cur.execute('''SELECT percentage from scales WHERE scale = "food"''').fetchone()[0]
    # нахождение времени отсутствия
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    # подсчет процентов с учетом отсутствия
    button_and_consts.perc_food = percents - 0.01388 * time if percents - 0.01388 * time >= 0 else 0
    x = 100 - button_and_consts.perc_food
    # отрисовка уведомления о надобности покормить кота
    if button_and_consts.perc_food <= 50:
        feed = pygame.transform.scale(load_image('data/feed.png'), (175, 50))
        screen.blit(feed, (10, 100))
    pygame.draw.rect(screen, (100, 100, 100), (300, 5, 90, x))
    # обновление времени в базе данных
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "food"''', (datetime.datetime.now(), ))
    connect.commit()
    connect.close()
    # отрисовка картинки шкалы
    food_scale = pygame.transform.scale(load_image('data/foodsc.png'), (90, 100))
    screen.blit(food_scale, (300, 5))


# отрисовка шкалы еды из циклов
def draw_foodsc():
    pygame.draw.rect(screen, (0, 255, 150), (300, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    # взятие даты последней отрисовки шкалы
    cur = connect.cursor()
    date = cur.execute('''SELECT date from scales WHERE scale = "food"''').fetchone()[0]
    # нахождение времени с прошлой отрисовки шкалы
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    # подсчет процентов с учетом прошедшего с прошлой отрисовки шкалы времени
    button_and_consts.perc_food = button_and_consts.perc_food - time * 0.01388 if \
        button_and_consts.perc_food - time * 0.01388 >= 0 else 0
    x = 100 - button_and_consts.perc_food
    # отрисовка уведомления о надобности покормить кота
    if button_and_consts.perc_food <= 50:
        feed = pygame.transform.scale(load_image('data/feed.png'), (175, 50))
        screen.blit(feed, (10, 100))
    pygame.draw.rect(screen, (100, 100, 100), (300, 5, 90, x))
    # обновление времени в базе данных
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "food"''', (datetime.datetime.now(),))
    connect.commit()
    connect.close()
    # отрисовка картинки шкалы
    food_scale = pygame.transform.scale(load_image('data/foodsc.png'), (90, 100))
    screen.blit(food_scale, (300, 5))


# первая отрисовка шкалы сна с учетом времени нахождения вне игры
def draw_sleepsc_start():
    pygame.draw.rect(screen, (0, 255, 150), (400, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    # взятие даты выхода, процентов шкалы при прошлом выходе из игры и инф. о том, спал ли кот во время отсутствия
    cur = connect.cursor()
    button_and_consts.sleeping = cur.execute('''SELECT issleeping from sleep''').fetchone()[0]
    date = cur.execute('''SELECT date from scales WHERE scale = "sleep"''').fetchone()[0]
    percents = cur.execute('''SELECT percentage from scales WHERE scale = "sleep"''').fetchone()[0]
    # нахождение времени отсутствия
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    # подсчет процентов с учетом отсутствия и инф. о том, спал ли кот во время отсутствия
    if not button_and_consts.sleeping:
        button_and_consts.perc_sleep = percents - 0.0023 * time if percents - 0.0023 * time >= 0 else 0
    else:
        button_and_consts.perc_sleep = percents + 0.00347 * time if percents + 0.00347 * time <= 100 else 100
    x = 100 - button_and_consts.perc_sleep
    # отрисовка уведомления о надобности дать поспать коту
    if button_and_consts.perc_sleep <= 50:
        feed = pygame.transform.scale(load_image('data/wantsleep.png'), (175, 79))
        screen.blit(feed, (10, 160))
    pygame.draw.rect(screen, (100, 100, 100), (400, 5, 90, x))
    # обновление времени в базе данных
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "sleep"''', (datetime.datetime.now(), ))
    connect.commit()
    connect.close()
    # отрисовка картинки шкалы
    food_scale = pygame.transform.scale(load_image('data/sleepsc.png'), (90, 100))
    screen.blit(food_scale, (400, 5))


# отрисовка шкалы сна из циклов
def draw_sleepsc():
    pygame.draw.rect(screen, (0, 255, 150), (400, 5, 90, 100))
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    # взятие даты последней отрисовки шкалы
    date = cur.execute('''SELECT date from scales WHERE scale = "sleep"''').fetchone()[0]
    # нахождение времени с прошлой отрисовки шкалы
    diff = datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    time = diff.seconds + diff.days * 24 * 60 * 60 + diff.microseconds / 1000000
    # подсчет процентов с учетом прошедшего с прошлой отрисовки шкалы времени и инф. о том, спит ли кот
    if not button_and_consts.sleeping:
        button_and_consts.perc_sleep = button_and_consts.perc_sleep - time * 0.0023 if \
            button_and_consts.perc_sleep - time * 0.0023 >= 0 else 0
    else:
        button_and_consts.perc_sleep = button_and_consts.perc_sleep + 0.00347 * time if \
            button_and_consts.perc_sleep + 0.00347 * time <= 100 else 100
    x = 100 - button_and_consts.perc_sleep
    # отрисовка уведомления о надобности дать поспать коту
    if button_and_consts.perc_sleep <= 50 and not button_and_consts.sleeping:
        feed = pygame.transform.scale(load_image('data/wantsleep.png'), (175, 79))
        screen.blit(feed, (10, 160))
    pygame.draw.rect(screen, (100, 100, 100), (400, 5, 90, x))
    # обновление времени в базе данных
    cur.execute('''UPDATE scales SET date = ? WHERE scale = "sleep"''', (datetime.datetime.now(),))
    connect.commit()
    connect.close()
    # отрисовка картинки шкалы
    food_scale = pygame.transform.scale(load_image('data/sleepsc.png'), (90, 100))
    screen.blit(food_scale, (400, 5))


# создание анимированного спрайта монеты
coin = AnimatedSprite(pygame.transform.scale(load_image('data/money.png'), (420, 70)), 6, 1, 5, 5, coins_gr)
k = 0


# отрисовка количества монет на главном экране
def draw_money():
    global k
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    coins = cur.execute('''SELECT coins from money''').fetchone()[0]
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(coins), bool(1), pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (80, 5)
    screen.blit(string_rendered, intro_rect)
    connect.close()
    if not k % 2:
        coin.update()
    coins_gr.draw(screen)
    k += 1


# создание экрана поверх основного при открытии меню миниигр или магазина
def extra_screen():
    pygame.draw.rect(screen, (255, 255, 255), (40, 40, 720, 470))
    quitb2 = Button(720, 40, load_image('data/cross.png'), (40, 40), screen)
    return quitb2


# создание экрана поверх основного при открытии холодильника или шкафа
def extra_screen_food_and_clothes():
    pygame.draw.rect(screen, (255, 255, 255), (40, 400, 720, 110))
    quitb2 = Button(720, 400, load_image('data/cross.png'), (40, 40), screen)
    return quitb2


# меню миниигр
def game_screen():
    q = extra_screen()
    flappycat = Button(50, 50, load_image('data/game3.png'), (500, 113), screen)
    micehuntb = Button(50, 183, load_image('data/game2.png'), (500, 113), screen)
    catchfood = Button(50, 316, load_image('data/game1.png'), (500, 113), screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        # обработка нажатия кнопки выхода из меню
        if q.draw():
            return
        # обработка нажатия кнопок мниигр
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


# экран холодильника
def food_screen():
    q = extra_screen_food_and_clothes()
    con = sqlite3.connect("clothes_and_food.db")
    # Создание курсора
    cur = con.cursor()
    con_scale_food = sqlite3.connect("tamagochi.db")
    result = cur.execute("""SELECT name, have FROM food""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))  # выбираем ту еду которой >= 1
    names = []
    buttons_food = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:  # добавляем картинки еды в качетсве кнопок и отрисовываем цены
        kol += 1
        buttons_food.append(
            Button(75 + 110 * (kol - 1), 420, load_image('data/eatings/' + i + '.PNG'), (50, 50), screen, i, False))
        screen.blit(pygame.transform.scale(load_image('data/costs/' + '1' + '.png'), (25, 25)),
                    (80 + 110 * (kol - 1), 475))
    for i in buttons_food:  # отрисовываем еду
        i.draw()
    while True:
        draw_fon()
        draw_money()
        draw_foodsc()
        draw_sleepsc()
        draw_maincat()
        extra_screen_food_and_clothes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons_food:
                    if i.draw():
                        pygame.mixer.Sound('sound_data/click.mp3').play()  # издаем звук при нажатии
                        button_and_consts.perc_food = button_and_consts.perc_food + 5 if \
                            button_and_consts.perc_food + 5 <= 100 else 100
                        # вычитаем одну еду из БД
                        cur.execute('UPDATE food SET have = ? WHERE name = ?', (int(cur.execute(
                            """SELECT have FROM food WHERE name = ?""", (
                                i.name_for_food_or_for_clothes,)).fetchall()[0][0]) - 1,
                                                                                i.name_for_food_or_for_clothes))
                        con.commit()
                        con_scale_food.commit()
        if q.draw():
            return
        result = cur.execute("""SELECT name, have FROM food""").fetchall()
        result = list(filter(lambda item: int(item[1]), result))
        names = {}
        buttons_food = []
        for i in result:
            names[i[0]] = int(i[1])
        kol = 0
        for key, volume in names.items():
            kol += 1
            buttons_food.append(
                Button(75 + 110 * (kol - 1), 420, load_image('data/eatings/' + key + '.PNG'), (
                    50, 50), screen, key, False))
            # печатаем цены
            if volume >= 10:
                screen.blit(pygame.transform.scale(load_image('data/costs/' + str(volume)[0] + '.png'), (25, 25)),
                            (80 + 110 * (kol - 1), 475))
                screen.blit(pygame.transform.scale(load_image('data/costs/' + str(volume)[1] + '.png'), (25, 25)),
                            (105 + 110 * (kol - 1), 475))
            else:
                screen.blit(pygame.transform.scale(load_image('data/costs/' + str(volume)[0] + '.png'), (25, 25)),
                            (80 + 110 * (kol - 1), 475))
        for i in buttons_food:
            i.draw()  # отображаем кнопки
        pygame.display.flip()
        clock.tick(FPS)


# экран шкафа одежды
def clothes_screen():
    q = extra_screen_food_and_clothes()
    con = sqlite3.connect("clothes_and_food.db")
    # Создание курсора
    cur = con.cursor()
    result = cur.execute("""SELECT name, have FROM clothes""").fetchall()
    result = list(filter(lambda item: int(item[1]), result))  # выбираем ту одежду которая куплена
    names = []
    buttons_clothes = []
    for i in result:
        names.append(i[0])
    kol = 0
    for i in names:
        kol += 1
        result = cur.execute('SELECT wearing FROM clothes WHERE name = ? AND have = 1',
                             (i,)).fetchone()[0]
        if result == 1:  # если одежда одета то рисуем ее темной
            buttons_clothes.append(
                Button(85 + 110 * (kol - 1), 420, load_image('data/clothes/' + i + '_dark.PNG'), (
                    70, 70), screen, i, False))
        else:  # иначе рисуем ее активной
            buttons_clothes.append(
                Button(85 + 110 * (kol - 1), 420, load_image('data/clothes/' + i + '.PNG'), (70, 70), screen, i, False))

    for i in buttons_clothes:
        i.draw()  # прорисовываем одежду

    while True:
        draw_fon()
        draw_money()
        draw_foodsc()
        draw_sleepsc()
        draw_maincat()
        extra_screen_food_and_clothes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons_clothes:
                    if i.draw():
                        pygame.mixer.Sound('sound_data/click.mp3').play()  # производим звук
                        result = cur.execute('SELECT wearing FROM clothes WHERE name = ? AND have = 1', (
                            i.name_for_food_or_for_clothes,)).fetchone()[0]
                        # при нажатии либо снимаем либо одеваем одежду
                        if result == 1:
                            cur.execute('UPDATE clothes SET wearing = 0 WHERE have = 1 AND name = ?', (
                                i.name_for_food_or_for_clothes, ))
                        else:
                            cur.execute('UPDATE clothes SET wearing = 1 WHERE have = 1 AND name = ?', (
                                i.name_for_food_or_for_clothes, ))
                        con.commit()

        if q.draw():
            return
        # повторяем то же что и раньше
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
                    Button(85 + 110 * (kol - 1), 420, load_image(
                        'clothes/' + i + '_dark.PNG'), (70, 70), screen, i, False))
            else:
                buttons_clothes.append(
                    Button(85 + 110 * (kol - 1), 420, load_image('data/clothes/' + i + '.PNG'), (70, 70), screen, i,
                           False))

        for i in buttons_clothes:
            i.draw()
        pygame.display.flip()
        clock.tick(FPS)


# экран магазина
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
    buy = pygame.transform.scale(load_image('data/buy.PNG'), (
        70, 40))
    kol = 0
    cost_of_food = ['5', '3', '4', '2', '5', '7']
    costs_of_food_with_names = {'burger': 5, 'chese': 3, 'chicken': 4, 'egg': 2, 'fish': 5, 'peach': 7}
    costs_of_clothes_with_names = {'bant': 60, 'choker_blue': 30, 'fartyk': 89, 'hair': 50,
                                   'hat': 35, 'jevelery': 40}

    for i in range(6):  # отрисовываем еду и цены
        kol += 1
        screen.blit(pygame.transform.scale(load_image('data/eatings/' + food[i] + '.png'), (
            40, 40)), (85 + 110 * i, 80))
        buttons_buy.append(Button(75 + 110 * (kol - 1), 160, buy, (70, 40), screen, food[i], False))
        screen.blit(pygame.transform.scale(load_image('data/costs/' + cost_of_food[i] + '.png'), (25, 25)),
                    (80 + 110 * (kol - 1), 125))
        screen.blit(pygame.transform.scale(load_image('data/coin.png'), (25, 25)),
                    (105 + 110 * (kol - 1), 125))
    kol = 0
    for key, volume in costs_of_clothes_with_names.items():  # отрисовываем одежду
        result = cur.execute('SELECT have FROM clothes WHERE name = ?',
                             (key,)).fetchone()[0]
        if result == '1':  # отрисовываем серым если уже куплено
            screen.blit(pygame.transform.scale(load_image('data/clothes/' + key + '_dark.png'), (50, 50)),
                        (80 + 110 * kol, 240))
        else:  # инчае рисуем одежду активной с кнопкой
            screen.blit(pygame.transform.scale(load_image('data/clothes/' + key + '.png'), (50, 50)),
                        (80 + 110 * kol, 240))
            first = str(volume)[0]
            second = str(volume)[1]
            screen.blit(pygame.transform.scale(load_image('data/costs/' + first + '.png'), (25, 25)),
                        (180 + 110 * (kol - 1), 285))
            screen.blit(pygame.transform.scale(load_image('data/costs/' + second + '.png'), (25, 25)),
                        (205 + 110 * (kol - 1), 285))
            screen.blit(pygame.transform.scale(load_image('data/coin.png'), (25, 25)),
                        (230 + 110 * (kol - 1), 285))
            buttons_buy.append(Button(75 + 110 * kol, 320, buy, (70, 40), screen, key, False))
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
            # отрисовываем еду
            screen.blit(pygame.transform.scale(load_image('data/eatings/' + food[i] + '.png'), (40, 40)),
                        (85 + 110 * i, 80))
        for i in range(len(buttons_buy)):
            button = buttons_buy[i]
            index = i
            if button.draw():
                pygame.mixer.Sound('sound_data/click.mp3').play()  # производим звук
                result = int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0])
                if button.name_for_food_or_for_clothes in costs_of_food_with_names:
                    if costs_of_food_with_names[button.name_for_food_or_for_clothes] > result:  # если денег не хватило
                        q = extra_screen()
                        screen.blit(pygame.transform.scale(load_image('data/fon_without_money.png'), (800, 550)),
                                    (0, 0))
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    terminate()
                            if q.draw():
                                return
                            pygame.display.flip()
                            clock.tick(FPS)
                    else:  # иначе покупаем еду и добавляем в БД
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
                        # если денег не хватило соощаем об этом
                        q = extra_screen()
                        screen.blit(pygame.transform.scale(load_image('data/fon_without_money.png'), (800, 550)),
                                    (0, 0))
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    terminate()
                            if q.draw():
                                return
                            pygame.display.flip()
                            clock.tick(FPS)
                    else:  # иначе покупаем одежду добавляем в БД и вычитаем деньги
                        result = cur.execute('SELECT have FROM clothes WHERE name = ?', (
                            button.name_for_food_or_for_clothes, )).fetchone()[0]
                        if result == '0':
                            cur_money.execute('UPDATE money SET coins = ?',
                                              (int(cur_money.execute("""SELECT coins FROM money""").fetchall()[0][0]) -
                                               costs_of_clothes_with_names[button.name_for_food_or_for_clothes],))

                        cur.execute('UPDATE clothes SET have = ? WHERE name = ?', (
                            '1', button.name_for_food_or_for_clothes,))
                        con.commit()
                        con_money.commit()
        extra_screen()
        if q.draw():
            return
        # повторяем тоже что и раньше
        buttons_buy = []
        food = ['burger', 'chese', 'chicken', 'egg', 'fish', 'peach']
        buy = pygame.transform.scale(load_image('data/buy.PNG'), (
            70, 40))
        kol = 0
        cost_of_food = ['5', '3', '4', '2', '5', '7']
        costs_of_food_with_names = {'burger': 5, 'chese': 3, 'chicken': 4, 'egg': 2, 'fish': 5, 'peach': 7}
        costs_of_clothes_with_names = {'bant': 60, 'choker_blue': 30, 'fartyk': 89, 'hair': 50,
                                       'hat': 35, 'jevelery': 40}

        for i in range(6):
            kol += 1
            screen.blit(pygame.transform.scale(load_image('data/eatings/' + food[i] + '.png'), (40, 40)),
                        (85 + 110 * i, 80))
            buttons_buy.append(Button(75 + 110 * (kol - 1), 160, buy, (70, 40), screen, food[i], False))
            screen.blit(pygame.transform.scale(load_image('data/costs/' + cost_of_food[i] + '.png'), (25, 25)),
                        (80 + 110 * (kol - 1), 125))
            screen.blit(pygame.transform.scale(load_image('data/coin.png'), (25, 25)),
                        (105 + 110 * (kol - 1), 125))
        kol = 0
        for key, volume in costs_of_clothes_with_names.items():
            result = cur.execute('SELECT have FROM clothes WHERE name = ?',
                                 (key,)).fetchone()[0]
            if result == '1':
                screen.blit(pygame.transform.scale(load_image('data/clothes/' + key + '_dark.png'), (50, 50)),
                            (80 + 110 * kol, 240))
            else:
                screen.blit(pygame.transform.scale(load_image('data/clothes/' + key + '.png'), (50, 50)),
                            (80 + 110 * kol, 240))
                first = str(volume)[0]
                second = str(volume)[1]
                screen.blit(pygame.transform.scale(load_image('data/costs/' + first + '.png'), (25, 25)),
                            (180 + 110 * (kol - 1), 285))
                screen.blit(pygame.transform.scale(load_image('data/costs/' + second + '.png'), (25, 25)),
                            (205 + 110 * (kol - 1), 285))
                screen.blit(pygame.transform.scale(load_image('data/coin.png'), (25, 25)),
                            (230 + 110 * (kol - 1), 285))
                buttons_buy.append(Button(75 + 110 * kol, 320, buy, (70, 40), screen, key, False))
                # screen.blit(pygame.transform.scale(load_image('data/costs/' + str(volume) + '.png'), (35, 35)),
                #            (145 + 110 * (kol - 1), 165))
            kol += 1
        for i in buttons_buy:
            i.draw()
        pygame.display.flip()
        clock.tick(FPS)


# переменная для проверки единственного нажатия на кота при зажатии кнопки
clicked = False


# обработка нажатия на кота
def meow(cat, pos):
    global clicked
    smile = pygame.transform.scale(load_image('data/smile.png'), (250, 250))
    r = cat.get_rect()
    r.topleft = (275, 185)
    if r.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] and not clicked:
            clicked = True
            button_and_consts.sleeping = 0
            pygame.mixer.Sound('sound_data/gameover.mp3').play()
            screen.blit(smile, (275, 185))

    if not pygame.mouse.get_pressed()[0]:
        clicked = False


# экран, уведомляющий о недоступности миниигр, холодильника, шкафа, магазина, если кот спит
def catsleep():
    catsl = pygame.transform.scale(load_image('data/catsleep.png'), (800, 550))
    screen.blit(catsl, (0, 0))
    quitb2 = Button(720, 40, load_image('data/cross.png'), (40, 40), screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(catsl, (0, 0))
        # обработка надатия на крестик
        if quitb2.draw():
            return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('CatLIFE')
    # фоновая музыка
    pygame.mixer.music.load('sound_data/fon.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    clock = pygame.time.Clock()
    running = True
    # начальный экран
    a = start_screen()
    if a:
        # создание кнопок для основного экрана
        gamesb = Button(72, 450, load_image('data/games.png'), (110, 110), screen)
        foodb = Button(254, 440, load_image('data/food.png'), (110, 110), screen)
        clothesb = Button(436, 440, load_image('data/clothes.png'), (110, 110), screen)
        shopb = Button(618, 440, load_image('data/shop.png'), (110, 110), screen)
        sleepb = Button(600, 260, load_image('data/sleepb.png'), (150, 60), screen)
        # первая отрисовка шкал
        draw_foodsc_start()
        draw_sleepsc_start()
        while True:
            for eve in pygame.event.get():
                if eve.type == pygame.QUIT:
                    terminate()
            draw_fon()
            # обработка нажатий на кнопки миниигр, холодильника, шкафа, магазина с учетом сна кота
            if gamesb.draw():
                if not button_and_consts.sleeping:
                    game_screen()
                else:
                    catsleep()
            if foodb.draw():
                if not button_and_consts.sleeping:
                    food_screen()
                else:
                    catsleep()
            if clothesb.draw():
                if not button_and_consts.sleeping:
                    clothes_screen()
                else:
                    catsleep()
            if shopb.draw():
                if not button_and_consts.sleeping:
                    shop_screen()
                else:
                    catsleep()
            # обработка нажатий на кнопку сна
            if sleepb.draw():
                button_and_consts.sleeping = 1 if not button_and_consts.sleeping else 0
            # обработка нажатий отрисовка монет, шкал, спрайта кота
            draw_money()
            draw_foodsc()
            draw_sleepsc()
            draw_maincat()
            pygame.display.flip()
            clock.tick(FPS)
