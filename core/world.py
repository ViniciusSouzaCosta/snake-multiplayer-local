import random

from core.config import GRID_WIDTH, GRID_HEIGHT
from core.commands import Command, Direction
from core.entities import Snake, Food, Position


class World:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        self.snake = Snake(start_x, start_y)
        self.food = self.create_food()

        self.score = 0
        self.game_over = False

    def create_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            position = Position(x, y)

            if not self.snake.occupies(position):
                return Food(position)

    def handle_command(self, command):
        if command == Command.MOVE_UP:
            self.snake.change_direction(Direction.UP)
        elif command == Command.MOVE_DOWN:
            self.snake.change_direction(Direction.DOWN)
        elif command == Command.MOVE_LEFT:
            self.snake.change_direction(Direction.LEFT)
        elif command == Command.MOVE_RIGHT:
            self.snake.change_direction(Direction.RIGHT)
        elif command == Command.RESTART:
            if self.game_over:
                self.reset()

    def update(self):
        if self.game_over:
            return

        self.snake.move()
        self.check_food_collision()
        self.check_wall_collision()
        self.check_self_collision()

    def check_food_collision(self):
        head = self.snake.head()

        if head.x == self.food.position.x and head.y == self.food.position.y:
            self.snake.grow()
            self.score += 1
            self.food = self.create_food()

    def check_wall_collision(self):
        head = self.snake.head()

        if head.x < 0 or head.x >= GRID_WIDTH or head.y < 0 or head.y >= GRID_HEIGHT:
            self.game_over = True

    def check_self_collision(self):
        if self.snake.collides_with_self():
            self.game_over = True
