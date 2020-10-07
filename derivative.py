from PyQt5.QtWidgets import *
from aux_classes import HLine
import styles
import sys


class Derivative(QWidget):
    def __init__(self):
        super().__init__()

        # main layout and sub layouts (for dynamic field insertion)
        self.layout_main = QGridLayout()
        self.layout_gen_by = QVBoxLayout()
        self.layout_src_data = QVBoxLayout()

        # lists of widgets for dynamically added (and subtracted) fields
        self.gen_by_ls = []
        self.src_data_ls = []

        self.setLayout(self.layout_main)
        self.init_ui()
        self.add_gen_by()

    def init_ui(self):
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        row = 0
        # section separation line
        h_line = HLine()
        self.layout_main.addWidget(h_line, row, 0, 1, -1)
        row += 1

        # GeneratedBy control
        gen_by_label = QLabel('GeneratedBy')
        gen_by_add_button = QPushButton('+')
        gen_by_add_button.clicked.connect(self.add_gen_by)
        gen_by_remove_button = QPushButton('-')
        gen_by_remove_button.clicked.connect(self.remove_gen_by)
        self.layout_main.addWidget(gen_by_label, row, 0)
        self.layout_main.addWidget(gen_by_remove_button, row, 1)
        self.layout_main.addWidget(gen_by_add_button, row, 2)
        row += 1

        # GeneratedBy fields
        self.layout_main.addLayout(self.layout_gen_by, row, 0, 1, -1)
        row += 1

        # SourceDatasets control
        src_data_label = QLabel('SourceDatasets')
        src_data_add_button = QPushButton('+')
        src_data_add_button.clicked.connect(self.add_src_data)
        src_data_remove_button = QPushButton('-')
        src_data_remove_button.clicked.connect(self.remove_src_data)
        self.layout_main.addWidget(src_data_label, row, 0)
        self.layout_main.addWidget(src_data_remove_button, row, 1)
        self.layout_main.addWidget(src_data_add_button, row, 2)
        row += 1

        # DataSources fields
        self.layout_main.addLayout(self.layout_src_data, row, 0, 1, -1)
        row += 1

        # spacers to push content to top left
        self.layout_main.addItem(QSpacerItem(0, 0), 0, 3, -1, 1)
        self.layout_main.addItem(QSpacerItem(0, 0), row, 0, 2, -1)

    def add_gen_by(self):
        gen_by = GeneratedBy()
        self.layout_gen_by.addWidget(gen_by)
        self.gen_by_ls.append(gen_by)

    def remove_gen_by(self):
        if len(self.gen_by_ls) == 1:
            return
        self.layout_gen_by.removeWidget(self.gen_by_ls[-1])
        self.gen_by_ls[-1].deleteLater()
        self.gen_by_ls = self.gen_by_ls[:-1]

    def add_src_data(self):
        src_data = SourceDatasets()
        self.layout_src_data.addWidget(src_data)
        self.src_data_ls.append(src_data)

    def remove_src_data(self):
        if len(self.src_data_ls) == 0:
            return
        self.layout_src_data.removeWidget(self.src_data_ls[-1])
        self.src_data_ls[-1].deleteLater()
        self.src_data_ls = self.src_data_ls[:-1]

    def get_data(self):
        return


class GeneratedBy(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        row = 0
        # Name
        name_label = QLabel('Name')
        name_value = QLineEdit()
        self.layout.addWidget(name_label, row, 0)
        self.layout.addWidget(name_value, row, 1, 1, -1)
        row += 1

        # Version
        version_label = QLabel('Version')
        version_value = QLineEdit()
        self.layout.addWidget(version_label, row, 0)
        self.layout.addWidget(version_value, row, 1, 1, -1)
        row += 1

        # Description
        desc_label = QLabel('Description')
        desc_value = QPlainTextEdit()
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        desc_value.setSizePolicy(policy)
        self.layout.addWidget(desc_label, row, 0)
        row += 1
        # TODO: fix space created when using plaintext widget
        self.layout.addWidget(desc_value, row, 0, 1, -1)
        row += 1

        # CodeURL
        url_label = QLabel('CodeURL')
        url_value = QLineEdit()
        self.layout.addWidget(url_label, row, 0)
        self.layout.addWidget(url_value, row, 1, 1, -1)
        row += 1

        # Container
        cont_label = QLabel('Container')
        self.layout.addWidget(cont_label, row, 0)
        row += 1

        cont_type_label = QLabel('Type')
        cont_type_value = QLineEdit()
        self.layout.addWidget(cont_type_label, row, 1)
        self.layout.addWidget(cont_type_value, row, 2, 1, -1)
        row += 1

        cont_tag_label = QLabel('Tag')
        cont_tag_value = QLineEdit()
        self.layout.addWidget(cont_tag_label, row, 1)
        self.layout.addWidget(cont_tag_value, row, 2, 1, -1)
        row += 1

        cont_uri_label = QLabel('URI')
        cont_uri_value = QLineEdit()
        self.layout.addWidget(cont_uri_label, row, 1)
        self.layout.addWidget(cont_uri_value, row, 2, 1, -1)
        row += 1

        # separator line
        h_line = HLine()
        self.layout.addWidget(h_line, row, 1, 1, -1)
        row += 1

        # spacer to push content to top
        self.layout.addItem(QSpacerItem(0, 0), row, 0, 2, -1)


class SourceDatasets(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        row = 0
        # DOI
        doi_label = QLabel('DOI')
        doi_value = QLineEdit()
        self.layout.addWidget(doi_label, row, 0)
        self.layout.addWidget(doi_value, row, 1, 1, -1)
        row += 1

        # URL
        url_label = QLabel('URL')
        url_value = QLineEdit()
        self.layout.addWidget(url_label, row, 0)
        self.layout.addWidget(url_value, row, 1, 1, -1)
        row += 1

        # Version
        version_label = QLabel('Version')
        version_value = QLineEdit()
        self.layout.addWidget(version_label, row, 0)
        self.layout.addWidget(version_value, row, 1, 1, -1)
        row += 1

        # separator line
        h_line = HLine()
        self.layout.addWidget(h_line, row, 1, 1, -1)
        row += 1

        # spacer to push content to top
        self.layout.addItem(QSpacerItem(0, 0), row, 0, 2, -1)




