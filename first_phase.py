import pygame
import os
import random
import time


all_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
fp_clock = pygame.time.Clock()
objects_existing_time = 5
FPS = 60
g = 4


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

    def update(self, game_speed):
        if self.on_ground:
            self.current_time = time.perf_counter()
            if self.current_time - self.start_time >= float(objects_existing_time // game_speed):
                self.erase = True
        if self.rect.top <= 415:
            self.rect = self.rect.move(0, self.current_speed * game_speed / FPS + g)
            self.y += self.current_speed * game_speed / FPS + g
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
        self.rect.w = 50
        self.rect.h = 50


class SpeedBooster(Object):
    def __init__(self, x, y, speed):
        super().__init__("booster_speed.png", x, y, speed)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.w = 50
        self.rect.h = 50


class Watches(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(all_objects)
        self.image = load_image("time.png")
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.w = 50
        self.rect.h = 50
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.erase = False

    def update(self, game_speed):
        self.rect = self.rect.move(self.speed_x * game_speed, self.speed_y * game_speed)
        self.x += self.speed_x * game_speed
        self.y += self.speed_y * game_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, jump_speed, rebound_speed):
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
        self.rebound = False
        self.rebound_speed = rebound_speed
        self.rebound_direction = 0

    def go_right(self, game_speed):
        self.rect.left += self.start_speed * game_speed

    def go_left(self, game_speed):
        self.rect.left -= self.start_speed * game_speed


def first_phase_loop(screen, width, height, fp_time, fp_player_health, health_appearing_chance, player_speed,
                     player_jump_speed, player_rebound_speed, Fg, health_text_x, health_text_y, player_health_x,
                     player_health_y, timer_y, health_max_count, trap_appearing_chance, traps_max_count,
                     watches_appearing_chance, watches_max_count, boosters_appearing_chance, boosters_max_count):
    time_left = fp_time
    player_health = fp_player_health
    pygame.event.set_allowed([pygame.QUIT])
    health_count = 1
    traps_count = 0
    watches_count = 0
    boosters_count = 0
    game_speed = 1
    objects = [Health(random.randint(5, width - 55), -50, 5)]
    player = Player("player.png", 400, 417, player_speed, player_jump_speed, player_rebound_speed)
    first_phase_running = True
    quiting_from_game = False
    background = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    health_text = pygame.font.Font(None, 30).render('Здоровье:', True, (255, 0, 0))
    player_health_text = pygame.font.Font(None, 30).render(str(fp_player_health), True, (255, 0, 0))
    timer_text = pygame.font.Font(None, 30).render('Время:', True, (130, 131, 133))
    seconds_timer_text = pygame.font.Font(None, 30).render(str(fp_time), True, (130, 131, 133))
    start_onesec = 0
    while first_phase_running:
        if not start_onesec:
            start_onesec = time.perf_counter()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_phase_running = False
                quiting_from_game = True
            if pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_a] and not player.rebound:
                    player.go_left(game_speed)
                if pygame.key.get_pressed()[pygame.K_d] and not player.rebound:
                    player.go_right(game_speed)
            if pygame.key.get_pressed():
                if (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_SPACE])\
                        and not player.rebound:
                    player.jumping = True
        if player.jumping:
            player.rect.top -= player.current_jump_speed * game_speed
            player.current_jump_speed -= Fg
            if player.rect.top >= 417:
                player.jumping = False
                player.current_jump_speed = player.start_jump_speed
        if player.rebound:
            player.rect.top -= player.current_jump_speed * game_speed // 2
            player.rect.left += player.rebound_speed * game_speed * player.rebound_direction
            player.current_jump_speed -= Fg
            if player.rect.top >= 417:
                player.rebound = False
                player.current_jump_speed = player.start_jump_speed
                player.rebound_direction = 0
        screen.blit(background, (0, 0))
        screen.blit(health_text, (health_text_x, health_text_y))
        screen.blit(player_health_text, (player_health_x, player_health_y))
        screen.blit(timer_text, (width - 115, timer_y))
        screen.blit(seconds_timer_text, (width - 35, timer_y))
        all_objects.draw(screen)
        all_objects.update(game_speed)
        player_group.draw(screen)
        pygame.display.flip()
        fp_clock.tick(FPS)
        dice = random.uniform(1.0, 100.0)
        if dice <= health_appearing_chance and health_count < health_max_count:
            objects.append(Health(random.randint(5, width - 55), -50, 5))
            health_count += 1
        dice = random.uniform(0.1, 100.0)
        if dice <= trap_appearing_chance and traps_count < traps_max_count:
            objects.append(Trap(random.randint(5, width - 55), -50, 5))
            traps_count += 1
        dice = random.uniform(0.1, 100.0)
        if dice <= watches_appearing_chance and watches_count < watches_max_count:
            watches_x = random.randint(-100, width + 105)
            if watches_x <= -50 or watches_x >= width + 50:
                watches_y = random.randint(height // 2.5, height // 1.5)
            else:
                watches_y = random.randint(-2, 1)
                if watches_y >= 0:
                    watches_y = random.randint(height + 105, height + 155)
                else:
                    watches_y = random.randint(-155, -105)
            if watches_x < 0:
                speed_x = random.randint(2, 5)
            else:
                speed_x = random.randint(-5, -2)
            if watches_y < 0:
                speed_y = random.randint(2, 5)
            else:
                speed_y = random.randint(-5, -2)
            objects.append(Watches(watches_x, watches_y, speed_x, speed_y))
            watches_count += 1
        dice = random.uniform(0.1, 100.0)
        if dice <= boosters_appearing_chance and boosters_count < boosters_max_count:
            objects.append(SpeedBooster(random.randint(5, 745), -50, 5))
        for obj_i in range(len(objects)):
            if objects[obj_i].rect.colliderect(player.rect):
                if type(objects[obj_i]) == Health:
                    player_health += 1
                    player_health_text = pygame.font.Font(None, 30).render(str(player_health), True, (255, 0, 0))
                    objects[obj_i].erase = True
                if type(objects[obj_i]) == Trap:
                    player.rebound = True
                    if objects[obj_i].rect.x < player.rect.x:
                        player.rebound_direction = 1
                    elif objects[obj_i].rect.x > player.rect.x:
                        player.rebound_direction = -1
                    player_health -= 1
                    player_health_text = pygame.font.Font(None, 30).render(str(player_health), True, (255, 0, 0))
                if type(objects[obj_i]) == Watches:
                    objects[obj_i].erase = True
                    time_left += 3
                    seconds_timer_text = pygame.font.Font(None, 30).render(str(time_left), True, (130, 131, 133))
            if type(objects[obj_i]) == Watches:
                if objects[obj_i].x <= -150 or objects[obj_i].x >= width + 175:
                    objects[obj_i].erase = True
                if objects[obj_i].y <= -150 or objects[obj_i].y >= height + 175:
                    objects[obj_i].erase = True
            if objects[obj_i].erase:
                if type(objects[obj_i]) == Health:
                    health_count -= 1
                if type(objects[obj_i]) == Trap:
                    traps_count -= 1
                if type(objects[obj_i]) == Watches:
                    watches_count -= 1
                all_objects.remove(objects[obj_i])
                objects.pop(obj_i)
                break
        if time.perf_counter() - start_onesec >= 1:
            time_left -= 1
            seconds_timer_text = pygame.font.Font(None, 30).render(str(time_left), True, (130, 131, 133))
            start_onesec = 0
        if not time_left:
            return 1
        if player_health <= 0:
            return 0
    if quiting_from_game:
        pygame.quit()
        return 0
    return 1
