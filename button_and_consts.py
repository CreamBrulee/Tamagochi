import sys

import pygame

FPS = 50
WIDTH = 800
HEIGHT = 550


class Button:
    def __init__(self, x, y, image, sizes, screen):
        self.image = pygame.transform.scale(image, sizes)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.sizes = sizes
        self.clicked = False
        self.click = pygame.mixer.Sound('sound_data/click.mp3')
        self.screen = screen

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                self.click.play()
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


def terminate():
    pygame.quit()
    sys.exit()

