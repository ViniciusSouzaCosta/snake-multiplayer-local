import pygame as pg

from core import config as C
from core.commands import Command
from core.world import World
from client.controls import InputMapper
from client.renderer import Renderer
from client.menu import Menu


class Game:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Snake Multiplayer - Up to 4 Players")
        
        self.clock = pg.time.Clock()
        self.running = True
        
        self.world = World()
        self.renderer = Renderer(self.screen)
        self.input_mapper = None
        
        # Show menu first
        self.show_menu()
    
    def show_menu(self):
        menu = Menu(self.screen)
        num_players = menu.run()
        
        if num_players > 0:
            self.world.initialize(num_players)
            self.input_mapper = InputMapper(num_players)
        else:
            self.running = False
    
    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            
            self.clock.tick(C.FPS)
        
        pg.quit()
    
    def process_input(self):
        if self.input_mapper:
            commands = self.input_mapper.get_commands()
            
            for command in commands:
                if command == Command.QUIT:
                    self.running = False
                else:
                    self.world.handle_command(command)
    
    def update(self):
        self.world.update()
    
    def render(self):
        self.renderer.draw(self.world)