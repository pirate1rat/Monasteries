from dataclasses import dataclass
from backend.models.enums import PlayerColor

@dataclass(frozen=True)
class Placement:
    piece_id: int
    anchor: tuple[int, int]
    rotation: int
    color: PlayerColor