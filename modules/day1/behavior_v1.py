class behavior_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion  = modules.getModule("motion")
    
    def walk(self, observation):
        """
        INPUT: observation
        RETURN: None
    
        Walk towards an observed object.
        """        
        print "Walking towards an observed object."
        
        # while not at the desired location
        while not self.isFinished(observation):
            # stand up if fallen
            if self.motion.standUp():
                print "Please check if Nao still sees the beacon!"
        
            # find the desired walking direction
            direction = self.calcDirection(observation)
            print "Found direction based on obersvation is", direction
            
            # update the walking parameters
            self.adjustWalk(direction)
    
    def adjustWalk(self, direction):
        """
        INPUT: direction [x, y, theta]
        
        Walk towards a specific point x,y with orientation theta
        """
        x, y, theta = direction
        if x != 0 or y != 0 or theta != 0:
            self.globals.motProxy.post.walkTo(x,y,theta)
    
    def calcDirection(self, observation):
        """ 
        INPUT: observation
        RETURN: direction [x, y, theta]
        
        Calculate in which direction the robot should walk.
        x = forward (negative = backwards)
        y = left (negative = right)
        theta = rotate CCW (negative = CW)
        """
        # TODO: find the direction based on an observation
        
        sig, distance, theta = observation
        from math import sin, cos
        x = cos(theta) * distance
        y = sin(theta) * distance
        direction = [x,y,theta]
        return direction
    
    def isFinished(self, observation):
        """RETURN: true or false
        
        Has robot arrived at the finish location?
        """
        # TODO: check if the robot should stop walking!
        return True