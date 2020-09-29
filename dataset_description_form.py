from PyQt5.QtWidgets import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = "data"
        self.layout = QGridLayout()
        self.author_layout = QVBoxLayout()
        self.author_qlines_ls = []
        self.widget = QWidget()
        print('log')
        self.setMinimumSize(400, 600)
        self.init_ui()
        self.widget.setLayout(self.layout)

        # self.form_fields()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setFixedSize(500, 50)

        self.setCentralWidget(self.scroll_area)
        self.show()

    def init_ui(self):
        row = 0

        # Dataset name
        name_label = QLabel('Name')
        name_value = QLineEdit()
        self.layout.addWidget(name_label, row, 0)
        self.layout.addWidget(name_value, row, 1, 1, 2)
        row += 1

        # BIDSVersion
        bids_ver_label = QLabel('BIDSVersion')
        bids_ver_value = QComboBox()
        bids_ver_value.addItems(['1.4.0'])
        bids_ver_value.setDisabled(True)  # to be modified in the future
        self.layout.addWidget(bids_ver_label, row, 0)
        self.layout.addWidget(bids_ver_value, row, 1, 1, 2)
        row += 1

        # DatasetType
        data_type_label = QLabel('DatasetType')
        data_type_value = QComboBox()
        data_type_value.addItems(['unspecified', 'raw', 'derivative'])
        self.layout.addWidget(data_type_label, row, 0)
        self.layout.addWidget(data_type_value, row, 1, 1, 2)
        row += 1

        # License
        license_label = QLabel('License')
        license_value = QComboBox()
        license_value.addItems(['unspecified', 'PD', 'PDDL', 'CC0'])
        self.layout.addWidget(license_label, row, 0)
        self.layout.addWidget(license_value, row, 1, 1, 2)
        row += 1

        # Authors
        author_label = QLabel('Author')
        author_button_add = QPushButton('+')
        author_button_add.clicked.connect(self.add_author)
        author_button_remove = QPushButton('-')
        author_button_remove.clicked.connect(self.remove_author)
        self.layout.addWidget(author_label, row, 0)
        self.layout.addWidget(author_button_remove, row, 1)
        self.layout.addWidget(author_button_add, row, 2)
        row += 1

        self.layout.addItem(QSpacerItem(0, 5, QSizePolicy.Expanding), row, 0, 1, 3)
        row += 1
        self.layout.addLayout(self.author_layout, row, 0, 1, -1)
        row += 1
        self.layout.addItem(QSpacerItem(0, 5, QSizePolicy.Expanding), row, 0, 1, 3)
        row += 1

        # Acknowledgements
        ack_label = QLabel('Acknowledgements')
        ack_value = QPlainTextEdit()
        ack_value.setFixedHeight(100)
        self.layout.addWidget(ack_label, row, 0)
        row += 1
        self.layout.addWidget(ack_value, row, 0, 1, 3)
        row += 1

        # HowToAcknowledge
        how_to_ack_label = QLabel('HowToAcknowledge')
        how_to_ack_value = QPlainTextEdit()
        how_to_ack_value.setFixedHeight(100)
        self.layout.addWidget(how_to_ack_label, row, 0)
        row += 1
        self.layout.addWidget(how_to_ack_value, row, 0, 1, 3)
        row += 1

        # spacer item
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding),
                            row, 0, 2, -1)
        # TODO: figure out how to make first colum fixed size

    def add_author(self):
        line = QLineEdit()
        self.author_qlines_ls.append(line)
        self.author_layout.addWidget(line)

    def remove_author(self):
        if len(self.author_qlines_ls) == 0:
            return
        self.author_layout.removeWidget(self.author_qlines_ls[-1])
        self.author_qlines_ls[-1].deleteLater()
        self.author_qlines_ls = self.author_qlines_ls[:-1]


    # def resizeEvent(self, event):
    #     print('entered')
    #     height = self.frameGeometry().height()
    #     print(height)
    #     self.widget.setFixedHeight(height)







    def get_data(self):
        return self.data


