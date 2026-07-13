from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    piece_id: int
    anchor: tuple[int, int]
    rotation: int
    move_timestamp: int