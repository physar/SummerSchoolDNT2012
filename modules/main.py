class main():
    globals         = None
    tools           = None
    motion          = None
    behaviour       = None
    vision          = None
    pathplanning    = None
    localization    = None

    def setDependencies(self, modules):
        self.globals        = modules.getModule("globals")
        self.tools          = modules.getModule("tools")
        self.motion         = modules.getModule("motion")
        self.behaviour      = modules.getModule("behaviour")
        self.vision         = modules.getModuleNone("vision")
        self.pathplanning   = modules.getModuleNone("pathplanning")
        self.localization   = modules.getModuleNone("localization")
        
    def start(self):
        finished = false
        map = tools.loadMap()
        
        #ipadress of NAO
        globals.setIPadress("192.168.1.43")
        globals.createProxies()
        
        #subscribe to camera, to recieve images
        self.tools.subscribe()
        
        while (finished == false):
        
            #check is robot is fallen
            state = self.motion.getState()
            if (state == "fallen"):
                self.motion.recover()
        
            #get snapshot from robot
            img = self.tools.getSnapshot()
            
            #process snapshot
            if (self.vision != None):
                #Day 2: Blob recognition
                observation = self.vision.getBeaconObservation(img)
            else
                #QR code recognition
                observation = self.tools.getBeaconObservation(img)
             
            #observation:
            # = 'None' if no observation is found
            # = [signatue, distance, theta] if an observation is found
            #   - signature = id of observed beacon
            #   - distance = distance towards beacon
            #   - theta = angle towards beacon
            
            # pathplanning or reactive behavior?
            if (self.tools.reactiveBeaconObserved(observation) != "path"):
                #Day 1: simple reactive behaviour
                direction = self.behaviour.calcDirection(observation)
                finished = self.behaviour.isFinished()
            else:
                #update localization
                if (self.localization != None):
                    #Day 4: Grid localization
                    pose = self.localization.updatePose(observation, map)
                else
                    #build in localization
                    pose = self.tools.updatePose(observation, map)        
                #pose: [x,y,theta]
            
                #Day 3: implementing pathplannig
                step = self.pathplanning.nextStep(pose, map)
                direction = self.pathplanning.calcDirection(pose, step)
                finished = self.pathplanning.isFinished()

            #direction: [x, y, theta]
            # x = forward (negative = backwards)
            # y = left (negative = right)
            # theta = rotate CCW (negative = CW)
            
            # walk into direction
            motion.walkTo(direction)
            