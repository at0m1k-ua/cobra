from pathlib import Path

from pygame import mixer

from order import StraightOrder


def update_order(function_to_decorate):
    def wrapper(self, *args, **kwargs):
        function_to_decorate(self, *args, **kwargs)

        order_type = type(self.__order)
        self.__order = order_type(
            len(self.__playlist),
            self.__order.current_id()
        )

    return wrapper


class AudioPlayer:

    def __init__(self):
        mixer.init()
        self.playlist: list = list()
        self.__order = StraightOrder(0, 0)

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

    @update_order
    def add(self, path: Path):
        if path in self.playlist:
            return
        self.playlist.append(path)

    @update_order
    def remove(self, index: int):
        del self.playlist[index]
