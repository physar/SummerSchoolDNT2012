import cv, cv2
import numpy

class main_vision():
    globals         = None
    tools           = None
    motion          = None

    def setDependencies(self, modules):
        self.globals        = modules.getModule("globals")
        self.tools          = modules.getModule("tools")
        self.motion         = modules.getModule("motion")
        
        
    def start(self):
        #ipadress of NAO
        self.globals.setIPadress("192.168.1.48")
        self.globals.createProxies()

        #init motions
        self.motion.init()
        
        #subscribe to camera, to recieve images
        self.tools.cSubscribe()
        
        while (True):
            
            #test image
            imgData = self.tools.getSnapshot()
            img = imgData[0]
                               
            yellow = self.vision2.filterImageYellow(img)
            #cv.SaveImage("yellow.jpg", yellow)
            yellow = numpy.asarray(yellow)
            x = numpy.sum(yellow, 0)
            y = numpy.sum(yellow, 1)
            coord = (numpy.argmax(x), numpy.argmax(y))
            print "yellow: " + str(coord)
            
            blue = self.vision2.filterImageBlue(img)
            #cv.SaveImage("blue.jpg", blue)
            blue = numpy.asarray(blue)
            x = numpy.sum(blue, 0)
            y = numpy.sum(blue, 1)
            coord = (numpy.argmax(x), numpy.argmax(y))
            print "blue: " + str(coord)
        
            