class CellTypes:
    EMPTY = "EMPTY"
    MINE = "MINE"


class Cell:
    def __init__(self, cell_type, mines_around=0):
        self.cell_type = cell_type
        self.is_flagged = False
        self.is_opened = False
        self.mines_around = mines_around

    def __repr__(self):
        if self.cell_type == CellTypes.MINE:
            return "M" + ('O' if self.is_opened else 'C')
        else:
            return "E" + ('O' if self.is_opened else 'C')
