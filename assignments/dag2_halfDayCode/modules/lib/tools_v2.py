import cv
from naoqi import ALProxy
import math

class tools_v2():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

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
        self.globals.vidProxy.subscribe("python_GVM", resolution, 13, 30)
       
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
        image = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 3)     
        cv.SetData(image, shot[6], shot[0]*3)
        image = self.convertColourSpace(image, cv.CV_BGR2HSV)
        
        return (image, (camPos, headAngles))
        
    # conversion is an int: cv.CV_<scrColorSpace>2<dstColorSpace>
    def convertColourSpace(self, srcImage, conversion):
        dstImage = cv.CreateImage(cv.GetSize(srcImage), cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(srcImage, dstImage, conversion)
        return dstImage
        
    def SaveImage(self, name, img):
        cv.SaveImage(name, img)
    
    def minimizedAngle( angle ):
        """ maps an angle to the interval [pi, pi] """
        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi
        return angle