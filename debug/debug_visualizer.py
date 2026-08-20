"""
debug_visualizer.py
-------------------
Tkinter debug window for the Cathedral board game.
Place next to run.py at the project root.

Game structure used:
  game.board                : Board
  game.moves                : list[Move]   (Move has .placement: Placement)
  game.current_turn         : PlayerColor
  game.status               : GameStatus
  game.result               : GameResult | None
  game.white_time_left      : float  (seconds)
  game.red_time_left        : float  (seconds)
  game.pieces_on_hand       : dict[PlayerColor, dict[int, int]]
  game.players              : bidict[player_id -> PlayerColor]
"""

import tkinter as tk
from backend.models.enums import PlayerColor, GameStatus
from backend.models.piece import PASS_TURN_ID

# ── visual constants ──────────────────────────────────────────────────────────

CELL    = 46
GRID    = 10
PAD     = 20
REFRESH = 1500        # auto-refresh ms

BG          = "#1e1e1e"
HEADER_BG   = "#252525"
BTN_BG      = "#383838"
BTN_FG      = "#e0e0e0"
ACCENT      = "#5b8dd9"
DIM         = "#777777"
MONO        = ("Courier New", 10)
MONO_SM     = ("Courier New", 9)

CELL_FILL = {
    PlayerColor.NEUTRAL: "#3b2a1e",
    PlayerColor.WHITE:   "#ddd0b3",
    PlayerColor.RED:     "#9b2418",
}
PIECE_FG = {
    PlayerColor.WHITE: "#1a1a1a",
    PlayerColor.RED:   "#f5ddb0",
}
TERR_FILL = {
    PlayerColor.WHITE: "#b8c9a0",
    PlayerColor.RED:   "#c08070",
}
ROW_TAG = {
    PlayerColor.WHITE:   "w",
    PlayerColor.RED:     "r",
    PlayerColor.NEUTRAL: "n",
}


def _fmt_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


