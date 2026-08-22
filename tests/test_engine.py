"""
Unit tests for Engine (backend/engine/engine.py).

Execution:
    pytest tests/test_engine.py -v
"""

import pytest
from backend.engine.engine import Engine
from backend.engine.board import Board
from backend.models.enums import PlayerColor, GameResult
from backend.models.piece import EMPTY_TILE
from backend.models.cell import Cell


def set_cell(board, x: int, y: int, color: PlayerColor, piece_id: int):
    """Helper to manually set board cell states in tests."""
    board.grid[y][x] = Cell(player_color=color, piece_id=piece_id)


@pytest.fixture
def board():
    return Board()


# ============================================================
# Engine.get_rotated_piece
# ============================================================

class TestGetRotatedPiece:
    """
    Clockwise rotation by 90°: (x, y) → (-y, x)

    NOTE: the original code has a bug – `for ((x, y), i) in enumerate(new_shape):`
    should be `for (i, (x, y)) in enumerate(new_shape):`.
    The following tests document the EXPECTED behavior (some of them fail on the buggy code).
    """

    def test_rotation_0_returns_original_shape(self):
        """Rotation 0 does not alter the shape."""
        result = Engine.get_rotated_piece(3, 0)   # ((0, 0), (0, -1))
        assert set(result) == {(0, 0), (0, 1)}

    def test_rotation_0_single_cell(self):
        result = Engine.get_rotated_piece(1, 0)   # ((0,0))
        assert result == [(0, 0)]

    def test_rotation_1_horizontal_to_vertical(self):
        """
        [(0, 0), (0, 1)] rotated by 90° clockwise:
          (0,0) → (0, 0)
          (0,1) → (-1, 0)
        """
        result = Engine.get_rotated_piece(3, 1)
        assert set(result) == {(0, 0), (-1, 0)}

    def test_rotation_2_is_point_reflection(self):
        """Two 90° rotations = 180° rotation: (x,y) → (-x,-y)"""
        result = Engine.get_rotated_piece(3, 2)
        assert set(result) == {(0, 0), (0, -1)}

    def test_rotation_3_is_270_degrees(self):
        """Three rotations: (x,y) → (y,-x)"""
        result = Engine.get_rotated_piece(3, 3)
        assert set(result) == {(0, 0), (1, 0)}

    def test_rotation_4_equals_rotation_0(self):
        """Four rotations = full rotation = original shape."""
        orig = Engine.get_rotated_piece(3, 0)
        full = Engine.get_rotated_piece(3, 4)
        assert set(full) == set(orig)

    def test_single_cell_invariant_under_rotation(self):
        """A single 1x1 cell (0,0) remains unchanged in all rotations."""
        for rot in range(4):
            result = Engine.get_rotated_piece(1, rot)
            assert result == [(0, 0)], f"Rotation {rot} modified a 1×1 shape"

    def test_l_shape_rotation_1(self):
        """
        L-shape [(0,0),(1,0),(0,1)] rotated by 90°:
          (0,0)→(0,0), (1,0)→(0,1), (0,1)→(-1,0)
        """
        result = Engine.get_rotated_piece(5, 1)
        assert set(result) == {(0, 0), (0, 1), (-1, 0)}

    def test_cathedral_rotation_0(self):
        """Cathedral (id=0) – 6 cells, rotation 0 = original."""
        result = Engine.get_rotated_piece(0, 0)
        expected = {(0, 0), (0, -1), (1, 0), (0, 1), (0, 2), (-1, 0)}
        assert set(result) == expected


# ============================================================
# Engine.validate_move
# ============================================================

