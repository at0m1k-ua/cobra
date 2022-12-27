from pathlib import Path

from PyQt6 import QtWidgets

from audio_player import AudioPlayer
from main_window_ui import MainWindowUI
from order import RandomOrder, StraightOrder, ReverseOrder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.__ui = MainWindowUI()
        self.__audio_player = AudioPlayer()

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
            self.__audio_player.remove(index.row())

    def __straight(self):
        self.__set_order(StraightOrder)

    def __reverse(self):
        self.__set_order(ReverseOrder)

    def __random(self):
        self.__set_order(RandomOrder)

    def __set_order(self, order_type: type):
        self.__audio_player.set_order_type(order_type)
        # TODO set order for UI

    def __play(self):
        pass

    def __timeline_pressed(self):
        pass

    def __timeline_released(self):
        pass

    def __set_up_events(self):
        pass
