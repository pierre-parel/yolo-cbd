# Run in terminal to get all packages: pip install imutils ultralytics numpy opencv-python
import imutils
from ultralytics import YOLO
import numpy as np
import cv2 as cv

import serial
import time

# Import models
model_detect = YOLO("weights/best-detect.pt")
model_cls = YOLO("weights/best-cls.pt")

vid = cv.VideoCapture(0)

temp = """Broken: 0.00%
Dried Cherry: 0.00%
Floater: 0.00%
Full Black: 0.00%
Full Sour: 0.00%
Fungus Damage: 0.00%
Good: 0.00%
Insect Damage: 0.00%"""
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print(p)

arduino = serial.Serial(port="COM6", timeout=.1)

def write_read(x):
    # print(bytes(x, 'utf-8'))
    num_bytes_written = arduino.write(bytes(x, 'utf-8'))
    # print(f"Number of bytes written: {num_bytes_written}")
    time.sleep(0.05)
    data = arduino.readline()
    return data

def read_serial():
    data = arduino.readline()
    return data

value = write_read(str(0))
queue = []
while True:
    if read_serial() == b'0':
        ret, frame = vid.read()
        # cv.imshow("Frame", frame)
        results = model_detect(source=frame, conf=0.6, verbose=False)
        boxes = results[0].boxes.xyxy.tolist()
        if len(boxes) != 1:
            # print("No beans or multiple beans in picture")
            if len(queue) == 4:
                val = str(queue.pop(0)) + '\n'
                value = write_read(val)
            else:
                write_read("-1")
            queue.append(0)
            # for v in queue:
            #     print(v, end=' ')
            # print()
            continue
        im = np.zeros(2)
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            im = frame[int(y1):int(y2), int(x1):int(x2)]

        im = cv.resize(im, (640, 640))
        results = model_cls(source=im, show=True, verbose=False)

        top1 = results[0].probs.top1
        val = ""
        if len(queue) == 4:
            val = str(queue.pop(0)) + '\n'
            value = write_read(val)
        else:
            write_read("-1")
        queue.append(top1)
        # print(f"Appended to queue: {top1}")
        # for v in queue:
        #     print(v, end=' ')
        # print()

cv.destroyAllWindows()
