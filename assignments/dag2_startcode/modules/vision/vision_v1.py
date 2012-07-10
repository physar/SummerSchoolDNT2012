import cv, cv2
import numpy, math

class vision_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #Filter HSV Image with given values
    def filterImage(self, img, minHSV, maxHSV):
        '''
        Input: HSV Image, 2 List of min and max HSV values 
        Output: Black White Matrix/Image      
        '''
        return filtImMat
        
    #Find Circle in a filtered image
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
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''
        return blobsFound , blobsList
        
    # Get Average Distance between multiple blobs  
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Avarege Distance in pixels
        '''
        return Distance
    
    # Find centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: center pixel as (x,y)
        '''
        return center
        
    # Find the angle between a found Landmark and the Nao
    def calcAngleLandmark(self, center):
        '''
        Input: center pixel, (x,y)
        Output: Angle in radians
        '''    
        return angle
    
    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Signature
        '''
        return signature

    