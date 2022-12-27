from PyQt6.uic.uiparser import QtWidgets

from main_window_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.__ui = MainWindowUI()
