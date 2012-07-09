import cv
class main:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()
        
        self.motion.stiff()
        self.motion.normalPose()
        
        #Throug extended research at the cost of many fallen Nao's
        #we at the Dutch Nao Team found that the optimal head position is
        self.motion.setHead(0,-0.5)
        
        finished = False
        
        while(finished == False):
            if self.motion.standUp():
                finished = True
                print 'Fallen'
            #when hitting a wall walk backwards   
            #NOTE: set memProxy aan in globals!!
            if ((self.globals.memProxy.getData("LeftBumperPressed", 0) != 0.0) or \
                (self.globals.memProxy.getData("RightBumperPressed", 0) != 0.0)):
                print "Stop hitting the wall"
                self.motion.walkTo(-0.4,0,0)
                
            #get snapshot from robot
            img = self.tools.getSnapshot()
            
            (image, (camPos, headAngles)) = img 
            
            blobsFound , blobsList = self.vision.getBlobsData(image)
            
            
        
        