import json
from dataset_description_form import MainWindow
from PyQt5.QtWidgets import QApplication, QScrollArea
import sys

app = QApplication([])
window = MainWindow()
sys.exit(app.exec())


