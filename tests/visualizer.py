import tkinter as tk
from backend.engine.board import Board
from backend.models.enums import PlayerColor
from backend.models.placement import Placement
from backend.models.piece import EMPTY_TILE

class BoardVisualizer:
    def __init__(self, board: Board, cell_size: int = 50):
        self.board = board
        self.cell_size = cell_size
        self.cols = len(board.grid[0])
        self.rows = len(board.grid)
        
        self.root = tk.Tk()
        self.root.title("Board Visualization")
        
        self.canvas = tk.Canvas(
            self.root, 
            width=self.cols * self.cell_size, 
            height=self.rows * self.cell_size
        )
        self.canvas.pack()
        self.draw_board()

    def get_color_for_cell(self, cell):
        """Returns the hex color based on the cell's state."""
        if cell.piece_id == EMPTY_TILE:
            return "#FFFFFF"  # White (empty)
        
        if cell.player_color == PlayerColor.WHITE:
            return "#D3D3D3"  # Light gray
        elif cell.player_color == PlayerColor.RED:
            return "#FF9999"  # Red
        elif cell.player_color == PlayerColor.NEUTRAL:
            return "#808080"  # Dark gray (e.g. Cathedral)
        
        return "#000000"

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.board.grid[y][x]
                color = self.get_color_for_cell(cell)
                
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=color, 
                    outline="black"
                )
                
                # Render the piece_id if the tile is not empty
                if cell.piece_id != EMPTY_TILE:
                    self.canvas.create_text(
                        x1 + self.cell_size/2, 
                        y1 + self.cell_size/2, 
                        text=str(cell.piece_id)
                    )

    def run(self):
        self.root.mainloop()

# Startup script
if __name__ == "__main__":
    # Initialize example board
    game_board = Board()
    
    # Place sample pieces (using Cathedral and Red/White Towers based on PIECE_CATALOG)
    game_board.place_piece(Placement(token_id="", piece_id=0, anchor=(4, 4), rotation=0, color=PlayerColor.NEUTRAL))
    game_board.place_piece(Placement(token_id="", piece_id=22, anchor=(2, 8), rotation=1, color=PlayerColor.RED))
    game_board.place_piece(Placement(token_id="", piece_id=21, anchor=(8, 2), rotation=0, color=PlayerColor.WHITE))
    
    # Start the visualization application
    app = BoardVisualizer(game_board)
    app.run()