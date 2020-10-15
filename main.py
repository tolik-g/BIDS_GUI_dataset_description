from form import FormScroll
from save_controller import SaveController
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from utils import validate_data
import sys
import styles


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()

        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.form_widget = FormScroll()
        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.form_widget.setSizePolicy(policy)
        self.form_widget.form.modified.connect(self.handle_form_modified)
        self.layout.addWidget(self.form_widget, 0, 0, 1, -1)
        self.save_control = SaveController(self.form_widget.form.get_data)
        self.layout.addWidget(self.save_control, 1, 0, 1, -1)
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnStretch(0, 1)
        self.setMinimumSize(600, 900)
        self.setStyleSheet(styles.STYLE)
        self.setWindowIcon(QtGui.QIcon('Icons/title.png'))
        self.setWindowTitle('Dataset Description Generator')
        self.show()

    def handle_form_modified(self):
        data = self.form_widget.form.get_data()
        self.save_control.set_valid(validate_data(data))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
