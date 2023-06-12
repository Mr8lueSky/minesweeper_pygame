import pygame
from pygame.constants import *
from pygame.event import Event


class MineEventHandler:
    def __init__(self, gm, fboard, info_panel=None):
        self.gm = gm
        self.fboard = fboard
        self.info_panel = info_panel
        self.lock_events = False
        self.events = {
            QUIT: [self.quit],
            MOUSEBUTTONDOWN: [self.mouse_click_handler],
            KEYDOWN: [self._on_key_down]
        }

    def quit(self, event=None):
        print("Quiting")
        raise Exception("Quiting")

    def _on_key_down(self, event: Event):
        if event.key == K_ESCAPE:
            self.quit()

    def on_event(self, event_type, callback):
        if event_type in self.events:
            self.events[event_type].append(callback)
        else:
            self.events[event_type] = [callback]

    def open_cell(self, cords):
        try:
            self.gm.open_cell(cords)
        except Exception as err:
            print(f"Mine exploded at {cords}", err)
            self.quit()

    def flag_cell(self, cords):
        self.gm.flag_cell(cords)

    def mouse_click_handler(self, event):
        pos = pygame.mouse.get_pos()
        cords = self.fboard.get_cords_by_fcords(pos)
        if cords is None:
            return
        if event.button == 1:
            self.open_cell(cords)
        if self.gm.is_board_inited() and event.button == 3:
            self.flag_cell(cords)

    def handle_events(self):
        if self.lock_events:
            return
        if self.gm.is_board_inited() and self.gm.is_done():
            self.quit()
        for event in pygame.event.get():
            if event.type in self.events:
                for event_call in self.events[event.type]:
                    event_call(event)
