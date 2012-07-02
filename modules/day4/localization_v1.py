class localization_v1():    

    def setDependencies(self, modules):
        pass
    
 #update pose of robot (grid localization)
    def updatePose(self, observation, map):
        pass
    #RETURN:
    #pose: [x,y,theta]
    #x/y: position in maze? (0:0, to 3:3? (4x4 maze))
    #       or in cm? (grid is rougly 88x88cm)