import pygame
import os
import random


all_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
TIME = 120  # в секундах
FPS = 60
g = 0.2  # ускорение свободного падения
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
        if self.rect.top <= 500:
            self.rect = self.rect.move(0, self.current_speed / FPS)
            self.y += self.current_speed / FPS
            self.current_speed += g
            print(1)


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
        if args:
            if args[0][pygame.K_w] or args[0][pygame.K_SPACE]:
                self.jumping = True
            if args[0][pygame.K_a]:
                self.rect.left -= self.start_speed
            if args[0][pygame.K_d]:
                self.rect.left += self.start_speed


def first_phase(screen):
    health = Health(random.randint(5, 795), -50, 5)
    player = Player("player.png", 400, 500, 3, 6)
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
            player.current_jump_speed -= g
        if player.rect.top >= 500:
            player.jumping = False
            player.current_jump_speed = player.start_jump_speed
        screen.fill((255, 255, 255))
        all_objects.draw(screen)
        all_objects.update()
        player_group.draw(screen)
        pygame.display.flip()
        fp_clock.tick(FPS)
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1


