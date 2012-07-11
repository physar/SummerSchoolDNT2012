import cv, cv2

class main_v3():
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

        
    def start(self):
    
    
        maze = {10:(2,0), 23:(1,3), 25:(2,3), 42:(3330,0),\
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
        
        
        self.motion.setHead(0,-0.2)
             
        print 'Start Maze Walker'
        

            