import time
from typing import Union

import pygame
from pygame.mixer import Sound


class SoundsManager:
    def __init__(self, sounds_dict: dict[str, Sound]):
        self.sounds_dict = sounds_dict
        self.current_playing = None
        self.volume = 1
        self.current_playing_times = 0
        self.start_playing_at = None

    @property
    def is_playing(self) -> Union[str, None]:
        if self.start_playing_at is None:
            return None
        if (time.time() - self.start_playing_at) < \
                (self.sounds_dict[self.current_playing].get_length() * self.current_playing_times):
            return self.current_playing

    def play(self, sound_name: str, times: int):
        self.stop()
        self.sounds_dict[sound_name].set_volume(self.volume)
        self.current_playing_times = self.sounds_dict[sound_name].get_length()
        self.start_playing_at = time.time()
        self.sounds_dict[sound_name].play(times)
        self.current_playing = sound_name

    def stop(self):
        if self.current_playing is None:
            return
        pygame.mixer.music.stop()
        self.current_playing = None
        self.current_playing_times = None
        self.start_playing_at = None
