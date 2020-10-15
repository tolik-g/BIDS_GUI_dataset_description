from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import json
import ntpath

from utils import remove_empty_fields


class SaveController(QWidget):
    def __init__(self, get_data_callback):
        super().__init__()
        self.save_as_button = QPushButton('Save As')
        self.save_button = QPushButton('Save')
        self.is_valid_text = QLabel('Missing required fields')
        self.is_valid_icon = QLabel()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.curr_file_name = None
        self.get_data = get_data_callback
        self.init_ui()

    def init_ui(self):
        row = 0
        self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))
        self.is_valid_icon.setFixedWidth(20)
        self.layout.addWidget(self.save_button, row, 0)
        self.layout.addWidget(self.save_as_button, row, 1)
        self.layout.addWidget(self.is_valid_icon, row, 2)
        self.layout.addWidget(self.is_valid_text, row, 3)
        self.layout.addItem(QSpacerItem(0, 0), row, 4)

        self.save_as_button.clicked.connect(self.save_as)
        self.save_as_button.setDisabled(True)
        self.save_button.clicked.connect(self.save_data_as_json)
        self.save_button.setDisabled(True)

    def set_valid(self, valid):
        if valid:
            self.is_valid_icon.setPixmap(QPixmap('icons/valid.png'))
            self.is_valid_text.setText("Valid")
        else:
            self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))
            self.is_valid_text.setText("Missing required fields")
            self.save_button.setDisabled(True)

        self.save_button.setDisabled(not valid or not self.curr_file_name)
        self.save_as_button.setDisabled(not valid)

    def save_data_as_json(self):
        cleaned_data = remove_empty_fields(self.get_data())
        with open(self.curr_file_name, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=4)

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as", "",
                                                   "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if not file_name or file_name == '':
            print('failed to save new file')
            return

        if not file_name.endswith('.json'):
            file_name += '.json'

        self.save_button.setDisabled(False)
        self.curr_file_name = file_name
        self.save_data_as_json()
