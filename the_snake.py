from random import randint

import pygame as pg

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=(0, 0), body_color=DEFAULT_COLOR) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Базовый метод отрисовки объекта.
        Переопределяется в классах наследниках.
        """
        pass


class Snake(GameObject):
    """Клаcc описсывающий змейку на игровом поле."""

    def __init__(self) -> None:
        super().__init__()
        self.reset()

    def start_position(self) -> tuple[int, int]:
        """Вычисляет стартовое положение змейки на игром поле."""
        return (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE,
        )

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущее положение головы змейки на игровом поле."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Сбрасывает длинну и положение змейки в начальное.
        Отрисовывает старую змейку в цвет фона.
        """
        self.lenght = 1
        self.position = self.start_position()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def move(self) -> None:
        """Логика движении змейки на игровом поле."""
        head_position = self.get_head_position()
        new_head_position_x = head_position[0] + self.direction[0] * GRID_SIZE
        new_head_position_y = head_position[1] + self.direction[1] * GRID_SIZE

        if new_head_position_x >= SCREEN_WIDTH:
            new_head_position_x -= SCREEN_WIDTH
        elif new_head_position_x < 0:
            new_head_position_x += SCREEN_WIDTH
        elif new_head_position_y >= SCREEN_HEIGHT:
            new_head_position_y -= SCREEN_HEIGHT
        elif new_head_position_y < 0:
            new_head_position_y += SCREEN_HEIGHT
        new_head_position = (
            new_head_position_x,
            new_head_position_y,
        )
        self.positions.insert(0, new_head_position)

    def loose_draw(self) -> None:
        """Отрисовка змейки в цвет фона при проигрыше."""
        for position in self.positions:
            current_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, current_rect)

    def draw(self) -> None:
        """Отрисовка змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Клаcc описсывающий яблоко на игровом поле."""

    def __init__(self) -> None:
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Возвращает рандомную координату положения яблока."""
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE,
        )

    def draw(self) -> None:
        """Отрисовка яблока на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def main() -> None:
    """Основная логика игры."""
    # Инициализация pg:
    pg.init()
    apple = Apple()
    snake = Snake()
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.lenght += 1
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
        else:
            snake.last = snake.positions.pop()
        if snake.get_head_position() in snake.positions[1:]:
            snake.loose_draw()
            snake.reset()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
