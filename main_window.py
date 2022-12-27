from pathlib import Path

from PyQt6.QtWidgets import QFileDialog
from PyQt6.uic.uiparser import QtWidgets

from audio_player import AudioPlayer
from main_window_ui import MainWindowUI
from order import RandomOrder, StraightOrder, ReverseOrder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.__ui = MainWindowUI()
        self.__audio_player = AudioPlayer()

    def __add(self):
        file_dialog = QFileDialog()
        paths_str = file_dialog.getOpenFileNames(self,
                                                 "Open some files",
                                                 str(Path.home()),
                                                 "MP3 files (*.mp3)")[0]
        for path_str in paths_str:
            path = Path(path_str)
            self.__ui_list.addItem(path_str.split("/")[-1])
            self.__audioplayer.add(path)

    def __remove(self):
        for index in self.__ui.list_tracks.selectedIndexes():
            self.__audioplayer.remove(index.row())

    def __straight(self):
        self.__audioplayer.straight_order()
        self.__set_order_ui(StraightOrder)

    def __reverse(self):
        pass

    def __random(self):
        pass

    def __set_order_ui(self, required_order: type):
        pass

    def __play(self):
        pass

    def __timeline_pressed(self):
        pass

    def __timeline_released(self):
        pass

    def __set_up_events(self):
        pass