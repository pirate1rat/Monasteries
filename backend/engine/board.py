from backend.engine.engine import Engine
from backend.models.cell import Cell
from backend.models.enums import PlayerColor
from backend.models.piece import PIECE_CATALOG

class Board:
    def __init__(self):
        self.grid: list[list[Cell]] = [[Cell for _ in range(10)] for _ in range(10)]
        self.bfs_grid: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.territories: dict[PlayerColor, set[tuple[int, int]]] = {
            PlayerColor.NEUTRAL: [],
            PlayerColor.WHITE: [],
            PlayerColor.RED: [],
        }
        self.bfs_iter: int = 0
        self.placements: dict[PlayerColor, list[tuple[tuple[int, int], int, int]]] = {}

    def place_piece(self, piece_id: int, anchor: tuple[int, int], rotation: int, color: PlayerColor) -> bool:
        if Engine.validate_move(self, piece_id, anchor, rotation, color):
            x_offset, y_offset = anchor

            for x, y in PIECE_CATALOG[piece_id].shape:
                self.grid[y + y_offset][x + x_offset] = Cell(color, piece_id)
            
            owner, tiles = Engine.calculate_territory(self, anchor)
            if owner != PlayerColor.NEUTRAL:
                match owner:
                    case PlayerColor.WHITE: opposite_col = PlayerColor.RED
                    case PlayerColor.RED: opposite_col = PlayerColor.WHITE
                self.territories[PlayerColor.NEUTRAL].difference(tiles)
                self.territories[opposite_col].difference(tiles)
                self.territories[owner].union(tiles) #|=
        else:
            return False

    def remove_piece(self, piece_id: int, anchor: tuple[int, int]) -> bool:
        pass

    def to_serializable(self) -> dict:
        pass

    