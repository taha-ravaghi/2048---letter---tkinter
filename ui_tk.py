# ui_tk.py
# 2048 Letter Edition - Tkinter UI

import tkinter as tk
from tkinter import messagebox
import copy
import os

import game_logic as gl

HIGHSCORE_FILE = "highscore.txt"


def read_highscore():
    try:
        f = open(HIGHSCORE_FILE, "r", encoding="utf-8")
        s = f.read().strip()
        f.close()
        if s == "":
            return 0
        return int(s)
    except:
        return 0


def write_highscore(score):
    f = open(HIGHSCORE_FILE, "w", encoding="utf-8")
    f.write(str(score))
    f.close()


class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 (Letter Edition)")

        self.score = 0
        self.highscore = read_highscore()
        self.board = gl.create_board()

        # Undo
        self.history = []

        # Top bar
        top = tk.Frame(root)
        top.pack(padx=10, pady=10, fill="x")

        self.score_lbl = tk.Label(top, text="Score: 0", font=("Arial", 14))
        self.score_lbl.pack(side="left")

        self.high_lbl = tk.Label(top, text="High Score: 0", font=("Arial", 14))
        self.high_lbl.pack(side="left", padx=20)

        btns = tk.Frame(top)
        btns.pack(side="right")

        tk.Button(btns, text="New Game (N)", command=self.new_game).pack(side="left", padx=5)
        tk.Button(btns, text="Undo (U)", command=self.undo).pack(side="left", padx=5)

        # Grid
        grid = tk.Frame(root)
        grid.pack(padx=10, pady=10)

        self.cells = []
        for r in range(gl.SIZE):
            row = []
            for c in range(gl.SIZE):
                lbl = tk.Label(
                    grid,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 20, "bold"),
                    relief="ridge",
                    borderwidth=2
                )
                lbl.grid(row=r, column=c, padx=4, pady=4)
                row.append(lbl)
            self.cells.append(row)

        # Help
        help_txt = "Controls: W/A/S/D move | U undo (2) | N new game | Q quit"
        self.help_lbl = tk.Label(root, text=help_txt, font=("Arial", 11))
        self.help_lbl.pack(pady=(0, 10))

        # Key bindings
        self.root.bind("<Key>", self.on_key)

        self.new_game()

    def new_game(self):
        self.score = 0
        self.board = gl.create_board()
        self.history = []

        gl.add_random_tile(self.board)
        gl.add_random_tile(self.board)

        self.render()

    def undo(self):
        if len(self.history) > 0:
            last_board, last_score = self.history.pop()
            self.board = last_board
            self.score = last_score
            self.render()

    def render(self):
        # update highscore if needed
        if self.score > self.highscore:
            self.highscore = self.score
            write_highscore(self.highscore)

        self.score_lbl.config(text="Score: " + str(self.score))
        self.high_lbl.config(text="High Score: " + str(self.highscore))

        for r in range(gl.SIZE):
            for c in range(gl.SIZE):
                v = self.board[r][c]
                if v == gl.EMPTY:
                    self.cells[r][c].config(text="")
                else:
                    self.cells[r][c].config(text=v)

    def do_move(self, direction):
        # snapshot before move (for undo)
        board_before = copy.deepcopy(self.board)
        score_before = self.score

        if direction == "left":
            new_board, gained, changed = gl.move_left(self.board)
        elif direction == "right":
            new_board, gained, changed = gl.move_right(self.board)
        elif direction == "up":
            new_board, gained, changed = gl.move_up(self.board)
        else:
            new_board, gained, changed = gl.move_down(self.board)

        if not changed:
            return

        # save undo (keep only last 2)
        self.history.append((board_before, score_before))
        if len(self.history) > 2:
            self.history.pop(0)

        self.board = new_board
        self.score += gained
        gl.add_random_tile(self.board)
        self.render()

        if gl.has_won(self.board):
            messagebox.showinfo("You win!", "🎉 You reached Z! You win!")
        else:
            if not gl.can_move(self.board):
                messagebox.showinfo("Game Over", "No more moves.")

    def on_key(self, event):
        k = ""
        if event.char is not None:
            k = event.char.lower()

        if k == "q":
            self.root.destroy()
            return
        if k == "n":
            self.new_game()
            return
        if k == "u":
            self.undo()
            return

        if k == "a":
            self.do_move("left")
        elif k == "d":
            self.do_move("right")
        elif k == "w":
            self.do_move("up")
        elif k == "s":
            self.do_move("down")


if __name__ == "__main__":
    root = tk.Tk()
    GameUI(root)
    root.mainloop()