from main_window_ui import Ui_mainWindow

class CustomMainWindow(Ui_mainWindow):
    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        mainWindow.setFixedHeight(352)
        mainWindow.setFixedWidth(202)
