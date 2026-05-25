import pygame as pg

from core.commands import Command


class InputMapper:
    def __init__(self, num_players=1):
        self.num_players = num_players
    
    def get_commands(self):
        commands = []
        
        # Key mappings for different players
        player_mappings = {
            1: {
                pg.K_UP: Command.PLAYER1_UP,
                pg.K_w: Command.PLAYER1_UP,
                pg.K_DOWN: Command.PLAYER1_DOWN,
                pg.K_s: Command.PLAYER1_DOWN,
                pg.K_LEFT: Command.PLAYER1_LEFT,
                pg.K_a: Command.PLAYER1_LEFT,
                pg.K_RIGHT: Command.PLAYER1_RIGHT,
                pg.K_d: Command.PLAYER1_RIGHT,
            },
            2: {
                pg.K_i: Command.PLAYER2_UP,
                pg.K_k: Command.PLAYER2_DOWN,
                pg.K_j: Command.PLAYER2_LEFT,
                pg.K_l: Command.PLAYER2_RIGHT,
            },
            3: {
                pg.K_t: Command.PLAYER3_UP,
                pg.K_g: Command.PLAYER3_DOWN,
                pg.K_f: Command.PLAYER3_LEFT,
                pg.K_h: Command.PLAYER3_RIGHT,
            },
            4: {
                pg.K_u: Command.PLAYER4_UP,
                pg.K_n: Command.PLAYER4_DOWN,
                pg.K_j: Command.PLAYER4_LEFT,
                pg.K_m: Command.PLAYER4_RIGHT,
            }
        }
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                commands.append(Command.QUIT)
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    commands.append(Command.QUIT)
                
                elif event.key == pg.K_RETURN:
                    commands.append(Command.RESTART)
                
                # Check player-specific mappings
                for player_id, mapping in player_mappings.items():
                    if player_id <= self.num_players and event.key in mapping:
                        commands.append(mapping[event.key])
        
        return commands