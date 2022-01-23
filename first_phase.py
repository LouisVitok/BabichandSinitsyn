import pygame
import os
import random
import time


fp_clock = pygame.time.Clock()
objects_existing_time = 5
FPS = 60
g = 4


def load_image(name):
    return pygame.image.load(os.path.join('images', name)).convert_alpha()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        if not hasattr(Object, "group"):
            Object.group = pygame.sprite.Group()
        super().__init__(Object.group)
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
        if self.rect.top < 541:
            self.rect = self.rect.move(0, self.current_speed * game_speed / FPS + g)
            self.y += self.current_speed * game_speed / FPS + g
            self.current_speed += g
        elif not self.on_ground:
            self.on_ground = True
            self.start_time = time.perf_counter()
            self.rect = self.rect.move(0, 544 - self.rect.top)


class Health(Object):
    def __init__(self, x, y, speed):
        super().__init__("health.png", x, y, speed)


class Trap(Object):
    def __init__(self, x, y, speed):
        super().__init__("trap.png", x, y, speed)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect.w = 40
        self.rect.h = 40


class SpeedBooster(Object):
    def __init__(self, x, y, speed):
        super().__init__("booster_speed.png", x, y, speed)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect.w = 40
        self.rect.h = 40


class Watches(Object):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__("time.png", x, y, speed_x)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect.w = 40
        self.rect.h = 40
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.erase = False

    def update(self, game_speed):
        self.rect = self.rect.move(self.speed_x * game_speed, self.speed_y * game_speed)
        self.x += self.speed_x * game_speed
        self.y += self.speed_y * game_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, max_speed, jump_speed, rebound_speed):
        if not hasattr(Player, "group"):
            Player.group = pygame.sprite.Group()
        super().__init__(Player.group)
        self.x = x
        self.y = y
        self.current_speed = 0
        self.max_speed = max_speed
        self.start_jump_speed = jump_speed
        self.current_jump_speed = jump_speed
        self.jumping = False
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.rebound = False
        self.rebound_speed = rebound_speed
        self.rebound_direction = 0

    def force(self, x, game_speed):
        if -self.max_speed * game_speed - x <= self.current_speed <= self.max_speed * game_speed - x:
            self.current_speed += x

    def move(self, x, y):
        if 0 < self.rect.x + x < pygame.display.get_surface().get_width() - self.rect.w:
            self.rect.x += x
            self.x += x
        else:
            self.current_speed = 0
        self.rect.y += y
        self.y += y

    def setImage(self, image):
        self.image = load_image(image)


class RegularSprite(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self, image, width, height, x, y):
        super().__init__(RegularSprite.group)
        self.image = pygame.transform.scale(load_image(image), (width, height))
        self.rect = self.image.get_rect().move(x, y)
        self.rect.w = width
        self.rect.h = height
        self.x = x
        self.y = y


