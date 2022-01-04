import os
import pygame
import sys
from first_phase import FirstPhase

FPS = 60

# константы первой фазы:
TIME = 120  # # таймер на первую фазу (в секундах)
Fg = 0.2  # сила притяжения
g = 4  # ускорение свободного падения
health_appearing_chance = 1.5  # шанс появления здоровья
trap_appearing_chance = 0.4  # шанс появления ловушек
watches_appearing_chance = 12.3  # шанс появления часов
boosters_appearing_chance = 0.5  # шанс появления бустеров
objects_existing_time = 5  # время жизни объектов на змеле (в секундах)
health_max_count = 4  # максимальное кол-во здоровья
traps_max_count = 2  # максимальное кол-во ловушек
watches_max_count = 1  # максимальное кол-во часов
boosters_max_count = 1  # максимальное кол-во бустеров
PLAYER_SPEED = 8  # скорость игрока
PLAYER_JUMP_SPEED = 9  # скорость/ускорения прыжка игрока
PLAYER_REBOUND_SPEED = 3  # скорость/ускорения отскока игрока по координате x
PLAYER_HEALTH = 10  # здоровье игрока
HEALTH_TEXT_X = 10
HEALTH_TEXT_Y = 10
PLAYER_HEALTH_X = 120
PLAYER_HEALTH_Y = 10
TIMER_Y = 10


def load_image(name):
    fullname = os.path.join('images', name)
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

    first_phase = FirstPhase(width, height, TIME, PLAYER_HEALTH, health_appearing_chance, PLAYER_SPEED,
                             PLAYER_JUMP_SPEED, PLAYER_REBOUND_SPEED, Fg, HEALTH_TEXT_X, HEALTH_TEXT_Y, PLAYER_HEALTH_X,
                             PLAYER_HEALTH_Y, TIMER_Y, health_max_count, trap_appearing_chance, traps_max_count,
                             watches_appearing_chance, watches_max_count, boosters_appearing_chance, boosters_max_count)
    if first_phase.loop(screen):
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
