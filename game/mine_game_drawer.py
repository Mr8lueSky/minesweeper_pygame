from pygame import Surface

from front.fboard import FBoard
from front.info_panel import InfoPanel


class MineGameDrawer:
    def __init__(self, fboard: FBoard, info_panel: InfoPanel, border):
        self.fboard = fboard
        self.info_panel = info_panel
        self.border = border

    @property
    def size(self):
        f_y, f_x = self.fboard.size
        i_y, i_x = self.info_panel.actual_size
        return (
            max(f_y, i_y) + self.border * 2,
            f_x + i_x + self.border * 3
        )

    def draw(self, surface: Surface):
        self.fboard.draw(surface)
        self.info_panel.draw(surface)
