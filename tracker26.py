import cv2
import numpy as np
import sys
from time import sleep

from ntcore import NetworkTableInstance
from PiggyVision25 import rotate

IP='localhost'

if len(sys.argv) >= 2:
    IP = sys.argv[1]

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

scale       = 1.5
width       = int(800 * scale)
height      = int(600 * scale)
FieldWidth  = int(691 * scale)
FieldHeight = int(317 * scale)
field_offset = np.array([50,50])
field = np.array([[0, 0], [0, FieldHeight], [FieldWidth, FieldHeight],  [FieldWidth, 0]] )
field = field + field_offset

# generate 1st hex
Hx = 176.75 * scale + field_offset[0]
Hy = FieldHeight/2 + field_offset[1]
R = 43.59 * scale
hex=np.array([],np.int32)
other_hex=np.array([],np.int32)
for I in range (0, 6):
    newx, newy = rotate (Hx+R, Hy, Hx, Hy, np.radians(I*60)+np.radians(30),Integer=True)
    #newx += field_offset[0]
    #newy += field_offset[1]
    hex = np.append(hex,[newx,newy])
    other_hex=np.append(other_hex,[newx+int(338 * scale),newy])

hex = hex.reshape((-1, 1, 2))
other_hex = other_hex.reshape((-1, 1, 2))
print (hex)

BLUE   = (255,0,0)
GREEN  = (0,255,0)
RED    = (0,0,255)
CYAN   = (255,255,0)
YELLOW = (0,255,255)
GRAY   = (140,140,140)
#img = cv2.polylines(img, [hex], isClosed, GREEN, thickness)


RobotX = subRobotWorldX.get()
while RobotX == -1:
    sleep(1)
    RobotX = subRobotWorldX.get()
print ("Talking to Table Server")
black_box = np.full((height,width,3),[0,0,0],dtype=np.uint8)
img = np.copy(black_box)
field_img = np.copy(img)
for G in range (FieldHeight,0,round(-20 * scale)):
    cv2.line(field_img, (50,G+50),(50+FieldWidth,G+50), GRAY, 1)
for G in range (0, FieldWidth, round(20 * scale)):
    cv2.line(field_img, (G+50,50),(G+50,50+FieldHeight), GRAY, 1)
cv2.polylines(field_img, [field], True, GREEN, 3 )
cv2.polylines(field_img, [hex], True, GREEN, 3 )
cv2.fillPoly(field_img, [hex], (0, 0, 0)) 
cv2.polylines(field_img, [other_hex], True, GREEN, 3 )
cv2.fillPoly(field_img, [other_hex], (0, 0, 0)) 
while True:
    img = np.copy(field_img)
    RobotX = round ((subRobotWorldX.get() + field_offset[0]) * scale)
    RobotY = field_offset[1] + FieldHeight - round (subRobotWorldY.get() * scale)
    CameraX = round ((subCamWorldX.get() + field_offset[0]) * scale)
    CameraY = field_offset[1] + FieldHeight - round (subCamWorldY.get() * scale)
    cv2.circle (img,(RobotX,RobotY),10,RED,-1)
    cv2.circle (img,(CameraX,CameraY),10,CYAN,-1)
    cv2.imshow   ('TRACKER',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