class TestValidateMove:

    def test_valid_placement_single_cell(self, board):
        """A single cell on an empty board – always valid."""
        assert Engine.validate_move(board, 1, (5, 5), 0, PlayerColor.WHITE) is True

    def test_valid_placement_in_corner(self, board):
        assert Engine.validate_move(board, 1, (0, 0), 0, PlayerColor.WHITE) is True
        assert Engine.validate_move(board, 1, (9, 9), 0, PlayerColor.WHITE) is True

    def test_invalid_out_of_bounds_right(self, board):
        """A 1x2 piece placed at the right edge with 270° rotation goes out of bounds."""
        assert Engine.validate_move(board, 3, (9, 5), 3, PlayerColor.WHITE) is False

    def test_invalid_out_of_bounds_bottom(self, board):
        """A 1x2 piece placed at the bottom"""
        assert Engine.validate_move(board, 3, (5, 9), 0, PlayerColor.WHITE) is False

    def test_invalid_out_of_bounds_negative(self, board):
        """Anchor outside the board."""
        assert Engine.validate_move(board, 1, (-1, 5), 0, PlayerColor.WHITE) is False
        assert Engine.validate_move(board, 1, (5, -1), 0, PlayerColor.WHITE) is False

    def test_invalid_overlap_with_existing_piece(self, board):
        """Cannot place a piece on an occupied cell."""
        set_cell(board, 5, 5, PlayerColor.WHITE, 1)
        assert Engine.validate_move(board, 1, (5, 5), 0, PlayerColor.WHITE) is False

    def test_invalid_partial_overlap(self, board):
        """A 1x2 piece: one cell is empty, the other is occupied."""
        set_cell(board, 6, 5, PlayerColor.WHITE, 1)
        assert Engine.validate_move(board, 3, (6, 4), 0, PlayerColor.WHITE) is False

    def test_invalid_placement_in_enemy_territory(self, board):
        """Cannot place a piece on opponent's territory (anchor in territory)."""
        board.territories[PlayerColor.RED].add((5, 5))
        assert Engine.validate_move(board, 1, (5, 5), 0, PlayerColor.WHITE) is False

    def test_valid_placement_in_own_territory(self, board):
        """Can place a piece in your own territory."""
        board.territories[PlayerColor.WHITE].add((5, 5))
        assert Engine.validate_move(board, 1, (5, 5), 0, PlayerColor.WHITE) is True

    def test_valid_placement_in_neutral_territory(self, board):
        """Neutral territory does not block moves."""
        board.territories[PlayerColor.NEUTRAL].add((5, 5))
        assert Engine.validate_move(board, 1, (5, 5), 0, PlayerColor.WHITE) is True

    def test_horizontal_piece_fits_exactly_at_edge(self, board):
        """A 1x2 piece with anchor at (8,5) – ends at (9,5), fits perfectly."""
        assert Engine.validate_move(board, 3, (8, 5), 0, PlayerColor.WHITE) is True

    def test_long_piece_out_of_bounds(self, board):
        """A 1x3 piece with anchor (5,9) | goes out of bounds."""
        assert Engine.validate_move(board, 7, (5, 9), 0, PlayerColor.WHITE) is False

    def test_both_players_can_place_on_empty_board(self, board):
        """Both players can place pieces on an empty board."""
        assert Engine.validate_move(board, 1, (0, 0), 0, PlayerColor.WHITE) is True
        assert Engine.validate_move(board, 2, (9, 9), 0, PlayerColor.RED) is True


# ============================================================
# Engine.calculate_territory
# ============================================================

class TestCalculateTerritory:
    """
    BFS from the specified position (must be an empty cell).
    Territory rules:
      - NEUTRAL: region not enclosed | enclosed by both players | touches the outer boundaries of the board
      - WHITE/RED: enclosed exclusively by a single player
      - when both colors surround it: won by whoever has more pieces (difference > 1), otherwise NEUTRAL
    """

    def test_open_region_is_neutral(self, board):
        """An empty cell connected to the rest of the empty board → NEUTRAL."""
        owner, tiles, interior_pieces = Engine.calculate_territory(board, (5, 5))
        assert owner == PlayerColor.NEUTRAL

    def test_single_empty_cell_surrounded_by_white(self, board):
        """
        A single empty cell surrounded on all 8 sides by WHITE pieces.
        The territory should be claimed by WHITE.
        """
        cx, cy = 5, 5
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                set_cell(board, cx + dx, cy + dy, PlayerColor.WHITE, 1)

        owner, tiles, interior_pieces = Engine.calculate_territory(board, (cx, cy))
        assert owner == PlayerColor.WHITE
        assert (cx, cy) in tiles

    def test_single_empty_cell_surrounded_by_red(self, board):
        cx, cy = 5, 5
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                set_cell(board, cx + dx, cy + dy, PlayerColor.RED, 2)

        owner, tiles, interior_pieces = Engine.calculate_territory(board, (cx, cy))
        assert owner == PlayerColor.RED
        assert (cx, cy) in tiles

    def test_mixed_border_returns_neutral(self, board):
        """
        Cell surrounded by both WHITE and RED – NEUTRAL territory
        (equal number of surrounding pieces for both players).
        """
        cx, cy = 5, 5
        neighbors = [
            (cx-1, cy-1), (cx, cy-1), (cx+1, cy-1),
            (cx-1, cy),               (cx+1, cy),
            (cx-1, cy+1), (cx, cy+1), (cx+1, cy+1),
        ]
        for i, (nx, ny) in enumerate(neighbors):
            color = PlayerColor.WHITE if i % 2 == 0 else PlayerColor.RED
            pid = 1 if color == PlayerColor.WHITE else 2
            set_cell(board, nx, ny, color, pid)

        owner, _, _ = Engine.calculate_territory(board, (cx, cy))
        assert owner == PlayerColor.NEUTRAL

    def test_territory_tiles_contains_all_empty_cells(self, board):
        """The returned tiles set should contain ALL empty cells in the region."""
        # Small 2x1 area enclosed by WHITE (cells (5,5) and (6,5))
        for dy in [-1, 1]:
            for x in [4, 5, 6, 7]:
                set_cell(board, x, 5 + dy, PlayerColor.WHITE, 1)
        set_cell(board, 4, 5, PlayerColor.WHITE, 1)
        set_cell(board, 7, 5, PlayerColor.WHITE, 1)

        owner, tiles, interior_pieces = Engine.calculate_territory(board, (5, 5))
        assert (5, 5) in tiles
        assert (6, 5) in tiles

    def test_territory_doesnt_include_piece_cells(self, board):
        """Cells occupied by pieces should not be included in the tiles set."""
        cx, cy = 5, 5
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                set_cell(board, cx + dx, cy + dy, PlayerColor.WHITE, 1)

        _, tiles, interior_pieces = Engine.calculate_territory(board, (cx, cy))
        for (tx, ty) in tiles:
            assert board.grid[ty][tx].piece_id == EMPTY_TILE, \
                f"Cell ({tx},{ty}) containing a piece was found in the tiles set"

    def test_bfs_iter_increments(self, board):
        """Every call to calculate_territory increments bfs_iter (BFS cache)."""
        before = board.bfs_iter
        Engine.calculate_territory(board, (5, 5))
        assert board.bfs_iter == before + 1


