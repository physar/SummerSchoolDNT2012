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
        
        #Make an image
        img = self.tools.getSnapshot()
        self.tools.SaveImage("test.png", img[0])
        
        #Throug extended research at the cost of many fallen Nao's
        #we at the Dutch Nao Team found that the optimal head position is
        self.motion.setHead(0,-0.5)
        

        
        