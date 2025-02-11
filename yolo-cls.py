#!/usr/bin/env python3

from ultralytics import YOLO # install ultralytics with `pip install ultralytics`
path="../datasets/cbd-classification/test/Black/*.jpg"
model = YOLO("weights/best-cls.pt")
# results = model(source=0, show=True, stream=True) # Change 0 to select other webcams
# results = model(source=path, stream=True)
# for res in results:
#     print(res.probs.top1)
#     input("Press enter to continue")
metrics = model.val()
