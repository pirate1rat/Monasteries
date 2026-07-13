from dataclasses import dataclass
from backend.models.enums import PlayerColor

@dataclass
class Cell:
    player_color: PlayerColor = PlayerColor.NEUTRAL
    piece_id: int