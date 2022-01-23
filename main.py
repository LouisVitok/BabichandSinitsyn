import os
import pygame
import sys
import time
import random
from first_phase import FirstPhase

FPS = 60

# константы первой фазы:
TIME = 45  # # таймер на первую фазу (в секундах)
Fg = 0.4  # сила притяжения
g = 4  # ускорение свободного падения
health_appearing_chance = 2.5  # шанс появления здоровья
trap_appearing_chance = 0.55  # шанс появления ловушек
watches_appearing_chance = 0.9  # шанс появления часов
boosters_appearing_chance = 0.35  # шанс появления бустеров
objects_existing_time = 5  # время жизни объектов на езмеле (в секундах)
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



class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, start_jump_speed, health):
        if not hasattr(Player, "group"):
            Player.group = pygame.sprite.Group()
        super().__init__(Player.group)
        self.x = x
        self.y = y
        self.jumping = False
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.jump_speed = start_jump_speed
        self.start_jump_speed = start_jump_speed
        self.health = health

        
class Trap(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        if not hasattr(Trap, "group"):
            Trap.group = pygame.sprite.Group()
        super().__init__(Trap.group)
        self.x = x
        self.y = y
        self.jumping = False
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.speed = speed
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect.w = 40
        self.rect.h = 40
        self.touched = False

    def update(self):
        self.rect.left -= self.speed
        self.x -= self.speed
        
        

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

        
def final_screen(score_num):
    background_img = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    screen.blit(background_img, (0, 0))
    score_text_ = pygame.font.Font(None, 120).render(str(score_num), True, (255, 255, 0))
    your_score_text = pygame.font.Font(None, 120).render("Ваши очки:", True, (255, 255, 0))
    screen.blit(your_score_text, (10, height // 2))
    screen.blit(score_text_, (your_score_text.get_width() + 5, height // 2))
    pygame.display.flip()
    running_screen = True
    while running_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    diff = start_screen(width, height)

    first_phase = FirstPhase(width, height, int(TIME // diff), int(PLAYER_HEALTH // diff), health_appearing_chance // diff,
                             PLAYER_MAX_SPEED, PLAYER_JUMP_SPEED, PLAYER_REBOUND_SPEED, Fg, HEALTH_TEXT_X, HEALTH_TEXT_Y,
                             PLAYER_HEALTH_X, PLAYER_HEALTH_Y, TIMER_Y, health_max_count, trap_appearing_chance * diff,
                             traps_max_count, watches_appearing_chance // diff, watches_max_count, boosters_appearing_chance,
                             boosters_max_count)
    health, score = first_phase.loop(screen)
    player = Player("player.png", width // 6, 545, PLAYER_JUMP_SPEED, health)
    score_text = pygame.font.Font(None, 30).render(str(score), True, (255, 255, 0))
    health_text = pygame.font.Font(None, 30).render(str(health), True, (255, 0, 0))
    running = True
    traps = [Trap("trap.png", width + 50, 545, 3)]
    traps_count = 1
    touched = False
    start_time = 0
    new_time_score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed():
                if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.jumping = True
        if player.jumping:
            player.rect.top -= player.jump_speed
            player.jump_speed -= Fg * 2
            if player.rect.top >= 545:
                player.jumping = False
                player.jump_speed = player.start_jump_speed

        background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
        screen.blit(background, (0, 0))
        Player.group.draw(screen)
        Trap.group.draw(screen)
        Trap.group.update()
        screen.blit(score_text, (0, 0))
        screen.blit(health_text, (width // 2, 0))
        pygame.display.flip()
        clock.tick(FPS)

        dice = random.uniform(0.0, 100.0)
        if dice <= 2.0 and traps_count < 3:
            traps.append(Trap("trap.png", width + 50, 545, 3))
            traps_count += 1
        for trap_i in range(len(traps)):
            if traps[trap_i].rect.colliderect(player.rect) and not touched:
                player.health -= 1
                health_text = pygame.font.Font(None, 30).render(str(player.health), True, (255, 0, 0))
                touched = True
                traps[trap_i].touched = True
            if traps[trap_i].x <= player.x - 50 and not traps[trap_i].touched:
                score += 1
                score_text = pygame.font.Font(None, 30).render(str(score), True, (255, 255, 0))
        for trap_i in range(len(traps)):
            if traps[trap_i].x <= -50:
                traps_count -= 1
                Trap.group.remove(traps[trap_i])
                traps.pop(trap_i)
                break
        if touched:
            start_time = time.perf_counter()
        if time.perf_counter() - start_time >= 1:
            touched = False
        if player.health <= 0:
            running = False
    final_screen(score)
