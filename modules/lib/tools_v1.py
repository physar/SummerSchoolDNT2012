import cv
from naoqi import ALProxy
    
class tools_v1():    


    # no dependencies
    def setDependencies(self, modules):
        pass
    
    # load map of maze from txt file
    def loadMap(self):
        pass
    #RETURN
    # map representation: double list? dict?
    
    # get snapshot from camera
    def getSnapshot(self):
        pass
    #RETURN:
    # HSV image of bottom camera?
       
    # process img, get QR-code data
    def getBeaconObservation(self, img):
        pass
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon
        
    #update pose of robot (grid localization)
    def updatePose(self, observation, map):
        pass
    #RETURN:
    #pose: [x,y,theta]
    #x/y: position in maze? (0:0, to 3:3? (4x4 maze))
    #       or in cm? (grid is rougly 88x88cm)
    
    #determine kind what kind of beacon is observed (pathplan/reactive/QR?)
    def reactiveBeaconObserved(self, observation):
        pass
    #RETURN:
    # - 'reactive', 'path', 'QR'