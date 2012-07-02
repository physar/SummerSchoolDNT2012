class behavior_v1():    

    #no dependencies
    def setDependencies(self, modules):
        pass
    
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
    def isFinished():
        pass
    #RETURN:
    # true or false