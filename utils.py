from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QComboBox, QFrame


def new_line_edit(cb):
    line_edit = QLineEdit()
    line_edit.textChanged.connect(cb)
    return line_edit


def new_text_edit(cb):
    text_edit = QPlainTextEdit()
    text_edit.textChanged.connect(cb)
    return text_edit


def new_combo_box(cb):
    combo_box = QComboBox()
    combo_box.currentIndexChanged.connect(cb)
    return combo_box


def validate_data(data):
    """
    validates that all required fields of the form have been filled.
    requirements are taken from the official BIDS specification.
    this function doesn't check for BIDS version as currently the user has
    no control over it, if updated check for version if necessary.
    the function assumes that data will have at least one GeneratedBy item if

    :param data: dict, that contains all the user input data from the form
    :return: bool, True if the data satisfies the requirements, false otherwise
    """
    if data['Name'] == '':
        return False
    if 'GeneratedBy' in data:
        gen_by = data['GeneratedBy']
        for item in gen_by:
            if item['Name'] == '':
                return False
    return True


def remove_empty_fields(data):
    """
    removes all the fields that were not filled by the user, will only check
    optional and recommended fields and not REQUIRED, make sure to validate
    the data before calling this function
    :param data:
    :return:
    """
    if data['DatasetType'] == 'unspecified':
        data.pop('DatasetType')
    if data['License'] == 'unspecified':
        data.pop('License')
    if not data['Authors']:
        data.pop('Authors')
    if data['Acknowledgements'] == '':
        data.pop('Acknowledgements')
    if data['HowToAcknowledge'] == '':
        data.pop('HowToAcknowledge')
    if not data['Funding']:
        data.pop('Funding')
    if not data['EthicsApprovals']:
        data.pop('EthicsApprovals')
    if not data['ReferencesAndLinks']:
        data.pop('ReferencesAndLinks')
    if not data['DatasetDOI']:
        data.pop('DatasetDOI')
    if 'GeneratedBy' in data:
        gen_by = data['GeneratedBy']
        for item in gen_by:
            if item['Version'] == '':
                item.pop('Version')
            if item['Description'] == '':
                item.pop('Description')
            if item['CodeURL'] == '':
                item.pop('CodeURL')
            if item['Container']['Type'] == '':
                item['Container'].pop('Type')
            if item['Container']['Tag'] == '':
                item['Container'].pop('Tag')
            if item['Container']['URI'] == '':
                item['Container'].pop('URI')
            if not item['Container']:
                item.pop('Container')
        data['GeneratedBy'] = [x for x in gen_by if x != {}]
        src_data = data['SourceDatasets']
        for item in src_data:
            if item['URL'] == '':
                item.pop('URL')
            if item['DOI'] == '':
                item.pop('DOI')
            if item['Version'] == '':
                item.pop('Version')
        data['SourceDatasets'] = [x for x in src_data if x != {}]
        if not data['SourceDatasets']:
            data.pop('SourceDatasets')
    return data


class HLine(QFrame):
    """
    visual line to separate sections in the form
    """
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
