from naoqi import ALProxy

class globals():    
    ipadress = None
    motProxy = None
    vidProxy = None
    memProxy = None
    ledProxy = None
    
    #no dependencies
    def setDependencies(self, modules):
        pass
    
    def setIPadress(self, ipadress):
        """ Set ip-adress of nao """
        self.ipadress = ipadress
        
    def createProxies(self):
        """ Set all proxies used by other modules """
        self.motProxy = ALProxy( "ALMotion", self.ipadress, 9559 )
        self.posProxy = ALProxy( "ALRobotPose", self.ipadress, 9559 )
        self.vidProxy = ALProxy( "ALVideoDevice", self.ipadress, 9559 )
        self.memProxy = ALProxy( "ALMemory", self.ipadress, 9559 ) 
        self.ledProxy = ALProxy( "ALLeds", self.ipadress, 9559 )
        self.redBallProxy = ALProxy( "ALRedBallTracker", self.ipadress, 9559 )
        self.speechProxy = ALProxy( "TextToSpeech", self.ipadress, 9559 )