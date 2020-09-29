import json
from dataset_description_form import MainWindow
from PyQt5.QtWidgets import QApplication, QScrollArea
import sys

# define pyqt5 main window class



# json generation from data

def gen_dict():
    data = {}
    data['Name'] = ''  # required
    data['BIDSVersion'] = ''  # make this drop down list # required
    data['DatasetType'] = ''  # recommended
    data['License'] = ''  # make this drop down list # recommended
    data['Authors'] = ''  # optional
    data['Acknowledgements'] = ''  # optional
    data['HowToAcknowledge'] = ''  # optional
    data['Funding'] = ['', '', '']  # optional
    data['ReferencesAndLinks'] = ['', '', '']  # optional
    data['DatasetDOI'] = ''  # optional
    # need to pull directory on computer

    return

def export_json():
    return


app = QApplication([])
window = MainWindow()
sys.exit(app.exec())


