from naoqi import ALProxy

class globals:
    ipadress = "..."
    
    def setDependencies(self, modules):
        pass

    def setProxies(self):
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipadress, 9559)
        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPose", self.ipadress, 9559)
        self.vidProxy = ALProxy( "ALVideoDevice", self.ipadress, 9559 )
