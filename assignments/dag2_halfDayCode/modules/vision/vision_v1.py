import cv, cv2
import numpy, math

class vision_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #Find Blue Blob
    def filterImage(self,image):
        '''
        Input: HSV Image
        Output: Black White Matrix/Image      
        '''
        return filtImMat
        
    #Find circle, as it is now should only find 1 circle per image
    def findCircle(self,imageMat):
        '''
        Input: Black Whit Image
        Return: List of center position of found Circle       
        '''
        if circles == None:
            return None
        else:
            return coordinates
            
            
    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Return: numberOfBlobsFound , [List [x,y-pixels] of 
        '''
        return blobsFound , blobsList
        
    # Get Average Distance between multiple blobs  
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Pink, Blue Orange]
        Output: Avarege Distance in pixels
        '''
        return Distance
    
    # Fince centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Pink, Blue Orange]
        Output: Center pixel
        '''
        return center
        
    # Find the angle of a pixel that the Nao has to walk
    def calcAngleLandmark(self, center):
        '''
        Input: Pixel
        Output: Angle
        '''    
        return angle
    
    # Find the Signature from 3 blobs
    def findSignature(self,blobList):
        '''
        Input: [Pink, Blue Orange]
        Output: Signature
        '''
        return signature

    