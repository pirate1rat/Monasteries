from enum import Enum, auto

class PlayerColor(Enum):
    WHITE = auto()
    RED = auto()
    NEUTRAL = auto()

class GameStatus(Enum):
    WAITING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    ABANDONED = auto()

class GameResult(Enum):
    WHITE_WINS = auto()
    RED_WINS = auto()
    DRAW = auto()
    ABANDONED = auto()