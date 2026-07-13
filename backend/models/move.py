from dataclasses import dataclass
from backend.models.placement import Placement

@dataclass(frozen=True)
class Move:
    placement: Placement
    move_timestamp: int