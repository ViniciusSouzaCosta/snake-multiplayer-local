import pygame as pg

from core.commands import Command


class InputMapper:
    def __init__(self, num_players=1):
        self.num_players = num_players
        
        # Initialize Pygame's Joystick API
        pg.joystick.init()
        self.joysticks = {}
        self.player_by_instance = {}
        self.refresh_joysticks()
        
    def refresh_joysticks(self):
        """Updates controller list and assigns each one to a player."""
        self.joysticks.clear()
        self.player_by_instance.clear()
        
        count = min(pg.joystick.get_count(), 4)
        
        for index in range(count):
            joy = pg.joystick.Joystick(index)
            joy.init()
            
            instance_id = joy.get_instance_id()
            player_id = index + 1
            
            self.joysticks[instance_id] = joy
            self.player_by_instance[instance_id] = player_id

    def _safe_axis(self, joy, axis: int) -> float:
        """Safe way to read axis."""
        if joy.get_numaxes() <= axis:
            return 0.0
        return joy.get_axis(axis)

    def _safe_hat(self, joy, hat: int) -> tuple[int, int]:
        """Safe way to read D-Pad."""
        if joy.get_numhats() <= hat:
            return 0, 0
        return joy.get_hat(hat)

    def get_commands(self):
        commands = []
        
        # Keyboard fallback 
        player_mappings = {
            1: {  # WASD
                pg.K_w: Command.PLAYER1_UP,
                pg.K_s: Command.PLAYER1_DOWN,
                pg.K_a: Command.PLAYER1_LEFT,
                pg.K_d: Command.PLAYER1_RIGHT,
            },
            2: {  # ARROWS
                pg.K_UP: Command.PLAYER2_UP,
                pg.K_DOWN: Command.PLAYER2_DOWN,
                pg.K_LEFT: Command.PLAYER2_LEFT,
                pg.K_RIGHT: Command.PLAYER2_RIGHT,
            },
            3: {  # IJKL
                pg.K_i: Command.PLAYER3_UP,
                pg.K_k: Command.PLAYER3_DOWN,
                pg.K_j: Command.PLAYER3_LEFT,
                pg.K_l: Command.PLAYER3_RIGHT,
            },
            4: {  # TFGH
                pg.K_t: Command.PLAYER4_UP,
                pg.K_g: Command.PLAYER4_DOWN,
                pg.K_f: Command.PLAYER4_LEFT,
                pg.K_h: Command.PLAYER4_RIGHT,
            }
        }
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                commands.append(Command.QUIT)
            
            # Plug & Play Events
            elif event.type in (pg.JOYDEVICEADDED, pg.JOYDEVICEREMOVED):
                self.refresh_joysticks()
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    commands.append(Command.QUIT)
                elif event.key == pg.K_RETURN:
                    commands.append(Command.RESTART)
                
                # Check player-specific mappings
                for player_id, mapping in player_mappings.items():
                    if player_id <= self.num_players and event.key in mapping:
                        commands.append(mapping[event.key])
            
            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == 7:  
                    commands.append(Command.RESTART)
        
        # Continuous Polling for Joysticks
        deadzone = 0.5
        for instance_id, joy in self.joysticks.items():
            player_id = self.player_by_instance.get(instance_id)
            
            if not player_id or player_id > self.num_players:
                continue
            
            x_axis = self._safe_axis(joy, 0)
            y_axis = self._safe_axis(joy, 1)
            hat_x, hat_y = self._safe_hat(joy, 0)
            
            cmd_dir = None
            
            # Priority 1: D-Pad (Hat)
            if hat_y == 1:
                cmd_dir = "UP"
            elif hat_y == -1:
                cmd_dir = "DOWN"
            elif hat_x == -1:
                cmd_dir = "LEFT"
            elif hat_x == 1:
                cmd_dir = "RIGHT"
            
            # Priority 2: Thumbstick
            elif abs(x_axis) > deadzone or abs(y_axis) > deadzone:
                if abs(x_axis) > abs(y_axis):
                    cmd_dir = "RIGHT" if x_axis > 0 else "LEFT"
                else:
                    cmd_dir = "DOWN" if y_axis > 0 else "UP"
                    
            if cmd_dir:
                commands.append(self._get_command_for_player(player_id, cmd_dir))
                
        return commands

    def _get_command_for_player(self, player_id, direction):
        """Retorna o enum Command correto baseado no ID do jogador e direção"""
        mapping = {
            1: {"UP": Command.PLAYER1_UP, "DOWN": Command.PLAYER1_DOWN, "LEFT": Command.PLAYER1_LEFT, "RIGHT": Command.PLAYER1_RIGHT},
            2: {"UP": Command.PLAYER2_UP, "DOWN": Command.PLAYER2_DOWN, "LEFT": Command.PLAYER2_LEFT, "RIGHT": Command.PLAYER2_RIGHT},
            3: {"UP": Command.PLAYER3_UP, "DOWN": Command.PLAYER3_DOWN, "LEFT": Command.PLAYER3_LEFT, "RIGHT": Command.PLAYER3_RIGHT},
            4: {"UP": Command.PLAYER4_UP, "DOWN": Command.PLAYER4_DOWN, "LEFT": Command.PLAYER4_LEFT, "RIGHT": Command.PLAYER4_RIGHT},
        }
        return mapping[player_id][direction]