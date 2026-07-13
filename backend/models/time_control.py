from dataclasses import dataclass

@dataclass
class TimeControl:
    base: int
    incremental: int