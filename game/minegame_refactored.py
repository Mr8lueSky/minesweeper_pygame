import pygame

from back.board import Board
from back.board_filler import BoardFiller
from back.game_manager_refactored import MineGameManager
from front.constants import GAME_BACKGROUND_COLOR
from front.fboard_refactored import FBoard
from front.info_panel import InfoPanel
from game.mine_event_handler_refactored import MineEventHandler
from game.mine_game_drawer_refactored import MineGameDrawer


class MineGame:
    def __init__(self, surface=None, event_handler=None, border=5, pos=(0, 0)):
        pygame.init()
        self.fboard = None
        self.border = border
        self.pos = pos
        self.surface = surface if surface else pygame.display.set_mode((1, 1))
        self.gm = MineGameManager()
        self.info_panel = None
        self.event_handler = MineEventHandler(self.gm, self.fboard) \
            if event_handler is None else event_handler
        self.drawer = None
        self.surface = None
        self.CL = pygame.time.Clock()
        self.running = False
        self.board = None
        self.plugins = []

    def set_info_panel(self, info_panel):
        self.info_panel = info_panel
        if self.drawer:
            self.drawer.set_fboard(info_panel)
        return self

    def set_gm(self, gm):
        if self.info_panel:
            self.info_panel.set_game_manager(gm)
        if self.event_handler:
            self.event_handler.set_gm(gm)
        self.gm = gm
        return self

    def set_drawer(self, drawer: MineGameDrawer):
        self.drawer = drawer
        self.surface = pygame.display.set_mode(self.drawer.size)
        if self.fboard:
            drawer.set_fboard(self.fboard)
        return self

    def set_board(self, board):
        self.board = board
        if self.fboard:
            self.fboard.set_board(board)
        if self.gm:
            self.gm.set_board(board)
        return self

    def set_fboard(self, fboard):
        self.fboard = fboard
        if self.drawer:
            self.drawer.set_fboard(fboard)
        if self.event_handler:
            self.event_handler.set_fboard(fboard)
        return self

    def clear_before_reset(self):
        self.running = False
        del self.board
        del self.gm
        del self.info_panel
        del self.fboard
        del self.event_handler
        del self.drawer

    def reset(self):
        self.board = Board(self.board.size, self.board.mines_count)
        self.gm = MineGameManager(self.board)
        self.info_panel = InfoPanel(self.gm)
        self.fboard = FBoard(self.board, border=self.fboard.border, cell_size=self.fboard.cell_size)
        self.event_handler = MineEventHandler(self.gm, self.fboard)
        self.drawer = MineGameDrawer(self.fboard, self.info_panel, self.drawer.border)
        self.running = True
        self.move(self.pos)

    def move(self, new_pos):
        self.pos = new_pos
        self.info_panel.pos = (
            self.drawer.border + new_pos[0],
            self.drawer.border + new_pos[1]
        )
        self.fboard.pos = (
            self.drawer.border + new_pos[0],
            self.drawer.size[1] + self.drawer.border * 2 + new_pos[1]
        )

    def quit(self, event=None):
        self.running = False

    def start_game(self):
        self.move(self.pos)
        self.running = True
        self._main_loop()

    def _main_loop(self):
        while self.running:
            self.CL.tick(60)
            self.surface.fill(GAME_BACKGROUND_COLOR)
            self.event_handler.handle_events()
            self.drawer.draw(self.surface)
            pygame.display.flip()
            for plugin in self.plugins:
                plugin.update()
