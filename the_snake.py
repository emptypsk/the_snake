from random import choice, randint
import time
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (153, 153, 0)
# Словарь цветов змейки в зависимости от очков
SNAKE_COLOR_DICT = {5: (204, 204, 0),
                    10: (255, 255, 0),
                    15: (255, 255, 51),
                    20: (255, 255, 102),
                    25: (255, 255, 153),
                    30: (255, 255, 204),
                    35: (128, 255, 0),
                    40: (0, 255, 0),
                    45: (0, 255, 255),
                    50: (255, 0, 255)
                    }
# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для представления игровых объектов"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = None

    def draw(self):
        """Отрисовывает игровой объект."""
        pass


class Apple(GameObject):
    """Класс для представления яблока на игровом поле."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки в игре."""
        head_position = self.get_head_position()
        x, y = self.direction
        new_head_position = ((head_position[0] + (x * GRID_SIZE)) %
                             SCREEN_WIDTH,
                             (head_position[1] + (y * GRID_SIZE)) %
                             SCREEN_HEIGHT)

        if new_head_position in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        global SPEED, BOARD_BACKGROUND_COLOR
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        SPEED = 5
        # При поражении делаем паузу, красим экран и возвращаем прежний вид
        BOARD_BACKGROUND_COLOR = (255, 0, 0)
        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()
        time.sleep(2)
        BOARD_BACKGROUND_COLOR = (0, 0, 0)
        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def check_collision(self):
        """Проверяет столкновения змейки с самой собой."""
        return len(self.positions) != len(set(self.positions))

    def draw(self):
        """Отрисовывает змейку на игровой поверхности."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            if self.length < 5:
                pygame.draw.rect(screen, self.body_color, rect)
            else:
                for k, v in SNAKE_COLOR_DICT.items():
                    if int(self.length) >= k:
                        pygame.draw.rect(screen, v, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для изменения направления
    движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:  # Добавляем проверку на
                pygame.quit()                   # нажатие клавиши Esc
                raise SystemExit
        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


def main():
    """Основная функция игры."""
    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    # Основной игровой цикл
    while True:
        # Обработка событий клавиш
        handle_keys(snake)
        global SPEED
        # Обновление направления движения змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Увеличение скорости на 1 единицу за каждые 3 яблока
            if snake.length % 3 == 0 and snake.length != 0:
                SPEED = SPEED + 1

        # Проверка столкновения змейки с собой
        if snake.check_collision():
            snake.reset()

        # Отрисовка змейки и яблока
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()
        # Ведение счета на заголовке окна
        pygame.display.set_caption(
            f'Змейка. Текущий счёт ={snake.length}')
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
