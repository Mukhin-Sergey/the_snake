from random import randint
import pygame

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

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# ** Тут опишите все классы игры. **
class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self):
        """Инициализация объекта игры, создание позиции."""
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = ()

    def draw(self):
        """Метод для отрисовки объекта. Пока не реализован."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока с заданием его цвета и случайной позицией."""
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Случайно изменяет позицию яблока на игровом поле."""
        w = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        h = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (w, h)

    def draw(self):
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализация змейки с ее начальной длиной и положением."""
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Обновляет направление змейки, если оно было изменено."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку по игровому полю."""
        now = self.get_head_position()
        self.last = self.positions[-1]
        new_x = now[0] + self.direction[0] * GRID_SIZE
        new_y = now[1] + self.direction[1] * GRID_SIZE

        new_x = new_x % SCREEN_WIDTH
        new_y = new_y % SCREEN_HEIGHT
        new = (new_x, new_y)
        if len(self.positions) > 2:
            for i in range(2, len(self.positions)):
                if self.positions[i] == new:
                    self.reset()
                    screen.fill(BOARD_BACKGROUND_COLOR)
                    return
        self.positions.insert(0, new)
        if self.length < len(self.positions):
            self.positions.pop()

    def draw(self):
        """Метод для отрисовки всей змейки на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions.clear()
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        t = randint(0, 3)
        if t == 0:
            self.direction = LEFT
        elif t == 1:
            self.direction = DOWN
        elif t == 2:
            self.direction = UP
        else:
            self.direction = RIGHT


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция, выполняющая логику игры."""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        # Устанавливаем скорость игры
        clock.tick(SPEED)

        # Обрабатываем нажатия клавиш
        handle_keys(snake)

        # Двигаем змейку
        snake.move()

        # Проверяем, съела ли змейка яблоко
        if apple.position == snake.positions[0]:
            snake.length += 1
            apple = Apple()  # Создаем новое яблоко

        # Обновляем направление змейки
        snake.update_direction()

        # Отрисовываем яблоко и змейку
        apple.draw()
        snake.draw()

        # Обновляем экран
        pygame.display.update()


if __name__ == '__main__':
    main()
