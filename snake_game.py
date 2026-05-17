import pygame
from pygame import Rect
from random import randrange

pygame.init()
screen = pygame.display.set_mode((490, 490))

fps = pygame.time.Clock()  # framerate per second

# background
rect_x = 0
rect_y = 0
rect_1 = Rect(rect_x, rect_y, 35, 35)
rect_2 = Rect(0, 0, 490, 490)
GREEN = 148, 255, 69
OTHER_GREEN = 148, 248, 69
SNAKE_BLUE = 98, 122, 241
APPLE_RED = 255, 75, 43
cell_size = 35
game_active = False
game_over = False
score = 0

# texts
title = pygame.font.SysFont("calibri", 70, pygame.font.Font.bold)
title_text1 = title.render("NA", True, SNAKE_BLUE)
title_text2 = title.render("KE", True, SNAKE_BLUE)
title_rect1 = Rect(cell_size * 3.5, cell_size * 4, cell_size, cell_size * 2)
title_rect2 = Rect(cell_size * 3.5, cell_size * 6, cell_size, cell_size * 2)

text = pygame.font.SysFont("calibri", 30)
start_text = text.render("Press SPACE to start the game", True, APPLE_RED)
start_rect = Rect(cell_size // 2, cell_size * 9, cell_size, cell_size)


class Fruit:
    def __init__(self, surf):
        self.x = 315
        self.y = 245
        self.surf = surf
        self.eaten = False
        self.rect = Rect(self.x, self.y, cell_size, cell_size)

    def place_fruit(self):
        # fruit_rect = self.surf.get_rect( midtop= (self.x, self.y))
        screen.blit(self.surf, self.rect)

    def pos(self, block_pos):
        x = randrange(0, 491 - 35, 35)
        y = randrange(0, 491 - 35, 35)
        for i in block_pos:
            if Rect(i[0], i[1], cell_size, cell_size).contains(Rect(x,y, cell_size, cell_size)):
                x, y = self.pos(block_pos)
        return x, y

    # update pos of fruit if you 1.eat fruit 2.place it where no snake exists 3.


class Snake:

    def __init__(self, direction):
        self.block_num = 3
        self.x = 140
        self.y = 245
        self.head = self.x, self.y
        self.blocks = [(self.x, self.y), (self.x - 35, self.y), (self.x - (35 * 2), self.y)]
        self.direction = direction

    def make_blocks(self):
        for i in self.blocks:
            block = pygame.draw.rect(screen, (98, 122, 241), Rect(i[0], i[1], cell_size, cell_size))


fruit = Fruit(pygame.image.load("Graphics/apple.png").convert_alpha())
snake = Snake("right")
restart = False


def background_squares(x, y, rect):
    start = 1
    stop = 490
    step = 35

    # 14 X 14columns
    # odd rows = start = col 1
    # odd rows ---> colored squares = 7
    while y <= 455:  # row sequence one
        for i in range(start - 1, stop + 1, step):  # complicated way of saying range(7) ---> total steps = 7
            pygame.draw.rect(screen, (GREEN), rect)
            rect = Rect(x, y, 35, 35)
            x += 70
            pygame.draw.rect(screen, (GREEN), rect)
        y += 70
        x = 0

    # even rows = start = col 2
    # odd rows ---> colored squares = 6
    x = 35
    y = 35
    while y <= 455:  # row_sequence2
        for i in range(7):
            pygame.draw.rect(screen, (GREEN), rect)
            rect = Rect(x, y, 35, 35)
            x += 70
            pygame.draw.rect(screen, (GREEN), rect)
        y += 70
        x = 35


if restart:
    restart = False
    game_active = True
    game_over = False
    score = 0

    fruit = Fruit(pygame.image.load("Graphics/apple.png").convert_alpha())
    snake = Snake("right")


while True and not restart:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                if game_over:
                    restart = True

                if not game_over:
                    game_active = True
                    snake.make_blocks()

        if game_active:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and snake.direction != "down":
                    snake.direction = "up"

                elif event.key == pygame.K_RIGHT and snake.direction != "left":
                    snake.direction = "right"


                elif event.key == pygame.K_DOWN and snake.direction != "up":
                    snake.direction = "down"


                elif event.key == pygame.K_LEFT and snake.direction != "right":
                    snake.direction = "left"

    if game_active:

        # background
        pygame.draw.rect(screen, (OTHER_GREEN), rect_2)
        background_squares(rect_x, rect_y, rect_1)

        if snake.direction == "up":
            snake.y -= 35
        elif snake.direction == "right":
            snake.x += 35
        elif snake.direction == "down":
            snake.y += 35
        elif snake.direction == "left":
            snake.x -= 35

        if snake.x > 490 - cell_size or snake.x < 0 or snake.y > 490 - cell_size or snake.y < 0:
            game_active = False
            game_over = True

        snake.blocks.insert(0, (snake.x, snake.y))
        if fruit.rect.collidepoint((snake.blocks[0])):
            fruit_pos = fruit.pos(snake.blocks)
            fruit.rect = Rect(fruit_pos[0], fruit_pos[1], cell_size, cell_size)
            score += 1
        else:
            del snake.blocks[-1]

        # score
        score_text = text.render(f"{score}", True, APPLE_RED)
        score_rect = Rect(0, 0, cell_size, cell_size)
        screen.blit(score_text, score_rect)

        j = 0
        for i in snake.blocks:
            block_rect = Rect(i[0], i[1], cell_size, cell_size)
            block = pygame.draw.rect(screen, (SNAKE_BLUE), block_rect)
            j += 1
            if j > 1:
                if block_rect == Rect(snake.x, snake.y, cell_size, cell_size):
                    game_over = True
                    game_active = False

        fruit.place_fruit()

    else:
        screen.fill(OTHER_GREEN)
        word = [
            Rect(cell_size * 1, 4 * cell_size, cell_size, cell_size),
            Rect(cell_size * 2, 4 * cell_size, cell_size, cell_size),
            Rect(cell_size * 1, 5 * cell_size, cell_size, cell_size),
            Rect(cell_size * 2, 6 * cell_size, cell_size, cell_size),
            Rect(cell_size * 2, 7 * cell_size, cell_size, cell_size),
            Rect(cell_size * 1, 7 * cell_size, cell_size, cell_size),
        ]
        for test in word:
            pygame.draw.rect(screen, (SNAKE_BLUE), test)
        screen.blit(title_text1, title_rect1)
        screen.blit(title_text2, title_rect2)

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    restart = True
            score_text = text.render(f"Score: {score}", True, APPLE_RED)
            score_rect = Rect(cell_size * 1, 8 * cell_size, cell_size, cell_size)
            screen.blit(score_text, score_rect)

        else:
            screen.blit(start_text, start_rect)

    pygame.display.update()
    fps.tick(9)
