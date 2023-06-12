from functools import reduce
from typing import Optional

from back.board import Board
from back.board_filler import BoardFiller
from back.cell import CellTypes
from utils import emptys_around, possible_cords_to_go


class BoardNotInitializedException(Exception):
    ...


class MineGameManager:
    def __init__(self, board=None, board_filler=BoardFiller):
        self._board = None
        self.flagged_left = None
        self.actual_flagged_left = None
        self.empty_left = None
        self._board_initialized = False
        if board:
            self.set_board(board)
        self.board_filler = board_filler

    def set_board(self, board):
        self._board = board
        self.flagged_left = board.mines_count
        self.actual_flagged_left = board.mines_count
        self.empty_left = (board.size[0] * board.size[1]) - board.mines_count
        self._board_initialized = False

    def is_board_inited(self):
        return self._board_initialized

    def check_board_inited(self, starting_cord):
        if not self._board_initialized:
            self.board_filler.fill_board(self._board, starting_cord)
            self._board_initialized = True

    def open_opened_cell(self, y: int, x: int, cell, possible_cords: list[tuple[int, int]]):
        if cell.is_opened:
            flagged_count = len([self._board[y_n][x_n]
                                 for y_n, x_n in possible_cords if self._board[y_n][x_n].is_flagged])
            if cell.mines_around and flagged_count == cell.mines_around:
                for y_n, x_n in possible_cords:
                    neib_cell = self._board[y_n][x_n]
                    if not neib_cell.is_flagged and not neib_cell.is_opened:
                        self.open_cell((y_n, x_n))
            return True
        return False

    def open_cell(self, cord: tuple[int, int]) -> Optional[int]:
        self.check_board_inited(cord)
        y, x = cord
        cell = self._board[y][x]

        possible_cords = possible_cords_to_go(self._board, cord)

        if cell.is_flagged or self.open_opened_cell(y, x, cell, possible_cords):
            return

        if cell.cell_type == CellTypes.MINE:
            raise Exception("BABAH")
        if not cell.is_opened:
            self.empty_left -= 1
            cell.is_opened = True
        empty_cords = emptys_around(self._board, cord)
        if empty_cords == len(possible_cords):
            for cord in possible_cords:
                self.open_cell(cord)
        return cell.mines_around

    def flag_opened_cell(self, y, x, cell):
        cord = y, x
        if cell.is_opened:
            possible_cords = possible_cords_to_go(self._board, cord)
            not_flagged_count = len([self._board[y_n][x_n]
                                     for y_n, x_n in possible_cords if not self._board[y_n][x_n].is_flagged
                                     and not self._board[y_n][x_n].is_opened])
            flagged_count = len([self._board[y_n][x_n]
                                 for y_n, x_n in possible_cords if self._board[y_n][x_n].is_flagged])
            if cell.mines_around and not_flagged_count + flagged_count == cell.mines_around:
                for y_n, x_n in possible_cords:
                    neib_cell = self._board[y_n][x_n]
                    if not neib_cell.is_flagged and not neib_cell.is_opened:
                        self.flag_cell((y_n, x_n))
            return True
        return False

    def flag_cell(self, cord):
        if not self.is_board_inited():
            return
        y, x = cord
        cell = self._board[y][x]
        if self.flag_opened_cell(y, x, cell):
            return
        if cell.is_flagged:
            if cell.cell_type == CellTypes.MINE:
                self.actual_flagged_left += 1
            self.flagged_left += 1
            cell.is_flagged = False
        else:
            if cell.cell_type == CellTypes.MINE:
                self.actual_flagged_left -= 1
            self.flagged_left -= 1
            cell.is_flagged = True

    def is_done(self):
        return not self.actual_flagged_left and not self.empty_left
