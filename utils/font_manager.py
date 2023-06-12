import pygame
from pygame.font import Font


class FontManager:
    fonts: dict[str, Font] = {}

    @staticmethod
    def get_font(font_name: str, size: int):
        font_id = f"{font_name}, {size}"
        if font_id in FontManager.fonts:
            return FontManager.fonts[font_id]
        FontManager.fonts[font_id] = pygame.font.SysFont(font_name, size)
        return FontManager.fonts[font_id]
