import cv2
import numpy as np

img = np.zeros((600, 800, 3), dtype='uint8')
fieldwall = np.array([
    [ 0,0 ]
   ,[ 651,0 ]
   ,[ 651,317 ]
   ,[ 0,317 ]
])
redhub = np.array([
       [ 159,135 ]
      ,[ 159,182 ]
      ,[ 206,182 ]
      ,[ 206,135 ]
])
redrightbump = np.array([
    [ 159,182 ]
   ,[ 159,255 ]
   ,[ 206,255 ]
   ,[ 206,182 ]
])
redleftbump = np.array([
    [ 159,135 ]
   ,[ 159,62 ]
   ,[ 206,62 ]
   ,[ 206,135 ]
])
redlefttrench = np.array([
    [ 179,62 ]
   ,[ 179,11 ]
   ,[ 185,11 ]
   ,[ 185,62 ]
])
redrighttrench = np.array([
    [ 180,255 ]
   ,[ 180,305 ] 
   ,[ 184,305 ]
   ,[ 184,255 ]
])
bluehub = np.array([
    [ 446,135 ]
   ,[ 446,182 ]
   ,[ 493,182 ]
   ,[ 493,135 ]
])
bluerightbump = np.array([
    [ 446,182 ]
   ,[ 446,255 ]
   ,[ 493,255 ]
   ,[ 493,182 ]
])
blueleftbump = np.array([
    [ 446,135 ]
   ,[ 446,62 ]
   ,[ 493,62 ]
   ,[ 493,135 ]
])
bluelefttrench = np.array([
    [ 466,62 ]
   ,[ 466,11 ]
   ,[ 472,11 ]
   ,[ 472,62 ]
])
bluerighttrench = np.array([
    [ 467,255 ]
   ,[ 467,305 ]
   ,[ 471,305 ]
   ,[ 471,255 ]
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
winname = 'example'
cv2.namedWindow(winname)
cv2.imshow(winname, img)
cv2.waitKey()
cv2.destroyWindow(winname)
