from back.board import Board
from back.cell import CellTypes, Cell

_directions = (
    (0, 1),
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (1, -1),
    (-1, 1)
)


def possible_cords_to_go(board: Board, cord: tuple[int, int]) -> list[tuple[int, int]]:
    cords = []
    y, x = cord
    y_size, x_size = len(board), len(board[0])
    for direction in _directions:
        y_dir, x_dir = direction
        if 0 <= y + y_dir < y_size and 0 <= x + x_dir < x_size:
            cords.append((y + y_dir, x + x_dir))
    return cords


def mines_around(board: Board, cord: tuple[int, int]) -> int:
    count = 0
    for cord in possible_cords_to_go(board, cord):
        y, x = cord
        if board[y][x].cell_type == CellTypes.MINE:
            count += 1
    return count


def emptys_around(board: Board, cord: tuple[int, int]) -> int:
    count = 0
    for cord in possible_cords_to_go(board, cord):
        y, x = cord
        if board[y][x].cell_type == CellTypes.EMPTY:
            count += 1
    return count


def opened_around(board: Board, cord: tuple[int, int]) -> list:
    cords = []
    for cord in possible_cords_to_go(board, cord):
        y, x = cord
        if board[y][x].is_opened:
            cords.append((y, x))
    return cords


def closed_around(board: Board, cord: tuple[int, int]) -> list:
    cords = []
    for cord in possible_cords_to_go(board, cord):
        y, x = cord
        if not board[y][x].is_opened:
            cords.append((y, x))
    return cords

def flagged_around(board: Board, cord: tuple[int, int]) -> list:
    cords = []
    for cord in possible_cords_to_go(board, cord):
        y, x = cord
        if board[y][x].is_flagged:
            cords.append((y, x))
    return cords
