import pygame

from game.mine_game import MineGame


def set_full_screen(minegame: MineGame, center=False, display=0):
    display_size = pygame.display.get_desktop_sizes()[display]
    cell_size = minegame.fboard.get_cell_size_depends_on_parametrs(
        minegame.board.size,
        minegame.fboard.border,
        (
            display_size[0] - minegame.info_panel.actual_size[0] - minegame.border * 3,
            display_size[1] - minegame.info_panel.actual_size[1] - minegame.border * 3
        )
    )
    minegame.fboard.cell_size = cell_size
    pygame.display.quit()
    minegame.surface = pygame.display.set_mode(display_size, pygame.FULLSCREEN, display=display)
    if not center:
        return
    center_pos = (
        (display_size[0] - minegame.drawer.size[0]) // 2, 0
    )

    minegame.pos = center_pos
    minegame.move(center_pos)
