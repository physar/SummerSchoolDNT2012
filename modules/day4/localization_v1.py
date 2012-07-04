from math import cos, sin, pi

class localization_v1():    
    globals = None

    #def setDependencies(self, modules):
    #    self.globals = modules.getModule("globals")    
        
    def localize_in_maze(self):
        # initialize belief in the map (4x4 positions, 4 orientations)
        b = 1/ ( 4.0**3 )

        edges = {(1, 3): [(0, 3)], (3, 0): [(2, 0), (4, 0)],
                 (2, 1): [(3, 1)], (0, 3): [(0, 2), (1, 3), (0, 4)],
                 (4, 0): [(3, 0), (4, 1)], (1, 2): [(0, 2), (2, 2)],
                 (3, 3): [(2, 3), (4, 3)], (4, 4): [(4, 3), (3, 4)],
                 (0, 4): [(0, 3), (1, 4)], (4, 1): [(4, 0), (3, 1), (4, 2)],
                 (1, 1): [(0, 1)], (3, 2): [(4, 2)], (0, 0): [(1, 0), (0, 1)],
                 (2, 2): [(1, 2)], (1, 4): [(0, 4), (2, 4)], (2, 3): [(3, 3)],
                 (4, 2): [(4, 1), (3, 2), (4, 3)], (1, 0): [(0, 0), (2, 0)],
                 (0, 1): [(0, 0), (1, 1), (0, 2)], (3, 1): [(2, 1), (4, 1)],
                 (2, 4): [(1, 4), (3, 4)], (2, 0): [(1, 0), (3, 0)],
                 (4, 3): [(4, 2), (3, 3), (4, 4)], (3, 4): [(2, 4), (4, 4)],
                 (0, 2): [(0, 1), (1, 2), (0, 3)]}
        
        map_belief = [[[b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b]],
                      [[b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b]],
                      [[b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b]],
                      [[b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b],
                       [b,b,b,b]]]
        try:
            motion = eval(raw_input("Input a motion in the form (x,y,theta): "))
            if type(motion) != tuple:
                raise Error, "Fiets"
        except:
            print "Motion must be of type tuple: (x,y,theta)"
            return False

        self.motion_update([0.0,0.0,0.0], motion, map_belief, edges)

        
    def motion_update(self, state, motion, map_belief, map_edges):
        """
        INPUT: state, motion, map_belief, map_edges
        RETURN: new state , new map_belief

        """
        # motion update vector u
        u_x, u_y, u_t = motion
        
        # update the current state, if possible
        
        pOvershoot = 0.1
        pUndershoot = 0.1
        pExact = 0.8
        # Initiate new map_belief for every position and orientation
        new_map_belief = [[[0 for i in range(4)] for i in range(4)] for i in range(4)]

        # Create the new belief over possible positions in the map
        for col in range(4):
            for row in range(4):
                for orientation in range(4):                   
                    old_x = row - u_x
                    old_y = col - u_y
                    # orientation = 3 + move_rotation = 1 --> new orientation = 0
                    old_t = orientation - u_t % 4
                    
                    if self.is_valid_move((old_x, old_y, old_t), motion, map_edges):
                        # belief is transferred from old positions to the new ones
                        belief = map_belief[old_x][old_y][old_t]
                        new_map_belief[row][col][orientation] = belief
                    else:
                        # if, based on the move, it is impossible to be here,
                        # the new probability is 0
                        new_map_belief[row][col][orientation] = 0
                        
        # normalize the array map (evenly spread out probabilities)
        new_map_belief = self.normalize_3D(new_map_belief)
        # print it in a fashionable way!
        self.prettyPrint(new_map_belief)

    def is_valid_move(self, position, motion, map_edges):
        """
        INPUT: position, motion, map_edges
        RETURNS: True/False

        Is the move valid?
        """
        # the position contains x, y and orientation
        x, y, t = position
        u_unrotated, v_unrotated, w = motion
        # keep orientation in mind!
        t = t * pi / 2.0
        u = int(cos(t)*u_unrotated - sin(t) * v_unrotated)
        v = int(sin(t)*u_unrotated + cos(t) * v_unrotated)
        # moves must end IN the maze
        if not(0 < x + u < 4 and 0 < y + v < 4):
            return False
        # and there must not be edges in the way
        validMoves = {(0, 1): [(1, 1)], (1, 2): [(0, 2), (2, 2), (1, 3)], (3, 2): [(2, 2)], (0, 0): [(1, 0)], (3, 3): [(2, 3)], (3, 0): [(2, 0)], (3, 1): [(2, 1)], (2, 1): [(1, 1), (3, 1), (2, 2)], (0, 2): [(1, 2)], (2, 0): [(1, 0), (3, 0)], (1, 3): [(1, 2), (0, 3), (2, 3)], (2, 3): [(1, 3), (3, 3)], (2, 2): [(2, 1), (1, 2), (3, 2)], (1, 0): [(0, 0), (2, 0), (1, 1)], (0, 3): [(1, 3)], (1, 1): [(1, 0), (0, 1), (2, 1)]}
        
        if not((x+u, y+v) in validMoves[(x,y)] ):
            return False
        # if all of the above was evaded, the move is valid
        print "Move", x,y,"{0:.2f} to".format(t), x+u,y+v, "is valid"
        return True
    
    #update pose of robot (grid localization)
    def vision_update(self, state, observation, map_belief):
        """
        INPUT: state, observation, map_edges
        RETURN: state of robot [x,y,theta]

        """    
        pass

    def prettyPrint(self, map_belief):
        """
        INPUT: map_belief (size X x Y x Orientation)

        Prints the map in a readable format
        """
        for x in range(len(map_belief)):
            for y in range(len(map_belief[0])):
                print x, y, "", map_belief[x][y]

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
