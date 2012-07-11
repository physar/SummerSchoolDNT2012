import cv #import this first!
import cv2
import numpy as np
import ARimport as ar


ARcode = ar.ARimport()
#ARcode.test()
image = cv.LoadImage("snapShot.png",cv.CV_LOAD_IMAGE_COLOR)
im_array = np.asarray( image[:,:] )
#im_array = im_array.astype(np.uint32)
ARcode.setOutputFileName("output.png")
ARcode.setShowOutput(True)
returnint = ARcode.findMarkers(im_array)

output = ARcode.getFoundMarker(0) #input < returnint
print 'output'
print output.ID
if output.ID == 4294967295L:
    print 'None'
else:
    print((output.ID, output.x, output.y))

                    
