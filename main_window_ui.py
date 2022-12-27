from PyQt6 import QtWidgets

from qt_main_window_ui import Ui_mainWindow


class MainWindowUI(Ui_mainWindow):
    def setupUi(self, main_window):
        super().setupUi(main_window)
        main_window.setFixedHeight(352)
        main_window.setFixedWidth(202)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUI()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
