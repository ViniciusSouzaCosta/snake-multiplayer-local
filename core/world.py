import random

from core.config import GRID_WIDTH, GRID_HEIGHT
from core.commands import Command, Direction
from core.entities import Snake, Food, Position


class World:
    def __init__(self):
        self.num_players = 0
        self.snakes = []
        self.foods = []  # Multiple foods for multiplayer
        self.score = 0
        self.game_over = False
        self.winner = None
    
    def initialize(self, num_players):
        """Initialize the world with specified number of players"""
        self.num_players = num_players
        self.snakes = []
        self.foods = []
        self.game_over = False
        self.winner = None
        
        # Starting positions for up to 4 players (corners of the map)
        start_positions = [
            (GRID_WIDTH // 4, GRID_HEIGHT // 2),           # Left-center
            (3 * GRID_WIDTH // 4, GRID_HEIGHT // 2),       # Right-center
            (GRID_WIDTH // 2, GRID_HEIGHT // 4),           # Top-center
            (GRID_WIDTH // 2, 3 * GRID_HEIGHT // 4)        # Bottom-center
        ]
        
        # Directions facing towards center for each player
        start_directions = [
            Direction.RIGHT,   # Left player goes right
            Direction.LEFT,    # Right player goes left
            Direction.DOWN,    # Top player goes down
            Direction.UP       # Bottom player goes up
        ]
        
        for i in range(num_players):
            start_x, start_y = start_positions[i]
            direction = start_directions[i]
            snake = Snake(start_x, start_y, i + 1, direction)
            self.snakes.append(snake)
        
        # Create initial food (one per player)
        for _ in range(num_players):
            self.create_food()
    
    def reset(self):
        """Reset the game with current number of players"""
        if self.num_players > 0:
            self.initialize(self.num_players)
    
    def create_food(self):
        """Create a new food at a position not occupied by any snake"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = Position(x, y)
            
            # Check if position is occupied by any snake
            occupied = False
            for snake in self.snakes:
                if snake.occupies(position):
                    occupied = True
                    break
            
            # Check if position already has food
            for food in self.foods:
                if food.position.x == x and food.position.y == y:
                    occupied = True
                    break
            
            if not occupied:
                self.foods.append(Food(position))
                return

    def handle_command(self, command, player_index=None):
        """Handle commands with optional player specification"""
        if command == Command.RESTART:
            if self.game_over:
                self.reset()
            return
        
        # Map commands to player-specific moves
        player_moves = {
            Command.PLAYER1_UP: (0, Direction.UP),
            Command.PLAYER1_DOWN: (0, Direction.DOWN),
            Command.PLAYER1_LEFT: (0, Direction.LEFT),
            Command.PLAYER1_RIGHT: (0, Direction.RIGHT),
            
            Command.PLAYER2_UP: (1, Direction.UP),
            Command.PLAYER2_DOWN: (1, Direction.DOWN),
            Command.PLAYER2_LEFT: (1, Direction.LEFT),
            Command.PLAYER2_RIGHT: (1, Direction.RIGHT),
            
            Command.PLAYER3_UP: (2, Direction.UP),
            Command.PLAYER3_DOWN: (2, Direction.DOWN),
            Command.PLAYER3_LEFT: (2, Direction.LEFT),
            Command.PLAYER3_RIGHT: (2, Direction.RIGHT),
            
            Command.PLAYER4_UP: (3, Direction.UP),
            Command.PLAYER4_DOWN: (3, Direction.DOWN),
            Command.PLAYER4_LEFT: (3, Direction.LEFT),
            Command.PLAYER4_RIGHT: (3, Direction.RIGHT),
        }
        
        if command in player_moves:
            idx, direction = player_moves[command]
            if idx < len(self.snakes):
                self.snakes[idx].change_direction(direction)

    def update(self):
        if self.game_over:
            return
        
        # Move all alive snakes
        for snake in self.snakes:
            if snake.is_alive():
                snake.move()
        
        # Check collisions for all snakes
        self.check_collisions()
        
        # Check food collisions
        self.check_food_collisions()
        
        # Check if game is over (only one snake alive or no snakes alive)
        alive_snakes = [s for s in self.snakes if s.is_alive()]
        if len(alive_snakes) <= 1:
            self.game_over = True
            if len(alive_snakes) == 1:
                self.winner = alive_snakes[0].player_id
            else:
                self.winner = None

    def check_collisions(self):
        """Check all collision types for all snakes"""
        alive_snakes = [s for s in self.snakes if s.is_alive()]
        
        for snake in alive_snakes:
            head = snake.head()
            if not head:
                continue
            
            # Wall collision
            if (head.x < 0 or head.x >= GRID_WIDTH or 
                head.y < 0 or head.y >= GRID_HEIGHT):
                snake.kill()
                continue
            
            # Self collision
            if snake.collides_with_self():
                snake.kill()
                continue
            
            # Collision with other snakes
            for other_snake in self.snakes:
                if other_snake == snake:
                    continue
                
                # Head collision with other snake's body
                if other_snake.occupies(head):
                    snake.kill()
                    break
                
                # Head-to-head collision
                other_head = other_snake.head()
                if other_head and head.x == other_head.x and head.y == other_head.y:
                    snake.kill()
                    other_snake.kill()
                    break

    def check_food_collisions(self):
        """Check if any snake's head collides with food"""
        foods_to_remove = []
        
        for snake in self.snakes:
            if not snake.is_alive():
                continue
                
            head = snake.head()
            if not head:
                continue
            
            for food in self.foods:
                if head.x == food.position.x and head.y == food.position.y:
                    snake.grow()
                    foods_to_remove.append(food)
                    break
        
        # Remove eaten foods and create new ones
        for food in foods_to_remove:
            if food in self.foods:
                self.foods.remove(food)
                self.create_food()
        
        # Ensure we always have at least 2 foods in multiplayer
        while len(self.foods) < 2 and len([s for s in self.snakes if s.is_alive()]) > 1:
            self.create_food()
        while len(self.foods) < 1 and len([s for s in self.snakes if s.is_alive()]) <= 1:
            self.create_food()