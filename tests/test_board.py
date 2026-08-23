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

class TestPlacingPieces:

    def test_board_initialization(self, empty_board):
        """Verifies that the board initializes as a 10x10 grid of empty cells."""
        assert len(empty_board.grid) == 10
        assert len(empty_board.grid[0]) == 10
        assert empty_board.grid[0][0].piece_id == EMPTY_TILE
        assert empty_board.grid[0][0].player_color == PlayerColor.NEUTRAL


    def test_place_piece_valid(self, empty_board):
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


    def test_place_piece_out_of_bounds(self, empty_board):
        """Verifies that the system rejects placing a piece out of bounds."""
        result = empty_board.place_piece(_pl(0, (9, 9), 0, PlayerColor.NEUTRAL))

        assert result is None
        assert empty_board.grid[9][9].piece_id == EMPTY_TILE


    def test_place_piece_overlap(self, empty_board):
        """Verifies that pieces cannot overlap each other."""
        empty_board.place_piece(_pl(0, (5, 5), 0, PlayerColor.NEUTRAL))

        # Attempt to place another piece in the exact same location (using Red Player's Tower: id 22)
        result = empty_board.place_piece(_pl(22, (5, 5), 0, PlayerColor.RED))

        assert result is None
        assert empty_board.grid[5][5].piece_id == 0  # The original piece should remain


    def test_remove_piece(self, empty_board):
        """Verifies correct removal of a piece from the board."""
        empty_board.place_piece(_pl(0, (5, 5), 0, PlayerColor.NEUTRAL))

        empty_board.remove_piece("0_0")

        assert empty_board.grid[5][5].piece_id == EMPTY_TILE
        assert empty_board.grid[4][5].piece_id == EMPTY_TILE

class TestTerritoryGrabbing:
    
    def test_corner_to_corner_leakage(self, empty_board):
        # A wall built corner-to-corner should NOT create a territory.
        # The 8-directional BFS in calculate_territory will "leak" through the diagonal.
        
        # Placing White Taverns to form a diagonal wall
        empty_board.place_piece(Placement("W1", 1, (1, 0), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (2, 1), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W3", 1, (3, 2), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W4", 1, (0, 1), 0, PlayerColor.WHITE))
        
        # The area (0,0) is partially enclosed but has a diagonal gap between (1,0) and (0,1).
        assert (0, 0) not in empty_board.territories[PlayerColor.WHITE]

    def test_map_edges_act_as_walls(self, empty_board):
        # The map boundaries should naturally act as walls for territory generation.
        
        # Enclosing a 1x1 space at the bottom right corner (9,9)
        empty_board.place_piece(Placement("W1", 1, (8, 9), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (9, 8), 0, PlayerColor.WHITE))
        
        # The corner itself (9,9) should now belong to WHITE
        assert (9, 9) in empty_board.territories[PlayerColor.WHITE]

    def test_build_on_own_territory_allowed(self, empty_board):
        # Players should be able to place pieces within their OWN captured territory.
        
        empty_board.place_piece(Placement("W1", 1, (0, 1), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (1, 0), 0, PlayerColor.WHITE))
        
        # (0,0) is now White's territory.
        # White attempts to build a Tavern there.
        result = empty_board.place_piece(Placement("W_INSIDE", 1, (0, 0), 0, PlayerColor.WHITE))
        
        assert result is not None, "Player should be able to build on their own territory"

    def test_build_on_enemy_territory_blocked(self, empty_board):
        # Players must be strictly blocked from building on the opponent's territory.
        
        # White secures the corner (0,0)
        empty_board.place_piece(Placement("W1", 1, (0, 1), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (1, 0), 0, PlayerColor.WHITE))
        
        # Red attempts to build on White's territory
        result = empty_board.place_piece(Placement("R1", 2, (0, 0), 0, PlayerColor.RED))
        
        assert result is None, "Opponent should be blocked from building on captured territory"


