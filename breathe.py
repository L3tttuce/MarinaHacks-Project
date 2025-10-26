from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Property

class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._radius = 10
        self.setMinimumSize(300, 300)

    def setRadius(self, radius: int):
        self._radius = int(radius)
        self.update()

    def getRadius(self) -> int:
        return int(self._radius)

    radius = Property(int, getRadius, setRadius)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("red"))
        center = self.rect().center()
        painter.drawEllipse(center, self._radius, self._radius)
