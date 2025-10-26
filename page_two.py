from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve, QAbstractAnimation
from breathe import CircleWidget

class PageTwo(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.animation: QSequentialAnimationGroup | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(20)

        title = QLabel("Breathing Techniques")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        subtitle = QLabel("Choose a technique to begin:")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #b0b6d0; margin-bottom: 18px;")
        layout.addWidget(subtitle)

        # Buttons
        row = QHBoxLayout()
        row.setSpacing(20)
        self.btn_478 = self._btn("🌬  4-7-8 Breathing")
        self.btn_box = self._btn("⬜  Box Breathing")
        self.btn_diaphragm = self._btn("🫁  Diaphragmatic Breathing")
        row.addWidget(self.btn_478)
        row.addWidget(self.btn_box)
        row.addWidget(self.btn_diaphragm)
        layout.addLayout(row)

        # Circle (aka the lungs)
        self.circle = CircleWidget()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        # Status
        self.timer_label = QLabel("")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 20px; color: #a0a8d0;")
        layout.addWidget(self.timer_label)

        # Back
        back = QPushButton("⬅ Back")
        back.setFixedWidth(120)
        back.clicked.connect(self.go_back)
        layout.addWidget(back, alignment=Qt.AlignCenter)

        # Signals
        self.btn_478.clicked.connect(self.start_478)
        self.btn_box.clicked.connect(self.start_box)
        self.btn_diaphragm.clicked.connect(self.start_diaphragm)

    def _btn(self, text):
        b = QPushButton(text)
        b.setMinimumHeight(60)
        b.setStyleSheet("""
            QPushButton {
                background: #253056;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 14px;
                padding: 14px 18px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover { background: #2b3868; }
        """)
        return b

    # Breathing Techniques
    def start_478(self):
        # Inhale for 4 seconds, Hold it for 7 seconds, Exhale for 8 seconds
        self.run_breath_cycle(inhale=4, hold=7, exhale=8, label="4-7-8 Breathing")

    def start_box(self):
        # Inhale for 4 seconds, Hold it for 4 seconds, Exhale for 4 seconds, Hold it again for 4 seconds
        self.run_breath_cycle(inhale=4, hold=4, exhale=4, label="Box Breathing", extra_hold=4)

    def start_diaphragm(self):
        # Inhale for 5 seconds, Exhale for 5 seconds
        self.run_breath_cycle(inhale=5, hold=0, exhale=5, label="Diaphragmatic Breathing")


    def run_breath_cycle(self, inhale: int, hold: int, exhale: int, label: str, extra_hold: int = 0, loop: bool = False):
        # Stop any previous animation
        if self.animation:
            self.animation.stop()
            self.animation.deleteLater()
            self.animation = None

        self.timer_label.setText(f"Starting {label}…")

        group = QSequentialAnimationGroup(self)

        # start from current radius for smoothness
        start_r = self.circle.getRadius()
        max_r = 120
        min_r = 20

        # Inhale (expand)
        anim_in = self._anim(self.circle, start=start_r, end=max(start_r, max_r), ms=inhale * 1000)

        # Hold (pause)
        if hold > 0:
            group.addPause(hold * 1000)

        # Exhale (shrink)
        anim_out = self._anim(self.circle, start=max(start_r, max_r), end=min_r, ms=exhale * 1000)

        # Extra hold
        if extra_hold > 0:
            group.addPause(extra_hold * 1000)

        group.addAnimation(anim_in)
        group.addAnimation(anim_out)

        # Optional looping
        if loop:
            group.setLoopCount(-1)  # infinite
        else:
            group.setLoopCount(1)

        group.finished.connect(lambda: self.timer_label.setText(f"{label} complete."))
        group.start(QAbstractAnimation.KeepWhenStopped)  # keep final radius
        self.animation = group  # keep a strong reference

    def _anim(self, target, start: int, end: int, ms: int) -> QPropertyAnimation:
        a = QPropertyAnimation(target, b"radius", self)
        a.setDuration(ms)
        a.setStartValue(int(start))
        a.setEndValue(int(end))
        a.setEasingCurve(QEasingCurve.InOutQuad)
        return a

    def go_back(self):
        # stop ongoing animation when leaving page
        if self.animation:
            self.animation.stop()
        self.stacked_widget.setCurrentIndex(0)
