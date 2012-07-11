import cv, cv2

class mainDag4():
    globals         = True
    tools           = True
    motion          = True
    behaviour       = True
    vision          = True
    pathplanning    = None
    localization    = None

    def setDependencies(self, modules):
        self.globals        = modules.getModule("globals")
        self.tools          = modules.getModule("tools")
        self.motion         = modules.getModule("motion")
        #self.behaviour      = modules.getModule("behaviour")
        self.arcode         = modules.getModule("arcode")
        self.vision         = modules.getModuleNone("vision")
        self.pathplanning   = modules.getModuleNone("pathplanning")
        self.localization   = modules.getModuleNone("localization")
        
        
    def start(self):
        #ipadress of NAO
        #self.globals.setIPadress("192.168.1.35")
        self.globals.setProxies()

        #init motions
        self.motion.init()
        
        #subscribe to camera, to recieve images
        self.tools.cSubscribe()
               
        self.motion.stiff()
        self.motion.normalPose()
        #with this posistion it always staight and high enough at the wall
        self.motion.setHead(0,-0.5)
             
        print 'Start Maze Walker'
        finished = False

        while (finished == False):
            #check if fallen
            if self.motion.standUp():
                finished = True
                print 'Fallen'
            #when hitting a wall walk backwards   
            if ((self.globals.memProxy.getData("LeftBumperPressed", 0) != 0.0) or \
                (self.globals.memProxy.getData("RightBumperPressed", 0) != 0.0)):
                print "Stop hitting the wall"
                self.motion.walkTo(-0.4,0,0)
                
            #get snapshot from robot
            img = self.tools.getSnapshot()
            
            (image, (camPos, headAngles)) = img 
            cv.SaveImage('snapShot.png', image)
            
            observation = self.arcode.getARCode(image)
            
            while( observation == None):
                #self.motion.walkTo(0,0,-1.3)
                img = self.tools.getSnapshot()
                (image, (camPos, headAngles)) = img
                cv.SaveImage('snapShot.png', image)
                observation = self.arcode.getARCode(image)
            
            iD, xAR, yAR = observation
            
            print 'ID , x, y'
            print iD , xAR, yAR 
            
            coordinates = self.vision.calcPosition((xAR,yAR), camPos, headAngles)
            (xPos, yPos, xAngle, yAngle) = coordinates
            print 'FOUND YOU MOTHERFUCKERS!!'
            print xPos, yPos
            
            #self.motion.walkTo(xPos, yPos, 0)
                
                

                    

    
            