from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QPauseAnimation, QEasingCurve, QAbstractAnimation
from breathe import CircleWidget

class PageTwo(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.animation: QSequentialAnimationGroup | None = None
        self.current_cycle = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 50, 80, 40)
        layout.setSpacing(16)

        # Title
        title = QLabel("Breathing Techniques")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: 800; margin-bottom: 6px;")
        layout.addWidget(title)

        sub = QLabel("Choose a technique to begin")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("font-size: 14px; color: #aeb6d6; margin-bottom: 10px;")
        layout.addWidget(sub)

        # Buttons for breathing
        row = QHBoxLayout()
        row.setSpacing(14)
        self.btn_478 = self._btn("🌬  4-7-8 Breathing")
        self.btn_box = self._btn("⬜  Box (Square) Breathing")
        self.btn_diaphragm = self._btn("🫁  Diaphragmatic Breathing")
        row.addWidget(self.btn_478)
        row.addWidget(self.btn_box)
        row.addWidget(self.btn_diaphragm)
        layout.addLayout(row)

        # Circle
        self.circle = CircleWidget()
        layout.addWidget(self.circle, alignment=Qt.AlignCenter)

        # The inhale, exhale, hold text
        self.phaseLabel = QLabel("")
        self.phaseLabel.setAlignment(Qt.AlignCenter)
        self.phaseLabel.setStyleSheet("font-size: 22px; font-weight: 700; margin-top: 8px;")
        layout.addWidget(self.phaseLabel)

        # Helper/status line
        self.infoLabel = QLabel("")
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.infoLabel.setStyleSheet("font-size: 13px; color: #9aa3c1;")
        layout.addWidget(self.infoLabel)

        # Back
        self.back = QPushButton("⬅ Back")
        self.back.setFixedWidth(120)
        layout.addWidget(self.back, alignment=Qt.AlignCenter)

        # Signals
        self.btn_478.clicked.connect(self.start_478)
        self.btn_box.clicked.connect(self.start_box)
        self.btn_diaphragm.clicked.connect(self.start_diaphragm)
        self.back.clicked.connect(self.go_back)

    def _btn(self, text: str) -> QPushButton:
        b = QPushButton(text)
        b.setMinimumHeight(56)
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

    # The breathing exercises
    def start_478(self):
        # Inhale 4s, Hold 7s, Exhale 8s
        self.run_sequence(inhale=4, hold=7, exhale=8, extra_hold=0, label="4-7-8 Breathing")

    def start_box(self):
        # Inhale 4s, Hold 4s, Exhale 4s, Hold 4s
        self.run_sequence(inhale=4, hold=4, exhale=4, extra_hold=4, label="Box Breathing")

    def start_diaphragm(self):
        # Inhale 5s, Exhale 5s (no hold)
        self.run_sequence(inhale=5, hold=0, exhale=5, extra_hold=0, label="Diaphragmatic Breathing")

    # Sequence
    def run_sequence(self, inhale: int, hold: int, exhale: int, extra_hold: int, label: str, loop: bool = True):
        if self.animation:
            self.animation.stop()
            self.animation.deleteLater()
            self.animation = None

        self.current_cycle = 0
        self.infoLabel.setText(f"{label} — tap Back to exit")
        self.phaseLabel.setText("")

        # Radius
        min_r = 20
        max_r = 120

        self.circle.setRadius(min_r)

        # animations
        anim_inhale = self._anim(self.circle, start=min_r, end=max_r, ms=inhale * 1000)
        pause_hold = QPauseAnimation(hold * 1000) if hold > 0 else None
        anim_exhale = self._anim(self.circle, start=max_r, end=min_r, ms=exhale * 1000)
        pause_extra = QPauseAnimation(extra_hold * 1000) if extra_hold > 0 else None

        group = QSequentialAnimationGroup(self)

        group.addAnimation(anim_inhale)
        if pause_hold:
            group.addAnimation(pause_hold)
        group.addAnimation(anim_exhale)
        if pause_extra:
            group.addAnimation(pause_extra)

        anim_inhale.stateChanged.connect(lambda s: self._set_phase("Inhale") if s == QAbstractAnimation.Running else None)
        if pause_hold:
            pause_hold.finished.connect(lambda: None) 
            anim_inhale.finished.connect(lambda: self._set_phase("Hold"))
        anim_exhale.stateChanged.connect(lambda s: self._set_phase("Exhale") if s == QAbstractAnimation.Running else None)
        if pause_extra:
            anim_exhale.finished.connect(lambda: self._set_phase("Hold"))

        # Looping behavior
        group.finished.connect(self._on_cycle_finished if loop else self._on_sequence_done)
        if loop:
            group.setLoopCount(1)
        else:
            group.setLoopCount(1)

        self.animation = group
        group.start()

    def _on_cycle_finished(self):
        self.current_cycle += 1

        phase_text = self.infoLabel.text()
        if "4-7-8" in phase_text:
            self.start_478()
        elif "Box" in phase_text:
            self.start_box()
        elif "Diaphragmatic" in phase_text:
            self.start_diaphragm()
        else:
            self._on_sequence_done()

    def _on_sequence_done(self):
        self._set_phase("Done")

    def _set_phase(self, text: str):
        self.phaseLabel.setText(text)

    def _anim(self, target, start: int, end: int, ms: int) -> QPropertyAnimation:
        a = QPropertyAnimation(target, b"radius", self)
        a.setDuration(ms)
        a.setStartValue(int(start))
        a.setEndValue(int(end))
        a.setEasingCurve(QEasingCurve.InOutCubic)
        return a

    def go_back(self):
        if self.animation:
            self.animation.stop()
        self.stacked_widget.setCurrentIndex(0)
