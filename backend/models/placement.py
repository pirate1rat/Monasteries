from dataclasses import dataclass
from backend.models.enums import PlayerColor

@dataclass(frozen=True)
class Placement:
    token_id: str
    piece_id: int
    anchor: tuple[int, int]
    rotation: int
    color: PlayerColor

    def __hash__(self):
        return hash((
            self.token_id,
            self.piece_id,
            self.anchor,
            self.rotation,
            self.color,
        ))