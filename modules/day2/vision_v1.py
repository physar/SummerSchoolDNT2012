class vision_v1():    

    def setDependencies(self, modules):
        pass
    
    # process image to detect color blobs
    def getBeaconObservation(self, img):
        pass
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon