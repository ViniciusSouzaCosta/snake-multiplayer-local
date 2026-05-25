import pygame as pg

from core import config as C
from core.commands import PLAYER_COLORS


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("consolas", 24)
        self.big_font = pg.font.SysFont("consolas", 54)
        self.small_font = pg.font.SysFont("consolas", 18)

    def draw(self, world):
        self.screen.fill(C.BACKGROUND_COLOR)
        
        # Don't draw gameplay if game hasn't started
        if world.num_players == 0:
            return
        
        self.draw_grid()
        self.draw_foods(world)
        self.draw_snakes(world.snakes)
        self.draw_scores(world.snakes)
        
        if world.game_over:
            self.draw_game_over(world.winner, world.snakes)
        
        pg.display.flip()

    def draw_grid(self):
        for x in range(0, C.WIDTH, C.CELL_SIZE):
            pg.draw.line(self.screen, C.GRID_COLOR, (x, 0), (x, C.HEIGHT))
        
        for y in range(0, C.HEIGHT, C.CELL_SIZE):
            pg.draw.line(self.screen, C.GRID_COLOR, (0, y), (C.WIDTH, y))

    def draw_snakes(self, snakes):
        for snake in snakes:
            if not snake.is_alive():
                continue
                
            colors = PLAYER_COLORS.get(snake.player_id, PLAYER_COLORS[1])
            
            for index, part in enumerate(snake.body):
                rect = pg.Rect(
                    part.x * C.CELL_SIZE,
                    part.y * C.CELL_SIZE,
                    C.CELL_SIZE,
                    C.CELL_SIZE
                )
                
                if index == 0:
                    color = colors["head"]
                else:
                    color = colors["body"]
                
                pg.draw.rect(self.screen, color, rect)
                pg.draw.rect(self.screen, C.BACKGROUND_COLOR, rect, 1)

    def draw_foods(self, world):
        for food in world.foods:
            rect = pg.Rect(
                food.position.x * C.CELL_SIZE,
                food.position.y * C.CELL_SIZE,
                C.CELL_SIZE,
                C.CELL_SIZE
            )
            pg.draw.rect(self.screen, C.FOOD_COLOR, rect)

    def draw_scores(self, snakes):
        # Draw scoreboard in top-left corner
        y_offset = 15
        for snake in snakes:
            color = PLAYER_COLORS.get(snake.player_id, PLAYER_COLORS[1])["body"]
            status = "✓" if snake.is_alive() else "✗"
            text = self.font.render(f"P{snake.player_id} [{status}]: {snake.score}", True, color)
            self.screen.blit(text, (20, y_offset))
            y_offset += 30

    def draw_game_over(self, winner, snakes):
        overlay = pg.Surface((C.WIDTH, C.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if winner:
            winner_color = PLAYER_COLORS.get(winner, PLAYER_COLORS[1])["body"]
            title = self.big_font.render(f"PLAYER {winner} WINS!", True, winner_color)
        else:
            title = self.big_font.render("GAME OVER - TIE!", True, C.GAME_OVER_COLOR)
        
        # Get final scores
        final_scores = [(s.player_id, s.score, s.is_alive()) for s in snakes]
        final_scores.sort(key=lambda x: x[1], reverse=True)
        
        restart_text = self.font.render("Press ENTER to restart", True, C.TEXT_COLOR)
        quit_text = self.font.render("Press ESC to quit", True, C.TEXT_COLOR)
        
        # Center everything
        title_rect = title.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 - 120))
        self.screen.blit(title, title_rect)
        
        # Draw final scores
        score_y = C.HEIGHT // 2 - 40
        for player_id, score, alive in final_scores[:4]:
            color = PLAYER_COLORS.get(player_id, PLAYER_COLORS[1])["body"]
            status = "ALIVE" if alive else "DEAD"
            score_text = self.small_font.render(f"Player {player_id} ({status}): {score}", True, color)
            score_rect = score_text.get_rect(center=(C.WIDTH // 2, score_y))
            self.screen.blit(score_text, score_rect)
            score_y += 30
        
        restart_rect = restart_text.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 + 40))
        quit_rect = quit_text.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 + 80))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)