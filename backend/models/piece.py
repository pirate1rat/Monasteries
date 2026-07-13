from dataclasses import dataclass
from backend.models.enums import PlayerColor

@dataclass(frozen=True)
class PiecePrefab:
    shape: list[tuple[int, int]]
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


PIECE_CATALOG: dict[str, PiecePrefab] = {
    "CH" : PiecePrefab(
        [(0, 0), (0, -1), (1, 0), (0, 1), (0, 2), (-1, 0)],
        6, PlayerColor.NEUTRAL, "Cathedral", 1
    ),

    "TVW" : PiecePrefab(
        [(0, 0)],
        1, PlayerColor.WHITE, "Tavern_white", 2
    ),

    "TVR" : PiecePrefab(
        [(0, 0)],
        1, PlayerColor.RED, "Tavern_red", 2
    ),

    "STW" : PiecePrefab(
        [(0, 0), (0, -1)],
        2, PlayerColor.WHITE, "Stable_white", 2
    ),

    "STR" : PiecePrefab(
        [(0, 0), (0, -1)],
        2, PlayerColor.RED, "Stable_red", 2
    ),

    "INW" : PiecePrefab(
        [(0, 0), (1, 0), (0, -1)],
        3, PlayerColor.WHITE, "Inn_white", 2
    ),

    "INR" : PiecePrefab(
        [(0, 0), (1, 0), (0, -1)],
        3, PlayerColor.RED, "Inn_red", 2
    ),

    "BW" : PiecePrefab(
        [(0, 0), (0, -1), (0, 1)],
        3, PlayerColor.WHITE, "Bridge_white", 1
    ),

    "BR" : PiecePrefab(
        [(0, 0), (0, -1), (0, 1)],
        3, PlayerColor.RED, "Bridge_red", 1
    ),

    "SQW" : PiecePrefab(
        [(0, 0), (1, 0), (1, 1), (0, 1)],
        4, PlayerColor.WHITE, "Square_white", 1
    ),

    "SQR" : PiecePrefab(
        [(0, 0), (1, 0), (1, 1), (0, 1)],
        4, PlayerColor.RED, "Square_red", 1
    ),

    "MW" : PiecePrefab(
        [(0, 0), (1, 0), (0, 1), (-1, 0)],
        4, PlayerColor.WHITE, "Manor_white", 1
    ),

    "MR" : PiecePrefab(
        [(0, 0), (1, 0), (0, 1), (-1, 0)],
        4, PlayerColor.RED, "Manor_red", 1
    ),

    "ABW" : PiecePrefab(
        [(0, 0), (1, 0), (0, 1), (-1, 1)],
        4, PlayerColor.WHITE, "Abbey_white", 1
    ),

    "ABR" : PiecePrefab(
        [(0, 0), (1, 1), (0, 1), (1, 0)],
        4, PlayerColor.RED, "Abbey_red", 1
    ),

    "ACW" : PiecePrefab(
        [(0, 0), (1, 0), (0, 1), (-1, -1), (0, -1)],
        5, PlayerColor.WHITE, "Academy_white", 1
    ),

    "ACR" : PiecePrefab(
        [(0, 0), (0, -1), (1, -1), (0, 1), (-1, 0)],
        5, PlayerColor.RED, "Academy_red", 1
    ),

    "IFW" : PiecePrefab(
        [(0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)],
        5, PlayerColor.WHITE, "Infirmary_white", 1
    ),

    "IFR" : PiecePrefab(
        [(0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)],
        5, PlayerColor.RED, "Infirmary_red", 1
    ),

    "CSW" : PiecePrefab(
        [(0, 0), (1, 0), (1, 1), (-1, 1), (-1, 0)],
        5, PlayerColor.WHITE, "Castle_white", 1
    ),

    "CSR" : PiecePrefab(
        [(0, 0), (1, 0), (1, 1), (-1, 1), (-1, 0)],
        5, PlayerColor.RED, "Castle_red", 1
    ),

    "TWW" : PiecePrefab(
        [(0, 0), (0, -1), (1, -1), (-1, 1), (-1, 0)],
        5, PlayerColor.RED, "Tower_white", 1
    ),

    "TWR" : PiecePrefab(
        [(0, 0), (0, -1), (1, -1), (-1, 1), (-1, 0)],
        5, PlayerColor.RED, "Tower_red", 1
    ),
}

PASS_TURN_ID = "PASS"
EMPTY_TILE = "EMPTY"