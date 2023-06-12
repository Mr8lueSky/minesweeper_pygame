from back.cell import Cell, CellTypes


class Board:
    def __init__(self, size: tuple[int, int], mines_count: int):
        if size[0] * size[1] < mines_count:
            raise Exception("Not enough room for all mines!")
        self.size = size
        self.mines_count = mines_count
        self.board = [
            [Cell(CellTypes.EMPTY) for _ in range(size[1])] for _ in range(size[0])
        ]

    def __getitem__(self, item):
        return self.board[item]

    def __len__(self):
        return self.size[0]

    def __repr__(self):
        return "\n".join([str(x) for x in self.board])
