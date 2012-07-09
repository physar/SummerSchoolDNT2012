import cv, cv2
import numpy, math

class vision_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

        
    #Find the Pink Blob
    def filterImage(self,img, minHSV, maxHSV):
        '''
        Input: HSV Image, 2 List of min and max HSV values 
        Output: Black White Matrix/Image      
        '''
        size = (320,240)   

        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        [hMin,sMin,vMin] = minHSV
        [hMax, sMax, vMax] = maxHSV
        hsvMin1B = cv.Scalar(hMin,sMin,vMin, 0)
        hsvMax1B = cv.Scalar(hMax, sMax, vMax, 0)    
        
        #filter image on given HSV values
        cv.InRangeS(image, hsvMin1B, hsvMax1B, filterdIm)

        cv.Smooth(filterdIm, filterdIm, cv.CV_MEDIAN, 5)
        cv.SaveImage('filterd.png' ,filterdIm)
        
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat
        
    #Find Blue Blob
    def filterImagePink(self,image):
        '''
        Input: HSV Image
        Output: Black White Matrix/Image      
        '''
        # Size of the images
        size = (320,240)
                
        filtImA = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filtImB = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)

        #pink saturday
        hsvMin1A = cv.Scalar(0,  148,  77, 0)
        hsvMax1A = cv.Scalar(7,  237,  217, 0)    

        hsvMin1B = cv.Scalar(174,  148,  77, 0)
        hsvMax1B = cv.Scalar(181,  237,  217, 0)    

        # Color detection using HSV
        
        cv.InRangeS(im, hsvMin1A, hsvMax1A, filtImA)
        cv.InRangeS(im, hsvMin1B, hsvMax1B, filtImB)
        
        cv.Or(filtImA, filtImA, filterdIm)
        cv.SaveImage('filterPink.png' ,filterdIm)
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat
        
    #Find circle, as it is now should only find 1 circle per image
    def findCircle(self,imageMat):
        '''
        Input: Black Whit Image
        Return: List of center position of found Circle       
        '''
        imagenp = numpy.asarray(imageMat)
         
        coordinates = []
        dp = 2
        minDist =120
        param1 = 255
        param2 = 27
        minSize = 8
        maxSize = 300
        circles = cv2.HoughCircles(imagenp,cv.CV_HOUGH_GRADIENT,dp,minDist, None,param1,param2,minSize, maxSize)
        #DEBUG
        print 'Found circles: ' + str(circles)

        if circles is not None:
            for i in xrange(len(circles[0])):
                radius = circles[0][ i][2]
                center = [circles[0][ i][0], circles[0][ i][1]]
                print 'Found radius and center'
                print (radius, center)
                coordinates.append(center)
                
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
        #filter image with given HSV
        filtImageB = self.filterImageBlue(image)
        filtImageP = self.filterImagePink(image)
        filtImageO = self.filterImageOrange(image)
        #Find Circles (should only be 1 per image ) Blobs = (x,y)
        blobsP = self.findCircle(filtImageP)
        blobsB = self.findCircle(filtImageB)
        blobsO = self.findCircle(filtImageO)
        
        blobsFound , blobsList = self.appendBlobs( blobsP, blobsB, blobsO)
        return blobsFound , blobsList
        
    #Put all the found blobs in a list
    def appendBlobs(self, blobsP, blobsB, blobsO):
        print blobsP, blobsB, blobsO
        blobsFound = 0
        blobsList = []
        
        #Count the blobs
        if blobsP != None: 
            #FALESAFE: now only the 1st found circle in a pic will be used              
            blobsList.append(blobsP[0])
            blobsFound +=1 
        else:
            blobsList.append(blobsP)
        if blobsB != None: 
            blobsList.append(blobsB[0])
            blobsFound +=1
        else:
            blobsList.append(blobsB)
        if blobsO != None: 
            blobsList.append(blobsO[0])
            blobsFound +=1 
        else:
            blobsList.append(blobsO)
        print 'BlobsFound: ' + str(blobsFound)
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

    