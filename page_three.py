from typing import List, Tuple, Optional
from PySide6 import QtCore, QtGui, QtWidgets

import cv2

# optional deepface (kept graceful if it's missing)
try:
    from deepface import DeepFace
    HAVE_DEEPFACE = True
except Exception:
    DeepFace = None
    HAVE_DEEPFACE = False

from logEmotion import LogEmotion

ANALYZE_EVERY = 5  
MIN_FACE = 60  
CAM_INDEX = 0    

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_faces(bgr_img) -> List[Tuple[int, int, int, int]]:
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(MIN_FACE, MIN_FACE)
    )
    return list(faces)

def draw_label(frame, x, y, w, h, label: Optional[str], score: Optional[int]):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if label:
        txt = f"{label} {score or 0}%"
        y_text = max(20, min(y - 10, frame.shape[0] - 10))
        cv2.putText(frame, txt, (x, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

class CameraWorker(QtCore.QThread):
    frameReady = QtCore.Signal(QtGui.QImage)         # emits the painted frame
    status     = QtCore.Signal(str)                  # status text
    lastEmotion = QtCore.Signal(str, int)            # (emotion, confidence%)

    def __init__(self, name: str = "Guest", logfile: str = "stats.json", parent=None):
        super().__init__(parent)
        self._running = False
        self.name = name or "Guest"
        self.logger = LogEmotion(logfile) if logfile else None

    def stop(self):
        self._running = False

    def run(self):
        self._running = True
        cap = cv2.VideoCapture(CAM_INDEX)
        if not cap.isOpened():
            self.status.emit("Could not open webcam. Check camera index/permissions.")
            return

        self.status.emit("Camera started.")
        frame_idx = 0
        try:
            while self._running:
                ok, frame = cap.read()
                if not ok:
                    self.status.emit("Camera read failed.")
                    break

                faces = detect_faces(frame)

                if HAVE_DEEPFACE and faces and (frame_idx % ANALYZE_EVERY == 0):
                    (x, y, w, h) = faces[0]
                    crop = frame[y:y + h, x:x + w]
                    try:
                        res = DeepFace.analyze(crop, actions=["emotion"], enforce_detection=False)
                        if isinstance(res, list) and res:
                            res = res[0]
                        emo = (res.get("dominant_emotion") or "").lower()
                        emo_dict = res.get("emotion", {})
                        conf = int(round(max(emo_dict.values()))) if emo_dict else 0

                        # draw & log
                        draw_label(frame, x, y, w, h, emo, conf)
                        if self.logger and emo:
                            self.logger.appendJSON(self.name, emo, conf)

                        self.lastEmotion.emit(emo, conf)
                    except Exception as e:
                        self.status.emit(f"DeepFace error: {e}")
                else:
                    # Draw boxes if not analyzing this frame
                    for (x, y, w, h) in faces:
                        draw_label(frame, x, y, w, h, None, None)

                # Convert BGR into RGB then into QImage
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qimg = QtGui.QImage(rgb.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
                self.frameReady.emit(qimg)

                frame_idx += 1
        finally:
            cap.release()
            self.status.emit("Camera stopped.")

class PageThree(QtWidgets.QWidget):
    def __init__(self, stacked_widget: QtWidgets.QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.worker: Optional[CameraWorker] = None

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # Header
        header = QtWidgets.QFrame()
        header.setObjectName("Header")
        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(24, 16, 24, 16)
        title = QtWidgets.QLabel("Real-Time Face Detection")
        title.setObjectName("Title")
        subtitle = QtWidgets.QLabel("Detect faces, analyze emotions, and log results")
        subtitle.setObjectName("Subtitle")
        col = QtWidgets.QVBoxLayout()
        col.addWidget(title); col.addWidget(subtitle)
        h.addLayout(col); h.addStretch(1)
        root.addWidget(header)

        # Controls row
        controls = QtWidgets.QHBoxLayout()
        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setPlaceholderText("Name to log (Guest if left default)")
        self.startBtn = QtWidgets.QPushButton("▶ Start")
        self.stopBtn  = QtWidgets.QPushButton("⏹ Stop")
        self.backBtn  = QtWidgets.QPushButton("⬅ Back")
        controls.addWidget(self.nameEdit)
        controls.addWidget(self.startBtn)
        controls.addWidget(self.stopBtn)
        controls.addStretch(1)
        controls.addWidget(self.backBtn)
        root.addLayout(controls)

        # Video surface
        self.videoLabel = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.videoLabel.setFixedSize(640, 480) 
        self.videoLabel.setStyleSheet("""
            background:#0a0f21;
            border:1px solid rgba(255,255,255,0.06);
            border-radius:12px;
        """)
        root.addWidget(self.videoLabel, alignment=QtCore.Qt.AlignCenter)


        # Status line
        self.statusLine = QtWidgets.QLabel("")
        self.statusLine.setAlignment(QtCore.Qt.AlignCenter)
        root.addWidget(self.statusLine)

        # Signals
        self.startBtn.clicked.connect(self.start_camera)
        self.stopBtn.clicked.connect(self.stop_camera)
        self.backBtn.clicked.connect(self.go_back)

    def start_camera(self):
        if self.worker and self.worker.isRunning():
            return
        name = (self.nameEdit.text() or "Guest").strip()
        self.worker = CameraWorker(name=name, logfile="stats.json", parent=self)
        self.worker.frameReady.connect(self.on_frame)
        self.worker.status.connect(self.statusLine.setText)
        self.worker.lastEmotion.connect(self.on_emotion)
        self.worker.start()
        self.statusLine.setText("Starting camera…")

    def stop_camera(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait(1500)
            self.worker = None

    def go_back(self):
        self.stop_camera()
        self.stacked_widget.setCurrentIndex(0)

    # Slots
    @QtCore.Slot(QtGui.QImage)
    def on_frame(self, qimg: QtGui.QImage):
        pix = QtGui.QPixmap.fromImage(qimg)
        self.videoLabel.setPixmap(pix.scaled(640, 480, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))


    @QtCore.Slot(str, int)
    def on_emotion(self, emo: str, conf: int):
        self.statusLine.setText(f"Detected: {emo or 'unknown'} ({conf}%)")

