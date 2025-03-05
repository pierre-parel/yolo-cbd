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

vid1 = cv.VideoCapture(0)
ret1, frame1 = vid1.read()
vid2 = cv.VideoCapture(1)
ret2, frame2 = vid2.read()
temp = """Broken: 0.00%
Dried Cherry: 0.00%
Floater: 0.00%
Full Black: 0.00%
Full Sour: 0.00%
Fungus Damage: 0.00%
Good: 0.00%
Insect Damage: 0.00%"""

while True:
    ret1, frame1 = vid1.read()
    ret2, frame2 = vid2.read()
    results1 = model_detect(source=frame1, conf=0.8, show=True)
    results2 = model_detect(source=frame2, conf=0.8, show=True)

    # Process top of bean
    boxes1 = results1[0].boxes.xyxy.tolist()
    boxes2 = results2[0].boxes.xyxy.tolist()

    if len(boxes2) == 0:
        continue
    if len(boxes1) == 0:
        continue

    im1 = np.zeros(2)
    for i, box in enumerate(boxes1):
        x1, y1, x2, y2 = box
        im1 = frame1[int(y1):int(y2), int(x1):int(x2)]

    im1 = cv.resize(im1, (640, 640))
    results1 = model_cls(source=im1, show=True)

    input("Press enter to view bottom")

    # Process bottom of bean
    im2 = np.zeros(2)
    for i, box in enumerate(boxes2):
        x1, y1, x2, y2 = box
        im2 = frame2[int(y1):int(y2), int(x1):int(x2)]

    im2 = cv.resize(im2, (640, 640))
    results2 = model_cls(source=im2, show=True)

    k = input("Do you still want to continue? (y/n): ")
    if k == "n":
        break

cv.destroyAllWindows()
