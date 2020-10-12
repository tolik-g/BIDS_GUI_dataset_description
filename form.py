import json
import ntpath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import styles
import tooltips as tt
from form_derivative import Derivative
from utils import new_line_edit, new_text_edit, new_combo_box, validate_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # static widgets with stored user input data
        self.derivative = None
        self.name_value = None
        self.bids_ver_value = None
        self.data_type_value = None
        self.license_value = None
        self.ack_value = None
        self.how_to_ack_value = None
        self.doi_value = None
        self.curr_file_name = None
        self.curr_saved_label = None
        self.is_valid_text = None
        self.is_valid_icon = None

        # main layout and sub layouts (for dynamic field insertion).
        # layouts *_author, *_funding, *_ethics, *_ref are for dynamically added
        # fields in the main layout.
        # layout *_derivative is for toggled derivative related fields.
        self.layout_main = QGridLayout()
        self.layout_author = QVBoxLayout()
        self.layout_funding = QVBoxLayout()
        self.layout_ethics = QVBoxLayout()
        self.layout_ref = QVBoxLayout()
        self.layout_derivative = QGridLayout()
        self.layout_src_data = QGridLayout()
        self.layout_gen_by = QVBoxLayout()

        # lists of widgets for dynamically added (and subtracted) fields
        self.ref_ls = []
        self.ethics_ls = []
        self.funding_ls = []
        self.author_ls = []
        self.gen_by_ls = []

        # main widget scrollable setup
        self.widget = QWidget()
        self.widget.setLayout(self.layout_main)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)

        # UI setup
        self.setMinimumSize(600, 800)
        self.init_ui()
        self.show()

        # non application-logic setup
        self.setWindowTitle('Dataset Description Generator')
        self.setStyleSheet(styles.STYLE)

    def init_ui(self):
        """
        Initialize UI components.
        Naming conventions for the labels are taken from official BIDS
        specification (v1.4.0).
        :return:
        """
        row = 0  # for main layout row count
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout_main.setColumnStretch(4, 1)

        # Name (Dataset name)
        name_label = QLabel('Name')
        name_label.setToolTip(tt.name)
        self.layout_main.addWidget(name_label, row, 0)
        self.name_value = new_line_edit(self.state_changed)

        self.layout_main.addWidget(self.name_value, row, 1, 1, 4)
        row += 1

        # BIDSVersion
        bids_ver_label = QLabel('BIDSVersion')
        bids_ver_label.setToolTip(tt.bids_version)
        self.bids_ver_value = QComboBox()
        self.bids_ver_value.addItems(['1.4.0'])
        self.bids_ver_value.setDisabled(True)  # to be modified in the future
        self.layout_main.addWidget(bids_ver_label, row, 0)
        self.layout_main.addWidget(self.bids_ver_value, row, 1, 1, 4)
        row += 1

        # DatasetType
        data_type_label = QLabel('DatasetType')
        data_type_label.setToolTip(tt.dataset_type)
        self.data_type_value = QComboBox()
        self.data_type_value.addItems(['unspecified', 'raw', 'derivative'])
        self.data_type_value.currentIndexChanged.connect(
            self.dataset_type_handler)
        self.layout_main.addWidget(data_type_label, row, 0)
        self.layout_main.addWidget(self.data_type_value, row, 1, 1, 4)
        row += 1

        # License
        license_label = QLabel('License')
        license_label.setToolTip(tt.dataset_license)
        self.license_value = new_combo_box(self.state_changed)
        self.license_value.addItems(['unspecified', 'PD', 'PDDL', 'CC0'])
        self.license_value.setItemData(1, tt.license_pd, Qt.ToolTipRole)
        self.license_value.setItemData(2, tt.license_pddl, Qt.ToolTipRole)
        self.license_value.setItemData(3, tt.license_cc0, Qt.ToolTipRole)
        self.layout_main.addWidget(license_label, row, 0)
        self.layout_main.addWidget(self.license_value, row, 1, 1, 4)
        row += 1

        # Authors
        author_label = QLabel('Author')
        author_label.setToolTip(tt.authors)
        author_button_add = QPushButton('+')
        author_button_add.clicked.connect(self.add_author)
        author_button_remove = QPushButton('-')
        author_button_remove.clicked.connect(self.remove_author)
        self.layout_main.addWidget(author_label, row, 0)
        self.layout_main.addWidget(author_button_remove, row, 1)
        self.layout_main.addWidget(author_button_add, row, 2)
        row += 1
        self.layout_main.addLayout(self.layout_author, row, 0, 1, -1)
        row += 1

        # Acknowledgements
        ack_label = QLabel('Acknowledgements')
        ack_label.setToolTip(tt.acknowledgements)
        self.ack_value = new_text_edit(self.state_changed)
        self.ack_value.setSizePolicy(policy)
        self.layout_main.addWidget(ack_label, row, 0)
        row += 1
        self.layout_main.addWidget(self.ack_value, row, 0, 1, -1)
        row += 1

        # HowToAcknowledge
        how_to_ack_label = QLabel('HowToAcknowledge')
        how_to_ack_label.setToolTip(tt.how_to_ack)
        self.how_to_ack_value = new_text_edit(self.state_changed)
        self.how_to_ack_value.setSizePolicy(policy)
        self.layout_main.addWidget(how_to_ack_label, row, 0)
        row += 1
        self.layout_main.addWidget(self.how_to_ack_value, row, 0, 1, -1)
        row += 1

        # Funding
        funding_label = QLabel('Funding')
        funding_label.setToolTip(tt.funding)
        funding_button_add = QPushButton('+')
        funding_button_add.clicked.connect(self.add_funding)
        funding_button_remove = QPushButton('-')
        funding_button_remove.clicked.connect(self.remove_funding)
        self.layout_main.addWidget(funding_label, row, 0)
        self.layout_main.addWidget(funding_button_remove, row, 1)
        self.layout_main.addWidget(funding_button_add, row, 2)
        row += 1
        self.layout_main.addLayout(self.layout_funding, row, 0, 1, -1)
        row += 1

        # EthicsApprovals
        ethics_label = QLabel('EthicsApprovals')
        ethics_label.setToolTip(tt.ethics_approval)
        ethics_button_add = QPushButton('+')
        ethics_button_add.clicked.connect(self.add_ethics)
        ethics_button_remove = QPushButton('-')
        ethics_button_remove.clicked.connect(self.remove_ethics)
        self.layout_main.addWidget(ethics_label, row, 0)
        self.layout_main.addWidget(ethics_button_remove, row, 1)
        self.layout_main.addWidget(ethics_button_add, row, 2)
        row += 1
        self.layout_main.addLayout(self.layout_ethics, row, 0, 1, -1)
        row += 1

        # ReferencesAndLinks
        ref_label = QLabel('ReferencesAndLinks')
        ref_label.setToolTip(tt.ref_and_links)
        ref_button_add = QPushButton('+')
        ref_button_add.clicked.connect(self.add_ref)
        ref_button_remove = QPushButton('-')
        ref_button_remove.clicked.connect(self.remove_ref)
        self.layout_main.addWidget(ref_label, row, 0)
        self.layout_main.addWidget(ref_button_remove, row, 1)
        self.layout_main.addWidget(ref_button_add, row, 2)
        row += 1
        self.layout_main.addLayout(self.layout_ref, row, 0, 1, -1)
        row += 1

        # DatasetDOI
        doi_label = QLabel('DatasetDOI')
        doi_label.setToolTip(tt.dataset_doi)
        self.doi_value = new_line_edit(self.state_changed)
        self.layout_main.addWidget(doi_label, row, 0)
        self.layout_main.addWidget(self.doi_value, row, 1, 1, -1)
        row += 1

        # Derivative sections (fields dynamically added to layout)
        self.layout_main.addLayout(self.layout_derivative, row, 0, 1, -1)
        row += 1

        # validation form
        valid_label = QLabel('Form validation')
        self.is_valid_text = QLabel("Missing required fields")
        self.is_valid_icon = QLabel()
        self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))

        self.layout_main.addWidget(valid_label, row, 0)
        self.layout_main.addWidget(self.is_valid_text, row, 1)
        self.layout_main.addWidget(self.is_valid_icon, row, 2)

        row += 1

        # save button, path selection section
        save_button = QPushButton("Save")
        save_as_button = QPushButton("Save as")
        self.curr_saved_label = QLabel('')
        self.layout_main.addWidget(save_button, row, 1)
        self.layout_main.addWidget(save_as_button, row, 2)
        self.layout_main.addWidget(self.curr_saved_label, row, 3)
        save_as_button.clicked.connect(self.save_as)
        save_button.clicked.connect(self.save_data_as_json)
        row += 1

        # spacer item to push content to top
        self.layout_main.addItem(QSpacerItem(0, 0), row, 0, 2, -1)
        col_count = self.layout_main.columnCount()
        self.layout_main.setColumnStretch(col_count-1, 1)


    def handle_form_valid_change(self):
        if self.is_valid_text is None:
            return

        if validate_data(self.get_data()):
            self.is_valid_icon.setPixmap(QPixmap('icons/valid.png'))
            self.is_valid_text.setText("Valid")
        else:
            self.is_valid_icon.setPixmap(QPixmap('icons/invalid.png'))
            self.is_valid_text.setText("Missing required fields")

    def state_changed(self):
        self.handle_form_valid_change()

        if not self.curr_file_name:
            return

        self.curr_saved_label.setText(ntpath.basename(self.curr_file_name) + ' *')

    def save_data_as_json(self):
        if not self.curr_file_name:
            self.save_as()
            return

        with open(self.curr_file_name, 'w', encoding='utf-8') as f:
            json.dump(self.get_data(), f, indent=4)

        self.curr_saved_label.setText(ntpath.basename(self.curr_file_name) + ' saved')

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as", "",
                                                   "All Files (*);;Text Files (*.txt)", options=options)
        if not file_name or file_name == '':
            print('failed to save new file')
            return

        if not file_name.endswith('.json'):
            file_name += '.json'
        self.curr_file_name = file_name
        self.save_data_as_json()

    def add_author(self):
        line = new_line_edit(self.state_changed)
        self.author_ls.append(line)
        self.layout_author.addWidget(line)

    def remove_author(self):
        if len(self.author_ls) == 0:
            return
        self.layout_author.removeWidget(self.author_ls[-1])
        self.author_ls[-1].deleteLater()
        self.author_ls = self.author_ls[:-1]

    def add_funding(self):
        line = new_line_edit(self.state_changed)
        self.funding_ls.append(line)
        self.layout_funding.addWidget(line)

    def remove_funding(self):
        if len(self.funding_ls) == 0:
            return
        self.layout_funding.removeWidget(self.funding_ls[-1])
        self.funding_ls[-1].deleteLater()
        self.funding_ls = self.funding_ls[:-1]

    def add_ethics(self):
        line = new_line_edit(self.state_changed)
        self.ethics_ls.append(line)
        self.layout_ethics.addWidget(line)

    def remove_ethics(self):
        if len(self.ethics_ls) == 0:
            return
        self.layout_ethics.removeWidget(self.ethics_ls[-1])
        self.ethics_ls[-1].deleteLater()
        self.ethics_ls = self.ethics_ls[:-1]

    def add_ref(self):
        line = new_line_edit(self.state_changed)
        self.ref_ls.append(line)
        self.layout_ref.addWidget(line)

    def remove_ref(self):
        if len(self.ref_ls) == 0:
            return
        self.layout_ref.removeWidget(self.ref_ls[-1])
        self.ref_ls[-1].deleteLater()
        self.ref_ls = self.ref_ls[:-1]

    def init_ui_derivative(self):
        self.derivative = Derivative(self.state_changed)
        self.layout_derivative.addWidget(self.derivative)

    def clear_ui_derivative(self):
        if self.derivative is None:
            return
        self.derivative.deleteLater()
        self.derivative = None

    def dataset_type_handler(self, index):
        if index == 2:
            self.init_ui_derivative()
        else:
            self.clear_ui_derivative()

    def get_data(self):
        data = {}
        data['Name'] = self.name_value.text()
        data['BIDSVersion'] = self.bids_ver_value.currentText()
        data['DatasetType'] = self.data_type_value.currentText()
        data['License'] = self.license_value.currentText()
        data['Authors'] = [i.text() for i in self.author_ls]
        data['Acknowledgements'] = self.ack_value.toPlainText()
        data['HowToAcknowledge'] = self.how_to_ack_value.toPlainText()
        data['Funding'] = [i.text() for i in self.funding_ls]
        data['EthicsApprovals'] = [i.text() for i in self.ethics_ls]
        data['ReferencesAndLinks'] = [i.text() for i in self.ref_ls]
        data['DatasetDOI'] = self.doi_value.text()

        if self.derivative is not None:
            data_derivative = self.derivative.get_data()
            data['GeneratedBy'] = data_derivative['GeneratedBy']
            data['SourceDatasets'] = data_derivative['SourceDatasets']
        return data
