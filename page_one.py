import sys
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

class PageOne(QtWidgets.QWidget):
    def __init__(self, stacked_widget: QtWidgets.QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # Header
        header = QtWidgets.QFrame()
        header.setObjectName("Header")
        h_layout = QtWidgets.QHBoxLayout(header)
        h_layout.setContentsMargins(24, 16, 24, 16)
        h_layout.setSpacing(16)

        # Logo Emblem
        emblem = QtWidgets.QLabel()
        emblem.setFixedSize(64, 64)
        pix = QtGui.QPixmap("assets/head-brain.png")
        if not pix.isNull():
            emblem.setPixmap(pix.scaled(64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        h_layout.addWidget(emblem)

        title_col = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Marina Mental")
        title.setObjectName("Title")
        subtitle = QtWidgets.QLabel("AI Emotion Detector • Journal Log • Breathing Guide")
        subtitle.setObjectName("Subtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        title_col.addStretch(1)
        h_layout.addLayout(title_col)
        h_layout.addStretch(1)

        root.addWidget(header)

        # Buttons Frames
        card = QtWidgets.QFrame()
        card.setObjectName("Card")
        card_layout = QtWidgets.QGridLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setHorizontalSpacing(14)
        card_layout.setVerticalSpacing(14)

        # Big, friendly buttons
        self.btn_log = self._make_button("Write Log", "📝")
        self.btn_emotion = self._make_button("Shawn Mendes Jumpscare", "🖼")
        self.btn_cam = self._make_button("Emotion Detector (Uses Webcam)", "📷")
        self.btn_breathe = self._make_button("Breathing Exercise", "🫁", object_name="Primary")
        self.btn_quit = self._make_button("Quit", "⏻", object_name="Danger")

        # Grid layout (2 x 3 with stretch)
        card_layout.addWidget(self.btn_log,     0, 0)
        card_layout.addWidget(self.btn_emotion, 0, 1)
        card_layout.addWidget(self.btn_cam,     0, 2)
        card_layout.addWidget(self.btn_breathe, 1, 0, 1, 2)
        card_layout.addWidget(self.btn_quit,    1, 2)

        root.addWidget(card)
        root.addStretch(1)

        # Signals
        self.btn_log.clicked.connect(self.write_log)
        self.btn_emotion.clicked.connect(self.emotion)
        self.btn_cam.clicked.connect(self.cam)
        self.btn_breathe.clicked.connect(self.breathe)
        self.btn_quit.clicked.connect(QtWidgets.QApplication.instance().quit)

    # Helpers
    def _make_button(self, text: str, emoji: str = "", object_name: str | None = None) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(f"{emoji}  {text}" if emoji else text)
        btn.setMinimumHeight(56)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        if object_name:
            btn.setObjectName(object_name)
        # bigger font for primary actions
        f = btn.font()
        f.setPointSize(f.pointSize() + 1)
        btn.setFont(f)
        return btn

    # Slots
    @QtCore.Slot()
    def write_log(self):
        QtWidgets.QMessageBox.information(self, "Log", "This is where you’d open a log window or save text.")

    @QtCore.Slot()
    def emotion(self):
        subprocess.Popen([sys.executable, "-u", "emotionDetection.py"])

    @QtCore.Slot()
    def cam(self):
        subprocess.Popen([sys.executable, "-u", "realTimeFaceDetection.py"])

    @QtCore.Slot()
    def breathe(self):
        self.stacked_widget.setCurrentIndex(1)
