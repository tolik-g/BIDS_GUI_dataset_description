from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class SaveController(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        row = 0
        save_button = QPushButton('Save')
        save_as_button = QPushButton('Save As')
        self.is_valid_icon = QLabel()
        self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))
        self.is_valid_text = QLabel('Missing required fields')
        self.is_valid_icon.setFixedWidth(20)
        self.layout.addWidget(save_button, row, 0)
        self.layout.addWidget(save_as_button, row, 1)
        self.layout.addWidget(self.is_valid_icon, row, 2)
        self.layout.addWidget(self.is_valid_text, row, 3)
        self.layout.addItem(QSpacerItem(0, 0), row, 4)


    def set_valid(self, valid):
        if valid:
            self.is_valid_icon.setPixmap(QPixmap('icons/valid.png'))
            self.is_valid_text.setText("Valid")
        else:
            self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))
            self.is_valid_text.setText("Missing required fields")
