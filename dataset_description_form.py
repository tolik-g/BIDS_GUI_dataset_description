from PyQt5.QtWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.data = "data"
        self.layout = QGridLayout()
        self.init_ui()
        # self.form_fields()

    def init_ui(self):
        row = 0

        # Dataset name
        name_label = QLabel('Name')
        name_value = QLineEdit()
        self.layout.addWidget(name_label, row, 0)
        self.layout.addWidget(name_value, row, 1)
        row += 1

        # BIDS version
        bids_ver_label = QLabel('BIDS version')
        bids_ver_value = QComboBox()
        bids_ver_value.addItems(['(update this)'])
        self.layout.addWidget(bids_ver_label, row, 0)
        self.layout.addWidget(bids_ver_value, row, 1)
        row += 1

        # Authors
        # TODO: check official specs for this







    def get_data(self):
        return self.data


app = QApplication([])
window = MainWindow()
app.exec()

print("this")
print(window.get_data())