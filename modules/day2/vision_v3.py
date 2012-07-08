import cv, cv2, math, numpy

class vision_v3():    
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
        
        blobsFound = 0
        blobsList = []
        
        if blobsP != None:
            blobsList.append(blobsP)
            blobsFound +=1 
        if blobsB != None:
            blobsList.append(blobsB)
            blobsFound +=1
        if blobsO != None:
            blobsList.append(blobsO)
            blobsFound +=1 
        print 'BlobsFound: ' + str(blobsFound)
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
            diff1 = self.findDiffrence(blobsP,blobsB)
            diff2 = self.findDiffrence(blobsP,blobsO)
            diff3 = self.findDiffrence(blobsO,blobsB)
            
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
                signature = self.findSignature(blobsO, blobsB, blobsP)
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
            diff = self.findDiffrence(blobsList[0],blobsList[1])
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
                realDistance = distance *0.01
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
            return 1, 0.01, angle
    
        
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon
    
    #signature: 1 = left, 2 = right , 3 = done. 0 = nothing
    def findSignature(self, orange, blue, pink):
        signature = 0
        xAverage, yAverage = self.findAvargePoint([orange,blue,pink])
        print xAverage, yAverage
        print orange 
        print blue
        print pink
      
        if (orange[0][0] < xAverage and pink[0][0] > xAverage and blue[0][1] < yAverage):
            print 'Signature: ' +str(1)
            signature = 1
            return signature
        if (blue[0][0] < xAverage and orange[0][0] > xAverage and pink[0][1] < yAverage):
            print 'Signature: ' +str(2)
            signature = 2
            return signature
        if (pink[0][0] < xAverage and blue[0][0] > xAverage and orange[0][1] < yAverage):
            print 'Signature: ' +str(3)
            signature = 3
            return signature
        else:
            print 'Signature fault!! couldnt find anything!!!'
            return 0
    
    
    
    def findAngle(self, x):
        #set the x to the middle of the screen
        xCoord = x - 160
        radiusPerPixelWidth = 0.003 #325
        xAngle = -((xCoord ) * radiusPerPixelWidth)  
        return xAngle
        
    
    #find diffrence between pixels in Image of 2 blobs (nothing to do with real world)
    def findDiffrence(self,blobYellow, blobBlue):
        [p1], [p2] = blobYellow, blobBlue
        [x1,y1] = p1
        [x2,y2] = p2
        diffPOW = math.pow(abs(y2 - y1),2)  + math.pow(abs(x1 -x2),2)
        diff = math.sqrt(diffPOW)
        return diff
        
        
    def findAvargePoint(self, blobsFound):
        global xTotal
        global yTotal
        xTotal , yTotal = 0,0
        #hack:
        #print 'DEBUG, blobsFound: ' + str(blobsFound)
        #print 'DEBUG, blobsFound[0]: ' + str(blobsFound[0])
        #print 'DEBUG, blobsFound[1]: ' + str(blobsFound[1])
        #print 'DEBUG, blobsFound[0][0]: ' + str(blobsFound[0][0])
        #print 'DEBUG, len(blobsFound): ' + str(len(blobsFound))
        #print 'DEBUG, len(blobsFound[0]): ' + str(len(blobsFound[0]))
        #blobsFound2 = blobsFound[0]
        for i in xrange(len(blobsFound)):
            #print 'Debug, blobsList: ' + str(blobsFound[i])
            Coordinates = blobsFound[i]
            [[x,y]] = Coordinates
            xTotal  += x
            yTotal += y
        xAvarge , yAvarge = (xTotal / len(blobsFound)) , (yTotal / len(blobsFound))
        print 'DEBRUG, average x,y!!!: ' + str(xAvarge) +', '+ str(yAvarge) 
        return xAvarge , yAvarge
       
       
            
            
    
    #Find circle, as it is now should only find 1 circle per image
    def findCircle(self,imageMat):
        imagenp = numpy.asarray(imageMat)
         
        coordinates = []
        dp = 2
        minDist =120
        param1 = 255
        param2 = 27
        minSize = 8
        maxSize = 300
        circles = cv2.HoughCircles(imagenp,cv.CV_HOUGH_GRADIENT,dp,minDist, None,param1,param2,minSize, maxSize)
        #debug
        print 'Found circles: ' + str(circles)

        if circles is not None:
            #print 'lengte cicles:' + str(circles)
            for i in xrange(len(circles[0])):
            #for i in range(0,circles.size/3-1):
                radius = circles[0][ i][2]
                center = [circles[0][ i][0], circles[0][ i][1]]
                print 'SUCCES'
                print (radius, center)
                coordinates.append(center)
                #debug
                #cv.Circle(picture, center, radius, (0, 0, 255), 3, 8, 0)
        
        if circles == None:
            return None
        else:
            return coordinates
    
    #find yellow blob (should probably be some other color)
    def filterImagePink(self, im):
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
        
        #yellow, circle
        #hsvMin1 = cv.Scalar(29,  100,  180, 0)
        #hsvMax1 = cv.Scalar(34,  210,  225, 0)

        #pink, from aibo pole
        #hsvMin1 = cv.Scalar(168,  50,  90, 0)
        #hsvMax1 = cv.Scalar(173,  200,  238, 0)
        
        #hsvMin2 = cv.Scalar(170,  90,  130, 0)
        #hsvMax2 = cv.Scalar(200, 256, 256, 0)

        # Color detection using HSV
        
        cv.InRangeS(im, hsvMin1A, hsvMax1A, filtImA)
        cv.InRangeS(im, hsvMin1B, hsvMax1B, filtImB)

        #thresh = 127
        #im_bw = cv.threshold(im, thresh, 255, cv.THRESH_BINARY)[1]
        #cv.Threshold(filtIm, filtIm, 100, 255, cv.CV_THRESH_BINARY)
        #cv.InRangeS(hsvFrame, hsvMin2, hsvMax2, filter2)
        cv.Or(filtImA, filtImA, filterdIm)
        cv.SaveImage('filterPink.png' ,filterdIm)
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat

    #find Blue Blob
    def filterImageBlue(self,image):
        size = (320,240)   

        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        hsvMin1B = cv.Scalar(110,214,100, 0)
        hsvMax1B = cv.Scalar(120,238,217, 0)    
        
        #Old Dark Blue, hsv values
        #hsvMin1B = cv.Scalar(113,154,20, 0)
        #hsvMax1B = cv.Scalar(124,256,200, 0)
        
        #filter image on given HSV values
        cv.InRangeS(image, hsvMin1B, hsvMax1B, filterdIm)

        cv.Smooth(filterdIm, filterdIm, cv.CV_MEDIAN, 5)
        cv.SaveImage('filterBlue.png' ,filterdIm)
        #filtIm2 = cv2.threshold(filtIm,  100, 255, cv.CV_THRESH_BINARY)[1]
        
        filtImMat = cv.GetMat(filterdIm)
        return filtImMat
     
    def filterImageOrange(self, im):
        # Size of the images
        size = (320,240)
        
        
        filtIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        #filter2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)

        hsvMin1 = cv.Scalar(6,171,72, 0)
        hsvMax1 = cv.Scalar(17,238,220, 0)

        #Blue from aibo pole
        #hsvMin1 = cv.Scalar(109,100,80, 0)
        #hsvMax1 = cv.Scalar(115,220,209, 0)
        
        #hsvMin2 = cv.Scalar(170,  90,  130, 0)
        #hsvMax2 = cv.Scalar(200, 256, 256, 0)

        # Color detection using HSV
        
        cv.InRangeS(im, hsvMin1, hsvMax1, filtIm)
        cv.Smooth(filtIm, filtIm, cv.CV_MEDIAN, 5)
        cv.SaveImage('filterOrange.png' ,filtIm)
        #cv.InRangeS(hsvFrame, hsvMin2, hsvMax2, filter2)
        #cv.Or(filter, filter2, filter)
        filtImMat = cv.GetMat(filtIm)
        return filtImMat    
        
    #for when we want to find shit on the ground   
    def calcPosition(self,coord, cam, headInfo):
        (width, height) = size
        #print 'size: ', width, ', ', height
        # coord with origin in the upperleft corner of the image
        (xCoord, yCoord) = coord
        #print 'pixelCoord from upperLeft: ', xCoord, ', ', yCoord
        # change the origin to centre of the image
        xCoord = -xCoord + width/2.0
        yCoord = yCoord - height/2.0
        #print 'pixelCoord from centre: ', xCoord, ', ', yCoord
        # convert pixel coord to angle
        radiusPerPixelHeight = 0.00345833333
        radiusPerPixelWidth = 0.003325
        xAngle = (xCoord +0.5) * radiusPerPixelWidth    
        yAngle = (yCoord+ 0.5) * radiusPerPixelHeight
        if -1 < xAngle < 1 and -1 < yAngle < 1:
            yAngle = -0.47 - headInfo[0] if yAngle + headInfo[0] < -0.47 else yAngle
            motion.changeAngles(['HeadPitch', 'HeadYaw'], [0.1*yAngle, 0.1*xAngle], 0.7)  # 0.3*angles for smoother movements, optional. Smoothinggg. 
            #motion.changeAngles(['HeadPitch', 'HeadYaw'], [0.3*yAngle, 0.3*xAngle], 0.7)  # 0.3*angles for smoother movements, optional. Smoothinggg. 

        #print 'angle from camera: ' + str(xAngle) + ', ' + str(yAngle)

        # the position (x, y, z) and angle (roll, pitch, yaw) of the camera
        (x,y,z, roll,pitch,yaw) = cam
        #print 'cam: ', cam

        # the pitch has an error of 0.940063x + 0.147563
        # print 'correctedPitch: ', pitch

        # position of the ball where
        # origin with position and rotation of camera
        #ballRadius = 0.0325     # in meters
        ballRadius = 0.065
        xPos = (z-ballRadius) / tan(pitch + yAngle)
        yPos = tan(xAngle) * xPos
        #print 'position from camera: ', xPos, ', ', yPos
        # position of the ball where
        #  origin with position of camera and rotation of body 
        xPos = cos(yaw)*xPos + -sin(yaw)*yPos
        yPos = sin(yaw)*xPos +  cos(yaw)*yPos
        # position of the ball where
        #  origin with position and rotation of body
        xPos += x
        yPos += y
        #print 'position ball: ', xPos, ', ', yPos
        #print 'new yaw/pitch: ', xAngle+yaw, yAngle+pitch
        #print 'z / tan(pitch): ',(z-ballRadius) / tan(pitch)
        return (xPos, yPos, xAngle, yAngle)
        