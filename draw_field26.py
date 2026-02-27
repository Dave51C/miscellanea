import argparse
import cv2
from   ntcore import NetworkTableInstance
import numpy as np

def rotBot (points, rot):
    rotMat  = np.array([[np.cos(rot), -np.sin(rot)]
                       ,[np.sin(rot),  np.cos(rot)]])
    # The transpose below (.T) is because of the way numpy stores the array.
    return np.round(points@rotMat.T).astype(int)

IP='localhost'

print (IP)
ntinst         = NetworkTableInstance.getDefault()
ntinst.setServer(IP)
ntinst.startClient4("Tracker")
BotPos_tbl     = ntinst.getTable("BotPos")
#subCamWorldX   = BotPos_tbl.getDoubleTopic("Camera_X").subscribe(-1)
#subCamWorldY   = BotPos_tbl.getDoubleTopic("Camera_Y").subscribe(-1)
subRobotRot    = BotPos_tbl.getDoubleTopic("Robot_Rot").subscribe(-1)
subRobotWorldX = BotPos_tbl.getDoubleTopic("Robot_X").subscribe(-1)
subRobotWorldY = BotPos_tbl.getDoubleTopic("Robot_Y").subscribe(-1)

TAGXYR={
    1: np.array([468, 292, 180]),
    2: np.array([469, 183, 90]),
    3: np.array([445, 173, 180]),
    4: np.array([445, 159, 180]),
    5: np.array([469, 135, 270]),
    6: np.array([468, 25, 180]),
    7: np.array([471, 25, 0]),
    8: np.array([483, 135, 270]),
    9: np.array([493, 144, 0]),
    10: np.array([493, 159, 0]),
    11: np.array([483, 183, 90]),
    12: np.array([471, 292, 0]),
    13: np.array([652, 291, 180]),
    14: np.array([651, 274, 180]),
    15: np.array([651, 170, 180]),
    16: np.array([651, 153, 180]),
    17: np.array([186, 25, 0]),
    18: np.array([182, 135, 270]),
    19: np.array([206, 145, 0]),
    20: np.array([206, 159, 0]),
    21: np.array([182, 183, 90]),
    22: np.array([184, 292, 0]),
    23: np.array([181, 292, 180]),
    24: np.array([168, 183, 90]),
    25: np.array([158, 172, 180]),
    26: np.array([158, 158, 180]),
    27: np.array([168, 135, 270]),
    28: np.array([181, 25, 180]),
    29: np.array([0, 26, 0]),
    30: np.array([0, 43, 0]),
    31: np.array([0, 147, 0]),
    32: np.array([0, 164, 0])
}
img      = np.zeros((600, 800, 3), dtype='uint8')
offset   = np.array([[75,75]])
tagProxy = np.array([[-5,5], [5,5], [5,-5], [-5,-5]])
polyBot  = np.array([[0,0],[-12,-8],[-12,-2],[-30,-2],[-30,2],[-12,2],[-12,8]])
#           (0,0)
#             /\
#            /  \
#           /    \
# (-12,-8) /__  __\ (-12,8)     ( exquisite visual aid )
#    (-12,-2)|  |(-12,1)
#            |  |
#            |  |
#            |  |
#    (-30,-2)|__|(-30,2)

fieldLength = 651
fieldWidth  = 317
fieldwall       = np.array([[0,  0] ,[fieldLength,  0] ,[fieldLength,fieldWidth]
                           ,[0,fieldWidth]])
redhub          = np.array( [[159,135] ,[159,182] ,[206,182] ,[206,135]])
redrightbump    = np.array( [[159,182] ,[159,255] ,[206,255] ,[206,182]])
redleftbump     = np.array( [[159,135] ,[159, 62] ,[206, 62] ,[206,135]])
redlefttrench   = np.array( [[179, 62] ,[179, 11] ,[185, 11] ,[185, 62]])
redrighttrench  = np.array( [[180,255] ,[180,305] ,[184,305] ,[184,255]])
bluehub         = np.array( [[446,135] ,[446,182] ,[493,182] ,[493,135]])
bluerightbump   = np.array( [[446,182] ,[446,255] ,[493,255] ,[493,182]])
blueleftbump    = np.array( [[446,135] ,[446, 62] ,[493, 62] ,[493,135]])
bluelefttrench  = np.array( [[466, 62] ,[466, 11] ,[472, 11] ,[472, 62]])
bluerighttrench = np.array( [[467,255] ,[467,305] ,[471,305] ,[471,255]])
reddepot        = np.array( [[  0 ,62] ,[ 27, 62] ,[ 27,104] ,[  0,104]])
bluedepot       = np.array( [[651,214] ,[624,214] ,[624,256] ,[651,256]])
redtower        = np.array( [[  0,153] ,[ 44,153] ,[ 44,147] ,[ 44,194]
                            ,[ 44,188] ,[  0,188]])
