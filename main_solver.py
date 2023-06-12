from time import time, sleep

from pygame import K_SPACE, KEYDOWN, K_ESCAPE

from back.game_manager import MineGameManager
from game.mine_game import MineGame
from utils import flagged_around, closed_around, opened_around
from utils.game_window_modes import set_full_screen
from threading import Thread


class Solver:
    def __init__(self, gm: MineGameManager, threads=False):
        self.working = False
        self.last_auto = time()
        self.auto_latency = 0.001
        self.gm = gm
        self.solve = self.solve_iterator()
        self.thread = None
        self.threads = threads

    def update(self):
        if self.threads:
            if self.working and self.thread is None:
                self.thread = Thread(target=self.solve_thread)
                self.thread.start()
            return
        if self.working and time() - self.last_auto >= self.auto_latency:
            self.last_auto = time()
            try:
                next(self.solve)
            except StopIteration:
                print("CAN't SoLve")
                self.working = False
                reinit()

    def handle_key(self, event):
        if event.key == K_SPACE:
            self.working = not self.working
            if self.working and self.threads:
                self.thread = Thread(target=self.solve_thread)
                self.thread.start()
            elif self.thread:
                self.thread = None
        if event.key == K_ESCAPE:
            self.working = False
            global is_working
            is_working = False

    def solve_thread(self):
        for _ in self.solve_iterator():
            if not self.working:
                break
            sleep(self.auto_latency)

    def quit_solver(self):
        print("dying")
        self.working = False

    def solve_iterator(self):
        board = self.gm.board
        if not self.gm.is_board_inited():
            self.gm.open_cell(
                (len(board) // 2, len(board[0]) // 2)
            )
        changed = True
        while changed:
            changed = False
            for y, line in enumerate(board):
                for x, cell in enumerate(line):
                    if cell.is_opened:
                        opened = opened_around(board, (y, x))
                        if len(opened) == 8:
                            continue
                        closed = closed_around(board, (y, x))
                        if len(closed) == 8:
                            continue
                        flagged = flagged_around(board, (y, x))
                        if cell.mines_around == len(closed):
                            for cord in closed:
                                if not board[cord[0]][cord[1]].is_flagged:
                                    self.gm.flag_cell(cord)
                                    changed = True
                                    yield
                        if cell.mines_around == len(flagged) and closed:
                            for cord in closed:
                                if not board[cord[0]][cord[1]].is_opened and not board[cord[0]][cord[1]].is_flagged:
                                    self.gm.open_cell(cord)
                                    changed = True
                                    yield
        reinit()
        solver.working = True


def reinit():
    global solver, is_working
    game.reset()
    solver = Solver(game.gm, threads=True)
    solver.working = is_working
    game.plugins.insert(0, solver)
    game.event_handler.on_event(KEYDOWN, solver.handle_key)


is_working = False
mines_count = 500
game = MineGame(mines_count=mines_count, board_size=(50, 50))
set_full_screen(game, center=True, display=0)
solver = Solver(game.gm, threads=True)
while True:
    reinit()
    game.start_game()
