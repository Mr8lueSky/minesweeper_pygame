from back.game_manager_refactored import MineGameManager
from front.info_panel_refactored import InfoPanel
from game.mine_game_drawer_refactored import MineGameDrawer
from game.minegame_refactored import MineGame
from utils.window_modes_refactored import set_full_screen
from back.board import Board
from front.fboard_refactored import FBoard

mines_count = 100
board_size = (25, 25)
game = MineGame()
board = Board(board_size, mines_count)
fboard = FBoard(border=1)
gm = MineGameManager().set_board(board)
# info_panel = InfoPanel(gm)
drawer = MineGameDrawer(0).set_fboard(fboard)#.set_infopanel(info_panel)

game\
    .set_fboard(fboard)\
    .set_board(board)\
    .set_gm(gm)\
    .set_drawer(drawer)\
    # .set_info_panel(info_panel)


# set_full_screen(game, center=True, display=0)
game.start_game()
