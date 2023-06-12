from back.board import Board
import pygame


from back.cell import Cell
from front.constants import BOARD_BACKGROUND_COLOR
from front.fcell import FCell


class FBoard:
    def __init__(self, board: Board, cell_size=(20, 20), pos=(0, 0),
                 border=0, cell_drawer=FCell()):
        self.color = BOARD_BACKGROUND_COLOR
        self.board = board
        self.cell_size = cell_size
        self.border = border
        self.pos = pos
        self.image = pygame.Surface(self.size).convert()
        self.image.fill(BOARD_BACKGROUND_COLOR)
        self.cd = cell_drawer

    def set_cell_drawer(self, cell_drawer):
        self.cd = cell_drawer

    @property
    def size(self):
        return self.get_fsize_depends_on_board(self.board.size, self.border, self.cell_size)

    @staticmethod
    def get_fsize_depends_on_board(board_size, border, cell_size=(20, 20)):
        return (
            board_size[0] * cell_size[0] + border * (board_size[0] + 1),
            board_size[1] * cell_size[1] + border * (board_size[1] + 1),
        )

    @staticmethod
    def get_cell_size_depends_on_parametrs(board_size, border, surface_size):
        cell_size = min(
            (border * (board_size[0] + 1) - surface_size[0]) // -board_size[0],
            (border * (board_size[1] + 1) - surface_size[1]) // -board_size[1]
        )
        return cell_size, cell_size

    def cell_cords_iterator(self) -> tuple[Cell, tuple[int, int], tuple[int, int]]:
        y_board, x_board = self.pos
        for y, line in enumerate(self.board):
            fy = y * self.cell_size[0] + self.border * (y + 1) + y_board
            for x, cell in enumerate(line):
                fx = x * self.cell_size[1] + self.border * (x + 1) + x_board
                yield cell, (fy, fx), (y, x)

    def get_cords_by_fcords(self, fcords):
        for _, fcell_cords, cell_cords in self.cell_cords_iterator():
            fy, fx = fcell_cords
            y, x = cell_cords
            if fy <= fcords[0] <= fy + self.cell_size[0] and \
                    fx <= fcords[1] <= fx + self.cell_size[1]:
                return y, x

    def draw(self, surface):
        surface.blit(self.image, self.pos)
        for cell_with_cord in self.cell_cords_iterator():
            cell, fcell_fcords, _ = cell_with_cord
            self.cd.draw(surface, cell, self.cell_size, fcell_fcords)
