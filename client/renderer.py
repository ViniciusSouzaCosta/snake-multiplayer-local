import pygame as pg

from core import config as C


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("consolas", 24)
        self.big_font = pg.font.SysFont("consolas", 54)

    def draw(self, world):
        self.screen.fill(C.BACKGROUND_COLOR)

        self.draw_grid()
        self.draw_food(world.food)
        self.draw_snake(world.snake)
        self.draw_score(world.score)

        if world.game_over:
            self.draw_game_over(world.score)

        pg.display.flip()

    def draw_grid(self):
        for x in range(0, C.WIDTH, C.CELL_SIZE):
            pg.draw.line(self.screen, C.GRID_COLOR, (x, 0), (x, C.HEIGHT))

        for y in range(0, C.HEIGHT, C.CELL_SIZE):
            pg.draw.line(self.screen, C.GRID_COLOR, (0, y), (C.WIDTH, y))

    def draw_snake(self, snake):
        for index, part in enumerate(snake.body):
            rect = pg.Rect(
                part.x * C.CELL_SIZE,
                part.y * C.CELL_SIZE,
                C.CELL_SIZE,
                C.CELL_SIZE
            )

            if index == 0:
                color = C.SNAKE_HEAD_COLOR
            else:
                color = C.SNAKE_COLOR

            pg.draw.rect(self.screen, color, rect)
            pg.draw.rect(self.screen, C.BACKGROUND_COLOR, rect, 1)

    def draw_food(self, food):
        rect = pg.Rect(
            food.position.x * C.CELL_SIZE,
            food.position.y * C.CELL_SIZE,
            C.CELL_SIZE,
            C.CELL_SIZE
        )

        pg.draw.rect(self.screen, C.FOOD_COLOR, rect)

    def draw_score(self, score):
        text = self.font.render(f"Score: {score}", True, C.TEXT_COLOR)
        self.screen.blit(text, (20, 15))

    def draw_game_over(self, score):
        overlay = pg.Surface((C.WIDTH, C.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("GAME OVER", True, C.GAME_OVER_COLOR)
        score_text = self.font.render(f"Score final: {score}", True, C.TEXT_COLOR)
        restart_text = self.font.render("Pressione ENTER para reiniciar", True, C.TEXT_COLOR)
        quit_text = self.font.render("Pressione ESC para sair", True, C.TEXT_COLOR)

        self.screen.blit(title, (C.WIDTH // 2 - title.get_width() // 2, C.HEIGHT // 2 - 110))
        self.screen.blit(score_text, (C.WIDTH // 2 - score_text.get_width() // 2, C.HEIGHT // 2 - 35))
        self.screen.blit(restart_text, (C.WIDTH // 2 - restart_text.get_width() // 2, C.HEIGHT // 2 + 15))
        self.screen.blit(quit_text, (C.WIDTH // 2 - quit_text.get_width() // 2, C.HEIGHT // 2 + 55))
