class motion_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        
    #return state of robot: fallen etc
    def getState(self):
        pass
    
    #recover when fallen
    def recover(self):
        pass
    
    #some functions from the DNT motion file
    #walkto, stifness, et cetera