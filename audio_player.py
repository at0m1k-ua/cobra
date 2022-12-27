from pathlib import Path

from pygame import mixer


class AudioPlayer:

    def __init__(self):
        mixer.init()
        self.playlist: list = list()

    def play(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def add(self, path: Path):
        if path in self.__playlist:
            return
        self.__playlist.append(path)
        self.__update_order()

    def remove(self, index: int):
        del self.__playlist[index]
        self.__update_order()

    def __update_order(self):
        pass
