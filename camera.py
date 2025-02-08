#!/usr/bin/env python3
import imutils
from ultralytics import YOLO
import numpy as np
import cv2 as cv
import dearpygui.dearpygui as dpg

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

dpg.create_context()
dpg.create_viewport(title='CBD', width=1280, height=720, resizable=False)
dpg.setup_dearpygui()

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

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data,
                        tag="texture_tag", format=dpg.mvFormat_Float_rgb)

temp = """Broken: 0.00%
Dried Cherry: 0.00%
Floater: 0.00%
Full Black: 0.00%
Full Sour: 0.00%
Fungus Damage: 0.00%
Good: 0.00%
Insect Damage: 0.00%"""

with dpg.window(label="main", tag="main", no_resize=True):
    with dpg.group(horizontal=True):
        with dpg.group():
            dpg.add_image("texture_tag")
        with dpg.child_window(autosize_x=True, autosize_y=True):
            dpg.add_text(f"{temp}", tag="prediction_text")


# dpg.show_metrics()
# dpg.show_font_manager()

dpg.set_global_font_scale(1.75)
dpg.show_viewport()
dpg.set_primary_window("main", True)

# while dpg.is_dearpygui_running():
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
    input("Press enter to continue")
    # label_probabilities = {class_labels[i]: prob for i, prob in enumerate(probabilities)}
    # sorted_predictions = sorted(label_probabilities.items(), key=lambda x: x[1], reverse=True)
    # output_string = "\n".join([f"{label.ljust(max_label_length)}: {prob * 100:.2f}%"
    #                            for label, prob in sorted_predictions])

    # y_pred = np.argmax(prediction, axis=1)[0]
    # predicted_label = f"{class_labels[y_pred]}"
    # dpg.set_value("prediction_text", f"{output_string}")

    # frame = imutils.resize(im, 665, 665)
    # data = np.flip(frame, 2)
    # data = data.ravel()
    # data = np.asarray(data, dtype='f')
    # texture_data = np.true_divide(data, 255.0)
    # dpg.set_value("texture_tag", texture_data)
    # dpg.render_dearpygui_frame()

vid.release()
dpg.destroy_context()
