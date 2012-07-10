import cv, cv2
import numpy, math

class vision_v2():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

        
    #Find a Blob with a color at one positions in the spectrum
    def filterImage(self, img, minHSV, maxHSV):
        '''
        Input: HSV Image, 2 List of min and max HSV values 
        Output: Black White Matrix/Image      
        '''
        size = (320,240)   

        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        [hMin, sMin, vMin] = minHSV
        [hMax, sMax, vMax] = maxHSV
        hsvMin1B = cv.Scalar(hMin,sMin,vMin, 0)
        hsvMax1B = cv.Scalar(hMax, sMax, vMax, 0)    
        
        #filter image on given HSV values
        cv.InRangeS(img, hsvMin1B, hsvMax1B, filterdIm)

        #smooth and return
        cv.Smooth(filterdIm, filterdIm, cv.CV_MEDIAN, 5)
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat
        
    #Find a Blob with a color at two positions in the spectrum
    def filterImageDouble(self, img, minHSV1, maxHSV1, minHSV2, maxHSV2):
        '''
        Input: HSV Image
        Output: Black White Matrix/Image      
        '''
        # Size of the images
        size = (320,240)
                
        filtIm1 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filtIm2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)

        #Color scalars
        [hMin1, sMin1, vMin1] = minHSV1
        [hMax1, sMax1, vMax1] = maxHSV1
        [hMin2, sMin2, vMin2] = minHSV2
        [hMax2, sMax2, vMax2] = maxHSV2
        hsvMin1 = cv.Scalar(hMin1, sMin1, vMin1, 0)
        hsvMax1 = cv.Scalar(hMax1, sMax1, vMax1, 0)  
        hsvMin2 = cv.Scalar(hMin2, sMin2, vMin2, 0)
        hsvMax2 = cv.Scalar(hMax2, sMax2, vMax2, 0)  

        # Color detection using HSV
        cv.InRangeS(img, hsvMin1, hsvMax1, filtIm1)
        cv.InRangeS(img, hsvMin2, hsvMax2, filtIm2)
        
        #combine images
        cv.Or(filtIm1, filtIm2, filterdIm)
        
        #smooth and return
        cv.Smooth(filterdIm, filterdIm, cv.CV_MEDIAN, 5)
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat
        
    #Find Circle in a filtered image
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
        minHSVBlue   = [110, 214, 100]
        maxHSVBlue   = [120, 238, 217]
        minHSVOrange = [  6, 171,  72]
        maxHSVOrange = [ 17, 238, 220]
        minHSVPink1  = [  0, 148,  77]
        maxHSVPink1  = [  7, 237, 217]
        minHSVPink2  = [174, 148,  77]
        maxHSVPink2  = [181, 237, 217]
        
        #filter image with given HSV
        filtImageB = self.filterImage(image, minHSVBlue, maxHSVBlue)
        filtImageO = self.filterImage(image, minHSVOrange, maxHSVOrange)
        filtImageP = self.filterImageDouble(image, minHSVPink1, maxHSVPink1, minHSVPink2, maxHSVPink2)
        
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
            blobsList.append(None)
        if blobsB != None: 
            blobsList.append(blobsB[0])
            blobsFound +=1
        else:
            blobsList.append(None)
        if blobsO != None: 
            blobsList.append(blobsO[0])
            blobsFound +=1 
        else:
            blobsList.append(None)
            
        print 'BlobsFound: ' + str(blobsFound)
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
        Output: center pixel, (x,y)
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
    