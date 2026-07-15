from dataclasses import dataclass
from backend.models.enums import PlayerColor

@dataclass(frozen=True)
class PiecePrefab:
    shape: tuple[tuple[int, int]]
    size: int
    color: PlayerColor
    name: str
    starting_amount: int

# Cathedral - CH
# Tavern - TV
# Stable - ST
# Inn - IN
# Bringe - B
# Square - SQ
# Manor - M
# Abbey - AB
# Academy - AC
# Infirmary - IF
# Castle - CS
# Tower - TW
# prefix W/R - White/Red

NEIGHBOR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1)
]

PIECE_CATALOG: dict[int, PiecePrefab] = {
    0 : PiecePrefab(
        ((0, 0), (0, -1), (1, 0), (0, 1), (0, 2), (-1, 0)),
        6, PlayerColor.NEUTRAL, "Cathedral", 1
    ),

    1 : PiecePrefab(
        ((0, 0)),
        1, PlayerColor.WHITE, "Tavern_white", 2
    ),

    2 : PiecePrefab(
        ((0, 0)),
        1, PlayerColor.RED, "Tavern_red", 2
    ),

    3 : PiecePrefab(
        ((0, 0), (0, -1)),
        2, PlayerColor.WHITE, "Stable_white", 2
    ),

    4 : PiecePrefab(
        ((0, 0), (0, -1)),
        2, PlayerColor.RED, "Stable_red", 2
    ),

    5 : PiecePrefab(
        ((0, 0), (1, 0), (0, -1)),
        3, PlayerColor.WHITE, "Inn_white", 2
    ),

    6 : PiecePrefab(
        ((0, 0), (1, 0), (0, -1)),
        3, PlayerColor.RED, "Inn_red", 2
    ),

    7 : PiecePrefab(
        ((0, 0), (0, -1), (0, 1)),
        3, PlayerColor.WHITE, "Bridge_white", 1
    ),

    8 : PiecePrefab(
        ((0, 0), (0, -1), (0, 1)),
        3, PlayerColor.RED, "Bridge_red", 1
    ),

    9 : PiecePrefab(
        ((0, 0), (1, 0), (1, 1), (0, 1)),
        4, PlayerColor.WHITE, "Square_white", 1
    ),

    10 : PiecePrefab(
        ((0, 0), (1, 0), (1, 1), (0, 1)),
        4, PlayerColor.RED, "Square_red", 1
    ),

    11 : PiecePrefab(
        ((0, 0), (1, 0), (0, 1), (-1, 0)),
        4, PlayerColor.WHITE, "Manor_white", 1
    ),

    12 : PiecePrefab(
        ((0, 0), (1, 0), (0, 1), (-1, 0)),
        4, PlayerColor.RED, "Manor_red", 1
    ),

    13 : PiecePrefab(
        ((0, 0), (1, 0), (0, 1), (-1, 1)),
        4, PlayerColor.WHITE, "Abbey_white", 1
    ),

    14 : PiecePrefab(
        ((0, 0), (1, 1), (0, 1), (1, 0)),
        4, PlayerColor.RED, "Abbey_red", 1
    ),

    15 : PiecePrefab(
        ((0, 0), (1, 0), (0, 1), (-1, -1), (0, -1)),
        5, PlayerColor.WHITE, "Academy_white", 1
    ),

    16 : PiecePrefab(
        ((0, 0), (0, -1), (1, -1), (0, 1), (-1, 0)),
        5, PlayerColor.RED, "Academy_red", 1
    ),

    17 : PiecePrefab(
        ((0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)),
        5, PlayerColor.WHITE, "Infirmary_white", 1
    ),

    18 : PiecePrefab(
        ((0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)),
        5, PlayerColor.RED, "Infirmary_red", 1
    ),

    19 : PiecePrefab(
        ((0, 0), (1, 0), (1, 1), (-1, 1), (-1, 0)),
        5, PlayerColor.WHITE, "Castle_white", 1
    ),

    20 : PiecePrefab(
        ((0, 0), (1, 0), (1, 1), (-1, 1), (-1, 0)),
        5, PlayerColor.RED, "Castle_red", 1
    ),

    21 : PiecePrefab(
        ((0, 0), (0, -1), (1, -1), (-1, 1), (-1, 0)),
        5, PlayerColor.WHITE, "Tower_white", 1
    ),

    22 : PiecePrefab(
        ((0, 0), (0, -1), (1, -1), (-1, 1), (-1, 0)),
        5, PlayerColor.RED, "Tower_red", 1
    ),
}

PASS_TURN_ID = "PASS"
EMPTY_TILE = -1