import pygame
import os


all_objects = pygame.sprite.Group()


def load_image(name):
    return pygame.image.load(os.path.join('images', name)).convert_alpha()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, ):
        super().__init__(all_objects)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y


class Health(Object):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)


def first_phase():
    ...
