from PyQt5 import Qt, QtCore, QtWidgets
from gui.chat_ui import Ui_MainWindow as ui_class


class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

    #     self.ui.button_add_contact.pressed.connect(self.press)
    #
    # def press(self):
    #     print('IN')

    def on_button_add_contact_pressed(self):
        # self.ui.contact_list.setText("111")
        print("IN")
