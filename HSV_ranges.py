# set up sliders for HSV ranges
# pip install PyQt6 superqt
import sys
import cv2
import numpy as np

try:
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
    from PyQt6 import QtCore
except:
    print ("PyQt6 not found. Please run:")
    print ("sudo pip install PyQt6 --break-system-packages")
    sys.exit()
try:
    from superqt import QRangeSlider
except:
    print ("superqt noy found. Please run:")
    print ("sudo pip install superqt --break-system-packages")
    sys.exit()

class HSVTuner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HSV Range Tuner")

        layout = QVBoxLayout(self)

        # H: 0–179 (OpenCV uses 0–179)
        self.h_label = QLabel()
        self.h_slider = QRangeSlider(QtCore.Qt.Orientation.Horizontal)
        self.h_slider.setRange(0, 179)
        self.h_slider.setValue((20, 40))
        self.h_slider.valueChanged.connect(self.update)

        # S: 0–255
        self.s_label = QLabel()
        self.s_slider = QRangeSlider(QtCore.Qt.Orientation.Horizontal)
        self.s_slider.setRange(0, 255)
        self.s_slider.setValue((100, 255))
        self.s_slider.valueChanged.connect(self.update)

        # V: 0–255
        self.v_label = QLabel()
        self.v_slider = QRangeSlider(QtCore.Qt.Orientation.Horizontal)
        self.v_slider.setRange(0, 255)
        self.v_slider.setValue((100, 255))
        self.v_slider.valueChanged.connect(self.update)

        for lbl, sld in [(self.h_label, self.h_slider),
                         (self.s_label, self.s_slider),
                         (self.v_label, self.v_slider)]:
            layout.addWidget(lbl)
            layout.addWidget(sld)

        self.update()

    def update(self):
        self.h = self.h_slider.value()
        self.s = self.s_slider.value()
        self.v = self.v_slider.value()

        self.h_label.setText(f"H: {self.h[0]} – {self.h[1]}")
        self.s_label.setText(f"S: {self.s[0]} – {self.s[1]}")
        self.v_label.setText(f"V: {self.v[0]} – {self.v[1]}")

    def get_ranges(self):
        return (self.h, self.s, self.v)


# OpenCV capture loop
cap = cv2.VideoCapture(2)

app = QApplication(sys.argv)
tuner = HSVTuner()
tuner.show()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    (h1, h2), (s1, s2), (v1, v2) = tuner.get_ranges()
    mask = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered", result)

    if cv2.waitKey(1) == 27:   # ESC
        break

print ("H:",(h1,h2))
print ("S:",(s1,s2))
print ("V:",(v1,v2))
cap.release()
cv2.destroyAllWindows()

