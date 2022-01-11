import os
import pygame
import sys
from first_phase import FirstPhase

FPS = 60

# константы первой фазы:
TIME = 120  # # таймер на первую фазу (в секундах)
Fg = 0.4  # сила притяжения
g = 4  # ускорение свободного падения
health_appearing_chance = 1.5  # шанс появления здоровья
trap_appearing_chance = 0.08  # шанс появления ловушек
watches_appearing_chance = 0.6  # шанс появления часов
boosters_appearing_chance = 0.00002  # шанс появления бустеров
objects_existing_time = 5  # время жизни объектов на змеле (в секундах)
health_max_count = 4  # максимальное кол-во здоровья
traps_max_count = 2  # максимальное кол-во ловушек
watches_max_count = 1  # максимальное кол-во часов
boosters_max_count = 1  # максимальное кол-во бустеров
PLAYER_MAX_SPEED = 4.0  # максимальная скорость игрока
PLAYER_JUMP_SPEED = 15  # скорость/ускорения прыжка игрока
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
    intro = ['Выберите сложность', 'Легко', 'Нормально', 'Сложно']
    fonts = []
    background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    screen.blit(background, (0, 0))
    y = 5
    for line in intro:
        s = pygame.font.Font(None, 70).render(line, True, (250, 250, 210))
        rect = s.get_rect()
        rect.x = width // 2 - rect.w // 2
        rect.y = y
        y += height // 4
        fonts.append(s)
        screen.blit(s, (rect.x, rect.y))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                y = 5
                for i in range(len(fonts)):
                    rect = fonts[i].get_rect()
                    rect.x = width // 2 - rect.w // 2
                    rect.y = y
                    if rect.collidepoint(pygame.mouse.get_pos()) and i != 0:
                        if intro[i] == 'Легко':
                            return 1
                        if intro[i] == 'Нормально':
                            return 1.5
                        if intro[i] == 'Сложно':
                            return 3
                    y += height // 4
        # screen.blit(background, (0, 0))
        for i in range(len(intro)):
            if fonts[i].get_rect().collidepoint(pygame.mouse.get_pos()):
                color = (255, 10, 10)
            else:
                color = (250, 250, 210)
            rect = fonts[i].get_rect()
            x = width // 2 - rect.w // 2
            screen.blit(fonts[i], (x, y))
            pygame.display.flip()
            y += height // 4
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
    diff = start_screen(width, height)

    first_phase = FirstPhase(width, height, int(TIME // diff), int(PLAYER_HEALTH // diff), health_appearing_chance // diff,
                             PLAYER_MAX_SPEED, PLAYER_JUMP_SPEED, PLAYER_REBOUND_SPEED, Fg, HEALTH_TEXT_X, HEALTH_TEXT_Y,
                             PLAYER_HEALTH_X, PLAYER_HEALTH_Y, TIMER_Y, health_max_count, trap_appearing_chance * diff,
                             traps_max_count, watches_appearing_chance // diff, watches_max_count, boosters_appearing_chance,
                             boosters_max_count)
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
