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
        self.maze = modules.getModule("mparser")
        self.astar = modules.getModule("astar")
        self.visu = modules.getModule("visualization")
        self.globals        = modules.getModule("globals")
        self.tools          = modules.getModule("tools")
        self.motion         = modules.getModule("motion")
        #self.behaviour      = modules.getModule("behaviour")
        self.arcode         = modules.getModule("arcode")
        self.vision         = modules.getModuleNone("vision")
        self.pathplanning   = modules.getModuleNone("pathplanning")
        self.localization   = modules.getModuleNone("localization")
 
    def getArDict():
        return {10:(2,0), 23:(1,3), 25:(2,3), 42:(0,0),\
            64:(0,2), 69:(0,0), 116:(3,0), 123:(1,2),\
            128:(0,0), 256:(2,2), 444:(3,2), 456:(3,1),\
            501:(0,0), 507:(0,0), 512:(1,0), 666:(2,1),\
            789:(0,0), 890:(0,1), 901:(1,1), 999:(0,0)}
        
    def start(self):
    
    
        dict = {10:(2,0), 23:(1,3), 25:(2,3), 42:(3330,0),\
            64:(0,2), 69:(3330,0), 116:(3,0), 123:(1,2),\
            128:(330,0), 256:(2,2), 444:(3,2), 456:(3,1),\
            501:(330,0), 507:(3330,0), 512:(1,0), 666:(2,1),\
            789:(0,0), 890:(0,1), 901:(1,1), 999:(3330,0)}
        #ipadress of NAO
        #self.globals.setIPadress("192.168.1.35")
        self.globals.setProxies()
        
        self.visu.init()
        e, v = self.maze.parseMaze()
        self.maze.prettyPrint(e)
        start = (0,0)
        finish = (3,0)
        pathdata = self.astar.findShortestPath(start, finish, v, e)
        print str(pathdata[2])
        self.visu.stop()

        #init motions
        self.motion.init()
        
        #subscribe to camera, to recieve images
        self.tools.cSubscribe()
               
        self.motion.stiff()
        self.motion.normalPose()
        #with this posistion it always staight and high enough at the wall
        self.motion.setHead(0,-0.2)
             
        print 'Start Maze Walker'
        finished = False
        
        for i in xrange(len(pathdata[2])):
            mark = pathdata[2][i]
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
            
            notRightMark = False
            
            while( notRightMark == False):
                self.motion.walkTo(0,0,-1.2)
                img = self.tools.getSnapshot()
                (image, (camPos, headAngles)) = img
                cv.SaveImage('snapShot.png', image)
                observation = self.arcode.getARCode(image)
                if not observation == None:
                    iD, xAR, yAR = observation
                    print 'ID , x, y'
                    print iD , xAR, yAR 
                    if dict[iD] == mark:
                        notRightMark = True
                        coordinates = self.vision.calcPosition((xAR,yAR), camPos, headAngles)
                        (xPos, yPos, xAngle, yAngle) = coordinates
                        print 'FOUND YOU MOTHERFUCKERS!!'
                        print xPos, yPos
                    
                        self.motion.walkTo(xPos, yPos, 0)
            
           
            

         
                    

    
            