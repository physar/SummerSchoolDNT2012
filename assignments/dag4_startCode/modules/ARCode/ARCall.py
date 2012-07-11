import cv #import this first!
import cv2
import numpy as np
import ARimport as ar


class getARCode():
    global ARcode
    ARcode = ar.ARimport()
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getARCode(self, image):
        print 'Going to find ARCode'
        
        im_array = np.asarray( image[:,:] )
        
        
        #im_array = im_array.astype(np.uint32)
        
        #DEBUG Purpose save your output Image
        #ARcode.setOutputFileName("output.png")
        #ARcode.setShowOutput(True)
       
        returnint = ARcode.findMarkers(im_array)
       

        output = ARcode.getFoundMarker(0) #input < returnint
      
        if output.ID == 4294967295L:
            print 'No ARCode found!!'
            return None
        else:
            print 'ARCode found!!: ID, x, y'
            print((output.ID, output.x, output.y))
            return output.ID, output.x, output.y
                







                    