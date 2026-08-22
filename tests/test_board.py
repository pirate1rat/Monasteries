import pytest
from backend.engine.board import Board
from backend.models.enums import PlayerColor
from backend.models.piece import EMPTY_TILE
from backend.models.placement import Placement


def _pl(piece_id, anchor, rotation, color):
    """Shorthand: create a Placement for tests (token_id is ignored by place_piece)."""
    return Placement("", piece_id, anchor, rotation, color)


@pytest.fixture
def empty_board():
    """Creates a new, clean board for each test."""
    return Board()


def test_board_initialization(empty_board):
    """Verifies that the board initializes as a 10x10 grid of empty cells."""
    assert len(empty_board.grid) == 10
    assert len(empty_board.grid[0]) == 10
    assert empty_board.grid[0][0].piece_id == EMPTY_TILE
    assert empty_board.grid[0][0].player_color == PlayerColor.NEUTRAL


def test_place_piece_valid(empty_board):
    """Verifies correct piece placement on the board."""
    # Cathedral (piece_id = 0) with offsets: (0, 0), (0, -1), (1, 0), (0, 1), (0, 2), (-1, 0)
    # Placing it at the center (5, 5) with rotation 0.
    result = empty_board.place_piece(_pl(0, (5, 5), 0, PlayerColor.NEUTRAL))

    assert result is not None

    # Verify that the piece anchor is placed correctly
    assert empty_board.grid[5][5].piece_id == 0
    assert empty_board.grid[5][5].player_color == PlayerColor.NEUTRAL

    # Verify adjacent parts of the piece based on its definition
    assert empty_board.grid[4][5].piece_id == 0  # offset (0, -1)
    assert empty_board.grid[5][6].piece_id == 0  # offset (1, 0)
    assert empty_board.grid[6][5].piece_id == 0  # offset (0, 1)


def test_place_piece_out_of_bounds(empty_board):
    """Verifies that the system rejects placing a piece out of bounds."""
    result = empty_board.place_piece(_pl(0, (9, 9), 0, PlayerColor.NEUTRAL))

    assert result is None
    assert empty_board.grid[9][9].piece_id == EMPTY_TILE


def test_place_piece_overlap(empty_board):
    """Verifies that pieces cannot overlap each other."""
    empty_board.place_piece(_pl(0, (5, 5), 0, PlayerColor.NEUTRAL))

    # Attempt to place another piece in the exact same location (using Red Player's Tower: id 22)
    result = empty_board.place_piece(_pl(22, (5, 5), 0, PlayerColor.RED))

    assert result is None
    assert empty_board.grid[5][5].piece_id == 0  # The original piece should remain


def test_remove_piece(empty_board):
    """Verifies correct removal of a piece from the board."""
    empty_board.place_piece(_pl(0, (5, 5), 0, PlayerColor.NEUTRAL))

    empty_board.remove_piece("0_0")

    assert empty_board.grid[5][5].piece_id == EMPTY_TILE
    assert empty_board.grid[4][5].piece_id == EMPTY_TILE
