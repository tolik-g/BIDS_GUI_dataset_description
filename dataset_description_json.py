import json
from dataset_description_form import MainWindow

# define pyqt5 main window class



# json generation from data

def gen_dict():
    data = {}
    data['Name'] = ''
    data['BIDSVersion'] = ''  # make this drop down list
    data['Authors'] = ''
    data['Acknowledgements'] = ''
    data['HowToAcknowledge'] = ''
    data['Funding'] = ['', '', '']
    data['ReferencesAndLinks'] = ['', '', '']
    data['DatasetDOI'] = ''
    # need to pull directory on computer

    return

def export_json():
    return