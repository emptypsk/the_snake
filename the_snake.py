from random import choice
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
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет поля
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет яблока
COLOR_RED = (255, 0, 0)
# Стартовый цвет змейки
SNAKE_COLOR = (153, 153, 0)
# Константа для граничного значения длины змейки для выбора цвета
LENGTH_THRESHOLD = 5
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
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для представления игровых объектов"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 color=None):
        self.position = position
        self.body_color = color

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError('Метод draw() должен быть переопределен в'
                                  + 'дочерних классах. Класс: {}, Метод: {}'
                                  .format(self.__class__.__name__, "draw"))

    def rect(self, position):
        """Отрисовывает ячейки и их границы"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        # Отрисовка границы ячейки
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        return rect


class Apple(GameObject):
    """Класс для представления яблока на игровом поле."""

    def __init__(self):
        super().__init__(color=COLOR_RED)

    def randomize_position(self, snake):
        """Устанавливает случайное положение яблока на игровом поле."""
        available_positions = [(x, y) for x in range(GRID_WIDTH) for y in
                               range(GRID_HEIGHT) if (x, y) not in
                               snake.positions]
        if not available_positions:
            # Если нет доступных позиций, предпринимаем действия
            self.handle_no_available_positions()
            return
        x, y = choice(available_positions)
        self.position = (x * GRID_SIZE, y * GRID_SIZE)

    def handle_no_available_positions(self):
        """Завершаем игру, если закончились клеточки на поле."""
        print('Вы победили! Вы заняли все ячейки!')
        pygame.quit()
        raise SystemExit

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        # Используем метод rect из родительского класса
        rect = self.rect(self.position)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.body_color, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки на игровом поле."""

    def __init__(self,):
        super().__init__(color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        opposite_directions = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if new_direction and new_direction != opposite_directions.get(
                self.direction):
            self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки в игре."""
        head_position = self.get_head_position()
        x, y = self.direction
        new_head_position = ((head_position[0] + (x * GRID_SIZE)) %
                             SCREEN_WIDTH, (head_position[1] + (y * GRID_SIZE))
                             % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.speed = 5
        self.tail = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def get_snake_color(self):
        """Возвращает цвет змейки в зависимости от её длины."""
        return (self.body_color if self.length < LENGTH_THRESHOLD
                else SNAKE_COLOR_DICT[(self.length // 5) * 5])

    def draw(self):
        """Отрисовывает змейку на игровой поверхности."""
        new_head_rect = self.rect(self.get_head_position())
        # Используем метод для получения цвета
        color = self.get_snake_color()
        pygame.draw.rect(screen, color, new_head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, new_head_rect, 1)
        # Удаляем последний сегмент только если змейка не съела яблоко
        self.tail = (
            self.positions.pop() if len(self.positions) > self.length else None
        )
        # Проверяем, есть ли след для стирания и отрисовываем его
        if self.tail:
            rect = self.rect(self.tail)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def increase_speed(self):
        """Увеличивает скорость змейки когда её длина больше 5."""
        if self.length // 2 > LENGTH_THRESHOLD:
            self.speed = self.length // 2


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для изменения направления
    движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
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
        # Движение змейки
        snake.move()
        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
        # Отрисовка змейки
        snake.draw()
        # Увеличение скорости змейки при необходимости
        snake.increase_speed()
        # Отрисовка яблока
        apple.draw()
        # Обновление экрана
        pygame.display.update()
        # Ведение счёта и скорости на заголовке окна
        pygame.display.set_caption(
            f'Змейка. Текущий счёт ={snake.length} Скорость: {snake.speed}')
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
