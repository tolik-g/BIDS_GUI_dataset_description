from PyQt5.QtWidgets import *
import tooltips as tt
from utils import new_line_edit, new_text_edit, HLine


class Derivative(QWidget):
    def __init__(self, state_change_callback):
        super().__init__()
        self.state_change_cb = state_change_callback

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
        gen_by_label.setToolTip(tt.generated_by)
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
        src_data_label.setToolTip(tt.sources_datasets)
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
        gen_by = GeneratedBy(self.state_change_cb)
        self.layout_gen_by.addWidget(gen_by)
        self.gen_by_ls.append(gen_by)

    def remove_gen_by(self):
        if len(self.gen_by_ls) == 1:
            return
        self.layout_gen_by.removeWidget(self.gen_by_ls[-1])
        self.gen_by_ls[-1].deleteLater()
        self.gen_by_ls = self.gen_by_ls[:-1]

    def add_src_data(self):
        src_data = SourceDatasets(self.state_change_cb)
        self.layout_src_data.addWidget(src_data)
        self.src_data_ls.append(src_data)

    def remove_src_data(self):
        if len(self.src_data_ls) == 0:
            return
        self.layout_src_data.removeWidget(self.src_data_ls[-1])
        self.src_data_ls[-1].deleteLater()
        self.src_data_ls = self.src_data_ls[:-1]

    def get_data(self):
        gen_by_data_ls = []
        src_data_data_ls = []
        for i in self.gen_by_ls:
            gen_by_data_ls.append(i.get_data())
        for i in self.src_data_ls:
            src_data_data_ls.append(i.get_data())
        data = {
            'GeneratedBy': gen_by_data_ls,
            'SourceDatasets': src_data_data_ls
        }
        return data


class GeneratedBy(QWidget):
    def __init__(self, state_change_callback):
        super().__init__()
        self.state_change_cb = state_change_callback

        # static widgets with stored user input data
        self.name_value = None
        self.version_value = None
        self.desc_value = None
        self.url_value = None
        self.cont_type_value = None
        self.cont_tag_value = None
        self.cont_uri_value = None

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        row = 0
        # Name
        name_label = QLabel('Name')
        name_label.setToolTip(tt.gen_name)
        self.layout.addWidget(name_label, row, 0)
        self.name_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(self.name_value, row, 1, 1, -1)
        row += 1

        # Version
        version_label = QLabel('Version')
        version_label.setToolTip(tt.gen_version)
        self.version_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(version_label, row, 0)
        self.layout.addWidget(self.version_value, row, 1, 1, -1)
        row += 1

        # Description
        desc_label = QLabel('Description')
        desc_label.setToolTip(tt.gen_description)
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.desc_value = new_text_edit(self.state_change_cb)
        self.desc_value.setSizePolicy(policy)
        self.layout.addWidget(desc_label, row, 0)
        row += 1
        self.layout.addWidget(self.desc_value, row, 0, 1, -1)
        row += 1

        # CodeURL
        url_label = QLabel('CodeURL')
        url_label.setToolTip(tt.gen_code_url)
        self.url_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(url_label, row, 0)
        self.layout.addWidget(self.url_value, row, 1, 1, -1)
        row += 1

        # Container
        cont_label = QLabel('Container')
        cont_label.setToolTip(tt.gen_container)
        self.layout.addWidget(cont_label, row, 0)
        row += 1

        cont_type_label = QLabel('Type')
        self.cont_type_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(cont_type_label, row, 1)
        self.layout.addWidget(self.cont_type_value, row, 2, 1, -1)
        row += 1

        cont_tag_label = QLabel('Tag')
        self.cont_tag_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(cont_tag_label, row, 1)
        self.layout.addWidget(self.cont_tag_value, row, 2, 1, -1)
        row += 1

        cont_uri_label = QLabel('URI')
        self.cont_uri_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(cont_uri_label, row, 1)
        self.layout.addWidget(self.cont_uri_value, row, 2, 1, -1)
        row += 1

        # separator line
        h_line = HLine()
        self.layout.addWidget(h_line, row, 1, 1, -1)
        row += 1

        # spacer to push content to top
        self.layout.addItem(QSpacerItem(0, 0), row, 0, 2, -1)

    def get_data(self):
        data = {
            'Name': self.name_value.text(),
            'Version': self.version_value.text(),
            'Description': self.desc_value.toPlainText(),
            'CodeURL': self.url_value.text(),
            'Container': {
                'Type': self.cont_type_value.text(),
                'Tag': self.cont_tag_value.text(),
                'URI': self.cont_uri_value.text(),
            }
        }
        return data


class SourceDatasets(QWidget):
    def __init__(self, state_change_callback):

        # static widgets with stored user input data
        self.doi_value = None
        self.url_value = None
        self.version_value = None

        super().__init__()
        self.state_change_cb = state_change_callback

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        row = 0
        # DOI
        doi_label = QLabel('DOI')
        self.doi_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(doi_label, row, 0)
        self.layout.addWidget(self.doi_value, row, 1, 1, -1)
        row += 1

        # URL
        url_label = QLabel('URL')
        self.url_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(url_label, row, 0)
        self.layout.addWidget(self.url_value, row, 1, 1, -1)
        row += 1

        # Version
        version_label = QLabel('Version')
        self.version_value = new_line_edit(self.state_change_cb)
        self.layout.addWidget(version_label, row, 0)
        self.layout.addWidget(self.version_value, row, 1, 1, -1)
        row += 1

        # separator line
        h_line = HLine()
        self.layout.addWidget(h_line, row, 1, 1, -1)
        row += 1

        # spacer to push content to top
        self.layout.addItem(QSpacerItem(0, 0), row, 0, 2, -1)

    def get_data(self):
        data = {
            'DOI': self.doi_value.text(),
            'URL': self.url_value.text(),
            'Version': self.version_value.text()
        }
        return data
