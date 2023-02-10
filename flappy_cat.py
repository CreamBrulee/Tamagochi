import pygame
import os
import sys
import random
from button_and_consts import Button, FPS, terminate, HEIGHT, WIDTH

screen = 0
clock = 0
score = 0

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def start_screen():
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    play = Button(325, 168, load_image('start_end/play.png', colorkey=-1), (150, 75), screen)
    logo = pygame.transform.scale(load_image('data/game3.png'), (400, 88))
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
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    logo = pygame.transform.scale(load_image('start_end/gameover.png'), (250, 125))
    screen.blit(logo, (275, 30))
    scim = pygame.transform.scale(load_image('start_end/score.png'), (150, 60))
    screen.blit(scim, (250, 165))
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(int(score)), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (420, 165)
    screen.blit(string_rendered, intro_rect)
    re = Button(300, 245, load_image('start_end/replay.png'), (200, 56), screen)
    pygame.mixer.Sound('sound_data/gameover.mp3').play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if re.draw():
            main()
        if q.draw():
            return True
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global score
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Flappy bird')
    pygame.display.flip()
    y = 200
    font = pygame.font.Font(None, 30)
    fontt = pygame.font.Font(None, 80)
    bird = pygame.Rect(200, y, 50, 50)
    imgbird = pygame.transform.scale(load_image('data/cat.png'), (70, 70))
    imgtrubs = pygame.transform.scale(load_image('data/true_fver.png'), (50, 200))
    imgtrubs1 = pygame.transform.scale(load_image('data/true_sniz.png'), (50, 200))
    imgfon = pygame.transform.scale(load_image('data/fon1.png'), (180, 560))
    trubs = []
    cadrs = 0
    fonk = []
    scores = []
    fonk.append(pygame.Rect(0, 0, 170, 560))
    fonk.append(pygame.Rect(170, 0, 170, 560))
    fonk.append(pygame.Rect(340, 0, 170, 560))
    fonk.append(pygame.Rect(510, 0, 170, 560))
    fonk.append(pygame.Rect(680, 0, 170, 560))
    y = 200
    v1 = 0
    v2 = 2
    begin = 0
    running = True
    r = 0
    st = True
    clicked = False
    st1 = False
    m = 1
    for i in range(len(fonk) - 1, -1, -1):
        bob = fonk[i]
        bob.x -= 1
        if bob.right < 0:
            fonk.remove(bob)
        if fonk[-1].right <= 800:
            fonk.append(pygame.Rect(fonk[-1].right, 0, 170, 550))
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    for h in fonk:
        screen.blit(imgfon, h)
    if start_screen():
        return True
    while running:
        m += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if begin == 0 and st:
            y = 200
            bird = pygame.Rect(200, y, 50, 50)
            r = 0
            if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                v2 += 2
                begin = 1
                st1 = True
        cadrs = (cadrs + 0.25) % 3
        if begin != 2:
            for i in range(len(fonk) - 1, -1, -1):
                bob = fonk[i]
                bob.x -= 1
                if bob.right < 0:
                    fonk.remove(bob)
                if fonk[-1].right <= 800:
                    fonk.append(pygame.Rect(fonk[-1].right, 0, 170, 550))
        if st and st1:
            for i in range(len(trubs) - 1, -1, -1):
                i1 = trubs[i]
                i1.x -= 3
                if i1.right < 0:
                    trubs.remove(i1)
                    if i1 in scores:
                        scores.remove(i1)
        if begin == 1 and st and st1:
            if pygame.mouse.get_pressed()[0] and not clicked:
                v1 = -20
                clicked = True
            if not pygame.mouse.get_pressed()[0]:
                clicked = False
            if not m % 3:
                y += v1
                v1 = v1 + v2
                bird.y = y
            if len(trubs) == 0 or trubs[-1].x < 550:
                trubs.append(pygame.Rect(800, -random.randint(0, 55), 50, 200))
                trubs.append(pygame.Rect(800, random.randint(350, 450), 50, 200))
            if bird.top < 0 or bird.bottom > 540:
                begin = 2
            for t in trubs:
                if bird.colliderect(t):
                    begin = 2
                if t.right < bird.left and t not in scores:
                    scores.append(t)
                    score += 0.5
        if begin == 2:
            r = 255
            st = False
            end_screen()

        for h in fonk:
            screen.blit(imgfon, h)
        for u in trubs:
            if u.y <= 0:
                re = imgtrubs1.get_rect(bottomleft=u.bottomleft)
                screen.blit(imgtrubs1, re)
            else:
                re = imgtrubs.get_rect(topleft=u.topleft)
                screen.blit(imgtrubs, re)

        cat = imgbird.subsurface(0, 0, 70, 70)
        if v1 > -25:
             cat = pygame.transform.rotate(cat, -v1 * 2)
        else:
            cat = pygame.transform.rotate(cat, 20 * 2)
        screen.blit(cat, bird)

        text = font.render('Очки: ' + str(int(score)), 1, pygame.Color(0, 0, 0))
        screen.blit(text, (10, 10))
        if q.draw():
            return True

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == 'main':
    pygame.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    main()