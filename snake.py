import pygame
from random import randrange

# Resolution and CellSize
RES = 600
SIZE = 30

# Colors
YELLOW = (255, 221, 51)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# GameVariables
x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
dirs = {'W': True, 'S': True, 'A': True, 'D': True}
snake = [(x, y)]
length = 1
dx, dy = 0, 0
score = 0
alive = True
FPS = 5

# Initialization
pygame.init()
screen = pygame.display.set_mode([RES, RES])
pygame.display.set_caption('Snake')

# SysVariables
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 24, bold=True)
font_end = pygame.font.SysFont('Arial', 44, bold=True)
font_space = pygame.font.SysFont('Arial', 24, bold=True)
img = pygame.image.load('bg.jpg').convert()

# Game cycle
running = True
while running:
    clock.tick(FPS)
    screen.blit(img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if alive:
                # control
                key = pygame.key.get_pressed()
                if key[pygame.K_w] or key[pygame.K_UP] and dirs['W']:
                    dx, dy = 0, -1
                    dirs = {'W': True, 'S': False, 'A': True, 'D': True}
                if key[pygame.K_s] or key[pygame.K_DOWN] and dirs['S']:
                    dx, dy = 0, 1
                    dirs = {'W': False, 'S': True, 'A': True, 'D': True}
                if key[pygame.K_a] or key[pygame.K_LEFT] and dirs['A']:
                    dx, dy = -1, 0
                    dirs = {'W': True, 'S': True, 'A': True, 'D': False}
                if key[pygame.K_d] or key[pygame.K_RIGHT] and dirs['D']:
                    dx, dy = 1, 0
                    dirs = {'W': True, 'S': True, 'A': False, 'D': True}
            else:
                # restart
                if event.key == pygame.K_SPACE:
                    alive = True
                    x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                    snake = [(x, y)]
                    length = 1
                    dx, dy = 0, 0
                    score = 0
                    apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                    FPS = 5

    # drawing snake, apple
    [(pygame.draw.rect(screen, YELLOW, (i, j, SIZE - 1, SIZE - 1))) for i, j in snake]
    pygame.draw.rect(screen, RED, (*apple, SIZE - 1, SIZE - 1))

    if alive:
        # snake movement
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]

        # eating apple
        if snake[-1] == apple:
            apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            length += 1
            score += 1
            FPS += 1

        # game over
        if (x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake))):
            alive = False
    else: # show game over
        render_end = font_end.render('GAME OVER', 1, WHITE)
        screen.blit(render_end, (RES // 2 - 115, RES // 3))
        render_space = font_space.render(
            'Press SPACE to restart the game', 1, WHITE)
        screen.blit(render_space, (RES // 2 - 155, RES // 3 + 60))

    # show score
    render_score = font_score.render(f'Score: {score}', 1, WHITE)
    screen.blit(render_score, (12, 5))

    #
    pygame.display.update()
