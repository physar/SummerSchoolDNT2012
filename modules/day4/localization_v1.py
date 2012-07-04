from math import cos, sin, pi


import mazeParser

class localization_v1():    
    globals = None

    #def setDependencies(self, modules):
    #    self.globals = modules.getModule("globals")    
        
    def localize_in_maze(self):
        """
        INPUT: None
        OUTPUT: Position (x,y,z)

        Main loop, finds the current location of the nao in the maze
        """

        edges, qrpos, valid_moves = mazeParser.parseMaze()
        
        # initialize belief in the map (4x4 positions, 4 orientations)
        b = 1/ ( 4.0**3 )
        map_belief = [[[b for i in range(4)] for i in range(4)] for i in range(4)]

        state = 1,0,0
        running = 1
        while running:
            print "Current REAL state", state
            
            # Ask user for a new motion
            motion = 0,0,0
            try:
                motion = eval(raw_input("Input a motion in the form (x,y,theta), in naocoordinates: "))
                if type(motion) != tuple:
                    raise Error, "Fiets"
            except:
                print "Motion must be of type tuple: (x,y,theta)"
                continue

            # if the move is possible, execute it
            x, y, t = state
            dx = int(cos(t)) * motion[0]
            dy = int(sin(t)) * motion[1]
            dt = motion[2]
            newstate = x+dx, y+dy, t+dt
            
            if self.is_valid_move(state, (dx,dy,dt), valid_moves):
                # rotate the motion based on 
                state = newstate
                self.walk(dx, dy, dt)
                
                # update the belief
                print "\nMotion", motion, ", updating belief..  \n"
                motion_map_belief = self.motion_update(motion, map_belief, edges, valid_moves)

                observation = [0,2,0]
                # if an observation is made, use it to update the belief
                if observation:
                    self.prettyPrint(motion_map_belief)

                    print "Observation: ", observation, ", updating belief..\n"
                    map_belief = self.vision_update(observation, motion_map_belief, valid_moves)
                else:
                    "No observerved features, the motion-updated belief will be used!"
                    map_belief = motion_map_belief


                # print it in a fashionable way!
                self.prettyPrint(map_belief)
            else:
                print "That move is not valid!"
                
            running = False

    def walk(self, x, y, theta):
        """
        INPUT: x, y, theta
        RETURNS: None

        Walk function that takes x,y,t and walks accordingly
        (x,y,t are in grid coordinates!)
        """
        pass
        
    def perceive(self):
        """
        RETURNS: bearing, distance, signature or None

        If a blob is seen, return its information, else None
        """
        return (0,1,0)
        
    def motion_update(self, motion, map_belief, map_edges, valid_moves):
        """
        INPUT: state, motion, map_belief, map_edges
        RETURNS: new state , new map_belief
        """
        # motion update vector u
        u_x, u_y, u_t = motion
        
        # Initiate new map_belief for every position and orientation
        new_map_belief = [[[0 for i in range(4)] for i in range(4)] for i in range(4)]

        # Create the new belief over possible positions in the map
        for col in range(4):
            for row in range(4):
                for orientation in range(4):                
                    
                    # keep orientation in mind!
                    t = orientation * pi / 2.0
                    u_x_rot = int(cos(t)*u_x - sin(t) * u_y)
                    u_y_rot = int(sin(t)*u_x + cos(t) * u_y)
                            
                    old_x = col - u_x_rot
                    old_y = row - u_y_rot
                    # orientation = 3 + move_rotation = 1 --> new orientation = 0
                    old_t = orientation - u_t % 4

                    old_location = (old_x, old_y, old_t)
                    
                    if self.is_valid_move(old_location, (u_x_rot,u_y_rot,u_t), valid_moves):
                        # belief is transferred from old positions to the new ones
                        belief = map_belief[old_x][old_y][old_t]
                        new_map_belief[col][row][orientation] += belief
                        
                    else:
                        # if, based on the move, it is impossible to be here,
                        # the new probability is 0
                        new_map_belief[col][row][orientation] += 0
                        
        # normalize the array map (evenly spread out probabilities)
        new_map_belief = self.normalize_3D(new_map_belief)

        return new_map_belief

    def is_valid_move(self, position, motion, valid_moves):
        """
        INPUT: position, motion, valid_moves
        RETURNS: True/False

        Is the move valid?
        """
        # the position contains x, y and orientation
        x, y, t = position
        # the motion is an already rotated vector containing the
        # x and y-offset, as seen from the nao
        u, v, w = motion

        
        # if there is a walking motion
        if (u == 1 or v == 1) and not (u==1 and v==1):
            # moves must end IN the maze
            if not(0 <= x + u < 4 and 0 <= y + v < 4):
                return False
            # and there must not be edges in the way
            if not((x, y) in valid_moves[(x+u,y+v)] ):
                return False
        elif w > 0 and u == 0 and v == 0:
            # if there is a rotation, the move is always valid
            return True
        else:
            return False
            
        # if all of the above was evaded, the move is valid
        #print "Move", x,y,"{0:.2f} to".format(t), x+u,y+v, "is valid"
        return True

    def vision_update(self, observation, map_belief, valid_moves):
        """
        INPUT: observation, map_edges
        RETURNS: map_belief

        Update the map of belief based on observation of blobs
        """        
        # the distance is in gridcoordinates , e.g. '2' instead of 166 cm.
        distance = self.parseObservation(observation)
        for col in range(4):
            for row in range(4):
                for orientation in range(4):
                    location = (col, row, orientation)
                    # calculate the probability of the observation given the location
                    prob_observation = self.prob_perception(location,
                                                            distance,
                                                            valid_moves)
                    # and find the new belief using this probability
                    new_belief = prob_observation * map_belief[col][row][orientation]
                    # then assign that to the correct place in map_belief
                    map_belief[col][row][orientation] = new_belief
                    
        # normalize it (spread out frequencies evenly)
        new_map_belief = self.normalize_3D(map_belief)
        return new_map_belief
    
    def prob_perception(self, location, distance, valid_moves):
        """
        INPUT: location, distance, valid_moves (dict)
        RETURNS: prob_observation (float between 0 and 1)

        Checks if a given distance is possible from the current location,
        given the edges, and assigns a probability to the observation. 
        """

        # find what the distance should be , given the location
        x, y, t = location
        real_distance = 0
        # an observation is possible if the moves needed to reach
        # the corresponding cell are valid.
        if t == 0:
            # keep walking until you hit a wall
            while (x+1,y) in valid_moves[(x, y)]:
                x += 1
                real_distance += 1
        elif t == 1:
            while (x,y+1) in valid_moves[(x, y)]:
                y += 1
                real_distance += 1
        elif t == 2:
            while (x-1,y) in valid_moves[(x, y)]:
                x -= 1
                real_distance += 1
        elif t == 3:
            while (x,y-1) in valid_moves[(x, y)]:
                y -= 1
                real_distance += 1
        
        # Based on this real distance, find the probability for the found
        # distance. Normally, this would be a continuous distribution (it
        # would be logical to input the real distance in cm and the found
        # distance, then use, for example, a gaussian distribution to find p).
        # To make matters easy, the distribution has been made discrete. 
        prob_observation = 0
        difference = distance - real_distance
        # if the observation was spot on, this has p = 0.8
        if difference == 0:
            prob_observation = 0.8
        # if we're off one gridcell, p = 0.1
        elif difference == 1 or difference == -1:
            prob_observation = 0.1

        return prob_observation
    
    def parseObservation(self, observation):
        """
        INPUT: Observation (bearing, distance, signature)
        RETURNS: Distance measure in worldcoordinates (cells)
        """
        bearing, distance, signature = observation
        if distance < 0.88:
            return 0
        elif distance < 1.76:
            return 1
        else:
            return 2

    def prettyPrint(self, map_belief):
        """
        INPUT: map_belief (size X x Y x Orientation)

        Prints the map in a (more) readable format
        """
        print "\n\t\t\tRight\tUp\tLeft\tDown"
        print "\t\t\t{0}\t{1}\t{2}\t{3}\t".format(0, 1.57, 3.14, 4.71)
        print "----------------------------------------------------"
        for y in range(len(map_belief[0])):
            for x in range(len(map_belief)):
                print "Row {0}, col {1} -->\t".format(y,x),
                for o in range(len(map_belief[0][0])):
                    print "{0:.2f}\t".format(map_belief[x][y][o]),
                print ""
        print ""

    def normalize_3D(self, map_belief):
        """
        INPUT: map_belief (3d array)
        RETURNS: normalized map_belief (3d array)
        
        Normalizes the belief matrix map_belief
        """
        sum_map = float(sum(sum(sum(i for i in cols) \
                          for cols in rows) \
                          for rows in map_belief))
        new_sum_map = [[[i/sum_map for i in cols]
                        for cols in rows]
                       for rows in map_belief]
        return new_sum_map


if __name__ == "__main__":
    loc = localization_v1()
    loc.localize_in_maze()
