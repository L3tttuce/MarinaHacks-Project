import cv2
from typing import List, Tuple

try:
    from deepface import DeepFace
    HAVE_DEEPFACE = True
except Exception:
    DeepFace = None
    HAVE_DEEPFACE = False

ANALYZE_EVERY = 5  
MIN_FACE = 60      
CAM_INDEX = 0   

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_bounding_box(bgr_img) -> List[Tuple[int, int, int, int]]:
    """Find faces and draw green rectangles"""
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(MIN_FACE, MIN_FACE)
    )
    return list(faces)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def draw_emotion_label(frame, x, y, w, h, label, score):
    """Overlay-Label."""
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if label:
        txt = f"{label} {int(score*100)}%"
        y_text = clamp(y - 10, 20, frame.shape[0] - 10)
        cv2.putText(frame, txt, (x, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def run():
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check CAM_INDEX or permissions.")

    frame_idx = 0
    last_emotions: List[Tuple[str, float]] = []

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            faces = detect_bounding_box(frame)

            if HAVE_DEEPFACE and frame_idx % ANALYZE_EVERY == 0 and faces:
                last_emotions = []
                for (x, y, w, h) in faces:
                    crop = frame[y:y+h, x:x+w]
                    try:
                        res = DeepFace.analyze(crop, actions=["emotion"], enforce_detection=False)
                        if isinstance(res, list) and res:
                            res = res[0]
                        emo = res.get("dominant_emotion")
                        conf = max(res.get("emotion", {}).values()) / 100.0 if "emotion" in res else 0.0
                        last_emotions.append((emo, conf))
                    except Exception:
                        last_emotions.append((None, None))
            for i, (x, y, w, h) in enumerate(faces):
                label, score = last_emotions[i] if i < len(last_emotions) else (None, None)
                draw_emotion_label(frame, x, y, w, h, label, score if score else 0.0)

            cv2.imshow("Face + Emotions (press 'q' to quit)", frame)
            frame_idx += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
