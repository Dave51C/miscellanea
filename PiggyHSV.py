import cv2
import sys
import numpy as np
from pprint import pprint

from cv2 import WINDOW_NORMAL

HSV       = np.array([0,0,0])
lower_HSV = np.array([0, 0, 0])
upper_HSV = np.array([0, 0, 0])

def open_stream(webcam):
    stream = cv2.VideoCapture(webcam)  # Initialize webcam
    width  = stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return(stream, width, height) 

def fetch_frame(stream):
    ret, frame = stream.read()          # Capture frame
    return(frame)

def on_mouse(event, x, y, flags, param):
    global HSV
    # Check if the event was the left mouse button being clicked 
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the BGR pixel value at the clicked location
        pixel = frame[y, x]

        # Convert BGR to HSV and print the pixel value
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
        HSV = hsv_pixel[0][0]

def set_initial_color():
    clicked = False
    while not clicked:
        frame = fetch_frame(cap)
        cv2.setMouseCallback('Webcam', on_mouse)
        cv2.imshow('Webcam', frame)              # Display frame
        clicked = True
        print (HSV)
    

def find_object_by_color(image, lower_color, upper_color):
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply morphological operations to remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

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
    print ("superqt not found. Please run:")
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
        self.h_slider.setValue((20, 40))           # Initialize h_slider tuple.
        self.h_slider.valueChanged.connect(self.update)

        # S: 0–255
        self.s_label = QLabel()
        self.s_slider = QRangeSlider(QtCore.Qt.Orientation.Horizontal)
        self.s_slider.setRange(0, 255)
        self.s_slider.setValue((100, 255))          # Initialize s_slider tuple.
        self.s_slider.valueChanged.connect(self.update)

        # V: 0–255
        self.v_label = QLabel()
        self.v_slider = QRangeSlider(QtCore.Qt.Orientation.Horizontal)
        self.v_slider.setRange(0, 255)
        self.v_slider.setValue((100, 255))          # Initialize v_slider tuple.
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
        return (self.h, self.s, self.v)   # Return H, S, & V range tuples.

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, help="video device number", default=0)
    args = parser.parse_args()

    cap,width,height = open_stream(args.device)
    cutoff_width     = width/2
    cutoff_height    = height/2
    cv2.namedWindow('Webcam', WINDOW_NORMAL)
    app          = QApplication(sys.argv)
    tuner        = HSVTuner()
    print(tuner.__dict__)
    print(tuner.__dict__.keys())
    set_initial_color()
    lower_HSV[0] = min(0,HSV[0]-10)
    lower_HSV[1] = min(0,HSV[1]-10)
    lower_HSV[2] = min(0,HSV[2]-10)
    upper_HSV[0] = max(179,HSV[0]+10)
    upper_HSV[1] = max(255,HSV[1]+10)
    upper_HSV[2] = max(255,HSV[2]+10)
    #print (HSV)
    print (lower_HSV)
    print (tuner.h)
    tuner.h_slider = (lower_HSV[0],upper_HSV[0])
    tuner.s_slider = (lower_HSV[1],upper_HSV[1])
    tuner.v_slider = (lower_HSV[2],upper_HSV[2])
    print (tuner.h)
    print (tuner.get_ranges())
    tuner.show()

    while True:                       # Repeat the following until "q" key hit
        frame = fetch_frame(cap)
        #cv2.setMouseCallback('Webcam', on_mouse)
        lower_HSV = np.array([tuner.h[0],tuner.s[0],tuner.v[0]])
        upper_HSV = np.array([tuner.h[1],tuner.s[1],tuner.v[1]])
        contour_list = find_object_by_color(frame, lower_HSV, upper_HSV)
        for contour in contour_list:
            # Draw a bounding box around the object
            x, y, w, h = cv2.boundingRect(contour)
            if w >= cutoff_width or h >= cutoff_height:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

        cv2.imshow('Webcam', frame)              # Display frame
        if cv2.waitKey(1) & 0xFF == ord('q'):    # Check for "q" 
            break
    cap.release()                     # Release the webcam
    cv2.destroyAllWindows()           # Close the window
