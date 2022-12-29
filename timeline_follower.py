from pathlib import Path

from PyQt6 import QtWidgets
from pygame import mixer
from pygame.threads import Thread
from pygame.time import delay


class TimelineFollower(Thread):
    def __init__(self, next_track):
        super().__init__()
        self.__timeline = None
        self.__song: mixer.Sound | None = None
        self.lock_slider: bool = True
        self.count: bool = False
        self.__pos_seconds = 0
        self.next_track = next_track

    @property
    def timeline(self):
        return self.__timeline

    @timeline.setter
    def timeline(self, value):
        self.__timeline = value

    def song(self, path: Path | None) -> None:
        if path:
            self.__song = mixer.Sound(path)

    def pos_seconds(self, pos: int):
        self.__pos_seconds = pos

    def run(self) -> None:
        self.__pos_seconds = 0
        while True:
            delay(1000)
            if self.count:
                self.__pos_seconds += 1

            self.update()

            if self.__song and self.__pos_seconds >= self.__song.get_length():
                self.next_track()

    def update(self):
        if not self.lock_slider:
            return
        if self.__song is None:
            self.__timeline.setValue(0)
        else:
            len_seconds = int(self.__song.get_length())
            self.__timeline.setValue(self.__pos_seconds * 100 // len_seconds)