class DebugVisualizer:
    def __init__(self, game_manager):
        self.gm          = game_manager
        self.game_ids    = []
        self.current_idx = 0

        self.root = tk.Tk()
        self.root.title("Cathedral — Debug")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._build_ui()
        self._schedule_refresh()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        W = CELL * GRID + PAD * 2   # canvas width

        # header
        hdr = tk.Frame(self.root, bg=HEADER_BG, pady=8)
        hdr.pack(fill="x")

        self._btn(hdr, "◀", self._prev).pack(side="left", padx=(12, 4))
        self.lbl_game = tk.Label(
            hdr, text="— no active games —", bg=HEADER_BG, fg="#cccccc",
            font=("Courier New", 12, "bold"), width=28,
        )
        self.lbl_game.pack(side="left")
        self._btn(hdr, "▶", self._next).pack(side="left", padx=(4, 0))
        self._btn(hdr, "⟳", self._refresh, accent=True).pack(side="right", padx=12)

        # board
        self.canvas = tk.Canvas(
            self.root, width=W, height=W,
            bg="#120d09", bd=0, highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=(10, 0))

        # ── status row ──
        status_frame = tk.Frame(self.root, bg=BG)
        status_frame.pack(fill="x", padx=14, pady=(6, 0))

        self.lbl_status = tk.Label(
            status_frame, text="", bg=BG, fg="#cccccc",
            font=MONO, anchor="w",
        )
        self.lbl_status.pack(side="left")

        self.lbl_turn = tk.Label(
            status_frame, text="", bg=BG, fg=ACCENT,
            font=("Courier New", 10, "bold"), anchor="e",
        )
        self.lbl_turn.pack(side="right")

        # ── time + pieces on hand ──
        info_frame = tk.Frame(self.root, bg=BG)
        info_frame.pack(fill="x", padx=14, pady=(4, 0))

        self.lbl_white = tk.Label(
            info_frame, text="", bg="#2a2820", fg="#ddd0b3",
            font=MONO, anchor="w", padx=6, pady=3,
        )
        self.lbl_white.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.lbl_red = tk.Label(
            info_frame, text="", bg="#2a1818", fg="#e07060",
            font=MONO, anchor="w", padx=6, pady=3,
        )
        self.lbl_red.pack(side="left", fill="x", expand=True)

        # ── last move ──
        tk.Label(self.root, text="LAST MOVE", bg=BG, fg=DIM,
                 font=("Courier New", 8, "bold"), anchor="w",
                 ).pack(fill="x", padx=14, pady=(8, 0))

        self.lbl_move = tk.Label(
            self.root, text="(no moves yet)", bg="#161616", fg="#c0c0c0",
            font=MONO, anchor="w", justify="left", padx=8, pady=5,
            wraplength=W,
        )
        self.lbl_move.pack(fill="x", padx=14)

        # ── placements table ──
        tk.Label(self.root, text="PLACED PIECES", bg=BG, fg=DIM,
                 font=("Courier New", 8, "bold"), anchor="w",
                 ).pack(fill="x", padx=14, pady=(8, 0))

        frame_txt = tk.Frame(self.root, bg=BG)
        frame_txt.pack(fill="x", padx=14, pady=(0, 14))

        self.txt = tk.Text(
            frame_txt, width=62, height=9,
            bg="#161616", fg="#aaaaaa",
            font=MONO_SM, bd=0, relief="flat", state="disabled",
        )
        sb = tk.Scrollbar(frame_txt, command=self.txt.yview, bg=BG)
        self.txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.txt.pack(side="left", fill="both")

        self.txt.tag_config("hdr", foreground=ACCENT)
        self.txt.tag_config("w",   foreground="#ddd0b3")
        self.txt.tag_config("r",   foreground="#e07060")
        self.txt.tag_config("n",   foreground=DIM)

    def _btn(self, parent, text, cmd, accent=False):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=ACCENT if accent else BTN_BG, fg=BTN_FG,
            activebackground="#7aaae8" if accent else "#484848",
            relief="flat", bd=0, padx=10, pady=4,
            font=("Courier New", 11),
        )

    # ── navigation ────────────────────────────────────────────────────────────

    def _prev(self):
        if self.game_ids:
            self.current_idx = (self.current_idx - 1) % len(self.game_ids)
            self._refresh()

    def _next(self):
        if self.game_ids:
            self.current_idx = (self.current_idx + 1) % len(self.game_ids)
            self._refresh()

    def _schedule_refresh(self):
        self._refresh()
        self.root.after(REFRESH, self._schedule_refresh)

    # ── refresh ───────────────────────────────────────────────────────────────

    def _refresh(self):
        self.game_ids = list(self.gm.active_games.keys())

        if not self.game_ids:
            self.lbl_game.config(text="— no active games —")
            self.lbl_status.config(text="")
            self.lbl_turn.config(text="")
            self.lbl_white.config(text="White  —:——")
            self.lbl_red.config(text="Red    —:——")
            self.lbl_move.config(text="(no games)")
            self._draw_empty()
            self._set_txt("(no games)", "n")
            return

        self.current_idx = min(self.current_idx, len(self.game_ids) - 1)
        gid  = self.game_ids[self.current_idx]
        game = self.gm.active_games[gid]

        self.lbl_game.config(
            text=f"game #{gid}  ({self.current_idx + 1}/{len(self.game_ids)})"
        )

        self._draw_board(game.board)
        self._update_status(game)
        self._update_last_move(game)
        self._update_placements(game.board)

    # ── board ─────────────────────────────────────────────────────────────────

    def _draw_empty(self):
        self.canvas.delete("all")
        for r in range(GRID):
            for c in range(GRID):
                x0, y0 = PAD + c * CELL, PAD + r * CELL
                self.canvas.create_rectangle(
                    x0, y0, x0 + CELL, y0 + CELL,
                    fill=CELL_FILL[PlayerColor.NEUTRAL], outline="#1a0f0a", width=1,
                )

    def _draw_board(self, board):
        self.canvas.delete("all")

        # territory tints
        for color, tiles in board.territories.items():
            tint = TERR_FILL.get(color)
            if not tint:
                continue
            for tx, ty in tiles:
                x0, y0 = PAD + tx * CELL, PAD + ty * CELL
                self.canvas.create_rectangle(
                    x0 + 1, y0 + 1, x0 + CELL - 1, y0 + CELL - 1,
                    fill=tint, outline="", width=0,
                )

        # cells
        for r in range(GRID):
            for c in range(GRID):
                cell = board.grid[r][c]
                pc   = cell.player_color
                x0, y0 = PAD + c * CELL, PAD + r * CELL
                self.canvas.create_rectangle(
                    x0, y0, x0 + CELL, y0 + CELL,
                    fill=CELL_FILL.get(pc, CELL_FILL[PlayerColor.NEUTRAL]),
                    outline="#1a0f0a", width=1,
                )
                if pc != PlayerColor.NEUTRAL:
                    self.canvas.create_text(
                        x0 + CELL // 2, y0 + CELL // 2,
                        text=str(cell.piece_id),
                        fill=PIECE_FG.get(pc, "#ccc"),
                        font=("Courier New", 9, "bold"),
                    )

        # grid lines + coord labels
        total = CELL * GRID
        for i in range(GRID + 1):
            self.canvas.create_line(PAD + i*CELL, PAD, PAD + i*CELL, PAD+total, fill="#1a0f0a")
            self.canvas.create_line(PAD, PAD + i*CELL, PAD+total, PAD + i*CELL, fill="#1a0f0a")
        for i in range(GRID):
            self.canvas.create_text(PAD + i*CELL + CELL//2, PAD - 7,
                                    text=chr(ord("A")+i), fill=DIM, font=("Courier New", 8))
            self.canvas.create_text(PAD - 9, PAD + i*CELL + CELL//2,
                                    text=str(i), fill=DIM, font=("Courier New", 8))

    # ── status / time / hand ──────────────────────────────────────────────────

    def _update_status(self, game):
        status_str = game.status.value.upper()
        if game.result:
            status_str += f"  [{game.result.value}]"
        self.lbl_status.config(text=status_str)

        if game.status == GameStatus.IN_PROGRESS:
            turn_color = game.current_turn.value.upper()
            self.lbl_turn.config(text=f"▶ {turn_color}'s turn")
        else:
            self.lbl_turn.config(text="")

        # pieces counts
        w_hand = game.pieces_on_hand.get(PlayerColor.WHITE, {})
        r_hand = game.pieces_on_hand.get(PlayerColor.RED,   {})
        w_total = sum(w_hand.values())
        r_total = sum(r_hand.values())

        self.lbl_white.config(
            text=f"White  {_fmt_time(game.white_time_left)}  ·  {w_total} piece(s) left"
        )
        self.lbl_red.config(
            text=f"Red    {_fmt_time(game.red_time_left)}  ·  {r_total} piece(s) left"
        )

    # ── last move ─────────────────────────────────────────────────────────────

    def _update_last_move(self, game):
        if not game.moves:
            self.lbl_move.config(text="(no moves yet)")
            return

        mv = game.moves[-1]
        p  = mv.placement
        move_num = len(game.moves)

        if p.piece_id == PASS_TURN_ID:
            text = f"#{move_num}  PASS  ({p.color.value})"
        else:
            col_letter = chr(ord("A") + p.anchor[0])
            row_num    = p.anchor[1]
            text = (
                f"#{move_num}  piece_id={p.piece_id}"
                f"  anchor={col_letter}{row_num}"
                f"  rot={p.rotation}"
                f"  color={p.color.value}"
            )
            if hasattr(mv, "move_timestamp") and mv.move_timestamp:
                text += f"  @ {mv.move_timestamp}"

        self.lbl_move.config(text=text)

    # ── placements table ──────────────────────────────────────────────────────

    def _update_placements(self, board):
        HDR = f"{'TOKEN':<22} {'PID':>4} {'ANCHOR':>7} {'ROT':>4}  COLOR\n"
        SEP = "─" * 52 + "\n"

        self._set_txt(HDR, "hdr", clear=True)
        self._append(SEP, "n")

        for tid, p in board.placements.items():
            col_letter = chr(ord("A") + p.anchor[0])
            row_num    = p.anchor[1]
            line = (
                f"{tid:<22} {p.piece_id:>4}"
                f"  {col_letter}{row_num:>2}"
                f" {p.rotation:>4}  {p.color.value}\n"
            )
            self._append(line, ROW_TAG.get(p.color, "n"))

    # ── text widget helpers ───────────────────────────────────────────────────

    def _set_txt(self, text, tag, clear=True):
        self.txt.config(state="normal")
        if clear:
            self.txt.delete("1.0", "end")
        self.txt.insert("end", text, tag)
        self.txt.config(state="disabled")

    def _append(self, text, tag):
        self.txt.config(state="normal")
        self.txt.insert("end", text, tag)
        self.txt.config(state="disabled")

    # ── entry point ───────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()
