import cv #import this first!
import cv2
import numpy as np
import ARimport as ar


class ARcall():

    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getARCode(self, image):
        im_array = np.asarray( image[:,:] )
        #im_array = im_array.astype(np.uint32)
        ARcode.setOutputFileName("output.png")
        ARcode.setShowOutput(True)
        returnint = ARcode.findMarkers(im_array)

        output = ARcode.getFoundMarker(0) #input < returnint
        print((output.ID, output.x, output.y))
        return output.ID, output.x, output.y
                






                    