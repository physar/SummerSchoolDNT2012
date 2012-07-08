import cv2
import cv

class vision_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    
    # process image to detect color blobs
    def getBeaconObservation(self, img):
        pass
    #RETURN:
    # = 'None' if no observation is found
    # = [signatue, distance, theta] if an observation is found
    #   - signature = id of observed beacon
    #   - distance = distance towards beacon
    #   - theta = angle towards beacon
	
	"""
	Perform a HSV and get the hue value of an image
	Input: 3 channel RGB image
	Output: 
	
	"""
    def getHue(self, img):
        hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv, cv.CV_BGR2HSV)    
        hue = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Split(hsv, hue, None, None, None)
        return hue

    def createHistogram(self,img, nbins):
	_HUESIZE = 180
	_IMGMAXINT = 255
	
	hist = cv.CreateHist([nbins], cv.CV_HIST_ARRAY, [[0,_HUESIZE]], 1)
	cv.CalcHist([img], hist, 0, None)
	cv.NormalizeHist(hist,1)
	(_,_,_,max_idx) = cv.GetMinMaxHistValue(hist)
	
	factor = _IMGMAXINT / hist.bins[max_idx];
	for i in range(0,nbins):
	    hist.bins[i] = hist.bins[i] * factor
	return hist
    
    def backProjection(self, img, hist):
	output = cv.CreateImage(cv.GetSize(img), 8L, 1);
	cv.CalcBackProject([img],output,hist);
	return output
    
    def filter(self, img):
	output = cv.CreateImage(cv.GetSize(img), 8L, 1);
	cv.Smooth(img, output, cv.CV_MEDIAN, 5)
	return output
    
    def getNeighbors(self, img, row, column):
	neighbors = []
	if(not(img[row-1,column] == 0)):
	    neighbors.append((row-1, column))
	if(not(img[row,column-1] == 0)):
	    neighbors.append((row, column-1))
	return neighbors
"""    
    def ConnectedComponent(self, img):
	labels = [[0 for row in range(img.height)] for col in range(img.width)]
		
	for row in range(1, img.height):
	    for column in range(1, img.width):
		if not(img[row,column] == 0):
		    neighbors = getNeighbors(img, row, column);
		    
		    if not(neighbors): #if neighbors is empty
			
"""	    
