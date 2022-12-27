from PyQt6 import QtWidgets

from main_window_ui import Ui_mainWindow

class CustomMainWindow(Ui_mainWindow):
    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        mainWindow.setFixedHeight(352)
        mainWindow.setFixedWidth(202)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = CustomMainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
