from dataclasses import dataclass
from backend.models.enums import PlayerColor
from backend.models.piece import EMPTY_TILE

@dataclass
class Cell:
    player_color: PlayerColor = PlayerColor.NEUTRAL
    piece_id: str = EMPTY_TILE