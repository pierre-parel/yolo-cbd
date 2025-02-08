# Run in terminal to get all packages: pip install imutils ultralytics numpy opencv-python
import imutils
from ultralytics import YOLO
import numpy as np
import cv2 as cv

model_detect = YOLO("weights/best-detect.pt")
model_cls = YOLO("weights/best-cls.pt")

class_labels = {
        0: "Broken",
        1: "Dried Cherry",
        2: "Floater",
        3: "Full Black",
        4: "Full Sour",
        5: "Fungus Damage",
        6: "Good",
        7: "Insect Damage"
}

max_label_length = max(len(label) for label in class_labels.values())

vid = cv.VideoCapture(0)
ret, frame = vid.read()
height, width = frame.shape[:2]
start_x = width // 2 - 112
start_y = height // 2 - 112
end_x = start_x + 224
end_y = start_y + 224
frame = frame[start_y:end_y, start_x:end_x]
frame = imutils.resize(frame, 665, 665)

# image size or you can get this from image shape
frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = vid.get(cv.CAP_PROP_FPS)
print(frame_width)
print(frame_height)
print(video_fps)

print("Frame Array:")
print("Array is of type: ", type(frame))
print("No. of dimensions: ", frame.ndim)
print("Shape of array: ", frame.shape)
print("Size of array: ", frame.size)
print("Array stores elements of type: ", frame.dtype)
data = np.flip(frame, 2)
data = data.ravel()
data = np.asarray(data, dtype='f')
texture_data = np.true_divide(data, 255.0)

temp = """Broken: 0.00%
Dried Cherry: 0.00%
Floater: 0.00%
Full Black: 0.00%
Full Sour: 0.00%
Fungus Damage: 0.00%
Good: 0.00%
Insect Damage: 0.00%"""

while True:
    ret, frame = vid.read()
    results = model_detect(source=frame, conf=0.6, show=True)
    boxes = results[0].boxes.xyxy.tolist()
    if len(boxes) == 0:
        continue

    im = np.zeros(2)
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        im = frame[int(y1):int(y2), int(x1):int(x2)]

    im = cv.resize(im, (640, 640))
    results = model_cls(source=im, show=True)
    k = input("Do you still want to continue? (y/n): ")
    if k == "n":
        break

cv.destroyAllWindows()
