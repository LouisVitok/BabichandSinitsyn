import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    running = True
    x_pos = 0
    v = 20
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.draw.rect(screen, (37, 42, 178), (0, 0, width, 400), 0)
        pygame.draw.rect(screen, (96, 44, 88), (0, 400, width, 200), 0)
        pygame.draw.circle(screen, (255, 0, 0), (200, 380), 20)
        pygame.draw.rect(screen, (0, 0, 33), (800 - int(x_pos), 380, 20, 20), 0)

        x_pos += v / fps
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
