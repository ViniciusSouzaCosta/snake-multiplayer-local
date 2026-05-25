import pygame as pg

from core.commands import Command


class InputMapper:
    def get_commands(self):
        commands = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                commands.append(Command.QUIT)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    commands.append(Command.QUIT)

                elif event.key == pg.K_RETURN:
                    commands.append(Command.RESTART)

                elif event.key == pg.K_UP or event.key == pg.K_w:
                    commands.append(Command.MOVE_UP)

                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    commands.append(Command.MOVE_DOWN)

                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    commands.append(Command.MOVE_LEFT)

                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    commands.append(Command.MOVE_RIGHT)

        return commands
