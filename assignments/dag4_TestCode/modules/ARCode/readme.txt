!- LOOK AT ARtest.py, IT EXPLAINS EVERYTHING -!

// Necessary library files

_ARimport.pyd
	Python Library file
ARimport.lib
	General library file
ARimport.py
	Include file for the library, interface
aruco123.dll
	Dynamically linked lib for AR code detection
camera.yml
	file that containts camera parameters

// Test files

readme.txt
	this file
ARtest.py
	Run this and see if output.png has the test.png picture 	with a red box
test.png
	Picture with arcode id = 25 used for testing

//Library functions
import library command:
	import ARimport as ar
	import numpy as np
	import cv

#load an image from disk, has to be a color image
image = cv.LoadImage("test.png",cv.CV_LOAD_IMAGE_COLOR)

#convert this image to a numpy array
im_array = np.asarray( image[:,:] )

#Tell the marker code to find the AR markers
#Returns an integer with the amount of markers found
intMarkerNum = ARcode.findMarkers(im_array)

#Get the i'th marker information, where i < intMarkerNum
output = ARcode.getFoundMarker(i)

#output is in the form
struct markerInfo {
    unsigned int x;
    unsigned int y;
    unsigned int ID;
};

#to get a tuple out of this:
(output.ID, output.x, output.y)

#if i >= intMarkerNum then struct is initialized with -1 everywhere


//Library functions for visualization
#Tell the module what the output picture path is
ARcode.setOutputFileName("output.png")

#Tell the module that the output should be written away nicely
#WARNING: This draws a red box in the ORIGINAL image, nothing is copied
ARcode.setShowOutput(True)
