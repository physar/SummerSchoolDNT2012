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
        print "Behaviour: Walking towards an observed object."
        import time
        now = time.time()
        
        # while not at the desired location
        while not self.isFinished(observation):
            # stand up if fallen
            if self.motion.standUp():
                print "Please check if Nao still sees the beacon!"
        
            # find the desired walking direction
            direction = self.calcDirection(observation)
            print "Found direction based on observation:", direction
            
            # update the observation, based on time and velocity 
            interval = time.time() - now
            observation = self.motionUpdate(direction, observation, interval)
            now = time.time()
            print "Found observation based on direction:", observation
            
            # update the walking parameters
            self.adjustWalk(direction)
    
    def motionUpdate(self, direction, observation, interval):
        """
        INPUT: direction [x,y,theta]
        RETURN: new observation, based on distance
        """
        x,y,theta = direction
        sig, distance, bearing = observation
        
        # calculate walked distance based on walking direction
        walked_distance_x = interval * ((x>0) * 0.05)
        walked_distance_y = interval * ((y>0) * 0.05)
        walked_distance_t = interval * ((theta > 0) * 0.7 )
        
        # update distance, bearing
        from math import sqrt
        new_distance = distance - sqrt(walked_distance_x**2 + walked_distance_y**2)
        new_bearing = bearing - walked_distance_t
        return sig, new_distance, new_bearing
    
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
        if observation[1] + observation[2] < 0.01:
            return True