class TestCaptureMechanics:

    def test_capture_exactly_one_enemy_piece(self, empty_board):
        # A single enemy piece fully enclosed by a player's wall should be captured.
        
        empty_board.place_piece(Placement("R1", 2, (0, 0), 0, PlayerColor.RED))
        
        empty_board.place_piece(Placement("W1", 1, (1, 0), 0, PlayerColor.WHITE))
        result = empty_board.place_piece(Placement("W2", 1, (0, 1), 0, PlayerColor.WHITE))
        
        assert result.captured is not None
        assert result.captured.token_id == "R1"
        assert (0, 0) in empty_board.territories[PlayerColor.WHITE], "The freed cell should be added to the territory"

    def test_do_not_capture_multiple_enemy_pieces(self, empty_board):
        # If a territory encloses MORE than one enemy piece, none should be captured.
        
        empty_board.place_piece(Placement("R1", 2, (0, 0), 0, PlayerColor.RED))
        empty_board.place_piece(Placement("R2", 2, (1, 0), 0, PlayerColor.RED))
        
        empty_board.place_piece(Placement("W1", 1, (2, 0), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (2, 1), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W3", 1, (1, 1), 0, PlayerColor.WHITE))
        result = empty_board.place_piece(Placement("W4", 1, (0, 1), 0, PlayerColor.WHITE))
        
        assert result.captured is None, "Two pieces enclosed should not trigger a capture"
        assert (0, 0) not in empty_board.territories[PlayerColor.WHITE], "Territory should not be granted if pieces are not captured"

    def test_do_not_capture_own_piece(self, empty_board):
        # Enclosing your own piece should NOT result in capturing it.
        
        empty_board.place_piece(Placement("W_INNER", 1, (0, 0), 0, PlayerColor.WHITE))
        
        empty_board.place_piece(Placement("W1", 1, (1, 0), 0, PlayerColor.WHITE))
        result = empty_board.place_piece(Placement("W2", 1, (0, 1), 0, PlayerColor.WHITE))
        
        assert result.captured is None, "Player cannot capture their own piece"

    def test_cathedral_interaction(self, empty_board):
        # Standard Cathedral rules often specify interactions with the neutral Cathedral (Piece ID 0).
        # We must verify if enclosing the neutral Cathedral (ID 0) alone captures it or not 
        # based on the strict engine logic.
        
        empty_board.place_piece(Placement("CATHEDRAL", 0, (0, 0), 0, PlayerColor.NEUTRAL))
        
        # Enclosing the Cathedral in the top-left corner
        empty_board.place_piece(Placement("W1", 1, (2, 0), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (2, 1), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W3", 1, (2, 2), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W4", 1, (1, 2), 0, PlayerColor.WHITE))
        result = empty_board.place_piece(Placement("W5", 1, (0, 2), 0, PlayerColor.WHITE))
        
        # Note: Depending on the specific iteration of the rules implemented in empty_board.py,
        # capturing neutral entities might be blocked by: 
        # `if len(interior) == 1 and interior[0].color == OPPOSITE[color]:`
        # Because OPPOSITE[WHITE] is RED, a NEUTRAL piece is not technically captured by current logic.
        assert result.captured is None, "Based on current engine logic, neutral pieces are not matching OPPOSITE[color]"

    def test_capture_large_piece(self, empty_board):
        # Ensuring multi-tile pieces are fully captured and all their tiles freed.
        
        # Red places a 2-tile Stable (Piece ID 4) at (0,0) and (0,1)
        empty_board.place_piece(Placement("R_STABLE", 4, (0, 0), 0, PlayerColor.RED))
        
        # White encloses it fully
        empty_board.place_piece(Placement("W1", 1, (1, 0), 0, PlayerColor.WHITE))
        empty_board.place_piece(Placement("W2", 1, (1, 1), 0, PlayerColor.WHITE))
        result = empty_board.place_piece(Placement("W3", 1, (0, 2), 0, PlayerColor.WHITE))
        
        assert result.captured is not None
        assert result.captured.token_id == "R_STABLE"
        
        # Both tiles previously occupied by the Stable should now be White's territory
        assert (0, 0) in empty_board.territories[PlayerColor.WHITE]
        assert (0, 1) in empty_board.territories[PlayerColor.WHITE]