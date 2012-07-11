import cv #import this first!
import cv2
import numpy as np
import ARimport as ar


class ARCall():
    global ARcode
    ARcode = ar.ARimport()
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getARCode(self, image):
        print 'Going to find ARCode'
        #image = cv.LoadImage("test.png",cv.CV_LOAD_IMAGE_COLOR)
        im_array = np.asarray( image[:,:] )
        
        
        #im_array = im_array.astype(np.uint32)
        #print 'array'
        #print im_array.dtype
        #print im_array.shape
        #ARcode.setOutputFileName("output.png")
    
        ARcode.setShowOutput(True)
       
        returnint = ARcode.findMarkers(im_array)
       

        output = ARcode.getFoundMarker(0) #input < returnint
      
        if output.ID == 4294967295L:
            print 'No ARCode found!!'
            return None
        else:
            print 'ARCode found!!: ID, x, y'
            print((output.ID, output.x, output.y))
            return output.ID, output.x, output.y
                







                    