import pygame
import os
import sys
screen = None
clock = None


def load_image(name, colorkey=None):
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


def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


ALL_SPRITES_MY = cut_sheet(load_image("pipes.png"), 4, 2)
ALL_SPRITES_MY_NUMBERS = cut_sheet(load_image("numbers.png"), 5, 2)
ALL_SPRITES_MY_NUMBERS_FOR_LvL = cut_sheet(load_image("numbers_for_LvL.png"), 5, 2)


class tablet_win_or_defeat:
    def __init__(self, width, height, win, lvl, stars):
        self.width = width
        self.win = win
        if stars >= 130:
            self.stars = 3
        else:
            if stars >= 57.5:
                self.stars = 2
            else:
                self.stars = 1
        self.lvl = lvl
        self.height = height

    def render(self, screen, sprites):
        for i in range(0, 800, 70):  # рисуем траву везде
            for j in range(0, 550, 70):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('trava_fon.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites.add(sprite_1)
                sprite_1.rect = i, j

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('win_fon.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 0, 0

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('break.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 760, 0

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('LvL.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 70, -30

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS_FOR_LvL[self.lvl]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 185, 15

        kol = 60

        for i in range(3):
            sprite_1 = pygame.sprite.Sprite()
            sprite_1.image = load_image('not_star.png')
            sprite_1.rect = sprite_1.image.get_rect()
            sprites.add(sprite_1)
            sprite_1.rect = 306 + kol * i, 140

        for i in range(self.stars):
            sprite_1 = pygame.sprite.Sprite()
            sprite_1.image = load_image('star.png')
            sprite_1.rect = sprite_1.image.get_rect()
            sprites.add(sprite_1)
            sprite_1.rect = 306 + kol * i, 140

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if 760 <= mouse_pos[0] <= 800 and 0 <= mouse_pos[1] <= 40:
            return True

    def get_cell(self, mouse_pos):
        if 445 - 95 <= mouse_pos[0] <= 445 and 449 <= mouse_pos[1] <= 489:
            if self.lvl <= 5:
                board = Board(10, 6)
                running1 = True
                clock = pygame.time.Clock()
                pygame.time.set_timer(pygame.USEREVENT, 100)
                board.set_view(50, 100, 70)
                screen1 = pygame.display.set_mode((800, 550))
                board.render_lvl(screen1, 'data_micehunt/lvl' + str(self.lvl + 1) + '.txt')
                background = pygame.Surface((800, 550))
                kol = 0
                sprites_for_win_or_defeat = pygame.sprite.Group()
                flag = False
                while running1:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            running1 = False
                        if event1.type == pygame.MOUSEBUTTONDOWN:
                            if board.get_click(screen1, sprites_for_win_or_defeat, event1.pos):
                                running1 = False
                        if event1.type == pygame.USEREVENT:
                            kol += 1
                    all_sprites_try = pygame.sprite.Group()
                    # all_sprites_try.clear(screen1,background )
                    board.render(all_sprites_try, screen1, kol)
                    # print(len(all_sprites_try))
                    # all_sprites_try.draw(screen1)
                    pygame.display.flip()
            else:
                pass


class Board:
    def __init__(self, width, height):
        self.kel = 0
        self.width = width
        self.lvl = 0
        self.now_stars = 0
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sprites, screen_for_render, seconds=1):
        self.kel += 1
        left = self.left
        top = self.top
        for i in range(0, 800, 70):  # рисуем траву везде
            for j in range(0, 550, 70):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('trava_fon.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites.add(sprite_1)
                sprite_1.rect = i, j
        for i in self.board:
            for j in i:
                if j != '0' and j != 'M' and j != 'C':  # рисуем болото на месте точек в карте
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('boloto_fon.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == 'C' or j == 'M':  # рисуем площадки на месте где должен быть кот и мышь
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = load_image('ploshadka.png')
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                    if j == 'C':  # рисуем кота
                        sprite_1 = pygame.sprite.Sprite()
                        sprite_1.image = load_image('cat.png')
                        sprite_1.rect = sprite_1.image.get_rect()
                        sprites.add(sprite_1)
                        sprite_1.rect = left, top
                    if j == 'M':  # рисуем мышь
                        sprite_1 = pygame.sprite.Sprite()
                        sprite_1.image = load_image('mouse.png')
                        sprite_1.rect = sprite_1.image.get_rect()
                        sprites.add(sprite_1)
                        sprite_1.rect = left, top
                # рисуем дососчки
                if j == '1':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[4]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '2':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[1]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '3':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[0]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '4':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[5]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '5':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[2]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                if j == '6':
                    sprite_1 = pygame.sprite.Sprite()
                    sprite_1.image = ALL_SPRITES_MY[6]
                    sprite_1.rect = sprite_1.image.get_rect()
                    sprites.add(sprite_1)
                    sprite_1.rect = left, top
                left += self.cell_size
            top += self.cell_size
            left = self.left

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('break.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 760, 0

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('button_check.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 380, -25

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('LvL.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 0, 430

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS_FOR_LvL[self.lvl]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 115, 475

        screen_for_render.fill((215, 125, 49))
        sprites.draw(screen_for_render)

        pygame.draw.rect(screen_for_render, (255, 255, 255), (140, 10, 210, 70))
        pygame.draw.rect(screen_for_render, (0, 255, 0), (140, 10, 210 - seconds / 8, 70))
        self.now_stars = 210 - seconds / 8
        # pygame.display.flip()

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('shkala_stars_with_fon.png')
        sprite_1.rect = sprite_1.image.get_rect()
        my_self = pygame.sprite.Group()
        my_self.add(sprite_1)
        sprite_1.rect = 140, 10

        my_self.draw(screen_for_render)

    def render_lvl(self, screen, lvl):
        left = self.left
        top = self.top
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
        for i in level:
            for j in i:
                if j == 'S':
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (left, top, self.cell_size, self.cell_size), 1)
                if j == 'F':
                    pygame.draw.rect(screen, (0, 0, 255),
                                     (left, top, self.cell_size, self.cell_size), 1)
                if j == '1':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left, top + self.cell_size / 2),
                                     (left + self.cell_size / 2, top + self.cell_size / 2), 1)
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top + self.cell_size / 2),
                                     (left + self.cell_size / 2, top + self.cell_size), 1)
                if j == '2':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top),
                                     (left + self.cell_size / 2, top + self.cell_size / 2), 1)
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top + self.cell_size / 2),
                                     (left, top + self.cell_size / 2), 1)
                if j == '3':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top),
                                     (left + self.cell_size / 2, top + self.cell_size / 2), 1)
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top + self.cell_size / 2),
                                     (left + self.cell_size, top + self.cell_size / 2), 1)
                if j == '4':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size, top),
                                     (left + self.cell_size / 2, top), 1)
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top),
                                     (left + self.cell_size / 2, top + self.cell_size / 2), 1)
                if j == '5':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left, top + self.cell_size / 2),
                                     (left + self.cell_size, top + self.cell_size / 2), 1)
                if j == '6':
                    pygame.draw.line(screen, (255, 255, 255),
                                     (left + self.cell_size / 2, top),
                                     (left + self.cell_size / 2, top + self.cell_size), 1)
                left += self.cell_size
            top += self.cell_size
            left = self.left
        """for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (left, top, self.cell_size, self.cell_size), 1)
                left += self.cell_size
            top += self.cell_size
            left = self.left"""

    def get_click(self, screen_for, sprites, mouse_pos):
        if self.get_cell(screen_for, sprites, mouse_pos):
            print(1)
            return True
        if 760 <= mouse_pos[0] <= 800 and 0 <= mouse_pos[1] <= 40:
            return True

    def get_cell(self, screen_for_get_cell, sprites, mouse_pos):
        if 380 <= mouse_pos[0] <= 520 and -25 <= mouse_pos[1] <= 100:
            print(3)
            if self.board == self.lvl_map_correct:
                running2 = True
                win = tablet_win_or_defeat(800, 550, True, self.lvl, self.now_stars)
                pygame.time.set_timer(pygame.USEREVENT, 100)
                screen_for_get_cell = pygame.display.set_mode((800, 550))
                sprites_for_win_or_defeat = pygame.sprite.Group()
                win.render(screen_for_get_cell, sprites_for_win_or_defeat)
                while running2:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            running2 = False
                            return True
                        if event1.type == pygame.MOUSEBUTTONDOWN:
                            if win.get_click(event1.pos):
                                print(1)
                                running2 = False
                                return True

                    screen.fill((215, 125, 49))
                    # all_sprites_try.clear(screen1,background )
                    win.render(screen_for_get_cell, sprites_for_win_or_defeat)
                    sprites_for_win_or_defeat.draw(screen_for_get_cell)
                    # print(len(all_sprites_try))
                    # all_sprites_try.draw(screen1)
                    pygame.display.flip()
                #print('WIN')

        if 0 <= (mouse_pos[0] - self.top) // self.cell_size <= len(self.board[0]) - 1 and \
                0 <= (mouse_pos[1] - self.left) // self.cell_size <= len(self.board) - 1:
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