class FirstPhase:
    def __init__(self, width, height, fp_time, fp_player_health, health_appearing_chance, player_speed,
                 player_jump_speed, player_rebound_speed, Fg, health_text_x, health_text_y, player_health_x,
                 player_health_y, timer_y, health_max_count, trap_appearing_chance, traps_max_count,
                 watches_appearing_chance, watches_max_count, boosters_appearing_chance, boosters_max_count):
        self.width = width
        self.height = height
        self.fp_time = fp_time
        self.fp_player_health = fp_player_health
        self.health_appearing_chance = health_appearing_chance
        self.player_speed = player_speed
        self.player_jump_speed = player_jump_speed
        self.player_rebound_speed = player_rebound_speed
        self.Fg = Fg
        self.health_text_x = health_text_x
        self.health_text_y = health_text_y
        self.player_health_x = player_health_x
        self.player_health_y = player_health_y
        self.timer_y = timer_y
        self.health_max_count = health_max_count
        self.trap_appearing_chance = trap_appearing_chance
        self.traps_max_count = traps_max_count
        self.watches_appearing_chance = watches_appearing_chance
        self.watches_max_count = watches_max_count
        self.boosters_appearing_chance = boosters_appearing_chance
        self.boosters_max_count = boosters_max_count

    def loop(self, screen):
        time_left = self.fp_time
        player_health = self.fp_player_health
        pygame.event.set_allowed([pygame.QUIT])
        health_count = 1
        traps_count = 0
        watches_count = 0
        boosters_count = 0
        game_speed = 1
        objects = [Health(random.randint(5, self.width - 55), -50, 5)]
        regular_sprites = []
        player = Player("player.png", 400, 545, self.player_speed, self.player_jump_speed, self.player_rebound_speed)
        first_phase_running = True
        quiting_from_game = False
        speed_booster_continue = False
        speed_booster_touched = False
        background = pygame.transform.scale(load_image('zastavka.jpg'), (self.width, self.height))
        health_text = pygame.font.Font(None, 30).render('Здоровье:', True, (255, 0, 0))
        player_health_text = pygame.font.Font(None, 30).render(str(self.fp_player_health), True, (255, 0, 0))
        timer_text = pygame.font.Font(None, 30).render('Время:', True, (130, 131, 133))
        seconds_timer_text = pygame.font.Font(None, 30).render(str(self.fp_time), True, (130, 131, 133))
        score_text = pygame.font.Font(None, 30).render("0", True, (255, 255, 0))
        start_onesec = 0
        start_speed_booster = 0
        player_score = 0
        score_gaining_multiply = 1
        touched = False
        touched_time = 0
        moving = False
        while first_phase_running:
            if not start_onesec:
                start_onesec = time.perf_counter()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    first_phase_running = False
                    quiting_from_game = True
                if pygame.KEYDOWN:
                    if not player.rebound and not player.jumping:
                        if pygame.key.get_pressed()[pygame.K_a]:
                            player.force(-0.25 * game_speed, game_speed)
                            moving = True
                        elif pygame.key.get_pressed()[pygame.K_d] and not player.rebound:
                            player.force(0.25 * game_speed, game_speed)
                            moving = True
                        else:
                            moving = False
                if pygame.key.get_pressed():
                    if (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_SPACE]) \
                            and not player.rebound:
                        player.jumping = True
            player.move(player.current_speed, 0)
            if not moving and not player.jumping and not player.rebound:
                if player.current_speed > 0.05 * game_speed:
                    player.current_speed -= 0.05 * game_speed
                elif player.current_speed < -0.05 * game_speed:
                    player.current_speed += 0.05 * game_speed
                else:
                    player.current_speed = 0
            if player.jumping:
                player.rect.top -= player.current_jump_speed * game_speed
                player.current_jump_speed -= self.Fg * game_speed
                if player.rect.top >= 545:
                    player.jumping = False
                    player.current_jump_speed = player.start_jump_speed
            if player.rebound:
                player.rect.top -= player.current_jump_speed * game_speed // 2
                if 0 < player.rect.x + player.rebound_speed * game_speed * player.rebound_direction < \
                        pygame.display.get_surface().get_width() - player.rect.w:
                    player.rect.left += player.rebound_speed * game_speed * player.rebound_direction
                player.current_jump_speed -= self.Fg * game_speed
                if player.rect.top >= 545:
                    player.rebound = False
                    player.current_jump_speed = player.start_jump_speed
                    player.rebound_direction = 0
            if player.rect.top > 545:
                player.rect.top = 545
                player.y = 545
            screen.blit(background, (0, 0))
            screen.blit(health_text, (self.health_text_x, self.health_text_y))
            screen.blit(player_health_text, (self.player_health_x, self.player_health_y))
            screen.blit(timer_text, (self.width - 115, self.timer_y))
            screen.blit(seconds_timer_text, (self.width - 35, self.timer_y))
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 5))
            Object.group.draw(screen)
            Object.group.update(game_speed)
            Player.group.draw(screen)
            RegularSprite.group.draw(screen)
            pygame.display.flip()
            fp_clock.tick(FPS)
            dice = random.uniform(1.0, 100.0)
            if dice <= self.health_appearing_chance and health_count < self.health_max_count:
                objects.append(Health(random.randint(5, self.width - 55), -50, 5))
                health_count += 1
            dice = random.uniform(0.1, 100.0)
            if dice <= self.trap_appearing_chance and traps_count < self.traps_max_count:
                objects.append(Trap(random.randint(5, self.width - 55), -50, 5))
                traps_count += 1
            dice = random.uniform(0.1, 100.0)
            if dice <= self.watches_appearing_chance and watches_count < self.watches_max_count:
                watches_x = random.randint(-100, self.width + 105)
                if watches_x <= -50 or watches_x >= self.width + 50:
                    watches_y = random.randint(self.height // 2.5, self.height // 1.5)
                else:
                    watches_y = random.randint(-2, 1)
                if watches_y >= 0:
                    watches_y = random.randint(self.height + 105, self.height + 155)
                else:
                    watches_y = random.randint(-155, -105)
                if watches_x < 0:
                    speed_x = random.randint(1, 3)
                else:
                    speed_x = random.randint(-3, -1)
                if watches_y < 0:
                    speed_y = random.randint(1, 3)
                else:
                    speed_y = random.randint(-3, -1)
                objects.append(Watches(watches_x, watches_y, speed_x, speed_y))
                watches_count += 1
            dice = random.uniform(0.1, 100.0)
            if dice <= self.boosters_appearing_chance and boosters_count < self.boosters_max_count:
                objects.append(SpeedBooster(random.randint(5, 745), -50, 5))
            for obj_i in range(len(objects)):
                if objects[obj_i].rect.colliderect(player.rect) and not touched:
                    if type(objects[obj_i]) == Health:
                        player_health += 1
                        player_score += 1 * score_gaining_multiply
                        score_text = pygame.font.Font(None, 30).render(str(player_score), True, (255, 255, 0))
                        player_health_text = pygame.font.Font(None, 30).render(str(player_health), True, (255, 0, 0))
                        objects[obj_i].erase = True
                    if type(objects[obj_i]) == Trap:
                        touched_time = time.perf_counter()
                        touched = True
                        player.setImage("player_transparent.png")
                        player.rebound = True
                        if abs(player.current_speed) >= 1:
                            player.rebound_speed = abs(player.current_speed)
                        else:
                            player.rebound_speed = 1
                        player.current_speed = 0
                        if objects[obj_i].rect.x < player.rect.x:
                            player.rebound_direction = 1
                        elif objects[obj_i].rect.x > player.rect.x:
                            player.rebound_direction = -1
                        player_health -= 1
                        player_health_text = pygame.font.Font(None, 30).render(str(player_health), True, (255, 0, 0))
                        if player_score >= 3:
                            player_score -= 3 * score_gaining_multiply
                            score_text = pygame.font.Font(None, 30).render(str(player_score), True, (255, 255, 0))
                        else:
                            player_score = 0
                            score_text = pygame.font.Font(None, 30).render(str(player_score), True, (255, 255, 0))
                    if type(objects[obj_i]) == Watches:
                        objects[obj_i].erase = True
                        time_left += 5 * game_speed
                        seconds_timer_text = pygame.font.Font(None, 30).render(str(time_left), True, (130, 131, 133))
                        player_score += 2 * score_gaining_multiply
                        score_text = pygame.font.Font(None, 30).render(str(player_score), True, (255, 255, 0))
                    if type(objects[obj_i]) == SpeedBooster and not speed_booster_touched:
                        objects[obj_i].erase = True
                        start_speed_booster = time.perf_counter()
                        speed_booster_continue = True
                        speed_booster_touched = True
                        game_speed = 2
                        score_gaining_multiply = 3
                        regular_sprites.append(RegularSprite("booster_speed.png", 100, 100, 45, 593))
                        regular_sprites.append(RegularSprite("red_frame.png", 100, 100, 45, 593))
                if type(objects[obj_i]) == Watches:
                    if objects[obj_i].x <= -150 or objects[obj_i].x >= self.width + 175:
                        objects[obj_i].erase = True
                    if objects[obj_i].y <= -150 or objects[obj_i].y >= self.height + 175:
                        objects[obj_i].erase = True
                if objects[obj_i].erase:
                    if type(objects[obj_i]) == Health:
                        health_count -= 1
                    if type(objects[obj_i]) == Trap:
                        traps_count -= 1
                    if type(objects[obj_i]) == Watches:
                        watches_count -= 1
                    Object.group.remove(objects[obj_i])
                    objects.pop(obj_i)
                    break
            if time.perf_counter() - start_onesec >= 1 / game_speed:
                time_left -= 1
                seconds_timer_text = pygame.font.Font(None, 30).render(str(time_left), True, (130, 131, 133))
                start_onesec = 0
            if touched and time.perf_counter() - touched_time >= 3.00 / game_speed:
                touched = False
                player.setImage("player.png")
            if speed_booster_continue:
                if time.perf_counter() - start_speed_booster >= 5.00 / game_speed:
                    speed_booster_continue = False
                    game_speed = 1
                    score_gaining_multiply = 1
                    for sprite_i in range(len(regular_sprites) - 1):
                        RegularSprite.group.remove(regular_sprites[sprite_i])
                        regular_sprites.pop(sprite_i)
                    speed_booster_touched = False
            if not time_left:
                return player_health, player_score
            if player_health <= 0:
                return 0
            if quiting_from_game:
                pygame.quit()
                return 0
        return player_health, player_score
