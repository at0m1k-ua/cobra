from pathlib import Path
from pygame import mixer

from order import StraightOrder
from timeline_follower import TimelineFollower


class AudioPlayer:

    def __init__(self):
        mixer.init()
        self.playlist: list = list()
        self.__timeline_follower = TimelineFollower(None)
        self.__order = StraightOrder(0, 0)
        self.__current_track = None
        self.__current_track_length = 0

    @property
    def timeline_follower(self):
        return self.__timeline_follower

    @timeline_follower.setter
    def timeline_follower(self, value):
        self.__timeline_follower = value

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
            return True

        return wrapper

    @__forbid_empty_playlist
    def play(self):
        self.__current_track = self.playlist[self.__order.current_id()]
        self.__current_track_length = int(mixer.Sound(self.__current_track).get_length())
        mixer.music.load(self.__current_track)
        mixer.music.play()

    @__forbid_empty_playlist
    def unpause(self):
        mixer.music.unpause()

    @__forbid_empty_playlist
    def stop(self):
        mixer.music.stop()
        mixer.music.unload()
        self.__current_track = None
        self.__current_track_length = 0

    @__forbid_empty_playlist
    def pause(self):
        mixer.music.pause()

    @__forbid_empty_playlist
    def prev(self):
        self.__order.move_backward()
        return self.play()

    @__forbid_empty_playlist
    def next(self):
        self.__order.move_forward()
        return self.play()

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

    @property
    def current_id(self):
        return self.__order.current_id()

    @property
    def track_is_loaded(self):
        return self.__current_track is not None

    @property
    def track_length(self):
        return self.__current_track_length

    @staticmethod
    def position(position: int):
        mixer.music.set_pos(position)
