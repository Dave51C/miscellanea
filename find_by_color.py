# $Source: /home/scrobotics/src/2025/RCS/find_by_color.py,v $
# $Revision: 1.3 $
# $Date: 2024-12-10 08:39:53-05 $
# $Author: scrobotics $
import cv2
import numpy as np
import argparse

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
    ## Find the largest contour (if any)
    #if len(contours) > 0:
    #    largest_contour = max(contours, key=cv2.contourArea)
    #    return largest_contour
    #else:
    #    return None

    # Read the image
    image = cv2.imread('image1783.png')
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    return(image)

def open_stream(webcam=0):
    stream = cv2.VideoCapture(webcam)  # Initialize webcam
    width  = stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return(stream, width, height)

def get_an_image(stream):
    _, frame = stream.read()          # Capture frame
    return(frame)

parser  = argparse.ArgumentParser()
parser.add_argument("--webcam", required=True, type=int, help="webcam number")
args    = parser.parse_args()
webcam  = args.webcam

# Define the color range for the object you want to find (in HSV)
#lower_orange = np.array([170, 0, 127])
#upper_orange = np.array([190, 255, 255])
lower_orange = np.array([160, 0, 127])
upper_orange = np.array([220, 255, 255])

stream, width, height = open_stream(webcam)
cutoff_width  = width/5
cutoff_height = height/5
prev_capture = get_an_image(stream)
while True:
    # Find the object
    capture      = get_an_image(stream)
    try:
        capture = cv2.bilateralFilter(capture, 9, 75, 75)
        #capture = cv2.medianBlur(capture, 5)
        #capture = cv2.GaussianBlur(capture, (5, 5), 0)
        #capture = cv2.blur(capture, (5, 5))
    except:
         pass
    contour_list = find_object_by_color(capture, lower_orange, upper_orange)

    for contour in contour_list:
        # Draw a bounding box around the object
        x, y, w, h = cv2.boundingRect(contour)
        if w >= cutoff_width or h >= cutoff_height:
            cv2.rectangle(capture, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # Display the result
    cv2.imshow('Image', capture)
    if cv2.waitKey(1) & 0xFF == ord('q'):    # Check for "q" 
         break

cv2.destroyAllWindows()           # Close the window

