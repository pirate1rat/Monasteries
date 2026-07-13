from dataclasses import dataclass

@dataclass(frozen=True)
class TimeControl:
    base: int
    incremental: int