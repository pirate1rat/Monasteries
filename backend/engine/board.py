from backend.engine.engine import Engine
from backend.models.cell import Cell
from backend.models.enums import PlayerColor
from backend.models.piece import PIECE_CATALOG, NEIGHBOR_OFFSETS, EMPTY_TILE
from backend.models.placement import Placement
from backend.models.move_result import MoveResult

OPPOSITE = {
    PlayerColor.WHITE: PlayerColor.RED,
    PlayerColor.RED:   PlayerColor.WHITE,
}

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
        self.placements: dict[str, Placement] = {}
        self._next_token: int = 0

    def place_piece(self, placement: Placement) -> MoveResult | None:
        """
        Places a piece on the board.
        Returns the token_id of the new piece, or None if the move is illegal.
        """
        print("????????????????????\n\n\n\n\n\n\n", placement)

        piece_id: int = placement.piece_id
        anchor: tuple[int, int] = placement.anchor
        rotation: int = placement.rotation
        color: PlayerColor = placement.color

        if not Engine.validate_move(self, piece_id, anchor, rotation, color):
            return None

        ax, ay = anchor
        offsets = Engine.get_rotated_piece(piece_id, rotation)

        for dx, dy in offsets:
            self.grid[ay + dy][ax + dx] = Cell(color, piece_id)

        token_id = f"{piece_id}_{self._next_token}"
        self._next_token += 1
        self.placements[token_id] = Placement(token_id, piece_id, anchor, rotation, color)

        if color == PlayerColor.NEUTRAL:
            return MoveResult(
                token_id=token_id,
                captured=None,
                territories_gained=set()
            )

        captured = None
        tiles = set()

        for dx, dy in offsets:
            cx, cy = ax + dx, ay + dy
            for ndx, ndy in NEIGHBOR_OFFSETS:
                nx, ny = cx + ndx, cy + ndy
                if not (0 <= nx < 10 and 0 <= ny < 10):
                    continue
                if self.bfs_iter <= self.bfs_grid[ny][nx]: # if bfs has been already run in this cell
                    continue
                if self.grid[ny][nx].piece_id != EMPTY_TILE:
                    continue

                owner, tiles, interior = Engine.calculate_territory(self, (nx, ny))

                if owner != color:
                    continue

                self.territories[PlayerColor.NEUTRAL] -= tiles
                self.territories[OPPOSITE[color]] -= tiles
                self.territories[color] |= tiles

                if len(interior) == 1 and interior[0].color == OPPOSITE[color]:
                    removed = interior[0]
                    freed_cells = {
                        (removed.anchor[0] + ddx, removed.anchor[1] + ddy)
                        for ddx, ddy in Engine.get_rotated_piece(
                            removed.piece_id, removed.rotation)
                    }
                    captured = self.remove_piece(removed.token_id) # Placement | None
                    self.territories[color] |= freed_cells

        return MoveResult(
            token_id=token_id,
            captured=captured,
            territories_gained=tiles | (freed_cells if captured else set())
        )

    def remove_piece(self, token_id: str) -> Placement | None:
        """
        Removes a piece from the board by token_id.
        Returns True if removed, False if token_id is unknown.
        """

        placement = self.placements.get(token_id)
        if placement is None:
            return None

        ax, ay = placement.anchor
        for dx, dy in Engine.get_rotated_piece(placement.piece_id, placement.rotation):
            self.grid[ay + dy][ax + dx] = Cell()  # EMPTY_TILE, NEUTRAL

        del self.placements[token_id]
        return placement

    def to_serializable(self) -> dict:
        return {
            "grid": [
                [
                    {"piece_id": cell.piece_id, "color": cell.player_color.value}
                    for cell in row
                ]
                for row in self.grid
            ],
        }

    