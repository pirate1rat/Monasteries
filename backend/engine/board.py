from backend.models.cell import Cell
from backend.models.enums import PlayerColor

class Board:
    def __init__(self):
        self.grid: list[list[Cell]] = [[Cell for _ in range(10)] for _ in range(10)]
        self.bfs_grid: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.territories: dict[PlayerColor, list[tuple[int, int]]] = {
            PlayerColor.NEUTRAL: [],
            PlayerColor.WHITE: [],
            PlayerColor.RED: [],
        }
        # self.white_placements: list[tuple[tuple[int, int], int, int]] = []
        # self.red_placements: list[tuple[tuple[int, int], int, int]] = []

    def place_piece(self, piece_id: int, anchor: tuple[int, int], rotation: int, color: PlayerColor) -> bool:
        pass

    def remove_piece(self, piece_id: int, anchor: tuple[int, int]) -> bool:
        pass

    def to_serializable(self) -> dict:
        pass

    