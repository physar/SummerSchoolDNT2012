class pathplanning_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    
    # get next step in path, based on map and current pose
    def nextStep(self, pose, map):
        pass
    #RETURN:
    #step: [x,y,theta] ???
        
    
    #calculate in which direction the robot should walk
    def calcDirection(self, observation):
        pass
    #RETURN:
    #direction: [x, y, theta]
    # x = forward (negative = backwards)
    # y = left (negative = right)
    # theta = rotate CCW (negative = CW)
    # --> TODO, check with motion!
    
    # has robot arrived at finish location?
    def isFinished(self):
        pass
    #RETURN:
    # true or false