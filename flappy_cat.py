import pygame
import random
from button_and_consts import Button, FPS, terminate, HEIGHT, WIDTH, earning_money
from button_and_consts import load_image
import sqlite3

screen = 0
clock = 0
score = 0


# экран старта
def start_screen():
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    play = Button(325, 168, load_image('start_end/play.png'), (150, 75), screen)
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


# экран проигрыша
def end_screen():
    global score
    connect = sqlite3.connect('tamagochi.db')
    cur = connect.cursor()
    bestsc = cur.execute('''SELECT bestscore from bestscores WHERE game = "flappy cat"''').fetchone()
    if bestsc[0] >= score:
        sc_image = 'start_end/score.png'
        s = (150, 60)
        x = 0
    else:
        sc_image = 'start_end/newscore.png'
        s = (180, 60)
        x = 50
    q = Button(760, 0, load_image('data/cross.png'), (40, 40), screen)
    logo = pygame.transform.scale(load_image('start_end/gameover.png'), (250, 125))
    screen.blit(logo, (275, 30))
    scim = pygame.transform.scale(load_image(sc_image), s)
    screen.blit(scim, (250 - x, 165))
    font = pygame.font.Font(None, 100)
    string_rendered = font.render(str(int(score)), bool(1), pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.topleft = (420, 165)
    screen.blit(string_rendered, intro_rect)
    re = Button(300, 245, load_image('start_end/replay.png'), (200, 56), screen)
    pygame.mixer.Sound('sound_data/gameover.mp3').play()
    if sc_image == 'start_end/newscore.png':
        cur.execute('UPDATE bestscores SET bestscore = ? WHERE game = "flappy cat"', (score,))
        connect.commit()
    connect.close()
    earning_money(screen, score)
    score = 0
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


# оснавная функция миниигры
def main():
    global score
    pygame.mixer.music.load('sound_data/fonk.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    sc = pygame.transform.scale(load_image('start_end/score.png'), (100, 40))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Flappy bird')
    pygame.display.flip()
    y = 200
    font = pygame.font.Font(None, 70)
    bird = pygame.Rect(200, y, 50, 50)
    imgbird = pygame.transform.scale(load_image('data/cat.png'), (70, 70))
    imgtrubs = pygame.transform.scale(load_image('data/true_fver.png'), (50, 300))
    imgtrubs1 = pygame.transform.scale(load_image('data/true_sniz.png'), (50, 300))
    imgfon = pygame.transform.scale(load_image('data/fon1.png'), (180, 560))
    trubs = []
    cadrs = 0
    fonk = []
    scores = []
    trubgs = 160
    trubgp = 550 // 2
    level = 3
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
        bob.x -= level // 2
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
                i1.x -= level
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
                r += 1
                trubs.append(pygame.Rect(800, 0, 50, trubgp - trubgs // 2))
                trubs.append(pygame.Rect(800, trubgp + trubgs // 2, 50, 550 - trubgp + trubgs // 2))
                if r % 2 == 0:
                    trubgp += random.randrange(20, 100, 10)
                if r % 2 == 1:
                    trubgp += random.randrange(-80, 0, 10)
                if trubgp < trubgs:
                    trubgp = trubgs
                elif trubgp > 550 - trubgs:
                    trubgp = 550 - trubgs
            if bird.top < 0 or bird.bottom > 540:
                begin = 2
            for t in trubs:
                if bird.colliderect(t):
                    begin = 2
                if t.right < bird.left and t not in scores:
                    scores.append(t)
                    score += 0.5
                    level = 3 + score // 5
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
        text = font.render(str(int(score)), bool(1), (0, 0, 0))
        screen.blit(sc, (10, 10))
        screen.blit(text, (118, 8))
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
