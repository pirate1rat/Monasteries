from backend.models.enums import GameResult, PlayerColor
from backend.models.piece import PIECE_CATALOG, EMPTY_TILE, NEIGHBOR_OFFSETS
from backend.models.placement import Placement
from queue import Queue
from itertools import product

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.engine.board import Board

OPPOSITE = {
    PlayerColor.WHITE: PlayerColor.RED,
    PlayerColor.RED:   PlayerColor.WHITE,
}

class Engine:
    def get_rotated_piece(piece_id: int, rotation: int) -> list[tuple[int, int]]:
        shape = list(PIECE_CATALOG[piece_id].shape)
        for _ in range(rotation % 4):
            shape = [(-y, x) for x, y in shape]
        return shape

    @staticmethod
    def validate_move(
            board: "Board",
            piece_id: int,
            anchor: tuple[int, int],
            rotation: int,
            color: PlayerColor) -> bool:

        piece = Engine.get_rotated_piece(piece_id, rotation)
        ax, ay = anchor

        if piece_id == 0:
            for dx, dy in piece:
                x, y = ax + dx, ay + dy
                if not (0 <= x < 10 and 0 <= y < 10):
                    return False
                if board.grid[y][x].piece_id != EMPTY_TILE:
                    return False
            return True

        opp_territory = board.territories.get(OPPOSITE.get(color), set())

        for dx, dy in piece:
            x, y = ax + dx, ay + dy
            if not (0 <= x < 10 and 0 <= y < 10):
                return False
            if board.grid[y][x].piece_id != EMPTY_TILE:
                return False
            if (x, y) in opp_territory:
                return False

        return True

    @staticmethod
    def calculate_territory(board: "Board", position: tuple[int, int], color: PlayerColor) -> tuple[PlayerColor, set[tuple[int, int]], list[Placement]]:
        """
        BFS starting from `position`.
        Returns (owner, empty_tiles, internal_pieces).

        Division into two classes of pieces:
        - boundary: they form the territory wall and determine the owner
        - internal: completely surrounded by the empty tiles of the territory,
                    subject to the capturing rule (max. 1 piece)
        """

        def get_piece_cells(p: Placement) -> frozenset[tuple[int, int]]:
            ax, ay = p.anchor
            return frozenset(
                (ax + dx, ay + dy)
                for dx, dy in Engine.get_rotated_piece(p.piece_id, p.rotation)
            )

        tiles: set[tuple[int, int]] = set()
        discovered_other_pieces: set[tuple[int, int]] = set()
        q: Queue = Queue()

        q.put(position)
        k = board.bfs_iter

        while not q.empty():
            x, y = q.get()

            if not (0 <= x < 10 and 0 <= y < 10):
                continue
            if board.bfs_grid[y][x] == k:
                continue
            board.bfs_grid[y][x] = k

            if board.grid[y][x].piece_id == EMPTY_TILE:
                tiles.add((x, y))
                for dx, dy in NEIGHBOR_OFFSETS:
                    q.put((x + dx, y + dy))
            elif board.grid[y][x].player_color != color:
                discovered_other_pieces.add((x, y))
                for dx, dy in NEIGHBOR_OFFSETS:
                    q.put((x + dx, y + dy))

        interior: set[tuple[int, int]] = set()
        for placement in board.placements.values():
            cells = get_piece_cells(placement)
            if cells.issubset(discovered_other_pieces):
                interior.add(placement)

        if board.bfs_iter <= 3:  # don't capture cathedral on first moves
            owner = PlayerColor.NEUTRAL if 1 <= len(interior) else color
        else:
            owner = PlayerColor.NEUTRAL if 1 < len(interior) else color

        return (owner, tiles, interior)

    @staticmethod
    def has_possible_moves(board: "Board", color: PlayerColor, remaining_pieces: dict[int, int]) -> bool:
        return any(
            Engine.validate_move(board, piece_id, (x, y), rot, color)
            for piece_id in remaining_pieces.keys()
            for x, y in product(range(10), repeat=2)
            if board.grid[y][x].piece_id == EMPTY_TILE
            for rot in range(4)
        )

    @staticmethod
    def check_game_over(board: "Board", white_remaining: dict[int, int], red_remaining: dict[int, int]) -> GameResult | None:
        if Engine.has_possible_moves(board, PlayerColor.WHITE, white_remaining) \
        or Engine.has_possible_moves(board, PlayerColor.RED,   red_remaining):
            return None

        white_remaining_tiles = sum(PIECE_CATALOG[pid].size * qty for pid, qty in white_remaining.items())
        red_remaining_tiles = sum(PIECE_CATALOG[pid].size * qty for pid, qty in red_remaining.items())

        if white_remaining_tiles == red_remaining_tiles: return GameResult.DRAW
        elif white_remaining_tiles < red_remaining_tiles: return GameResult.WHITE_WINS
        else: return GameResult.RED_WINS

    @staticmethod
    def reconstruct_from_moves(moves: str) -> "Board":
        pass