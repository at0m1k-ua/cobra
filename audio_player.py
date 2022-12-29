from pathlib import Path

from pygame import mixer

from order import StraightOrder


class AudioPlayer:

    def __init__(self):
        mixer.init()
        self.playlist: list = list()
        self.__order = StraightOrder(0, 0)
        self.__current_track = None
        self.__is_paused = False

    @staticmethod
    def __update_order(method_to_decorate):
        def wrapper(self, *args, **kwargs):
            result = method_to_decorate(self, *args, **kwargs)

            order_type = type(self.__order)
            self.__order = order_type(
                len(self.playlist),
                self.__order.current_id()
            )
            return result

        return wrapper

    @staticmethod
    def __forbid_empty_playlist(method_to_decorate):
        def wrapper(self, *args, **kwargs):
            if not len(self.playlist):
                return False  # don't change UI
            result = method_to_decorate(self, *args, **kwargs)
            return result or True

        return wrapper

    @__forbid_empty_playlist
    def play(self):
        if not self.__is_paused:
            self.__current_track = self.playlist[self.__order.current_id()]
            mixer.music.load(self.__current_track)
            mixer.music.play()
        else:
            mixer.music.unpause()
            self.__is_paused = False

    @__forbid_empty_playlist
    def stop(self):
        self.__is_paused = False
        mixer.music.stop()
        mixer.music.unload()
        self.__current_track = None

    @__forbid_empty_playlist
    def pause(self):
        mixer.music.pause()
        self.__is_paused = True

    @__forbid_empty_playlist
    def prev(self):
        pass

    def next(self):
        pass

    def set_order_type(self, new_order_type: type):
        self.__order = new_order_type(
            len(self.playlist),
            self.__order.current_id()
        )

    @__update_order
    def add(self, path: Path):
        if path in self.playlist:
            return
        self.playlist.append(path)

    @__update_order
    def remove(self, index: int):
        set_stop_state = False
        if self.playlist[index] == self.__current_track:
            self.stop()
            set_stop_state = True

        del self.playlist[index]
        return set_stop_state
