import pygame as pg
from core import config as C


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pg.font.SysFont("consolas", 72)
        self.font = pg.font.SysFont("consolas", 36)
        self.small_font = pg.font.SysFont("consolas", 24)
        self.selected_players = None
        self.buttons = []
        
    def run(self):
        """Run the menu and return number of players selected"""
        self.create_buttons()
        
        while True:
            self.handle_events()
            self.draw()
            pg.display.flip()
            
            if self.selected_players is not None:
                return self.selected_players
    
    def create_buttons(self):
        button_width = 200
        button_height = 60
        start_y = C.HEIGHT // 2 - 50
        
        self.buttons = []
        for i in range(4):
            button = {
                "num_players": i + 1,
                "rect": pg.Rect(
                    C.WIDTH // 2 - button_width // 2,
                    start_y + i * 80,
                    button_width,
                    button_height
                ),
                "hover": False
            }
            self.buttons.append(button)
    
    def handle_events(self):
        mouse_pos = pg.mouse.get_pos()
        
        for button in self.buttons:
            button["hover"] = button["rect"].collidepoint(mouse_pos)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.selected_players = 0
                return
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.selected_players = 0
                    return
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for button in self.buttons:
                        if button["hover"]:
                            self.selected_players = button["num_players"]
                            return
    
    def draw(self):
        self.screen.fill(C.MENU_BG_COLOR)
        
        # Draw title
        title = self.font_title.render("SNAKE MULTIPLAYER", True, C.MENU_TITLE_COLOR)
        title_rect = title.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.small_font.render("Select number of players:", True, C.MENU_TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 - 100))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            color = C.MENU_BUTTON_HOVER_COLOR if button["hover"] else C.MENU_BUTTON_COLOR
            pg.draw.rect(self.screen, color, button["rect"])
            pg.draw.rect(self.screen, C.MENU_TEXT_COLOR, button["rect"], 2)
            
            text = self.font.render(f"{button['num_players']} Players", True, C.MENU_TEXT_COLOR)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        # Draw controls info
        controls_y = C.HEIGHT - 140
        controls_text = [
            "Controles / Cores:",
            "P1 (Azul):      WASD / Controle 1",
            "P2 (Vermelho):  ⬆⬅⬇⮕ / Controle 2",
            "P3 (Verde):     IJKL / Controle 3",
            "P4 (Laranja):   TFGH / Controle 4"
        ]
        
        y_offset = 0
        for text in controls_text:
            rendered = self.small_font.render(text, True, C.MENU_TEXT_COLOR)
            self.screen.blit(rendered, (20, controls_y + y_offset))
            y_offset += 25