import random

from core.config import GRID_WIDTH, GRID_HEIGHT
from core.commands import Command, Direction
from core.entities import Snake, Food, Position


class World:
    def __init__(self):
        self.num_players = 0
        self.snakes = []
        self.foods = []
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
        
        # Starting positions for up to 4 players - posições completamente seguras
        # Todas as posições garantem espaço para a cobra de 3 segmentos
        start_positions = [
            (10, GRID_HEIGHT // 2),                    # Left side (x=10)
            (GRID_WIDTH - 10, GRID_HEIGHT // 2),       # Right side (x=width-10)
            (GRID_WIDTH // 2, 10),                     # Top side (y=10)
            (GRID_WIDTH // 2, GRID_HEIGHT - 10)        # Bottom side (y=height-10)
        ]
        
        # Validar e ajustar posições para garantir que estão dentro do grid
        valid_positions = []
        for x, y in start_positions:
            # Garantir que a cobra inteira caiba (3 segmentos)
            # Para cobras que andam para a direita, precisamos de espaço à esquerda
            # Para cobras que andam para a esquerda, precisamos de espaço à direita
            # Para cima, espaço em baixo, etc.
            adjusted_x = max(5, min(GRID_WIDTH - 5, x))
            adjusted_y = max(5, min(GRID_HEIGHT - 5, y))
            valid_positions.append((adjusted_x, adjusted_y))
        
        # Directions facing towards center for each player
        start_directions = [
            Direction.RIGHT,   # Left player goes right
            Direction.LEFT,    # Right player goes left
            Direction.DOWN,    # Top player goes down
            Direction.UP       # Bottom player goes up
        ]
        
        for i in range(num_players):
            start_x, start_y = valid_positions[i]
            direction = start_directions[i]
            
            # Ajustar posição específica baseada na direção para garantir que a cobra não nasça colidindo
            if direction == Direction.RIGHT:
                # Cobra vai para direita, então precisa de espaço à esquerda
                start_x = max(3, start_x)
            elif direction == Direction.LEFT:
                # Cobra vai para esquerda, então precisa de espaço à direita
                start_x = min(GRID_WIDTH - 4, start_x)
            elif direction == Direction.DOWN:
                # Cobra vai para baixo, então precisa de espaço acima
                start_y = max(3, start_y)
            elif direction == Direction.UP:
                # Cobra vai para cima, então precisa de espaço abaixo
                start_y = min(GRID_HEIGHT - 4, start_y)
            
            snake = Snake(start_x, start_y, i + 1, direction)
            self.snakes.append(snake)
        
        # Create initial food (quantidade baseada no número de jogadores)
        initial_food_count = 2 if num_players > 1 else 1
        for _ in range(initial_food_count):
            self.create_food()
    
    def reset(self):
        """Reset the game with current number of players"""
        if self.num_players > 0:
            self.initialize(self.num_players)
    
    def create_food(self):
        """Create a new food at a position not occupied by any snake"""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 2)
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
        
        # Se não encontrar posição depois de muitas tentativas, colocar em qualquer lugar
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = Position(x, y)
                occupied = False
                for snake in self.snakes:
                    if snake.occupies(pos):
                        occupied = True
                        break
                if not occupied:
                    self.foods.append(Food(pos))
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
        
        # Check win condition based on number of players
        self.check_win_condition()
    
    def check_win_condition(self):
        """Check win condition - different for single player vs multiplayer"""
        alive_snakes = [s for s in self.snakes if s.is_alive()]
        
        if self.num_players == 1:
            # Single player mode: win by reaching a target score or maximum size
            # Vence ao atingir tamanho máximo que preenche o grid
            single_snake = self.snakes[0]
            max_size = GRID_WIDTH * GRID_HEIGHT
            
            if len(single_snake.body) >= max_size:
                self.game_over = True
                self.winner = 1
        else:
            # Multiplayer mode: win by being the last alive
            if len(alive_snakes) <= 1:
                self.game_over = True
                if len(alive_snakes) == 1:
                    self.winner = alive_snakes[0].player_id
                else:
                    self.winner = None

    def check_collisions(self):
        """Check all collision types for all snakes"""
        # Primeiro, marcar todas as cobras que colidem com paredes
        for snake in self.snakes:
            if not snake.is_alive():
                continue
                
            head = snake.head()
            if not head:
                continue
            
            # Wall collision
            if (head.x < 0 or head.x >= GRID_WIDTH or 
                head.y < 0 or head.y >= GRID_HEIGHT):
                snake.kill()
        
        # Depois, verificar auto-colisão e colisão entre cobras
        for snake in self.snakes:
            if not snake.is_alive():
                continue
            
            # Self collision
            if snake.collides_with_self():
                snake.kill()
                continue
            
            # Collision with other snakes (apenas para multiplayer)
            if self.num_players > 1:
                for other_snake in self.snakes:
                    if other_snake == snake or not other_snake.is_alive():
                        continue
                    
                    # Head collision with other snake's body
                    head = snake.head()
                    if head and other_snake.occupies(head):
                        snake.kill()
                        break
                    
                    # Head-to-head collision (ambas morrem)
                    other_head = other_snake.head()
                    if head and other_head and head.x == other_head.x and head.y == other_head.y:
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
            
            for food in self.foods[:]:  # Iterar sobre cópia da lista
                if head.x == food.position.x and head.y == food.position.y:
                    snake.grow()
                    foods_to_remove.append(food)
                    break
        
        # Remove eaten foods and create new ones
        for food in foods_to_remove:
            if food in self.foods:
                self.foods.remove(food)
                self.create_food()
        
        # Ensure we always have enough foods based on player count
        if self.num_players == 1:
            while len(self.foods) < 1:
                self.create_food()
        else:
            # Para multiplayer, manter pelo menos 2 comidas se houver mais de 1 jogador vivo
            alive_count = len([s for s in self.snakes if s.is_alive()])
            target_food_count = 2 if alive_count > 1 else 1
            while len(self.foods) < target_food_count:
                self.create_food()