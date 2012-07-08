from naoqi import ALProxy

class globals:
    ipadress = "192.168.1.35"
    
    def setDependencies(self, modules):
        pass

    def setProxies(self):
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipadress, 9559)
        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPose", self.ipadress, 9559)
        