bluetower       = np.array( [[651,130] ,[607,130] ,[607,124] ,[607,171]
                            ,[607,165] ,[651,165]])
WHITE  = (255,255,255)
RED    = (0,0,255)
GRAY   = (100,100,100)
GREEN  = (0,255,0)
YELLOW = (0,255,255)
BLUE   = (0,255,0)
parser = argparse.ArgumentParser()
parser.add_argument("--tags", nargs='+', type=int, help="List of Tag IDs to show")
#parser.add_argument("--cam", nargs=2, type=int, help="camera's x & y")
args = parser.parse_args()

# Draw field elements
cv2.polylines(img, [fieldwall+offset],       1, WHITE, 2)
cv2.polylines(img, [redhub+offset],          1, YELLOW, 2)
cv2.polylines(img, [redrightbump+offset],    1, YELLOW, 2)
cv2.polylines(img, [redleftbump+offset],     1, YELLOW, 2)
cv2.polylines(img, [redlefttrench+offset],   1, YELLOW, 2)
cv2.polylines(img, [redrighttrench+offset],  1, YELLOW, 2)
cv2.polylines(img, [bluehub+offset],         1, BLUE, 2)
cv2.polylines(img, [bluerightbump+offset],   1, BLUE, 2)
cv2.polylines(img, [blueleftbump+offset],    1, BLUE, 2)
cv2.polylines(img, [bluelefttrench+offset],  1, BLUE, 2)
cv2.polylines(img, [bluerighttrench+offset], 1, BLUE, 2)
cv2.polylines(img, [reddepot+offset],        1, YELLOW, 2)
cv2.polylines(img, [bluedepot+offset],       1, BLUE, 2)
cv2.polylines(img, [redtower+offset],        1, YELLOW, 2)
cv2.polylines(img, [bluetower+offset],       1, BLUE, 2)

# Draw grid lines
for G in range (fieldWidth,0,-20):
    cv2.line(img, (offset[0][0],G+offset[0][1]),
                  (offset[0][0]+fieldLength,G+offset[0][1]), GRAY, 1)
for G in range (0, fieldLength,20):
    cv2.line(img, (G+offset[0][0],offset[0][1]),
                  (G+offset[0][0],offset[0][1]+fieldWidth), GRAY, 1)


# TagXYR Ys are adjusted because screen's Y increases downward (sigh)
for T in TAGXYR:
   TAGXYR[T][1] = fieldWidth - TAGXYR[T][1]

#for P in polyBot:              # polyBot Ys are adjusted because screen's Y
#   P[1] = fieldWidth - P[1]    # increases downward

# Draw the requested tags
for T in args.tags:
    cv2.polylines(img,[tagProxy+offset+TAGXYR[T][0:2]], 1, WHITE, 2)

field_img = np.copy(img)
winname   = 'example'
cv2.namedWindow(winname)
img     = np.copy(field_img)
while True:
    img     = np.copy(field_img)
    RobotX  = round (subRobotWorldX.get()) + offset[0][0]
    RobotY  = fieldWidth - round (subRobotWorldY.get()) + offset[0][1]
    rot     = -np.deg2rad(subRobotRot.get())
    #drawBot = np.copy(polyBot)
    drawBot = rotBot(np.copy(polyBot),rot)
    drawBot[:,0] += RobotX
    drawBot[:,1] += RobotY
    cv2.fillPoly (img, [drawBot], RED)
    #cv2.circle   (img,(RobotX,RobotY),10,GREEN,-1)
    cv2.imshow   (winname,img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyWindow(winname)
