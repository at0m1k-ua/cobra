from threading import Thread

from PyQt6 import QtWidgets
from pygame.time import delay

from audio_player import AudioPlayer


class TimelineDaemon(Thread):

    def __init__(self,
                 audio_player: AudioPlayer,
                 timeline: QtWidgets.QSlider,
                 start_next_track):
        super().__init__()
        self.__audio_player = audio_player
        self.__timeline = timeline
        self.__pos_seconds = 0
        self.is_incrementing = False
        self.lock_slider = True
        self.daemon = True
        self.__start_next_track = start_next_track

    def run(self):
        while True:
            delay(1000)
            if self.is_incrementing:
                self.__increment_pos()

            self.update()

    def __increment_pos(self):
        self.__pos_seconds += 1

        if self.__pos_seconds >= self.__audio_player.track_length:
            self.__start_next_track()

    def update(self):
        if not self.lock_slider:
            return
        if not self.__audio_player.track_length:
            self.reset()
            return
        self.__timeline.setValue(self.__pos_seconds * 100 // self.__audio_player.track_length)

    def reset(self):
        self.__pos_seconds = 0
        self.__timeline.setValue(0)

    def rewind(self, percentage: int):
        position = percentage * self.__audio_player.track_length // 100
        self.__audio_player.position(position)
        self.__pos_seconds = position
        self.update()
