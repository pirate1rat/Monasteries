from dataclasses import dataclass
from backend.models.enums import PlayerColor
from backend.models.piece import EMPTY_TILE

@dataclass
class Cell:
    player_color: PlayerColor = PlayerColor.NEUTRAL
    piece_id: int = EMPTY_TILE