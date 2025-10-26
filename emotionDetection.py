import cv2
import matplotlib.pyplot as plt

def run():
    imagePath = "input_image.jpg"  # make sure this file exists in the same folder
    img = cv2.imread(imagePath)
    if img is None:
        raise FileNotFoundError(f"Could not read {imagePath}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(12, 8))
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title("Detected Faces")
    plt.show()

if __name__ == "__main__":
    run()
