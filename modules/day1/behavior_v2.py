class behavior_v2():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    def searchWithHead(self):
        """ Moves the head from left to right, up to down, and vice
        versa.. twice. """
        
        # To move the head twice, a 'for' loop is used. It looks like this:
        
        # for <variable> in <some_iterable>:
        #    ..do anything
        
        print "\n\nHere follows an example:"
        print "The range function creates a python array: range(5) =", range(5)
        print "A for loop loops through this array: \n"
        print "for i in range(5): "   
        print "    print 'Variable i is now', i"
        print "\nwill give us:\n"
            
        for i in range(5):
            print "Variable i is now {0}.".format(i)
        
        
        # For loops can be used to loop through each element of a list, 
        # or, as in this case, to repeat a sequence of actions. Try
        # changing the number of loops and see what happens!
        self.moveHead("CENTER")
        
        number_of_loops = 2
        for i in range(number_of_loops):
            # Show a message that says how far we are
            print "Starting the {0}th iteration".format(i)
            self.moveHead("UP")
            self.moveHead("DOWN")
            self.moveHead("LEFT")
            self.moveHead("RIGHT")    
            
    def moveHead(self, direction):
        """Moves the head in a specified direction"""
        if direction == "CENTER":
            # set the angles for headpose 'center'
            headYawAngle = 0.0     # angle left/right
            headPitchAngle = 0.0   # angle up/down
            
            names = ["HeadYaw", "HeadPitch"]
            angles = [headYawAngle, headPitchAngle]
            speed = 0.5            # speed must be a number between 0 and 1
            
            self.globals.motProxy.setAngles(names, angles, speed)
            import time
            time.sleep(1)
            
        elif direction == "UP":
            # TODO: fill in your own code!
            pass
        elif direction == "DOWN":
            # TODO: fill in your own code!
            pass
        elif direction == "LEFT":
            # TODO: fill in your own code!
            pass
        elif direction == "RIGHT":
            # TODO: fill in your own code!
            pass