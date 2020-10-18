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

        # generic layout/widget setup for QMainWindow
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # setup form widget
        self.form_widget = FormScroll()
        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.form_widget.setSizePolicy(policy)
        # connect form modification signal to modification handler
        self.form_widget.form.modified.connect(self.handle_form_modified)

        # setup save buttons/status controller
        self.save_control = SaveController(self.form_widget.form.get_data)

        # setup UI
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.layout.addWidget(self.form_widget, 0, 0, 1, -1)
        self.layout.addWidget(self.save_control, 1, 0, 1, -1)
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnStretch(0, 1)
        self.setMinimumSize(600, 900)
        self.setStyleSheet(styles.STYLE)
        self.setWindowIcon(QtGui.QIcon('Icons/title.png'))
        self.setWindowTitle('Dataset Description Generator')

    def handle_form_modified(self):
        """
        decides what actions to take when selected fields in the form are
        modified, the selected fields will be determined by BIDS specification
        (required fields that affect validity of the dataset description file)
        :return:
        """
        data = self.form_widget.form.get_data()
        self.save_control.set_valid(validate_data(data))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
