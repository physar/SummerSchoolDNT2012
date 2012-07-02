import cv
import Image
from naoqi import ALProxy
    
class tools_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    # load map of maze from txt file
    def loadMap(self):
        pass
    #RETURN
    # map representation: double list? dict?
    
    def unsubscribe(self):
        """Try to unsubscribe from the camera""" 
        try:
            self.globals.vidProxy.unsubscribe("python_GVM")
        except Exception as inst:
            print "Unsubscribing impossible:", inst
    
    def subscribe(self, resolution=1):
        """ subscribe() -> String visionID

        Subscribe to the camera feed.
        
        """
        self.unsubscribe()
        # subscribe(gvmName, resolution={0,1,2}, colorSpace={0,9,10,11,12,13},
        #           fps={5,10,15,30}
        return self.globals.vidProxy.subscribe("python_GVM", resolution, 11, 30)
            
    # get snapshot from camera
    def getSnapshot(self):
        """ snapShot() -> iplImg, (cameraPos6D, headAngles)

        Take a snapshot from the current subscribed video feed. 
        
        """
        # getPosition(name, space={0,1,2}, useSensorValues)
        # Make image
        camPos = self.globals.motProxy.getPosition("CameraBottom", 2, True)
        headAngles = self.globals.motProxy.getAngles(["HeadPitch", "HeadYaw"], True)
        shot = self.gloabls.vidProxy.getImageRemote(self.visionID)
        
        # Get image
        # shot[0]=width, shot[1]=height, shot[6]=image-data
        size = (shot[0], shot[1])
        picture = Image.frombuffer("RGB", size, shot[6], "raw", "BGR", 0, 1)
        
        size = picture.size
        # convert the type to OpenCV
        image = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(image, picture.tostring(), picture.size[0]*3)
        hsvFrame = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(image, hsvFrame, cv.CV_BGR2HSV)
    
        return (hsvFrame, (camPos, headAngles))
    
    
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