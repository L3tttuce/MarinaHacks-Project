import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = "To be implemented"

        self.button = QtWidgets.QPushButton("Write Log")
        self.button2 = QtWidgets.QPushButton("Shawn Mendes Jumpscare")
        self.text = QtWidgets.QLabel("MarinaHacks Project",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)

        self.button.clicked.connect(self.magic)
        self.button2.clicked.connect(self.emotion)

        THEME = {
            "bg":      "#0f1115",
            "card":    "#151821",
            "border":  "#232736",
            "text":    "#e6e9ef",
            "muted":   "#a5adbf",
            "accent":  "#d2f77a",  # pick your brand color
            "accentHi":"#9ab8ff"
        }

    @QtCore.Slot()
    def magic(self):
        self.text.setText(self.hello)

    @QtCore.Slot()
    def emotion(self):
        with open('emotionDetection.py') as f:
            exec(f.read())
