import time
import math

class mainDag1:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools  = modules.getModule("tools")
        

    def start(self):
        self.globals.createProxies()
        #self.globals.speechProxy.say("Where is my ball at")
        self.motion.init()
        self.motion.stiff()
        self.motion.normalPose()
        #self.motion.walkTo(0.5,0,0)
        self.motion.setHead(0,-0.5)
        

        #subscribe to camera, to recieve images
        self.tools.cSubscribe()
        
        
       # 
        
        #with this posistion it always staight and high enough at the wall
        
        
        start = time.time()
        #self.motion.walkTo(0.89,0.02,0)
        
        
        while (time.time() - start < 30):
            self.globals.redBallProxy.startTracker()
            position = self.globals.redBallProxy.getPosition()
            print position
            [x,y,_] = position
            
            self.motion.walkTo(x,y,0)
            time.sleep(0.5)
            '''if x > 0.
            theta = math.atan(y/x)
            # hacked influencing of perception, causing walking forward to have priority
            
                theta *= 0.4      
                x = (3.0 * (x - 0.17))  
                y *= 0.6 
                if x >1:
                    x =1
                self.motion.setWalkTargetVelocity(x , y, theta, 0.8)#max ( 1-x, 0.85 ))
            
                #self.globals.motProxy.waitUntilWalkIsFinished()

                #self.motion.walkTo(x,y,0)
                #time.sleep(5)
            if x != 0: 
                self.motion.kickStraight(0)
            
            
            theta = math.atan(y/x)
            # hacked influencing of perception, causing walking forward to have priority
            
            theta *= 0.4      
            x = (3.0 * (x - 0.17))  
            y *= 0.6 
            if x >1:
                x =1
            self.motion.setWalkTargetVelocity(x , y, theta, 0.8)#max ( 1-x, 0.85 ))
            time.sleep(0.5)
            '''
        
           
        
        self.globals.redBallProxy.stopTracker()
        self.motion.init()
        
        