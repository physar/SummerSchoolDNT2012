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
            
            blobsFound , blobsList = self.vision.getBlobsData(img)
            
            if blobsFound == 0:
                self.motion.walkTo(0.1,0,0)
            else:
                xAverage, yAverage = self.vision.findAvargePoint(blobsList)
                angle = self.vision.findAngle(xAverage)
            
            if blobsFound == 1:            
                print 'DEBUG, angle: ' + str(angle)
                self.motion.walkTo(0.05,0,angle)

            if blobsFound == 2:
                xAverage, yAverage = self.findAvargePoint(blobsList)
                twoBlobs = blobList
                twoBlobs.remove(None)
                distance = self.findDistance(twoBlobs)              
                angle = self.findAngle(xAverage)
                
                distance = -(diff - 78 )
                #when small diffrence your at the Mark but didnt find the signature
                #you need 3 blobs for that (can be done with out)
                if abs(distance) < 5:
                    print 'This was my distance to the goal: ' + str(distance)
                    print 'Still need to find the signature'
                    self.motion.walkTo(0,0,angle)                                       
                else:                  
                    realDistance = distance *0.005
                    print 'Distance to walk to the mark: ' + str(realDistance)
                    self.motion.walkTo( 0, realDistance, angle)
                    
            if blobsFound == 3:       
            
                print 'px,py coord Yellow Blob: ' + str(blobsList[0])
                print 'px,py coord Blue Blob: ' + str(blobsList[1])
                print 'px,py coord Orange Blob: ' + str(blobsList[2])
                
                #Diffrence in distance off pixels between blobs
                dist1 = self.findDistance(blobsList[0],blobsList[1])
                dist2 = self.findDistance(blobsList[0],blobsList[2])
                diff3 = self.findDistance(blobsList[1],blobsList[2])
                
                avrage = (diff1 +diff2 + diff3) /3
                
                print 'Distance off 3 blobs: ' +str(avrage)
                ### Need to find perfect diff
                #Bullcrap: 97 pix is the spot, groter is te dichtbij etc 
                distance = -(avrage - 78 )
                #when small diffrence your done
                if abs(distance) < 5:
                    print 'This was my distance to the goal: ' + str(distance) + ' !!IM DONE!!'
                    cv.SaveImage('goal.png', image)
                    #return signal(links, rechts), distance, theta
                    signature = self.findSignature(blobsList)
                    
                else:
                    xAverage, yAverage = self.findAvargePoint(blobsList)
                    angle = self.findAngle(xAverage)
                    #####MOET KALIBREREN!!!!!!
                    realDistance = distance *0.002
                    print 'Distance to walk to the goal: ' + str(realDistance)
                    print 'DEBUG, angle: ' + str(angle)
                    return 0, realDistance, angle
            
                
            
            
            
            if observation != None:
                signature, distance, theta = observation
                #at goal, when 0 dist and theta
                if (distance == 0 and signature == 3):
                    print 'I AM FINISHED... FREEDOM!!!'
                    finished = True
                if (distance == 0 and signature == 2):
                    self.motion.walkTo(0,0,-1.3)
                    self.motion.walkTo(0.05,0,0)
                if (distance == 0 and signature == 1):
                    self.motion.walkTo(0,0,1.25)
                    self.motion.walkTo(0.05,0,0)
                    
                    
                #found something walk in that direction
                if distance == 0 and theta != 0:
                    direction = self.behaviour.calcDirection(observation)
                    [x, y, theta] = direction
                    self.motion.walkTo(0.001,0,theta)
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
                self.motion.walkTo(0.1,0,0)
            count +=1
    
            