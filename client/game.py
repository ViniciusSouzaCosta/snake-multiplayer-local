import pygame as pg

from core import config as C
from core.commands import Command
from core.world import World
from client.controls import InputMapper
from client.renderer import Renderer


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Snake Single Player")

        self.clock = pg.time.Clock()
        self.running = True

        self.world = World()
        self.input_mapper = InputMapper()
        self.renderer = Renderer(self.screen)

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            self.clock.tick(C.FPS)

        pg.quit()

    def process_input(self):
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
