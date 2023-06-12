import pygame

from back.game_manager import MineGameManager
from front.constants import INFOPANEL_BACKGROUND_COLOR, FONT_NAME, FONT_SIZE
from utils.font_manager import FontManager


class InfoPanel:
    def __init__(self, gm: MineGameManager, pos=(0, 0), size=(100, 50), color=INFOPANEL_BACKGROUND_COLOR,
                 font_name=FONT_NAME, font_size=FONT_SIZE):
        self.gm = gm
        self.pos = pos
        self.color = color
        self.font_name = font_name
        self.font_size = font_size
        self.size = self.actual_size
        self.image = pygame.Surface(self.size).convert()

    def set_game_manager(self, gm):
        self.gm = gm

    @property
    def message(self):
        if not self.gm.is_board_inited():
            return f"Mines left: UNKNOWN"
        else:
            return f"Mines left: {self.gm.flagged_left}"

    @property
    def actual_size(self):
        return FontManager.get_font(self.font_name, self.font_size).size(self.message)

    def draw(self, surface):
        self.image.fill(self.color)
        text = FontManager.get_font(self.font_name, self.font_size).render(
            self.message, True, (255, 255, 255)
        )
        surface.blit(self.image, self.pos)
        surface.blit(text, self.pos)

