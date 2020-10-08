from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit, QComboBox


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
