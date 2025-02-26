#!/usr/bin/env python3

from ultralytics import YOLO

model = YOLO("weights/best-cls.pt")
path = "../datasets/cbd-classification/test/Fungus_Damage/*.jpg"

results = model(source=path, visualize=True, show=True)

for res in results:
    prob = res.probs
    input("Press enter to continue")
