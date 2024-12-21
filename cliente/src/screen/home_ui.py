from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/screen/ui/home.ui', self)
        self.show()

