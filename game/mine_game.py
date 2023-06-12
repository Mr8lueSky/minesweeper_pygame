import pygame

from back.board import Board
from back.board_filler import BoardFiller
from back.game_manager import MineGameManager
from front.constants import GAME_BACKGROUND_COLOR
from front.fboard import FBoard
from front.info_panel import InfoPanel
from game.mine_event_handler import MineEventHandler
from game.mine_game_drawer import MineGameDrawer


class MineGame:
    def __init__(self, surface=None, board_size=(10, 10), mines_count=5, event_handler=None, board=None,
                 b_filler=BoardFiller, fb_border=1, border=5, pos=(0, 0)):
        pygame.init()
        self.border = border
        self.pos = pos
        self.surface = surface if surface else pygame.display.set_mode((1, 1))
        self.board = Board(board_size, mines_count) if board is None else board
        self.b_filler = b_filler
        self.gm = MineGameManager(self.board)
        self.info_panel = InfoPanel(self.gm)
        self.fboard = FBoard(self.board, border=fb_border)
        self.event_handler = MineEventHandler(self.gm, self.fboard) \
            if event_handler is None else event_handler
        self.drawer = MineGameDrawer(self.fboard, self.info_panel, border)
        self.surface = pygame.display.set_mode(self.drawer.size)
        self.CL = pygame.time.Clock()
        self.running = False
        self.move(pos)
        self.plugins = []

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
            self.info_panel.size[1] + self.drawer.border * 2 + new_pos[1]
        )

    def quit(self, event=None):
        self.running = False

    def start_game(self):
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
