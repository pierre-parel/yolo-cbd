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

vid1 = cv.VideoCapture(0)
vid2 = cv.VideoCapture(1)


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

        ret1, frame1 = vid1.read()
        ret2, frame2 = vid2.read()
        results1 = model_detect(source=frame1, conf=0.8, show=True)
        results2 = model_detect(source=frame2, conf=0.8, show=True)

        # Process top of bean
        boxes1 = results1[0].boxes.xyxy.tolist()
        boxes2 = results2[0].boxes.xyxy.tolist()

        if len(boxes1) != 1 or len(boxes2) != 1:

            # print("No beans or multiple beans in picture")

            if len(queue) == 4:

                val = str(queue.pop(0)) + '\n'

                value = write_read(val)
            else:

                write_read("-1")

            queue.append(0)
            continue

        im1 = np.zeros(2)
        for i, box in enumerate(boxes1):
            x1, y1, x2, y2 = box
            im1 = frame1[int(y1):int(y2), int(x1):int(x2)]

        im1 = cv.resize(im1, (640, 640))
        results1 = model_cls(source=im1, show=True)


        im2 = np.zeros(2)
        for i, box in enumerate(boxes2):
            x1, y1, x2, y2 = box
            im2 = frame2[int(y1):int(y2), int(x1):int(x2)]

        im2 = cv.resize(im2, (640, 640))
        results2 = model_cls(source=im2, show=True)

        top_result = results1[0].probs.top1 
        bot_result = results2[0].probs.top1

        result = -1
        # If one is black and the other is dried cherry, use black
        if (top_result == 0 and bot_result == 1) or (top_result == 1 and bot_result == 0):
            result = 0
        # If one is good, and the other is not, pick the other
        elif (top_result == 5 and bot_result != 5):
            result = bot_result
        elif (top_result != 5 and bot_result == 5):
            result = bot_result
        else:
            result = max(results1[0].probs.top1conf.item(), results2[0].probs.top1conf.item())

        val = ""

        if len(queue) == 4:

            val = str(queue.pop(0)) + '\n'

            value = write_read(val)
        else:
            write_read("-1")

        queue.append(result)

        # print(f"Appended to queue: {top1}")

        # for v in queue:

        #     print(v, end=' ')

        # print()


cv.destroyAllWindows()

