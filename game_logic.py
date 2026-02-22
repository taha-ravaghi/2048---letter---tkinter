# game_logic.py
# 2048 Letter Edition - Game Logic

import random

SIZE = 4
EMPTY = 'emp'


def letter_to_value(ch):
    # A -> 2, B -> 4, ..., Z -> 2**26
    idx = ord(ch) - ord('A') + 1
    return 2 ** idx


def create_board():
    board = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            row.append(EMPTY)
        board.append(row)
    return board


def empty_cells(board):
    cells = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == EMPTY:
                cells.append((r, c))
    return cells


def add_random_tile(board):
    cells = empty_cells(board)
    if len(cells) == 0:
        return False

    r, c = random.choice(cells)
    
    if random.random() < 0.9:
        board[r][c] = 'A'
    else:
        board[r][c] = 'B'
    return True


def merge_line_left(line):
    # 1) remove EMPTY
    tiles = []
    for x in line:
        if x != EMPTY:
            tiles.append(x)

    # 2) merge
    new_tiles = []
    gained = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            if tiles[i] == 'Z':
                
                new_tiles.append(tiles[i])
                i += 1
            else:
                merged = chr(ord(tiles[i]) + 1) 
                new_tiles.append(merged)
                gained += letter_to_value(merged)
                i += 2
        else:
            new_tiles.append(tiles[i])
            i += 1

    # 3) pad with EMPTY to length SIZE
    while len(new_tiles) < SIZE:
        new_tiles.append(EMPTY)

    return new_tiles, gained


def transpose(board):
    
    t = []
    for c in range(SIZE):
        row = []
        for r in range(SIZE):
            row.append(board[r][c])
        t.append(row)
    return t


def reverse_rows(board):
    new_board = []
    for r in range(SIZE):
        new_board.append(list(reversed(board[r])))
    return new_board


def move_left(board):
    new_board = []
    gained_total = 0
    changed = False

    for r in range(SIZE):
        merged_row, gained = merge_line_left(board[r])
        new_board.append(merged_row)
        gained_total += gained
        if merged_row != board[r]:
            changed = True

    return new_board, gained_total, changed


def move_right(board):
    rev = reverse_rows(board)
    moved, gained, changed = move_left(rev)
    return reverse_rows(moved), gained, changed


def move_up(board):
    t = transpose(board)
    moved, gained, changed = move_left(t)
    return transpose(moved), gained, changed


def move_down(board):
    t = transpose(board)
    moved, gained, changed = move_right(t)
    return transpose(moved), gained, changed


def has_won(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 'Z':
                return True
    return False


def can_move(board):
    # any empty cell => can move
    if len(empty_cells(board)) > 0:
        return True

    # check any adjacent equal horizontally/vertically
    for r in range(SIZE):
        for c in range(SIZE):
            v = board[r][c]
            if c + 1 < SIZE and board[r][c + 1] == v:
                return True
            if r + 1 < SIZE and board[r + 1][c] == v:
                return True

    return False