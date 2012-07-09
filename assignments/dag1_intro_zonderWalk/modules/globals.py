from naoqi import ALProxy

class globals:
    ipadress = 'wind.local' #"192.168.1.35"
    
    def setDependencies(self, modules):
        pass

    def setProxies(self):
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipadress, 9559)
        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPose", self.ipadress, 9559)
        self.redBallProxy = ALProxy( "ALRedBallTracker", self.ipadress, 9559 )
        self.vidProxy = ALProxy( "ALVideoDevice", self.ipadress, 9559 )
        
        self.ledProxy = ALProxy( "ALLeds", self.ipadress, 9559 )
        