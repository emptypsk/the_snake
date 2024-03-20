from random import choice, randint
import time
import pygame

# Инициализация PyGame.
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

# Цвет поля - чёрный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)
# Цвет яблока.
APPLE_COLOR = (255, 0, 0)
# Цвет Анти-Яблока.
BAD_APPLE_COLLOR = (255, 0, 255)
# Стартовый цвет змейки.
SNAKE_COLOR = (153, 153, 0)
# Словарь цветов змейки в зависимости от очков.
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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для представления игровых объектов."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = None

    def draw(self):
        """
        Абстрактный метод, который предназначен для
        переопределения в дочерних классах.
        """
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


class BadApple(GameObject):
    """Класс для представления плохого яблока на игровом поле."""

    def __init__(self):
        super().__init__()
        self.body_color = BAD_APPLE_COLLOR
        self.is_visible = False

    def randomize_position(self):
        """Устанавливает случайное положение плохого яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает плохое яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        self.is_visible = True


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.speed = 5
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def update_length(self):
        """Обновляет длину змейки после поедания плохого яблока."""
        self.last = self.positions.pop()

    def move(self):
        """Обновляет позицию змейки в игре."""
        head_position = self.get_head_position()
        x, y = self.direction
        new_head_position = ((head_position[0] + (x * GRID_SIZE)),
                             (head_position[1] + (y * GRID_SIZE)))

        # Проверка на столкновение с границами поля.
        if (new_head_position[0] < 0
                or new_head_position[0] >= SCREEN_WIDTH
                or new_head_position[1] < 0
                or new_head_position[1] >= SCREEN_HEIGHT):
            self.reset()
            return

        if new_head_position in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def increase_speed(self):
        """Увеличивает скорость змейки от её длины"""
        if self.length // 2 > 5:
            self.speed = self.length // 2

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        global BOARD_BACKGROUND_COLOR
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        self.speed = 5
        # При поражении делаем паузу, красим экран и возвращаем прежний вид.
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


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления
    движения змейки.
    """
    # Проверяем события клавиатуры только раз в несколько кадров
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


def check_apple(
        apple, snake, bad_apple,
        bad_apple_two, bad_apple_three):
    """Проверка позиции яблока."""
    if apple.position in snake.position:
        apple.randomize_position()
    if apple.position == bad_apple.position:
        apple.randomize_position()
    if apple.position == bad_apple_two.position:
        apple.randomize_position()
    if apple.position == bad_apple_three.position:
        apple.randomize_position()
    return apple.draw()


def check_bad_apples(apple, snake, bad_apple, bad_apple_two, bad_apple_three):
    """Настройка видимости плохих яблок."""
    # Проверяем где появилось плохое яблоко.
    if bad_apple.position == apple.position:
        bad_apple.randomize_position()
        bad_apple.draw()
    if snake.length <= 5:
        bad_apple_two.is_visible = False
        bad_apple_three.is_visible = False
    if 10 > snake.length > 5:
        if bad_apple_two.is_visible is False:
            bad_apple_two.randomize_position()
        bad_apple_three.is_visible = False
        bad_apple_two.draw()
    elif snake.length >= 10:
        if bad_apple_three.is_visible is False:
            bad_apple_three.randomize_position()
        bad_apple_two.draw()
        bad_apple_three.draw()
    if bad_apple.is_visible is False:
        bad_apple.randomize_position()
    bad_apple.draw()


def check_bad_apples_consume(snake, bad_apple, bad_apple_two, bad_apple_three):
    """Проверка, съела ли змейка плохое яблоко."""
    if snake.length == 1:
        if (snake.get_head_position() == bad_apple.position
                or snake.get_head_position() == bad_apple_two.position
                or snake.get_head_position() == bad_apple_three.position):
            snake.reset()
    else:
        if snake.get_head_position() == bad_apple.position:
            snake.length -= 1
            snake.update_length()
            bad_apple.randomize_position()
        elif snake.get_head_position() == bad_apple_two.position:
            if bad_apple_two.is_visible is True:
                snake.length -= 1
                snake.update_length()
                bad_apple_two.randomize_position()
                bad_apple_two.draw()
        elif snake.get_head_position() == bad_apple_three.position:
            if bad_apple_three.is_visible is True:
                snake.length -= 1
                snake.update_length()
                bad_apple_three.randomize_position()
                bad_apple_three.draw()


def draw_borders():
    """Отрисовка границ экрана."""
    border_thickness = 4
    # Верхняя граница.
    pygame.draw.rect(
        screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, border_thickness))
    # Левая граница.
    pygame.draw.rect(
        screen, BORDER_COLOR, (0, 0, border_thickness, SCREEN_HEIGHT))
    # Нижняя граница.
    pygame.draw.rect(
        screen, BORDER_COLOR, (0, SCREEN_HEIGHT - border_thickness,
                               SCREEN_WIDTH, border_thickness))
    # Правая граница.
    pygame.draw.rect(
        screen, BORDER_COLOR, (SCREEN_WIDTH - border_thickness,
                               0, border_thickness, SCREEN_HEIGHT))


def main():
    """Основная функция игры."""
    # Создание экземпляров классов.
    snake, apple, bad_apple, bad_apple_two, bad_apple_three = (
        Snake(), Apple(), BadApple(), BadApple(), BadApple())
    # Начальный рекорд
    highest_score = 0
    # Основной игровой цикл.
    while True:
        # Обработка событий клавиш.
        handle_keys(snake)
        # Отрисовка поля
        screen.fill(BOARD_BACKGROUND_COLOR)
        """Настройка змейки"""
        # Обновление направления движения змейки.
        snake.update_direction()
        # Движение змейки
        snake.move()
        # Проверка, съела ли змейка яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Проверка столкновения змейки с собой.
        if snake.check_collision():
            snake.reset()
        # Изменение скорости и прорисовка змейки
        snake.increase_speed()
        snake.draw()

        check_apple(apple, snake, bad_apple, bad_apple_two, bad_apple_three)
        check_bad_apples(apple, snake, bad_apple,
                         bad_apple_two, bad_apple_three)
        check_bad_apples_consume(snake, bad_apple, bad_apple_two,
                                 bad_apple_three)
        draw_borders()
        pygame.display.update()
        # Индикация счёта, рейтинга и скорости в заголовке окна.
        if snake.length > highest_score:
            highest_score = snake.length
        pygame.display.set_caption(
            f'Змейка. Текущий счёт = {snake.length}.'
            f' Текущая скорость = {snake.speed}'
            f' Рекорд {highest_score}')
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
