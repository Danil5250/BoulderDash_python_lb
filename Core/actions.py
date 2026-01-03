from enum import Enum, auto

class ActionType(Enum):
    MOVE = auto()
    WAIT = auto()
    PLACE_BOMB = auto()

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    JUMP_UP = (0, -2)
    JUMP_DOWN = (0, 2)
    JUMP_LEFT = (-2, 0)
    JUMP_RIGHT = (2, 0)

class Action:
    def __init__(self, action_type, direction=None):
        self.type = action_type
        self.direction = direction
