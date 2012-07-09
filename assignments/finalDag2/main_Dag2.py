import cv, cv2

class main_Dag2():
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
        #self.globals.setIPadress("192.168.1.35")
        self.globals.createProxies()

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
            
            blobsFound , blobsList = self.vision.getBlobsData(image)
            
            if blobsFound == 0:
                self.motion.walkTo(0.1,0,0)
            else:
                xAverage, yAverage = self.vision.findAvargePoint(blobsList)
                angle = self.vision.findAngle(xAverage)
            
            if blobsFound == 1:            
                print 'DEBUG, angle: ' + str(angle)
                self.motion.walkTo(0.05,0,angle)

            if blobsFound == 2:
                xAverage, yAverage = self.vision.findAvargePoint(blobsList)
                twoBlobs = blobsList
                twoBlobs.remove(None)
                distance = self.vision.findDistance(twoBlobs)              
                angle = self.vision.findAngle(xAverage)
                
                optimalDistance = -(distance - 78 )
                #when small diffrence your at the Mark but didnt find the signature
                #you need 3 blobs for that (can be done with out)
                if abs(optimalDistance) < 5:
                    print 'This was my distance to the goal: ' + str(distance)
                    print 'Still need to find the signature'
                    self.motion.walkTo(0,0,angle)                                       
                else:                  
                    realDistance = optimalDistance *0.005
                    print 'Distance to walk to the mark: ' + str(realDistance)
                    self.motion.walkTo( realDistance,0, angle)
                    
            if blobsFound == 3:       
            
                print 'px,py coord Pink Blob: ' + str(blobsList[0])
                print 'px,py coord Blue Blob: ' + str(blobsList[1])
                print 'px,py coord Orange Blob: ' + str(blobsList[2])
                
                #Diffrence in distance off pixels between blobs
                dist1 = self.vision.findDistance([blobsList[0],blobsList[1]])
                dist2 = self.vision.findDistance([blobsList[0],blobsList[2]])
                dist3 = self.vision.findDistance([blobsList[1],blobsList[2]])
                
                avrage = (dist1 +dist2 + dist3) /3
                
                print 'Distance off 3 blobs: ' +str(avrage)
                ### Need to find perfect diff
                #Bullcrap: 97 pix is the spot, groter is te dichtbij etc 
                distance = -(avrage - 78 )
                #when small diffrence your done
                if abs(distance) < 5:
                    print 'This was my distance to the goal: ' + str(distance) + ' !!IM AT MY MARK!!'
                    cv.SaveImage('goal.png', image)
                    #return signal(links, rechts), distance, theta
                    signature = self.vision.findSignature(blobsList)
                    if (signature == 3):
                        print 'I AM FINISHED... FREEDOM!!!'
                        finished = True
                    if (signature == 2):
                        self.motion.walkTo(0,0,-1.3)
                        self.motion.walkTo(0.05,0,0)
                    if (signature == 1):
                        self.motion.walkTo(0,0,1.25)
                        self.motion.walkTo(0.05,0,0)
                #3 blobs found but not yet at the mark    
                else:
                    xAverage, yAverage = self.vision.findAvargePoint(blobsList)
                    angle = self.vision.findAngle(xAverage)
                    #####MOET KALIBREREN!!!!!!
                    realDistance = distance *0.002
                    print 'Distance to walk to the goal: ' + str(realDistance)
                    print 'DEBUG, angle: ' + str(angle)
                    self.motion.walkTo(0, realDistance, angle)
            
                
            
            

                    

    
            