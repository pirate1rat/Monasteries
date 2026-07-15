from backend.models.enums import GameResult, PlayerColor
from backend.models.piece import PIECE_CATALOG, EMPTY_TILE, NEIGHBOR_OFFSETS
from queue import Queue
from itertools import product

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.engine.board import Board

class Engine:
    @staticmethod
    def get_rotated_piece(piece_id: int, rotation: int) -> list[tuple[int, int]]:
        new_shape = list(PIECE_CATALOG[piece_id].shape)
        
        for _ in range(rotation):
            new_shape = [(-y, x) for x, y in new_shape]

        return new_shape

    @staticmethod
    def validate_move(
            board: "Board",
            piece_id: int,
            anchor: tuple[int, int],
            rotation: int,
            color: PlayerColor) -> bool:
        piece = Engine.get_rotated_piece(piece_id, rotation)

        for x_offset, y_offset in piece:
            x, y = anchor

            # is on board
            if not ((0 <= x + x_offset < 10) and (0 <= y + y_offset < 10)):
                return False
            # does overlap with other piece
            if board.grid[y + y_offset][x + x_offset].piece_id != EMPTY_TILE:
                return False
        
        # is on territory
        opposite = {
            PlayerColor.WHITE: PlayerColor.RED,
            PlayerColor.RED: PlayerColor.WHITE,
        }

        if opposite.get(color, False) and anchor in board.territories[opposite[color]]:
            return False

        return True

    @staticmethod
    def calculate_territory(board: "Board", position: tuple[int, int]) -> tuple[PlayerColor, list[tuple[int, int]]]:
        discovered_colors = set()
        discovered_pieces = set()
        tiles = set()

        def _bfs(start):
            nonlocal discovered_colors, discovered_pieces
            q = Queue()
            q.put(start)
            board.bfs_iter += 1
            k = board.bfs_iter

            while not q.empty():
                x, y = q.get()

                if not ((0 <= x < 10) and (0 <= y < 10)):
                    continue
                if board.bfs_grid[y][x] == k:
                    continue
                board.bfs_grid[y][x] = k
                if board.grid[y][x].piece_id != EMPTY_TILE:
                    discovered_colors.add(board.grid[y][x].player_color)
                    discovered_pieces.add(board.grid[y][x].piece_id)
                else:
                    tiles.add((x, y))
                    for dx, dy in NEIGHBOR_OFFSETS:
                        q.put((x + dx, y + dy))
        
        _bfs(position)
        if len(discovered_colors) == 0 or PlayerColor.NEUTRAL in discovered_colors:
            return (PlayerColor.NEUTRAL, tiles)
        elif len(discovered_colors) == 1:
            return (discovered_colors.pop(), tiles)
        else:
            white = len({x for x in discovered_pieces if x % 2 == 1})
            red = len({x for x in discovered_pieces if x % 2 == 0 and x != 0})
            if abs(white - red) > 1:
                return (PlayerColor.NEUTRAL, tiles)
            elif white > red:
                return (PlayerColor.WHITE, tiles)
            else:
                return (PlayerColor.RED, tiles)

    @staticmethod
    def has_possible_moves(board: "Board", color: PlayerColor, remaining_pices: list[int]) -> bool:
        return any(
            Engine.validate_move(board, piece_id, (x, y), rot, color)
            for piece_id in remaining_pices
            for x, y in product(range(10), repeat=2)
            if  board.grid[y][x].piece_id == EMPTY_TILE
            for rot in range(4)
        )

    @staticmethod
    def check_game_over(board: "Board", white_remaining_pices: list[int], red_remaining_pices: list[int]) -> GameResult | None:
        if Engine.has_possible_moves(board, PlayerColor.WHITE, white_remaining_pices) \
        or Engine.has_possible_moves(board, PlayerColor.RED, red_remaining_pices): return None
        else:
            white_score = sum(PIECE_CATALOG[piece_id].size for piece_id in white_remaining_pices)
            red_score = sum(PIECE_CATALOG[piece_id].size for piece_id in red_remaining_pices)
            if white_score == red_score: return GameResult.DRAW
            elif white_score > red_score: return GameResult.WHITE_WINS
            else: return GameResult.RED_WINS

    @staticmethod
    def reconstruct_from_moves(moves: str) -> Board:
        pass
