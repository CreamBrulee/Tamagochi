import datetime
import os
import sqlite3
import sys

import pygame

# константы и переменные шкал
FPS = 60
WIDTH = 800
HEIGHT = 550
perc_food = 0
perc_sleep = 0
sleeping = 0


# функция для загрузки фото
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


# функция заработка денег в минииграх
def earning_money(screen, money):
    coin = pygame.transform.scale(load_image('data/coin.png'), (60, 60))
    font = pygame.font.Font(None, 100)
    string_rendered = font.render('+' + str(int(money)), bool(1), pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (5, 60)
    screen.blit(coin, (intro_rect.right + 5, 60))
    screen.blit(string_rendered, intro_rect)
    # функция для загрузки фото сохранение заработанных денег в базу данных
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    cur.execute('UPDATE money SET coins = coins + ?', (money,))
    connect.commit()
    connect.close()


# класс кнопки
class Button:
    def __init__(self, x, y, image, sizes, screen, name_for_food_or_for_clothes=None, music=True):
        self.name_for_food_or_for_clothes = name_for_food_or_for_clothes
        self.image = pygame.transform.scale(image, sizes)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.sizes = sizes
        self.clicked = False
        self.music = music
        if self.music:
            self.click = pygame.mixer.Sound('sound_data/click.mp3')
        self.screen = screen

    def draw(self):
        # функция отрисовки и обработки нажатия кнопки
        action = False
        pos = pygame.mouse.get_pos()
        # проверка пересечения кнопки и курсова
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                if self.music:
                    self.click.play()
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        # возвращаем была ли нажата кнопка
        return action


# функция завершения программы
def terminate():
    # запись в бд даты выхода, процентов шкал при выходе, инф. о том, спит ли кот
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    cur.execute('''UPDATE scales SET date = ?,
     percentage = ? WHERE scale = "food"''', (datetime.datetime.now(), perc_food))
    cur.execute('''UPDATE scales SET date = ?,
         percentage = ? WHERE scale = "sleep"''', (datetime.datetime.now(), perc_sleep))
    cur.execute('''UPDATE sleep SET issleeping = ? ''', (sleeping, ))
    connect.commit()
    connect.close()
    pygame.quit()
    sys.exit()
