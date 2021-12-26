import os
import pygame
import sys
from first_phase import first_phase

FPS = 60


def load_image(name):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def start_screen(width, height):
    intro = ['Нажмите клавишу']
    background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    screen.blit(background, (0, 0))
    for line in intro:
        s = pygame.font.Font(None, 70).render(line, True, (250, 250, 210))
        rect = s.get_rect()
        rect.x = width // 2 - 220
        rect.y = height // 2 - 30
        screen.blit(s, (rect.x, rect.y))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    # pygame.mixer.music.load("sound2.mp3")
    # pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    start_screen(800, 600)

    if first_phase(screen):
        running = True
        x_pos = 0
        v = 30
        fps = 60
        a = -10
        sc = 15
        is_upper = False
        pos = 447
        k = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_upper = True

            background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
            screen.blit(background, (0, 0))
            if is_upper:
                if k <= 3:
                    pos = pos - sc + a / 2
                else:
                    pos = pos + sc - a / 2
                pygame.draw.circle(screen, (255, 0, 0), (200, pos), 20)
                k += 1
                if k > 6:
                    is_upper = False
                    k = 0
                    pos = 447
            else:
                pygame.draw.circle(screen, (255, 0, 0), (200, 447), 20)
            pygame.draw.rect(screen, (0, 250, 154), (800 - int(x_pos), 447, 20, 20), 0)

            x_pos += v / fps
            clock.tick(fps)
            pygame.display.flip()
        pygame.quit()
