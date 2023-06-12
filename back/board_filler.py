from back.board import Board
from back.cell import Cell, CellTypes
from utils import possible_cords_to_go, emptys_around
from random import choice


class BoardFiller:
    @staticmethod
    def fill_board(board: Board, start_cord=None) -> None:
        booked_cells = set([start_cord] + possible_cords_to_go(board, start_cord)) if start_cord else set()
        height, width = board.size
        m_count = board.mines_count
        mines_placed = 0

        cells_to_fill = {
            h: [w for w in range(width) if (h, w) not in booked_cells] for h in range(height)
        }

        while m_count and cells_to_fill:
            h = choice(list(cells_to_fill.keys()))
            w = choice(cells_to_fill[h])
            mines_placed += 1
            board[h][w] = Cell(CellTypes.MINE)

            cells_to_fill[h].remove(w)
            if not cells_to_fill[h]:
                cells_to_fill.pop(h)

            m_count -= 1
            for y, x in possible_cords_to_go(board, (h, w)):
                cell = board[y][x]
                if cell.cell_type == CellTypes.EMPTY:
                    cell.mines_around += 1
        board.mines_count = mines_placed
