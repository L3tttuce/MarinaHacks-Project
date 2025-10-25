import cv2
from typing import List, Tuple

from deepface import DeepFace
HAVE_DEEPFACE = True

ANALYZE_EVERY = 5
MIN_FACE = 60
CAM_INDEX = 0

# --- Gesichtserkenner (Haar) ---
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_bounding_box(bgr_img) -> List[Tuple[int, int, int, int]]:
    """Find faces and draw green rectangles"""
    gray_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(bgr_img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

def draw_emotion_label(img, x, y, w, h, label, score):
    """Overlay-Label."""
    if not label:
        return
    txt = label
    if score is not None:
        try:
            pct = int(round(float(score)))
            txt += f" ({pct}%)"
        except Exception:
            pass

    y1 = max(0, y - 28)
    y2 = max(0, y - 2)
    cv2.rectangle(img, (x, y1), (x + max(120, w), y2), (0, 0, 0), -1)
    cv2.putText(img, txt, (x + 6, max(12, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)


video_capture = cv2.VideoCapture(CAM_INDEX)
if not video_capture.isOpened():
    raise RuntimeError("Could not open webcam. Check CAM_INDEX or permissions.")

frame_idx = 0
last_emotions: List[Tuple[str, float]] = []

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

while True:
    result, video_frame = video_capture.read()
    if not result:
        break

    frame_idx += 1


    faces = detect_bounding_box(video_frame)


    curr_emotions: List[Tuple[str, float]] = []
    if HAVE_DEEPFACE and faces is not None and len(faces):
        if frame_idx % ANALYZE_EVERY == 0:

            rgb = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
            for (x, y, w, h) in faces:
                if w < MIN_FACE or h < MIN_FACE:
                    curr_emotions.append((None, None))
                    continue
                pad = int(0.10 * max(w, h))
                H, W = video_frame.shape[:2]
                x1 = clamp(x - pad, 0, W - 1)
                y1 = clamp(y - pad, 0, H - 1)
                x2 = clamp(x + w + pad, 0, W - 1)
                y2 = clamp(y + h + pad, 0, H - 1)
                face_rgb = rgb[y1:y2, x1:x2]
                if face_rgb.size == 0:
                    curr_emotions.append((None, None))
                    continue
                try:
                    res = DeepFace.analyze(
                        face_rgb,
                        actions=["emotion"],
                        enforce_detection=False,
                        detector_backend="skip"
                    )
                    if isinstance(res, list):
                        res = res[0]
                    label = res.get("dominant_emotion")
                    emod = res.get("emotion") or {}
                    score = emod.get(label, None)

                    if isinstance(score, float) and score <= 1.0:
                        score *= 100.0
                    curr_emotions.append((label, score))
                except Exception:
                    curr_emotions.append((None, None))
            last_emotions = curr_emotions
        else:

            curr_emotions = (last_emotions[:len(faces)] +
                             [(None, None)] * max(0, len(faces) - len(last_emotions)))
    else:
        curr_emotions = [(None, None)] * len(faces)

    for i, (x, y, w, h) in enumerate(faces):
        label, score = curr_emotions[i] if i < len(curr_emotions) else (None, None)
        draw_emotion_label(video_frame, x, y, w, h, label, score)

    cv2.imshow("Face + Emotions (press 'q' to quit)", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
