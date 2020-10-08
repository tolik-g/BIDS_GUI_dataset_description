from form import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication([])
window = MainWindow()
sys.exit(app.exec())
