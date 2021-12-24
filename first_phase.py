import pygame
import os
import random


all_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
TIME = 120  # в секундах
FPS = 60
g = 1
fp_clock = pygame.time.Clock()


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

    def update(self):
        if self.y <= 500:
            self.rect = self.rect.move(0, self.current_speed / FPS)
            self.y += self.current_speed / FPS
            self.current_speed += g


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
        if self.jumping:
            self.rect.move(0, -self.current_jump_speed)
            self.current_jump_speed -= g
            self.y -= self.current_jump_speed
        if self.y >= 500:
            self.jumping = False
            self.current_jump_speed = self.start_jump_speed
        if args:
            if args[0][pygame.K_SPACE]:
                self.jumping = True
            if args[0][pygame.K_a]:
                self.rect.left -= self.start_speed


def first_phase(screen):
    health = Health(random.randint(5, 795), -50, 5)
    first_phase_running = True
    quiting_from_game = False
    while first_phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_phase_running = False
                quiting_from_game = True
            if pygame.key.get_pressed():
                player_group.update(pygame.key.get_pressed())
        screen.fill((255, 255, 255))
        all_objects.draw(screen)
        all_objects.update()
        fp_clock.tick(FPS)
        pygame.display.flip()
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1


