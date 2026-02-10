import cv2
import numpy as np
from ntcore import NetworkTableInstance

IP='localhost'

print (IP)
ntinst       = NetworkTableInstance.getDefault()
ntinst.setServer(IP)
ntinst.startClient4("Tracker")
CamPos_tbl   = ntinst.getTable("CamPos")
subCamWorldX = CamPos_tbl.getDoubleTopic("Camera_X").subscribe(-1)
subCamWorldY = CamPos_tbl.getDoubleTopic("Camera_Y").subscribe(-1)
subCamWorldR = CamPos_tbl.getDoubleTopic("Robot_Rot").subscribe(-1)
subRobotWorldX = CamPos_tbl.getDoubleTopic("Robot_X").subscribe(-1)
subRobotWorldY = CamPos_tbl.getDoubleTopic("Robot_Y").subscribe(-1)

img = np.zeros((600, 800, 3), dtype='uint8')
fieldwall = np.array([
    [ 50,50 ]
   ,[ 701,50 ]
   ,[ 701,367 ]
   ,[ 50,367 ]
])
redhub = np.array([
    [ 209,185 ]
   ,[ 209,232 ]
   ,[ 256,232 ]
   ,[ 256,185 ]
])
redrightbump = np.array([
    [ 209,232 ]
   ,[ 209,305 ]
   ,[ 256,305 ]
   ,[ 256,232 ]
])
redleftbump = np.array([
    [ 209,185 ]
   ,[ 209,112 ]
   ,[ 256,112 ]
   ,[ 256,185 ]
])
redlefttrench = np.array([
    [ 229,112 ]
   ,[ 229,61 ]
   ,[ 235,61 ]
   ,[ 235,112 ]
])
redrighttrench = np.array([
    [ 230,305 ]
   ,[ 230,355 ] 
   ,[ 234,355 ]
   ,[ 234,305 ]
])
bluehub = np.array([
    [ 496,185 ]
   ,[ 496,232 ]
   ,[ 543,232 ]
   ,[ 543,185 ]
])
bluerightbump = np.array([
    [ 496,232 ]
   ,[ 496,305 ]
   ,[ 543,305 ]
   ,[ 543,232 ]
])
blueleftbump = np.array([
    [ 496,185 ]
   ,[ 496,112 ]
   ,[ 543,112 ]
   ,[ 543,185 ]
])
bluelefttrench = np.array([
    [ 516,112 ]
   ,[ 516,61 ]
   ,[ 522,61 ]
   ,[ 522,112 ]
])
bluerighttrench = np.array([
    [ 517,305 ]
   ,[ 517,355 ]
   ,[ 521,355 ]
   ,[ 521,305 ]
])
reddepot = np.array([
    [ 50,112 ]
   ,[ 77,112 ]
   ,[ 77,154 ]
   ,[ 50,154 ]
])
bluedepot = np.array([
    [ 701,264 ]
   ,[ 674,264 ]
   ,[ 674,306 ]
   ,[ 701,306 ]
])
redtower = np.array([
    [ 50,203 ]
   ,[ 94,203 ]
   ,[ 94,197 ]
   ,[ 94,244 ]
   ,[ 94,238 ]
   ,[ 50,238 ]
])
bluetower = np.array([
    [ 701,180 ]
   ,[ 657,180 ]
   ,[ 657,174 ]
   ,[ 657,221 ]
   ,[ 657,215 ]
   ,[ 701,215 ]
])
WHITE = (255,255,255)
REDy = (0,255,255)
BLUEg = (0,255,0)
cv2.polylines(img, [fieldwall], 1, WHITE, 2)
cv2.polylines(img, [redhub], 1, REDy, 2)
cv2.polylines(img, [redrightbump], 1, REDy, 2)
cv2.polylines(img, [redleftbump], 1, REDy, 2)
cv2.polylines(img, [redlefttrench], 1, REDy, 2)
cv2.polylines(img, [redrighttrench], 1, REDy, 2)
cv2.polylines(img, [bluehub], 1, BLUEg, 2)
cv2.polylines(img, [bluerightbump], 1, BLUEg, 2)
cv2.polylines(img, [blueleftbump], 1, BLUEg, 2)
cv2.polylines(img, [bluelefttrench], 1, BLUEg, 2)
cv2.polylines(img, [bluerighttrench], 1, BLUEg, 2)
cv2.polylines(img, [reddepot], 1, REDy, 2)
cv2.polylines(img, [bluedepot], 1, BLUEg, 2)
cv2.polylines(img, [redtower], 1, REDy, 2)
cv2.polylines(img, [bluetower], 1, BLUEg, 2)
winname = 'example'
cv2.namedWindow(winname)
cv2.imshow(winname, img)
cv2.waitKey()
cv2.destroyWindow(winname)
