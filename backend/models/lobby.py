from dataclasses import dataclass, field
import datetime

from uuid import UUID
from backend.models.enums import PlayerColor
from backend.models.time_control import TimeControl

@dataclass
class Lobby:
    lobby_id: UUID
    host_id: int
    host_color: PlayerColor
    time_control: TimeControl
    created_at: datetime = field(default_factory=datetime.datetime.now)