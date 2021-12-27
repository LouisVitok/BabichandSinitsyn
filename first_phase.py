import pygame
import os
import random
import time


all_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
TIME = 120  # в секундах
FPS = 60
Fg = 0.2  # сила притяжения
g = 4
fp_clock = pygame.time.Clock()
health_appearing_chance = 1.5
trap_appearing_chance = 0.4
objects_existing_time = 5
health_max_count = 4
traps_max_count = 2
PLAYER_SPEED = 10
PLAYER_JUMP_SPEED = 9


def load_image(name):
    return pygame.image.load(os.path.join('images', name)).convert_alpha()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__(all_objects)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y
        self.start_speed = speed
        self.current_speed = speed
        self.on_ground = False
        self.start_time = 0
        self.current_time = 0
        self.erase = False

    def update(self):
        if self.on_ground:
            self.current_time = time.perf_counter()
            if self.current_time - self.start_time >= float(objects_existing_time):
                self.erase = True
        if self.rect.top <= 500:
            self.rect = self.rect.move(0, self.current_speed / FPS + g)
            self.y += self.current_speed / FPS + g
            self.current_speed += g
        elif not self.on_ground:
            self.on_ground = True
            self.start_time = time.perf_counter()


class Health(Object):
    def __init__(self, x, y, speed):
        super().__init__("health.png", x, y, speed)


class Trap(Object):
    def __init__(self, x, y, speed):
        super().__init__("trap.png", x, y, speed)
        self.image = pygame.transform.scale(self.image, (50, 50))


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, jump_speed):
        super().__init__(player_group)
        self.x = x
        self.y = y
        self.start_speed = speed
        self.current_speed = speed
        self.start_jump_speed = jump_speed
        self.current_jump_speed = jump_speed
        self.jumping = False
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)

    def go_right(self):
        self.rect.left += self.start_speed

    def go_left(self):
        self.rect.left -= self.start_speed


def first_phase(screen, width, height):
    pygame.event.set_allowed([pygame.QUIT])
    health_count = 1
    traps_count = 0
    objects = [Health(random.randint(5, 795), -50, 5)]
    player = Player("player.png", 400, 500, PLAYER_SPEED, PLAYER_JUMP_SPEED)
    first_phase_running = True
    quiting_from_game = False
    background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    screen.blit(background, (0, 0))
    while first_phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_phase_running = False
                quiting_from_game = True
            if pygame.key.get_pressed():
                if pygame.key.get_pressed()[pygame.K_a]:
                    player.go_left()
                if pygame.key.get_pressed()[pygame.K_d]:
                    player.go_right()
                if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.jumping = True
        if player.jumping:
            player.rect.top -= player.current_jump_speed
            player.current_jump_speed -= Fg
        if player.rect.top >= 500:
            player.jumping = False
            player.current_jump_speed = player.start_jump_speed
        screen.blit(background, (0, 0))
        all_objects.draw(screen)
        all_objects.update()
        player_group.draw(screen)
        pygame.display.flip()
        fp_clock.tick(FPS)
        dice = random.uniform(1.0, 100.0)
        if dice <= health_appearing_chance and health_count <= health_max_count:
            objects.append(Health(random.randint(5, 795), -50, 5))
            health_count += 1
        dice = random.uniform(0.1, 100.0)
        if dice <= trap_appearing_chance and traps_count <= traps_max_count:
            objects.append(Trap(random.randint(5, 795), -50, 5))
            traps_count += 1
        for obj_i in range(len(objects)):
            if objects[obj_i].erase:
                if type(objects[obj_i]) == Health:
                    health_count -= 1
                if type(objects[obj_i]) == Trap:
                    traps_count -= 1
                all_objects.remove(objects[obj_i])
                objects.pop(obj_i)
                break
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1


