from pathlib import Path

from PyQt6 import QtWidgets

from audio_player import AudioPlayer
from main_window_ui import MainWindowUI
from order import RandomOrder, StraightOrder, ReverseOrder
from timeline_daemon import TimelineDaemon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__ui = MainWindowUI()
        self.__ui.setupUi(self)
        self.__audio_player = AudioPlayer()
        self.__set_order(StraightOrder)
        self.__set_up_events()
        self.__timeline_daemon = TimelineDaemon(
            self.__audio_player,
            self.__ui.timeline,
            self.__next
        )
        self.__timeline_daemon.start()
        self.__is_paused = False

    @staticmethod
    def __ignore_empty_playlist(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except IndexError("Playlist is empty"):
                pass
        return wrapper

    def __add(self):
        file_dialog = QtWidgets.QFileDialog()
        paths_str = file_dialog.getOpenFileNames(self,
                                                 "Open some files",
                                                 str(Path.home()),
                                                 "MP3 files (*.mp3)")[0]
        for path_str in paths_str:
            path = Path(path_str)
            self.__ui.list_tracks.addItem(path.name)
            self.__audio_player.add(path)

    def __remove(self):
        for index in self.__ui.list_tracks.selectedIndexes()[::-1]:
            row: int = index.row()
            self.__ui.list_tracks.takeItem(row)
            if self.__audio_player.remove(row):
                self.__set_stop_state()

    def __straight(self):
        self.__set_order(StraightOrder)

    def __reverse(self):
        self.__set_order(ReverseOrder)

    def __random(self):
        self.__set_order(RandomOrder)

    def __set_order(self, order_type: type):
        self.__audio_player.set_order_type(order_type)

        order_types = {
            self.__ui.straight_button: StraightOrder,
            self.__ui.reverse_button: ReverseOrder,
            self.__ui.random_button: RandomOrder,
        }

        for button in order_types:
            button.setEnabled(order_type != order_types[button])

    @__ignore_empty_playlist
    def __play(self):
        if self.__is_paused:
            self.__audio_player.unpause()
            self.__is_paused = False
        else:
            self.__audio_player.play()
            self.__timeline_daemon.reset()
            self.__timeline_daemon.is_incrementing = True
        self.__set_play_state()

    @__ignore_empty_playlist
    def __pause(self):
        self.__audio_player.pause()
        self.__is_paused = True
        self.__timeline_daemon.is_incrementing = False
        self.__set_pause_state()

    @__ignore_empty_playlist
    def __stop(self):
        self.__audio_player.stop()
        self.__is_paused = False
        self.__timeline_daemon.is_incrementing = False
        self.__timeline_daemon.reset()
        self.__set_stop_state()

    def __set_play_state(self):
        self.__ui.play_button.setEnabled(False)
        self.__ui.pause_button.setEnabled(True)
        self.__ui.stop_button.setEnabled(True)

    def __set_stop_state(self):
        self.__ui.play_button.setEnabled(True)
        self.__ui.pause_button.setEnabled(False)
        self.__ui.stop_button.setEnabled(False)

    def __set_pause_state(self):
        self.__ui.play_button.setEnabled(True)
        self.__ui.pause_button.setEnabled(False)
        self.__ui.stop_button.setEnabled(True)

    @__ignore_empty_playlist
    def __prev(self):
        self.__audio_player.prev()
        self.__timeline_daemon.reset()
        self.__ui.list_tracks.setCurrentRow(self.__audio_player.current_id)
        self.__set_play_state()

    @__ignore_empty_playlist
    def __next(self):
        self.__audio_player.next()
        self.__timeline_daemon.reset()
        self.__set_play_state()
        self.__ui.list_tracks.setCurrentRow(self.__audio_player.current_id)

    def __timeline_pressed(self):
        self.__timeline_daemon.lock_slider = False

    def __timeline_released(self):
        self.__timeline_daemon.lock_slider = True
        self.__timeline_daemon.rewind(self.__ui.timeline.value())

    def __set_up_events(self):
        events = {
            self.__ui.add_button.pressed: self.__add,
            self.__ui.remove_button.pressed: self.__remove,
            self.__ui.straight_button.pressed: lambda: self.__set_order(StraightOrder),
            self.__ui.reverse_button.pressed: lambda: self.__set_order(ReverseOrder),
            self.__ui.random_button.pressed: lambda: self.__set_order(RandomOrder),
            self.__ui.play_button.pressed: self.__play,
            self.__ui.pause_button.pressed: self.__pause,
            self.__ui.stop_button.pressed: self.__stop,
            self.__ui.prev_button.pressed: self.__prev,
            self.__ui.next_button.pressed: self.__next,
            self.__ui.timeline.sliderPressed: self.__timeline_pressed,
            self.__ui.timeline.sliderReleased: self.__timeline_released
        }

        for event in events:
            event.connect(events[event])
