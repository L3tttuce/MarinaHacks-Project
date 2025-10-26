import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from page_one import PageOne
from page_two import PageTwo
from page_three import PageThree

APP_STYLES = """
* { font-family: Inter, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
QWidget { background: #0b1020; color: #e8eaf6; }
#Header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #1b2a4a, stop:1 #213a7a);
    border-radius: 18px;
    padding: 24px;
    margin: 8px 8px 16px 8px;
}
#Title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 0.5px;
}
#Subtitle {
    font-size: 13px;
    color: #b6c2ff;
    margin-top: 6px;
}
#Card {
    background: #111731;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 18px;
}
QPushButton {
    background: #253056;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 14px 18px;
    font-weight: 600;
}
QPushButton:hover { background: #2b3868; }
QPushButton:pressed { background: #202a4f; }
#Primary {
    background: #3251ff;
    border: 1px solid #2b46d9;
}
#Primary:hover { background: #4662ff; }
#Danger { background: #65273a; border: 1px solid #7c2e45; }
#Danger:hover { background: #7a2d42; }
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarinaHacks Project")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.stacked = QStackedWidget()
        self.page1 = PageOne(self.stacked)
        self.page2 = PageTwo(self.stacked)
        self.page3 = PageThree(self.stacked)

        self.stacked.addWidget(self.page1)  # index 0
        self.stacked.addWidget(self.page2)  # index 1
        self.stacked.addWidget(self.page3)  # index 2

        layout.addWidget(self.stacked)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLES)
    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec())