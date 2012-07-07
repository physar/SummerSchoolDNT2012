import cv, cv2, math, numpy

class vision_v2():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getBeaconObservation(self, img):
        (image, (camPos, headAngles)) = img
        #filter image with given HSV
        filtImageY = self.filterImageYellow(image)
        filtImageB = self.filterImageBlue(image)
        #Find Circles (should only be 1 per image 
        blobsY = self.findCircle(filtImageY)
        blobsB = self.findCircle(filtImageB)
        
        #When nothing found
        if blobsY == None and blobsB == None:           
            cv.SaveImage('None.png', image)
            return None
        #when both color blobs are found    
        if blobsY != None and blobsB != None:
            #debug: kalibrate when perfect spot is found
            print 'px,py coord Yellow Blob: ' + str(blobsY)
            print 'px,py coord Blue Blob: ' + str(blobsB)
            
            #Diffrence in distance off pixels between blobs
            diff = self.findDiffrence(blobsY,blobsB)
            print 'Differnce in pixels between blobs: ' +str(diff)
            ### Need to find perfect diff
            #Bullcrap: 60 pix is the spot, groter is te dichtbij etc 
            distance = (diff - 35 )
            #when small diffrence your done
            if abs(distance) < 5:
                print 'This was my distance to the goal: ' + str(distance) + ' !!IM DONE!!'
                cv.SaveImage('goal.png', image)
                #return signal(links, rechts), distance, theta
                return 1, 0, 0
            else:
                
                #####MOET KALIBREREN!!!!!!
                realDistance = distance *0.01
                print 'Distance to walk to the goal: ' + str(realDistance)
                return 1, realDistance, 0
        #one of the 2 blobs was found
        ##Moeten bij 1 blob ook hoek meenemen zodat hij er recht op af loopt
        else:         
            if blobsY == None:
                print 'Only Blue was found!!'
            else:
                print 'Only Yellow was found!!'
            return None
    
        
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon
    
    #find diffrence between pixels in Image of 2 blobs (nothing to do with real world)
    def findDiffrence(self,blobYellow, blobBlue):
        [p1], [p2] = blobYellow, blobBlue
        y1 = p1[1]
        y2 = p2[1]
        diff = abs(y2 - y1)
        return diff
    
    #Find circle, as it is now should only find 1 circle per image
    def findCircle(self,imageMat):
        imagenp = numpy.asarray(imageMat)
         
        coordinates = []
        dp = 2
        minDist =30
        param1 = 255
        param2 = 27
        minSize = 3
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
    def filterImageYellow(self,image):
        size = (320,240)   
        filtImYellow = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        
        #yellow, circle
        hsvMin1Y = cv.Scalar(28,  99,  164, 0)
        hsvMax1Y = cv.Scalar(35,  212,  230, 0)
        
        #filter image on given HSV values
        cv.InRangeS(image, hsvMin1Y, hsvMax1Y, filtImYellow)

        cv.Smooth(filtImYellow, filtImYellow, cv.CV_MEDIAN, 5)
        cv.SaveImage('filterYellow.png' ,filtImYellow)
        #filtIm2 = cv2.threshold(filtIm,  100, 255, cv.CV_THRESH_BINARY)[1]
        
        filtImMat = cv.GetMat(filtImYellow)
        return filtImMat

    #find Blue Blob
    def filterImageBlue(self,image):
        size = (320,240)   

        filterdIm = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)

        #Blue, hsv values
        hsvMin1B = cv.Scalar(113,154,20, 0)
        hsvMax1B = cv.Scalar(124,256,200, 0)
        
        #filter image on given HSV values
        cv.InRangeS(image, hsvMin1B, hsvMax1B, filterdIm)

        cv.Smooth(filterdIm, filterdIm, cv.CV_MEDIAN, 5)
        cv.SaveImage('filterBlue.png' ,filterdIm)
        #filtIm2 = cv2.threshold(filtIm,  100, 255, cv.CV_THRESH_BINARY)[1]
        
        filtImMat = cv.GetMat(filterdIm)
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
        