# ============================================================
# Engine.has_possible_moves
# ============================================================

class TestHasPossibleMoves:

    def test_empty_board_has_moves(self, board):
        remaining = {1: 1}
        assert Engine.has_possible_moves(board, PlayerColor.WHITE, remaining) is True

    def test_no_pieces_no_moves(self, board):
        assert Engine.has_possible_moves(board, PlayerColor.WHITE, {}) is False

    def test_full_board_no_moves(self, board):
        """Fully occupied board – no available empty cells."""
        for y in range(10):
            for x in range(10):
                set_cell(board, x, y, PlayerColor.WHITE, 1)
        assert Engine.has_possible_moves(board, PlayerColor.WHITE, {1: 1}) is False

    def test_piece_fits_only_in_specific_rotation(self, board):
        """
        Only 1 row of width 1 is empty – a 1x2 piece only fits if rotated.
        """
        # Fill everything except row 0 (y=0)
        for y in range(1, 10):
            for x in range(10):
                set_cell(board, x, y, PlayerColor.WHITE, 1)
        # A 1x2 piece horizontally (rotation=0) fits in row 0
        assert Engine.has_possible_moves(board, PlayerColor.RED, {4: 1}) is True

    def test_board_blocked_by_enemy_territory(self, board):
        """If the only empty spaces are enemy territory – no moves available."""
        # Only (5,5) is empty, but it is WHITE territory
        for y in range(10):
            for x in range(10):
                if not (x == 5 and y == 5):
                    set_cell(board, x, y, PlayerColor.RED, 2)
        board.territories[PlayerColor.WHITE].add((5, 5))
        assert Engine.has_possible_moves(board, PlayerColor.RED, {2: 1}) is False


# ============================================================
# Engine.check_game_over
# ============================================================

class TestCheckGameOver:

    def test_game_not_over_when_moves_available(self, board):
        result = Engine.check_game_over(board, {1: 1}, {2: 1})
        assert result is None

    def test_draw_when_scores_equal(self, board):
        """
        Both players have no moves, and the sizes of remaining pieces are equal → DRAW.
        Pieces: WHITE=[1 (size=1)], RED=[2 (size=1)]
        """
        for y in range(10):
            for x in range(10):
                set_cell(board, x, y, PlayerColor.WHITE, 1)
        result = Engine.check_game_over(board, {1: 1}, {2: 1})
        assert result == GameResult.DRAW

    def test_white_wins_when_red_has_more_remaining(self, board):
        """
        Lower score = fewer unplayed piece cells = WIN.
        WHITE remaining: size=1, RED remaining: size=1+2=3 → WHITE_WINS.

        NOTE: original code has a bug – red_score calculates using white_remaining_pieces!
        This test fails on the original code.
        """
        for y in range(10):
            for x in range(10):
                set_cell(board, x, y, PlayerColor.WHITE, 1)
        # WHITE: piece_id=1 size=1; RED: piece_id=2 size=1 + piece_id=4 size=2 → total 3
        result = Engine.check_game_over(board, {1: 1}, {2: 1, 4: 1})
        assert result == GameResult.WHITE_WINS, (
            "BUG: red_score uses white_remaining_pieces instead of red_remaining_pieces"
        )

    def test_red_wins_when_white_has_more_remaining(self, board):
        for y in range(10):
            for x in range(10):
                set_cell(board, x, y, PlayerColor.WHITE, 1)
        # WHITE: piece_id=1 size=1 + piece_id=3 size=2 → total 3; RED: piece_id=2 size=1
        result = Engine.check_game_over(board, {1: 1, 3: 1}, {2: 1})
        assert result == GameResult.RED_WINS

    def test_returns_none_when_one_player_can_move(self, board):
        """The game continues as long as at least one player can make a move."""
        # Only WHITE can move – RED has no pieces left
        result = Engine.check_game_over(board, {1: 1}, {})
        assert result is None
