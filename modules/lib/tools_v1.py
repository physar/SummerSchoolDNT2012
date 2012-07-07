import cv
from naoqi import ALProxy
import math
import Image

class tools_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    # load map of maze from txt file
    def loadMap(self):
        pass
    #RETURN
    # map representation: double list? dict?
    
    #unsubscribe from camera
    def cUnsubscribe(self):
        """ Try to unsubscribe from the camera """ 
        try:
            self.globals.vidProxy.unsubscribe("python_GVM")
        except Exception as inst:
            print "Unsubscribing impossible:", inst

    #subscribe to camera        
    def cSubscribe(self, resolution=1):
        """ Subscribe to the camera feed. """
        self.cUnsubscribe()
        self.globals.vidProxy.setParam(18,1)
        # subscribe(gvmName, resolution={0,1,2}, colorSpace={0,9,10,rgb=11,hsy=12,bgr=13}, fps={5,10,15,30}
        self.globals.vidProxy.subscribe("python_GVM", resolution, 11, 30)
       
       
    # get snapshot from camera
    def getSnapshot(self):
        """ snapShot() -> iplImg, (cameraPos6D, headAngles)

        Take a snapshot from the current subscribed video feed. 
        
        """
        # Get camPos
        # getPosition(name, space={0,1,2}, useSensorValues)
        camPos = self.globals.motProxy.getPosition("CameraBottom", 2, True)
        headAngles = self.globals.motProxy.getAngles(["HeadPitch", "HeadYaw"], True)   
        
        # Get image
        # shot[0]=width, shot[1]=height, shot[6]=image-data
        shot = self.globals.vidProxy.getImageRemote("python_GVM")
        size = (shot[0], shot[1])
        picture = Image.frombuffer("RGB", size, shot[6], "raw", "BGR", 0, 1)
        image = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 3)     
        cv.SetData(image,picture.tostring(), picture.size[0]*3)
        image = self.convertColourSpace(image, cv.CV_BGR2HSV)
        #cv.SaveImage('test.png', image)
        return (image, (camPos, headAngles))
       
    def saveImage(self, img, name):
        """ save image, using given name. 
        Note that SaveImage/2 expects the colorspace BGR """ 
        cv.SaveImage(name, img)
        
    # conversion is an int: cv.CV_<scrColorSpace>2<dstColorSpace>
    def convertColourSpace(self, srcImage, conversion):
        dstImage = cv.CreateImage(cv.GetSize(srcImage), cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(srcImage, dstImage, conversion)
        return dstImage
    
    def minimizedAngle( angle ):
        """ maps an angle to the interval [pi, pi] """
        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi
        return angle
    
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
        return None
    #RETURN:
    # - 'reactive', 'path', 'QR'