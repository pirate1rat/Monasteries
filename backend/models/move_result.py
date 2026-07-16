from dataclasses import dataclass
from backend.models.placement import Placement

@dataclass
class MoveResult:
    token_id: str #placed piece
    captured: Placement | None
    territories_gained: set[tuple[int, int]]