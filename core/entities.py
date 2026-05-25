from dataclasses import dataclass
from core.commands import Direction


@dataclass
class Position:
    x: int
    y: int


class Snake:
    def __init__(self, start_x, start_y, player_id, start_direction=Direction.RIGHT):
        self.player_id = player_id
        
        # Garantir que a cobra comece dentro dos limites do grid com espaço suficiente
        start_x = max(3, min(start_x, GRID_WIDTH - 4))
        start_y = max(3, min(start_y, GRID_HEIGHT - 4))
        
        # Criar o corpo baseado na direção inicial
        self.body = []
        if start_direction == Direction.RIGHT:
            self.body = [
                Position(start_x, start_y),
                Position(start_x - 1, start_y),
                Position(start_x - 2, start_y)
            ]
        elif start_direction == Direction.LEFT:
            self.body = [
                Position(start_x, start_y),
                Position(start_x + 1, start_y),
                Position(start_x + 2, start_y)
            ]
        elif start_direction == Direction.DOWN:
            self.body = [
                Position(start_x, start_y),
                Position(start_x, start_y - 1),
                Position(start_x, start_y - 2)
            ]
        else:  # Direction.UP
            self.body = [
                Position(start_x, start_y),
                Position(start_x, start_y + 1),
                Position(start_x, start_y + 2)
            ]
        
        self.direction = start_direction
        self.next_direction = start_direction
        self.grow_next = False
        self.alive = True
        self.score = 0

    def change_direction(self, direction):
        if not self.alive:
            return
            
        if self.direction == Direction.UP and direction == Direction.DOWN:
            return
        if self.direction == Direction.DOWN and direction == Direction.UP:
            return
        if self.direction == Direction.LEFT and direction == Direction.RIGHT:
            return
        if self.direction == Direction.RIGHT and direction == Direction.LEFT:
            return

        self.next_direction = direction

    def move(self):
        if not self.alive:
            return
            
        self.direction = self.next_direction
        head = self.body[0]

        if self.direction == Direction.UP:
            new_head = Position(head.x, head.y - 1)
        elif self.direction == Direction.DOWN:
            new_head = Position(head.x, head.y + 1)
        elif self.direction == Direction.LEFT:
            new_head = Position(head.x - 1, head.y)
        else:
            new_head = Position(head.x + 1, head.y)

        self.body.insert(0, new_head)

        if self.grow_next:
            self.grow_next = False
        else:
            self.body.pop()

    def grow(self):
        if self.alive:
            self.grow_next = True
            self.score += 1

    def head(self):
        return self.body[0] if self.body else None

    def collides_with_self(self):
        head = self.head()
        if not head:
            return False

        for part in self.body[1:]:
            if head.x == part.x and head.y == part.y:
                return True

        return False

    def occupies(self, position):
        for part in self.body:
            if part.x == position.x and part.y == position.y:
                return True

        return False
    
    def kill(self):
        self.alive = False
    
    def is_alive(self):
        return self.alive


@dataclass
class Food:
    position: Position


# Importar GRID_WIDTH e GRID_HEIGHT para usar na validação
from core.config import GRID_WIDTH, GRID_HEIGHT