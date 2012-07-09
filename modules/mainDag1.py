import time

class mainDag1():
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
        self.behaviour      = modules.getModule("behaviour")

        
    def start(self):
        #ipadress of NAO
        self.globals.setIPadress("192.168.1.35")
        self.globals.createProxies()
        self.globals.speechProxy.say(' Where is my ball!!')

        #init motions
        self.motion.init()
        
        #subscribe to camera, to recieve images
        #self.tools.cSubscribe()
        
        
        self.motion.stiff()
        self.motion.normalPose()
        #with this posistion it always staight and high enough at the wall
        self.motion.setHead(0,-0.5)
        
        search = False
        
        while (search == False):
            self.globals.redBallProxy.startTracker()
            
        
        
            time.sleep(60)
        
        self.globals.redBallProxy.stopTracker()
        
        
        
        