from enum import Enum, IntEnum, auto

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

# White - odd
# Red - even (except 0)
class LocationType(IntEnum):
    CATHEDRAL = 0

    TAVERN_WHITE = auto()
    TAVERN_RED = auto()

    STABLE_WHITE = auto()
    STABLE_RED = auto()

    INN_WHITE = auto()
    INN_RED = auto()

    BRIDGE_WHITE = auto()
    BRIDGE_RED = auto()

    SQUARE_WHITE = auto()
    SQUARE_RED = auto()

    MANOR_WHITE = auto()
    MANOR_RED = auto()

    ABBEY_WHITE = auto()
    ABBEY_RED = auto()

    ACADEMY_WHITE = auto()
    ACADEMY_RED = auto()

    INFIRMARY_WHITE = auto()
    INFIRMARY_RED = auto()

    CASTLE_WHITE = auto()
    CASTLE_RED = auto()

    TOWER_WHITE = auto()
    TOWER_RED = auto()