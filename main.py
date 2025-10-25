import sys
from PySide6 import QtCore, QtWidgets, QtGui
import qt_ui 


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = qt_ui.MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())