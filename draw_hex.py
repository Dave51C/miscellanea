import cv2
import numpy as np

img = np.zeros((300, 800, 3), dtype='uint8')
points = np.array([
       [ 209,177 ]
      ,[ 177,196 ]
      ,[ 145,177 ]
      ,[ 145,140 ]
      ,[ 177,121 ]
      ,[ 209,140 ]
])

cv2.polylines(img, [points], 1, (255,255,255))
winname = 'example'
cv2.namedWindow(winname)
cv2.imshow(winname, img)
cv2.waitKey()
cv2.destroyWindow(winname)
