from backend.models.enums import GameResult, PlayerColor
from backend.engine.board import Board

class Engine:
    def get_rotated_piece(piece_id: int, rotation: int):
        pass

    def validate_move(board: Board, piece_id: int, anchor: int, rotation: int, color: PlayerColor):
        pass

    def calculate_territory(board: Board, position: tuple[int, int]) -> tuple[PlayerColor, list[tuple[int, int]]]:
        pass

    def check_game_over(board: Board) -> GameResult | None:
        pass

    def reconstruct_from_moves(moves: str) -> Board:
        pass
