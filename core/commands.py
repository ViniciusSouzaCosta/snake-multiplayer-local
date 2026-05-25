from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Command(Enum):
    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    MOVE_LEFT = "MOVE_LEFT"
    MOVE_RIGHT = "MOVE_RIGHT"
    RESTART = "RESTART"
    QUIT = "QUIT"
    
    # Player-specific move commands for multiplayer
    PLAYER1_UP = "PLAYER1_UP"
    PLAYER1_DOWN = "PLAYER1_DOWN"
    PLAYER1_LEFT = "PLAYER1_LEFT"
    PLAYER1_RIGHT = "PLAYER1_RIGHT"
    
    PLAYER2_UP = "PLAYER2_UP"
    PLAYER2_DOWN = "PLAYER2_DOWN"
    PLAYER2_LEFT = "PLAYER2_LEFT"
    PLAYER2_RIGHT = "PLAYER2_RIGHT"
    
    PLAYER3_UP = "PLAYER3_UP"
    PLAYER3_DOWN = "PLAYER3_DOWN"
    PLAYER3_LEFT = "PLAYER3_LEFT"
    PLAYER3_RIGHT = "PLAYER3_RIGHT"
    
    PLAYER4_UP = "PLAYER4_UP"
    PLAYER4_DOWN = "PLAYER4_DOWN"
    PLAYER4_LEFT = "PLAYER4_LEFT"
    PLAYER4_RIGHT = "PLAYER4_RIGHT"


# Color scheme for different players
PLAYER_COLORS = {
    1: {"body": (40, 110, 230), "head": (80, 160, 255)},      # Blue
    2: {"body": (230, 70, 70), "head": (255, 100, 100)},       # Red
    3: {"body": (70, 230, 70), "head": (100, 255, 100)},       # Green
    4: {"body": (230, 180, 70), "head": (255, 210, 100)}       # Orange
}