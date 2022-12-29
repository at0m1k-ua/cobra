from pathlib import Path

from PyQt6 import QtWidgets

from audio_player import AudioPlayer
from main_window_ui import MainWindowUI
from order import RandomOrder, StraightOrder, ReverseOrder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__ui = MainWindowUI()
        self.__ui.setupUi(self)
        self.__audio_player = AudioPlayer()
        self.__set_order(StraightOrder)
        self.__set_up_events()

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
        for index in self.__ui.list_tracks.selectedIndexes():
            row: int = index.row()
            self.__audio_player.remove(row)
            self.__ui.list_tracks.takeItem(row)

    def __straight(self):
        self.__set_order(StraightOrder)

    def __reverse(self):
        self.__set_order(ReverseOrder)

    def __random(self):
        self.__set_order(RandomOrder)

    def __set_order(self, order_type: type):
        self.__audio_player.set_order_type(order_type)
        self.__ui.straight_button.setEnabled(order_type != StraightOrder)
        self.__ui.reverse_button.setEnabled(order_type != ReverseOrder)
        self.__ui.random_button.setEnabled(order_type != RandomOrder)

    def __play(self):
        pass

    def __timeline_pressed(self):
        pass

    def __timeline_released(self):
        pass

    def __set_up_events(self):
        events = {
            self.__ui.add_button.pressed: self.__add,
            self.__ui.remove_button.pressed: self.__remove,
            self.__ui.straight_button.pressed: lambda: self.__set_order(StraightOrder),
            self.__ui.reverse_button.pressed: lambda: self.__set_order(ReverseOrder),
            self.__ui.random_button.pressed: lambda: self.__set_order(RandomOrder)
        }

        for event in events:
            event.connect(events[event])
