from backend.engine.engine import Engine
from backend.models.cell import Cell
from backend.models.enums import PlayerColor
from backend.models.piece import PIECE_CATALOG, NEIGHBOR_OFFSETS, EMPTY_TILE
from backend.models.placement import Placement

class Board:
    def __init__(self):
        self.grid: list[list[Cell]] = [[Cell() for _ in range(10)] for _ in range(10)]
        self.bfs_grid: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.territories: dict[PlayerColor, set[tuple[int, int]]] = {
            PlayerColor.NEUTRAL: set(),
            PlayerColor.WHITE: set(),
            PlayerColor.RED: set(),
        }
        self.bfs_iter: int = 0
        self.placements: dict[PlayerColor, dict[tuple[int, int], Placement]] = {
            PlayerColor.WHITE: {}, 
            PlayerColor.RED: {}
        }

    def place_piece(self, piece_id: int, anchor: tuple[int, int], rotation: int, color: PlayerColor) -> bool:
        if not Engine.validate_move(self, piece_id, anchor, rotation, color):
            return False

        x, y = anchor

        opposite = {
            PlayerColor.WHITE: PlayerColor.RED,
            PlayerColor.RED: PlayerColor.WHITE,
        }

        for x_offset, y_offset in Engine.get_rotated_piece(piece_id, rotation):
            self.grid[y + y_offset][x + x_offset] = Cell(color, piece_id)

            for dx, dy in NEIGHBOR_OFFSETS:
                nx = x + x_offset + dx
                ny = y + y_offset + dy

                if self.grid[ny][nx].piece_id != EMPTY_TILE or self.bfs_iter <= self.bfs_grid[ny][nx]:
                    continue

                owner, tiles = Engine.calculate_territory(self, (nx, ny))
                if owner != PlayerColor.NEUTRAL:
                    self.territories[PlayerColor.NEUTRAL] -= tiles
                    self.territories[opposite[owner]] -= tiles
                    self.territories[owner] |= tiles

                    for placed in self.placements[opposite[owner]].values():
                        if placed.anchor in self.territories[owner]:
                            self.remove_piece(placed.anchor)
                            break

    def remove_piece(self, anchor: tuple[int, int]) -> bool:
        x, y = anchor
        piece_id, col = self.grid[y][x].piece_id, self.grid[y][x].player_color
        rot = self.placements[col].get(anchor).rotation

        for x_offset, y_offset in Engine.get_rotated_piece(piece_id, rot):
            self.grid[y + y_offset][x + x_offset] = Cell(PlayerColor.NEUTRAL, EMPTY_TILE)
        
        del self.placements[col][anchor]

    def to_serializable(self) -> dict:
        pass

    