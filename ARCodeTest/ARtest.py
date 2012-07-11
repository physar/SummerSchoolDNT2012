import cv #import de opencv/numpy en AR code recognition library
import cv2
import numpy as np
import ARimport as ar


ARcode = ar.ARimport() #maak een nieuwe AR detectie object
image = cv.LoadImage("test.png",cv.CV_LOAD_IMAGE_COLOR) #laad het testplaatje
im_array = np.asarray( image[:,:] ) #maak van de opencv image een numpy array
ARcode.setOutputFileName("output.png") #Ze de naam voor de output file
ARcode.setShowOutput(True) #zeg dat het algoritme output moet tonen, kan je ook uitzetten
returnint = ARcode.findMarkers(im_array) #vind de markers in het plaatje, returned hoeveel markers gevonden zijn

output = ARcode.getFoundMarker(0) #input < returnint # 0 is voor de eerste marker 1 voor de 2e etc. # output structs met .x .y en .ID informatie
print((output.ID, output.x, output.y))

                    
