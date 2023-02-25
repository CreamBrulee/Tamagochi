import pygame
import os
import sqlite3
import sys
from button_and_consts import Button, FPS, terminate, earning_money

screen = None
clock = None


def load_image(name):
    fullname = os.path.join('../Tamagochi/data_micehunt', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites_try = pygame.sprite.Group()
sprites = pygame.sprite.Group()


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# создадим группу, содержащую все спрайты
# all_sprites = pygame.sprite.Group()


def cut_sheet(sheet, columns, rows):  # функция для разреза спрайтов
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


ALL_SPRITES_MY = cut_sheet(load_image("pipes.png"), 4, 2)  # спрайты досочки
ALL_SPRITES_MY_NUMBERS = cut_sheet(load_image("numbers.png"), 5, 2)  # спрайты цифры
ALL_SPRITES_MY_NUMBERS_FOR_LvL = cut_sheet(load_image("numbers_for_LvL.png"), 5, 2)  # спрайты цифры для уровней


class tablet_win_or_defeat:  # класс для таблички победа/поражение после уровня
    def __init__(self, width, height, win, lvl, stars):
        self.krestik = None
        self.con = sqlite3.connect("mice.db")
        if win:
            self.first = True
        else:
            self.first = False

        self.cur = self.con.cursor()
        self.width = width
        self.win = win
        if stars >= 130:  # определяем количество звезд за уровень по шкале
            self.stars = 3
        else:
            if stars >= 57.5:
                self.stars = 2
            else:
                self.stars = 1
        self.lvl = lvl
        self.height = height

    def render(self, screen_for_render, sprites_for_render):

        self.krestik = Button(760, 0, load_image('break.png'), (40, 40), screen_for_render)  # рисуем крестик для выхода

        if self.win:  # если победили
            sprite_1 = pygame.sprite.Sprite()  # отрисовываем номер уровня
            sprite_1.image = load_image('LvL.png')
            sprite_1.rect = sprite_1.image.get_rect()
            sprites_for_render.add(sprite_1)
            sprite_1.rect = 70, -30

            sprite_1 = pygame.sprite.Sprite()
            sprite_1.image = ALL_SPRITES_MY_NUMBERS_FOR_LvL[self.lvl]
            sprite_1.rect = sprite_1.image.get_rect()
            sprites_for_render.add(sprite_1)
            sprite_1.rect = 185, 15

            kol = 60

            for i in range(3):
                sprite_1 = pygame.sprite.Sprite()  # отрисовываем серые звездочки везде
                sprite_1.image = load_image('not_star.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render.add(sprite_1)
                sprite_1.rect = 306 + kol * i, 140

            for i in range(self.stars):  # отрисовываем поверх полученные звездочки
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('star.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render.add(sprite_1)
                sprite_1.rect = 306 + kol * i, 140
        else:  # если проиграли отоброжаем экран поражения
            sprite_1 = pygame.sprite.Sprite()
            sprite_1.image = load_image('defeat_fon.png')
            sprite_1.rect = sprite_1.image.get_rect()
            sprites_for_render.add(sprite_1)
            sprite_1.rect = 0, 0

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

    def get_cell(self, mouse_pos):
        clock_for_get_cell = pygame.time.Clock()
        if self.win:
            if 445 - 95 <= mouse_pos[0] <= 445 and 449 <= mouse_pos[
                1] <= 489:  # если нажали на кнопку следующий уровень
                if self.lvl <= 5:  # если нажали на кнопку след уровень до 5 вкл уровня
                    board = Board(10, 6)
                    running1 = True
                    pygame.time.set_timer(pygame.USEREVENT, 100)
                    board.set_view(50, 100, 70)
                    screen1 = pygame.display.set_mode((800, 550))
                    board.render_lvl(screen1,
                                     'data_micehunt/lvl' + str(self.lvl + 1) + '.txt')  # рендерим следующий уровень
                    kol = 0
                    while running1:
                        for event1 in pygame.event.get():
                            if event1.type == pygame.QUIT:
                                terminate()
                            if event1.type == pygame.MOUSEBUTTONDOWN:
                                if board.get_click(screen1, event1.pos):
                                    return True
                            if event1.type == pygame.USEREVENT:
                                kol += 1
                        all_sprites_try_better = pygame.sprite.Group()
                        board.render(all_sprites_try_better, screen1, kol)
                        pygame.display.flip()
                else:  # если нажали на 6 уровне отрисовываем табличку
                    my_sprite = pygame.sprite.Group()
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('coming_soon.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    my_sprite.add(sprite_1)
                    sprite_1.rect = 0, 0
                    for i in range(100):
                        my_sprite.draw(screen)
                        pygame.display.flip()
                        clock_for_get_cell.tick(FPS)
                    if micehunt_f():  # возвращаемся в выбор уровней
                        return True
        else:  # если проиграли
            if 299 <= mouse_pos[0] <= 489 and 422 <= mouse_pos[1] <= 482:  # если нажали на кнопку реплей
                board = Board(10, 6)
                running1 = True
                pygame.time.set_timer(pygame.USEREVENT, 100)
                board.set_view(50, 100, 70)
                screen1 = pygame.display.set_mode((800, 550))
                board.render_lvl(screen1, 'data_micehunt/lvl' + str(self.lvl) + '.txt')
                kol = 0
                while running1:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            terminate()
                        if event1.type == pygame.MOUSEBUTTONDOWN:
                            if board.get_click(screen1, event1.pos):
                                return True
                        if event1.type == pygame.USEREVENT:
                            kol += 1
                    all_sprites_try_better = pygame.sprite.Group()
                    board.render(all_sprites_try_better, screen1, kol)
                    pygame.display.flip()


class Board:  # класс для уровня
    def __init__(self, width, height):
        self.lvl_map_correct = None
        self.screen = None
        self.kel = 0
        self.first = True
        self.width = width
        self.lvl = 0
        self.now_stars = 0
        self.height = height
        self.board = [['.'] * width for _ in range(height)]  # создаем карту
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sprites_for_render_2, screen_for_render, seconds=1):
        self.kel += 1
        left = self.left
        top = self.top
        for i in range(0, 800, 70):  # рисуем траву везде
            for j in range(0, 550, 70):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('trava_fon.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render_2.add(sprite_1)
                sprite_1.rect = i, j
        for i in self.board:
            for j in i:
                if j != '0' and j != 'M' and j != 'C':  # рисуем болото на месте точек в карте
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('boloto_fon.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == 'C' or j == 'M':  # рисуем площадки на месте где должен быть кот и мышь
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('ploshadka.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                    if j == 'C':  # рисуем кота
                        sprite_1 = pygame.sprite.Sprite()
                        sprite_1.image = load_image('cat.png')
                        sprite_1.rect = sprite_1.image.get_rect()
                        sprites_for_render_2.add(sprite_1)
                        sprite_1.rect = left, top
                    if j == 'M':  # рисуем мышь
                        sprite_1 = pygame.sprite.Sprite()
                        sprite_1.image = load_image('mouse.png')
                        sprite_1.rect = sprite_1.image.get_rect()
                        sprites_for_render_2.add(sprite_1)
                        sprite_1.rect = left, top
                # рисуем дососчки
                if j == '1':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[4]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '2':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[1]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '3':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[0]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '4':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[5]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '5':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[2]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '6':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[6]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render_2.add(sprite_1)
                    sprite_1.rect = left, top
                left += self.cell_size
            top += self.cell_size
            left = self.left

        sprite_1 = pygame.sprite.Sprite()  # кнопка для проверки победы в уровне
        sprite_1.image = load_image('button_check.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render_2.add(sprite_1)
        sprite_1.rect = 380, -25

        sprite_1 = pygame.sprite.Sprite()  # отобрадем номер уровня
        sprite_1.image = load_image('LvL.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render_2.add(sprite_1)
        sprite_1.rect = 0, 430

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS_FOR_LvL[self.lvl]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render_2.add(sprite_1)
        sprite_1.rect = 115, 475

        sprite_1 = pygame.sprite.Sprite()  # отображаем крестик
        sprite_1.image = load_image('break.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render_2.add(sprite_1)
        sprite_1.rect = 760, 0

        screen_for_render.fill((215, 125, 49))
        sprites_for_render_2.draw(screen_for_render)

        pygame.draw.rect(screen_for_render, (255, 255, 255), (140, 10, 210, 70))  # отображаем шкалу для звездочек
        pygame.draw.rect(screen_for_render, (0, 255, 0), (140, 10, 210 - seconds / 7, 70))
        self.now_stars = 210 - seconds / 7
        # pygame.display.flip()

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('shkala_stars_with_fon.png')
        sprite_1.rect = sprite_1.image.get_rect()
        my_self = pygame.sprite.Group()
        my_self.add(sprite_1)
        sprite_1.rect = 140, 10
        my_self.draw(screen_for_render)

    def render_lvl(self, screen_for_render_lvl, lvl):
        self.screen = screen_for_render_lvl
        # заполняем корректную комбинацию уровня
        self.lvl_map_correct = []
        level = load_level(lvl)
        self.lvl = int(lvl[-5])
        for i in range(len(level)):
            a = level[i]
            ben = []
            for j in range(len(a.split()[0])):
                b = a.split()[0][j]
                ben.append(a.split()[1][j])
                self.board[i][j] = b
            self.lvl_map_correct.append(ben)

    def get_click(self, screen_for, mouse_pos):
        if self.get_cell(screen_for, mouse_pos):
            return True
        if 760 <= mouse_pos[0] <= 800 and 0 <= mouse_pos[1] <= 40:  # если нажали на крестик
            return True

    def get_cell(self, screen_for_get_cell, mouse_pos):
        if 380 <= mouse_pos[0] <= 520 and -25 <= mouse_pos[1] <= 100:  # нажали на кнопку проверки
            if self.board == self.lvl_map_correct:  # если победили

                pygame.mixer.quit()
                pygame.mixer.init()
                pygame.mixer.Sound('sound_data/newscore.wav').play()  # проигрываем звук победы
                pygame.mixer.music.load('sound_data/micesound.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.05)
                running2 = True

                win = tablet_win_or_defeat(800, 550, True, self.lvl,
                                           self.now_stars)  # создаем поле для отобрадения победы

                pygame.time.set_timer(pygame.USEREVENT, 100)
                screen_for_get_cell = pygame.display.set_mode((800, 550))
                sprites_for_win_or_defeat = pygame.sprite.Group()
                win.render(screen_for_get_cell, sprites_for_win_or_defeat)

                for i in range(0, 800, 70):  # рисуем траву везде
                    for j in range(0, 550, 70):
                        screen_for_get_cell.blit(load_image('trava_fon.png'), (i, j))

                screen_for_get_cell.blit(load_image('win_fon.png'), (0, 0))
                result_before = \
                    win.cur.execute('SELECT stars from micehunt_bestscores WHERE level = ?', (win.lvl,)).fetchall()[0][0]
                print(result_before)
                win.cur.execute('UPDATE micehunt_bestscores SET stars = ? WHERE level = ?', (win.stars, win.lvl,))
                win.con.commit()
                earning_money(screen_for_get_cell, (win.stars - result_before) * 3)
                result_after = \
                    win.cur.execute('SELECT stars from micehunt_bestscores WHERE level = ?', (win.lvl,)).fetchall()[
                        0][0]
                while running2:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            terminate()
                        if event1.type == pygame.MOUSEBUTTONDOWN:
                            if win.get_click(event1.pos):
                                return True
                    win.render(screen_for_get_cell, sprites_for_win_or_defeat)
                    sprites_for_win_or_defeat.draw(screen_for_get_cell)

                    if win.krestik.draw():
                        if micehunt_f():
                            return True
                    pygame.display.flip()

            else:  # если проиграли
                if self.now_stars <= 0:
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    pygame.mixer.Sound('sound_data/game_over.wav')  # проигрываем звук поражения
                    pygame.mixer.music.load('sound_data/micesound.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.05)
                    running2 = True
                    win = tablet_win_or_defeat(800, 550, False, self.lvl,
                                               self.now_stars)  # создаем табличку для поражения
                    pygame.time.set_timer(pygame.USEREVENT, 100)
                    screen_for_get_cell = pygame.display.set_mode((800, 550))
                    sprites_for_win_or_defeat = pygame.sprite.Group()
                    win.render(screen_for_get_cell, sprites_for_win_or_defeat)
                    while running2:
                        for event1 in pygame.event.get():
                            if event1.type == pygame.QUIT:
                                terminate()
                            if event1.type == pygame.MOUSEBUTTONDOWN:
                                if win.get_click(event1.pos):
                                    return True

                        screen.fill((215, 125, 49))
                        win.render(screen_for_get_cell, sprites_for_win_or_defeat)
                        sprites_for_win_or_defeat.draw(screen_for_get_cell)

                        if win.krestik.draw():
                            micehunt_f()
                        pygame.display.flip()
                else:  # если проверили, но не выиграли

                    my_sprite = pygame.sprite.Group()
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = pygame.transform.scale(load_image('try_better.png'),
                                                            (155, 36))  # говорим сделать попытку еще раз
                    sprite_1.rect = sprite_1.image.get_rect()
                    my_sprite.add(sprite_1)
                    sprite_1.rect = 540, 30

                    for i in range(100):
                        my_sprite.draw(screen_for_get_cell)
                        pygame.display.flip()
                        clock.tick(FPS)

        try:  # меняем досочки при нажатии
            clicked = self.board[(mouse_pos[1] - self.top) // self.cell_size][
                (mouse_pos[0] - self.left) // self.cell_size]
            if clicked == '5':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '6'
            if clicked == '6':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '5'
            if clicked == '1':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '2'
            if clicked == '2':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '3'
            if clicked == '3':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '4'
            if clicked == '4':
                self.board[(mouse_pos[1] - self.top) // self.cell_size][
                    (mouse_pos[0] - self.left) // self.cell_size] = '1'
        except IndexError:
            pass


class menu_lvl:  # класс для выбора уровней
    def __init__(self, width, height):
        self.con = sqlite3.connect("mice.db")

        # Создание курсор
        self.cur = self.con.cursor()
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sprites_for_render):
        for i in range(0, 800, 70):  # рисуем траву везде
            for j in range(0, 550, 70):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('fon_leveles.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render.add(sprite_1)
                sprite_1.rect = i, j

        sprite_1 = pygame.sprite.Sprite()  # рисуем рамочки для уровней
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 150, 115

        sprite_1 = pygame.sprite.Sprite()  # рисуем стрелочку
        sprite_1.image = pygame.transform.scale(load_image('next_rofl.png'), (70, 70))
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 635, 230

        sprite_1 = pygame.sprite.Sprite()  # риусем обрамление для уровней
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 180 + 150, 115

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 360 + 150, 115

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 150, 295

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 180 + 150, 295

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 360 + 150, 295

        sprite_1 = pygame.sprite.Sprite()  # рисуем номера уровней
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[1]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[2]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 180 + 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[3]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 360 + 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[4]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 150 + 20, 295 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[5]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 180 + 150 + 20, 295 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[6]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 360 + 150 + 20, 295 + 20

        kol = 30
        x = 175
        level = 1

        # прорисовываем звездочки над уровнями
        for i in range(1, 4):
            result = self.cur.execute("""SELECT stars FROM micehunt_bestscores
                                        WHERE level = ?""", (level,)).fetchall()

            star = int(result[0][0])
            for j in range(1, 4):

                sprite_1 = pygame.sprite.Sprite()  # отрисовываем везде серые звездочки
                sprite_1.image = pygame.transform.scale(load_image('not_star.png'), (30 * 1, 30))
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render.add(sprite_1)
                sprite_1.rect = x + kol * (j - 1), 85

                if star > 0:  # отрисовываем реальные звездочки
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = pygame.transform.scale(load_image('star.png'), (30, 30))
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render.add(sprite_1)
                    sprite_1.rect = x + kol * (j - 1), 85
                    star -= 1
            x += 180
            level += 1

        kol = 30
        x = 175
        level = 4
        #  то же самое для нижних уровней
        for i in range(1, 4):
            result = self.cur.execute("""SELECT stars FROM micehunt_bestscores
                                                WHERE level = ?""", (level,)).fetchall()
            star = int(result[0][0])
            for j in range(1, 4):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = pygame.transform.scale(load_image('not_star.png'), (30, 30))
                sprite_1.rect = sprite_1.image.get_rect()
                sprites_for_render.add(sprite_1)
                sprite_1.rect = x + kol * (j - 1), 265

                if star > 0:
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = pygame.transform.scale(load_image('star.png'), (30 * 1, 30 * 1))
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites_for_render.add(sprite_1)
                    sprite_1.rect = x + kol * (j - 1), 265
                    star -= 1

            x += 180
            level += 1

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('break.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites_for_render.add(sprite_1)
        sprite_1.rect = 760, 0

    def get_click(self, mouse_pos):
        if type(self.get_cell(mouse_pos)) == int and 1 <= self.get_cell(mouse_pos) <= 6:  # если нажали на кнопку уровня
            board = Board(10, 6)
            running1 = True
            pygame.time.set_timer(pygame.USEREVENT, 100)
            board.set_view(50, 100, 70)
            screen1 = pygame.display.set_mode((800, 550))
            board.render_lvl(screen1, 'data_micehunt/lvl' + str(
                self.get_cell(mouse_pos)) + '.txt')  # запускаем уровень на который нажали
            kol = 0
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        terminate()
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        pos = event1.pos
                        if 760 <= pos[0] <= 800 and 0 <= pos[1] <= 40:  # нажали на крестик выходим
                            if micehunt_f():
                                return True
                        if board.get_click(screen1, event1.pos):
                            return True
                    if event1.type == pygame.USEREVENT:
                        kol += 1
                all_sprites_try_for_better_3 = pygame.sprite.Group()
                board.render(all_sprites_try_for_better_3, screen1, kol)
                pygame.display.flip()

    def get_cell(self, mouse_pos):
        # определяем на какой из уровней нажали
        if 150 <= mouse_pos[0] <= 140 + 150 and 115 <= mouse_pos[1] <= 115 + 140:
            return 1
        if 150 + 180 <= mouse_pos[0] <= 150 + 140 + 180 and 115 <= mouse_pos[1] <= 115 + 140:
            return 2
        if 150 + 360 <= mouse_pos[0] <= 150 + 360140 and 115 <= mouse_pos[1] <= 115 + 140:
            return 3
        if 150 <= mouse_pos[0] <= 150 + 140 and 295 <= mouse_pos[1] <= 295 + 140:
            return 4
        if 150 + 180 <= mouse_pos[0] <= 150 + 140 + 180 and 295 <= mouse_pos[1] <= 295 + 140:
            return 5
        if 150 + 360 <= mouse_pos[0] <= 150 + 360 + 140 and 295 <= mouse_pos[1] <= 295 + 140:
            return 6


def micehunt_f():  # функция для запуска музыки и создания окна для игры
    pygame.mixer.music.load('sound_data/micesound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    board1 = menu_lvl(10, 6)
    running = True
    board1.set_view(50, 65, 70)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if board1.get_click(event.pos):
                    return True
                if 760 <= pos[0] <= 800 and 0 <= pos[1] <= 40:  # если нажали на крестик
                    return True
                if 655 <= pos[0] <= 700 and 230 <= pos[1] <= 300:  # если нажали на стрелочку
                    my_sprite = pygame.sprite.Group()
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('coming_soon.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    my_sprite.add(sprite_1)
                    sprite_1.rect = 0, 0
                    for i in range(100):
                        my_sprite.draw(screen)
                        pygame.display.flip()
                        clock.tick(FPS)

        screen.fill((215, 125, 49))
        all_sprites_for_menu_lvl = pygame.sprite.Group()
        board1.render(all_sprites_for_menu_lvl)
        all_sprites_for_menu_lvl.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 550))
    pygame.mixer.music.load('sound_data/micesound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    micehunt_f()
