class main_v2():
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
        self.vision         = modules.getModuleNone("vision")
        self.pathplanning   = modules.getModuleNone("pathplanning")
        self.localization   = modules.getModuleNone("localization")
        
    def start(self):
        #ipadress of NAO
        self.globals.setIPadress("192.168.1.35")
        self.globals.createProxies()

        #init motions
        self.motion.init()
        
        #subscribe to camera, to recieve images
        self.tools.cSubscribe()
        
        
        self.motion.stiff()
        self.motion.normalPose()
        #with this posistion it always staight and high enough at the wall
        self.motion.setHead(0,-0.5)
        
        
        #Pseudo:
        #While != finished
        #   check if standing
        ### ADD: button interface to stop the loop
        #   get image
        #   findCircles ###ADD: give argument off which set of blobs (2 sets of 4 different colors)
        #   if observation =! None
        #       if Distance == 0: your at your goal, turn the right way, find next goal
        #       else: walk the right distance
        #   else: no circles found so walk a short distance straight
        
        
        
        finished = False
        #map = tools.loadMap()
        global count 
        count = 0
        while (finished == False) or count < 10:
            global count
            if self.motion.standUp():
                finished = True
                print 'Fallen'
                break
            #check is robot is fallen
            #state = self.motion.getState()
            #if (state == "fallen"):
                #self.motion.recover()
        
            #get snapshot from robot
            img = self.tools.getSnapshot()
            
            #process snapshot
            #if (self.vision != None):
                #Day 2: Blob recognition
            observation = self.vision.getBeaconObservation(img)
            #else:
                #QR code recognition
               # observation = self.tools.getBeaconObservation(img)
             
            #observation:
            # = 'None' if no observation is found
            # = [signatue, distance, theta] if an observation is found
            #   - signature = id of observed beacon
            #   - distance = distance towards beacon
            #   - theta = angle towards beacon
            
            # pathplanning or reactive behavior?
            if observation != None:
                signatue, distance, theta = observation
                if distance == 0:
                    print 'I FOUND THE SPOT'
                    finished = True
                    break
                else:
                    #if (self.tools.reactiveBeaconObserved(observation) != "path"):
                    #Day 1: simple reactive behaviour
                    direction = self.behaviour.calcDirection(observation)
                    #finished = self.behaviour.isFinished()
                    '''
                    else:
                        #update localization
                        if (self.localization != None):
                            #Day 4: Grid localization
                            pose = self.localization.updatePose(observation, map)
                        else:
                            #build in localization
                            pose = self.tools.updatePose(observation, map)        
                        #pose: [x,y,theta]
                    
                        #Day 3: implementing pathplannig
                        step = self.pathplanning.nextStep(pose, map)
                        direction = self.pathplanning.calcDirection(pose, step)
                        finished = self.pathplanning.isFinished()
                    '''
                    #direction: [x, y, theta]
                    # x = forward (negative = backwards)
                    # y = left (negative = right)
                    # theta = rotate CCW (negative = CW)
                    
                    # walk into direction
                    print "DIrection?!?!: " +str(direction)
                    [x,y,theta ] = direction
                    self.motion.walkTo(x,y, theta)
            else:
                self.motion.walkTo(0.05,0,0)
            count +=1
    
            