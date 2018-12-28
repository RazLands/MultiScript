from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog, QComboBox
from gui import Ui_MainWindow
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # self.action_idx = self.choose_action.currentIndex()
        idx = self.choose_action.currentIndexChanged.connect(self.mySlot)

        self.run_button.clicked.connect(self.open_edit_dialog)

        # self.choose_action.setCurrentIndex()

    def mySlot(self, i):
        return self.choose_action.currentIndex()

    def switch_title(self, idx):
        title = {
            0: "Input Site Name",
            1: "Input AP1",
            2: "Input AP2",
            3: "",
            4: "",
            5: ""
        }

        return title[idx]

    def open_edit_dialog(self):
        # self.dialog = MainWindow2()
        # self.dialog.show()

        action_idx = self.mySlot(self.choose_action.currentIndex())
        title = self.switch_title(action_idx)

        if action_idx == 1:
            input_text = QInputDialog.getText(self, "Input Dialog", title)

        if action_idx == 2:
            pass

        if action_idx == 3:
            pass

        if action_idx == 4:
            pass

        if action_idx == 5:
            pass

        print(input_text[0])

class MainWindow2(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow2, self).__init__()
        self.setupUi(self)
        # self.run_button.clicked.connect(sys.exit(self))

app = QApplication(sys.argv)
ui = MainWindow()
ui.show()
sys.exit(app.exec_())