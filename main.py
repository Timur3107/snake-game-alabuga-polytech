import pygame
import pygame_menu
import random
import os

pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SNAKE_SPEED = 10


# Функция для отрисовки змейки и еды
def draw_block(surface, color, position):
    x, y = position
    pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Функция для создания новой еды
def create_food(snake):
    food = None
    while food is None:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in snake:
            food = position
    return food


# Функция для отрисовки сетки на игровом поле
def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (WINDOW_WIDTH, y))


# Функция для чтения рекорда из файла
def read_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    else:
        return 0


# Функция для записи новрго рекорда в файл
def write_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


# Главная функция игрового цикла
def run_game():
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Змейка')

    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food = create_food(snake)

    direction = RIGHT

    clock = pygame.time.Clock()

    score = 0
    high_score = read_high_score()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_s and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_a and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_d and direction != LEFT:
                    direction = RIGHT

        head = snake[0]
        if head in snake[1:]:
            if score > high_score:
                write_high_score(score)
            return False

        if (head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT):
            if score > high_score:
                write_high_score(score)
            return False

        new_head = (head[0] + direction[0], head[1] + direction[1])
        snake.insert(0, new_head)

        if snake[0] == food:
            food = create_food(snake)
            score += 1
        else:
            snake.pop()

        surface.fill((0, 0, 0))
        draw_grid(surface)
        for segment in snake:
            random_green_color = random.randint(0, 255)
            color = (0, random_green_color, 0)

            draw_block(surface, color, segment)

        draw_block(surface, RED, food)

        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        high_score_text = font.render(f"Прошлый рекорд: {high_score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (WINDOW_WIDTH - high_score_text.get_width() - 10, 10))

        window.blit(surface, (0, 0))
        pygame.display.update()

        clock.tick(SNAKE_SPEED)


# Главное меню
def main_menu():
    menu = pygame_menu.Menu("Змейка", WINDOW_WIDTH, WINDOW_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Snake game. Управление - WASD")
    menu.add.button('Играть', run_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(window)


if __name__ == '__main__':
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    main_menu()
