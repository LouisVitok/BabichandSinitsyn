import pygame
import os
import random


all_objects = pygame.sprite.Group()
TIME = 120  # в секундах


def load_image(name):
    return pygame.image.load(os.path.join('images', name)).convert_alpha()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__(all_objects)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y
        self.speed = speed


class Health(Object):
    def __init__(self, x, y, speed):
        super().__init__("health.png", x, y, speed)


def first_phase(screen):
    health = Health(random.randint(5, 795), -50, 5)
    first_phase_running = True
    quiting_from_game = False
    while first_phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_phase_running = False
                quiting_from_game = True
        all_objects.draw(screen)
        all_objects.update()
        pygame.display.flip()
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1


