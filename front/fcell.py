import pygame

from back.cell import CellTypes
from front.constants import OPENED_CELL_COLOR, FLAGGED_CELL_COLOR, DEFAULT_CELL_COLOR, FONT_NAME, FONT_SIZE, FONT_COLOR
from utils.font_manager import FontManager


class FCell:
    def __init__(self, font_name=FONT_NAME, font_size=FONT_SIZE):
        self.font_name = font_name
        self.font_size = font_size
        self._font = None

    @property
    def font(self):
        return FontManager.get_font(self.font_name, self.font_size)

    def draw(self, surface, fcell, size, fpos):
        if fcell.is_opened:
            color = OPENED_CELL_COLOR
        elif fcell.is_flagged:
            color = FLAGGED_CELL_COLOR
        else:
            color = DEFAULT_CELL_COLOR

        image = pygame.Surface(size).convert()
        image.fill(color)
        surface.blit(image, fpos)
        if fcell.cell_type == CellTypes.EMPTY and fcell.is_opened and fcell.mines_around:
            text = self.font.render(str(fcell.mines_around), True, FONT_COLOR)
            text_size = text.get_size()
            text_pos = (
                (size[0] - text_size[0]) // 2 + fpos[0],
                (size[1] - text_size[1]) // 2 + fpos[1]
            )
            surface.blit(text, text_pos)
