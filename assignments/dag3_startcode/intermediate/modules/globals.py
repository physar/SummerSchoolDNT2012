from naoqi import ALProxy

class globals:
    ipadress = "localhost"
    
    def setDependencies(self, modules):
        pass

    def setProxies(self):
        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPose", self.ipadress, 9559)
        self.vidProxy = ALProxy("ALVideoDevice", self.ipadress, 9559)
        
        #If you want you can use these
        #self.speechProxy = ALProxy("ALTextToSpeech", self.ipadress, 9559)
        #self.memProxy = ALProxy( "ALMemory", self.ipadress, 9559 ) 
        #self.ledProxy = ALProxy( "ALLeds", self.ipadress, 9559 )