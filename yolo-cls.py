#!/usr/bin/env python3

from ultralytics import YOLO # install ultralytics with `pip install ultralytics`
path="../datasets/cbd-classification/test/Black/*.jpg"
model = YOLO("best-cls.pt")
# results = model(source=0, show=True, stream=True) # Change 0 to select other webcams
results = model(source=path, stream=True)
for res in results:
    print(res.probs)
    input("Press enter to continue")
