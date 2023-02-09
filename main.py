import os
import sys
import pygame

FPS = 50
WIDTH = 800
HEIGHT = 550
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


class Button:
    def __init__(self, x, y, image, sizes):
        self.image = pygame.transform.scale(image, sizes)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.sizes = sizes
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            print('H')
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                print(1)
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action



def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    imagel = pygame.transform.scale(load_image('logo.png'), (400, 200))
    screen.blit(imagel, (10, 20))
    startb = Button(50, 220, load_image('start.png'), (250, 75))
    quitb = Button(50, 305, load_image('quit.png'), (250, 75))
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
    # imagec = pygame.transform.scale(load_image('cross.png'), (40, 40))
    # screen.blit(imagec, (720, 40))
    quitb2 = Button(720, 40, load_image('cross.png'), (40, 40))
    return quitb2
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             terminate()
    #     pygame.draw.rect(screen, pygame.Color('#362e26'), (40, 40, 720, 470))
    #     pygame.display.flip()


def game_screen():
    q = extra_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if q.draw():
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('CatLIFE')
    pygame.mixer.music.load('data/fon1.mp3')
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    running = True
    a = start_screen()
    if a:
        print(2)
        fon = pygame.transform.scale(load_image('fon2.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        gamesb = Button(72, 450, load_image('games.png'), (110, 110))
        foodb = Button(254, 440, load_image('food.png'), (110, 110))
        clothesb = Button(436, 440, load_image('clothes.png'), (110, 110))
        shopb = Button(618, 440, load_image('shop.png'), (110, 110))
        maincat = pygame.transform.scale(load_image('maincat.png'), (250, 250))
        screen.blit(maincat, (275, 185))
        while True:
            print(22)
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
            pygame.display.flip()
            clock.tick(FPS)