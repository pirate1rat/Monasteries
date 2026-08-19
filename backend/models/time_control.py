from dataclasses import dataclass

@dataclass(frozen=True)
class TimeControl:
    base: int
    incremental: int

    def to_serializable(self) -> dict:
        return {
            "base": self.base,
            "incremental": self.incremental,
        }