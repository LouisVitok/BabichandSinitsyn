import pygame
import os
import random
import time


all_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
TIME = 120  # в секундах
FPS = 60
Fg = 0.2  # сила притяжения
fp_clock = pygame.time.Clock()
health_appearing_chance = 5
objects_existing_time = 5


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
            self.rect = self.rect.move(0, self.current_speed / FPS)
            self.y += self.current_speed / FPS
            self.current_speed += Fg
        elif not self.on_ground:
            self.on_ground = True
            self.start_time = time.perf_counter()


class Health(Object):
    def __init__(self, x, y, speed):
        super().__init__("health.png", x, y, speed)


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

    def update(self, *args):
        timedelta = fp_clock.tick(FPS) / 1000
        print(timedelta)
        if args:
            if args[0][pygame.K_w] or args[0][pygame.K_SPACE]:
                self.jumping = True
            if args[0][pygame.K_a]:
                self.rect.left -= self.start_speed * timedelta
            if args[0][pygame.K_d]:
                self.rect.left += self.start_speed * timedelta


def first_phase(screen):
    objects = [Health(random.randint(5, 795), -50, 5)]
    player = Player("player.png", 400, 500, 160, 6)
    first_phase_running = True
    quiting_from_game = False
    while first_phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_phase_running = False
                quiting_from_game = True
            if pygame.key.get_pressed():
                player_group.update(pygame.key.get_pressed())
        if player.jumping:
            player.rect.top -= player.current_jump_speed
            player.current_jump_speed -= Fg
        if player.rect.top >= 500:
            player.jumping = False
            player.current_jump_speed = player.start_jump_speed
        screen.fill((255, 255, 255))
        all_objects.draw(screen)
        all_objects.update()
        player_group.draw(screen)
        pygame.display.flip()
        fp_clock.tick(FPS)
        dice = random.randint(1, 100)
        if dice <= health_appearing_chance and len(objects) <= 4:
            objects.append(Health(random.randint(5, 795), -50, 5))
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1


