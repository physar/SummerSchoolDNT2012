import cv, cv2, math, numpy

class vision_v4():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getBeaconObservation(self, img):
        (image, (camPos, headAngles)) = img
        #filter image with given HSV
        filtImageB = self.filterImageBlue(image)
        filtImageP = self.filterImagePink(image)
        filtImageO = self.filterImageOrange(image)
        #Find Circles (should only be 1 per image ) Blobs = (x,y)
        blobsP = self.findCircle(filtImageP)
        blobsB = self.findCircle(filtImageB)
        blobsO = self.findCircle(filtImageO)
        
        blobsFound , blobsList = self.appendBlobs( blobsP, blobsB, blobsO)
      
        #When nothing found
        if blobsFound == 0:           
            cv.SaveImage('None.png', image)
            return None
        #when all color blobs are found    
        #if blobsP != None and blobsB != None and blobsO != None:
        if blobsFound == 3:
            #debug: kalibrate when perfect spot is found
            print 'px,py coord Yellow Blob: ' + str(blobsP)
            print 'px,py coord Blue Blob: ' + str(blobsB)
            print 'px,py coord Orange Blob: ' + str(blobsO)
            
            #Diffrence in distance off pixels between blobs
            diff1 = self.findDistances(blobsP[0],blobsB[0])
            diff2 = self.findDistances(blobsP[0],blobsO[0])
            diff3 = self.findDistances(blobsO[0],blobsB[0])
            
            avrage = (diff1 +diff2 + diff3) /3
            
            print 'Differnce in pixels between blobs: ' +str(avrage)
            ### Need to find perfect diff
            #Bullcrap: 97 pix is the spot, groter is te dichtbij etc 
            distance = -(avrage - 78 )
            #when small diffrence your done
            if abs(distance) < 5:
                print 'This was my distance to the goal: ' + str(distance) + ' !!IM DONE!!'
                cv.SaveImage('goal.png', image)
                #return signal(links, rechts), distance, theta
                signature = self.findSignature(blobsO[0], blobsB[0], blobsP[0])
                return signature, 0, 0
            else:
                xAverage, yAverage = self.findAvargePoint(blobsList)
                angle = self.findAngle(xAverage)
                #####MOET KALIBREREN!!!!!!
                realDistance = distance *0.002
                print 'Distance to walk to the goal: ' + str(realDistance)
                print 'DEBUG, angle: ' + str(angle)
                return 0, realDistance, angle
        #2 Blobs was found !!!TO DO: Radian toevoegen
        if blobsFound == 2:
            diff = self.findDistances(blobsList[0],blobsList[1])
            xAverage, yAverage = self.findAvargePoint(blobsList)
            angle = self.findAngle(xAverage)
            
            distance = -(diff - 78 )
            #when small diffrence your done
            if abs(distance) < 5:
                print 'This was my distance to the goal: ' + str(distance) + ' !!IM DONE!!'
                cv.SaveImage('goal.png', image)
                #return signal(links, rechts), distance, theta
                return 0, 0, 0
            else:
                #####MOET KALIBREREN!!!!!!
                realDistance = distance *0.005
                print 'Distance to walk to the goal: ' + str(realDistance)
                print 'DEBUG, angle: ' + str(angle)
                return 0, realDistance, angle
                       
        
        #one of the 3 blobs was found
        ##Moeten bij 1 blob ook hoek meenemen zodat hij er recht op af loopt
        else:     
            #TO DO radius gebruiken om terug te lopen 
            
            xAverage, yAverage = self.findAvargePoint(blobsList)
            angle = self.findAngle(xAverage)
            #Debug
            if blobsP != None:
                print 'Pink was Found!!'
            if blobsO != None:
                print 'Orange was Found!!'
            if blobsB != None:
                print 'Blue was Found!!'
            print 'DEBUG, angle: ' + str(angle)
            return 1, 0.03, angle
    
        
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon
    
    #Put all the found blobs in a list
    def appendBlobs(self, blobsP, blobsB, blobsO):
    
        blobsFound = 0
        blobsList = []
        if blobsP != None:
            #now only the 1st found circle in a pic will be used
            blobsList.append(blobsP[0])
            blobsFound +=1 
        if blobsB != None:
            blobsList.append(blobsB[0])
            blobsFound +=1
        if blobsO != None:
            blobsList.append(blobsO[0])
            blobsFound +=1 
        print 'BlobsFound: ' + str(blobsFound)
        return blobsFound , blobsList
    
    #signature: 1 = left, 2 = right , 3 = done. 0 = nothing
    def findSignature(self, orange, blue, pink):
        signature = 0
        xAverage, yAverage = self.findAvargePoint([orange,blue,pink])
        print xAverage, yAverage
        print orange 
        print blue
        print pink
      
        if (orange[0] < xAverage and pink[0] > xAverage and blue[1] < yAverage):
            print 'Signature: ' +str(1)
            signature = 1
            return signature
        if (blue[0] < xAverage and orange[0] > xAverage and pink[1] < yAverage):
            print 'Signature: ' +str(2)
            signature = 2
            return signature
        if (pink[0] < xAverage and blue[0] > xAverage and orange[1] < yAverage):
            print 'Signature: ' +str(3)
            signature = 3
            return signature
        else:
            print 'Signature fault!! couldnt find anything!!!'
            return 0
    
    
    #Find the angle of Pixel found in the Image
    def findAngle(self, x):
        '''
        Input: x pixel (horizontal plane)
        Return: Angle in Radian
        
        Hint: radiusPerPixelWidth = 0.003
        ''' 
        return xAngle
        
    
    #find diffrence between pixels in Image of 2 blobs (nothing to do with real world)
    def findDistances(self,blob1, blob2):
        ''' 
        Input: 2 x,y pixel positions of the Center of 2 
        Return: Distance in pixels between the 2
        
        Use Pythagoras
        '''
        return diff
        
    #Find the avargePoint off multiple Circles/Blobs   
    def findAvargePoint(self, blobsFound):
        '''
        Input: List [], containing x,y pixel positions of found Blobs
        Return: Average x,y pixel of all the Blobs found                   
        '''       
        return xAvarge , yAvarge          
            
    
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

        if circles is not None:
            ############ CODE MISSING ###########
            #Find all the centers off the found Circles and append them in 1 list[]
            #print 'lengte cicles:' + str(circles)
                      
        if circles == None:
            return None
        else:
            return coordinates
    
    #Find the PinkBlob has 2 values in HSV 
    def filterImagePink(self, im):
        # Size of the images
        size = (320,240)
      
        filtImA = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filtImB = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)

        hsvMin1A = cv.Scalar(0,  148,  77, 0)
        hsvMax1A = cv.Scalar(7,  237,  217, 0)    

        hsvMin1B = cv.Scalar(174,  148,  77, 0)
        hsvMax1B = cv.Scalar(181,  237,  217, 0)            
        cv.InRangeS(im, hsvMin1A, hsvMax1A, filtImA)
        cv.InRangeS(im, hsvMin1B, hsvMax1B, filtImB)
        cv.Or(filtImA, filtImA, filterdIm)
        cv.SaveImage('filterPink.png' ,filterdIm)
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat

    #Find Blue Blob
    def filterImageBlue(self,image):
        '''
        Input: HSV Image
        Output: Black White Matrix/Image
       
        hsvMin1B = cv.Scalar(110,214,100, 0)
        hsvMax1B = cv.Scalar(120,238,217, 0)       
        '''
        return filtImMat
        
    #Find the OrangeBlob 
    def filterImageOrange(self, im):
        '''
        Input: HSV Image
        Output: Black White Matrix/Image
        hsvMin1 = cv.Scalar(6,171,72, 0)
        hsvMax1 = cv.Scalar(17,238,220, 0)
        '''
        return filtImMat    
        