class menu_lvl:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, sprites):
        left = self.left
        top = self.top
        for i in range(0, 800, 70):  # рисуем траву везде
            for j in range(0, 550, 70):
                sprite_1 = pygame.sprite.Sprite()
                sprite_1.image = load_image('fon_leveles.png')
                sprite_1.rect = sprite_1.image.get_rect()
                sprites.add(sprite_1)
                sprite_1.rect = i, j
        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('break.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 760, 0

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 150, 115

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 180 + 150, 115

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 360 + 150, 115

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 150, 295

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 180 + 150, 295

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = load_image('levels_obramlenie.png')
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 360 + 150, 295

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[1]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[2]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 180 + 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[3]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 360 + 150 + 20, 115 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[4]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 150 + 20, 295 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[5]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 180 + 150 + 20, 295 + 20

        sprite_1 = pygame.sprite.Sprite()
        sprite_1.image = ALL_SPRITES_MY_NUMBERS[6]
        sprite_1.rect = sprite_1.image.get_rect()
        sprites.add(sprite_1)
        sprite_1.rect = 360 + 150 + 20, 295 + 20

    def get_click(self, mouse_pos):
        if type(self.get_cell(mouse_pos)) == 'int' and 1 <= self.get_cell(mouse_pos) <= 6:
            board = Board(10, 6)
            running1 = True
            pygame.time.set_timer(pygame.USEREVENT, 100)
            board.set_view(50, 100, 70)
            screen1 = pygame.display.set_mode((800, 550))
            board.render_lvl(screen1, 'data_micehunt/lvl' + str(self.get_cell(mouse_pos)) + '.txt')
            background = pygame.Surface((800, 550))
            kol = 0
            sprites_for_win_or_defeat = pygame.sprite.Group()
            flag = False
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running1 = False
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        board.get_click(screen1, sprites_for_win_or_defeat, event1.pos)
                    if event1.type == pygame.USEREVENT:
                        kol += 1
                all_sprites_try = pygame.sprite.Group()
                # all_sprites_try.clear(screen1,background )
                board.render(all_sprites_try, screen1, kol)
                # print(len(all_sprites_try))
                # all_sprites_try.draw(screen1)
                pygame.display.flip()

    def get_cell(self, mouse_pos):
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


def micehunt_f():
    board1 = menu_lvl(10, 6)
    running = True
    board1.set_view(50, 65, 70)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board1.get_click(event.pos)
        screen.fill((215, 125, 49))
        all_sprites_for_menu_lvl = pygame.sprite.Group()
        board1.render(screen, all_sprites_for_menu_lvl)
        # print(all1_sprites, 'all1_sprites')
        all_sprites_for_menu_lvl.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 550))
    micehunt_f()
