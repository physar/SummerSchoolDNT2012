import cv #import opencv met deze twee functies
import cv2 #
import numpy as np #import de numpy library
import ARimport as ar #import de AR code herkennings module


ARcode = ar.ARimport()  #maak een class aan van de AR code herkennings module
image = cv.LoadImage("test.png",cv.CV_LOAD_IMAGE_COLOR) # Laad het test.png plaatje uit de folder (laad deze als kleuren plaatje!)
im_array = np.asarray( image[:,:] ) #van dit plaatje maken we een numpy array. Het is belangrijk dat dit het type uint_8 heeft (unsigned int 8bit)
ARcode.setOutputFileName("output.png")  #De output van het algoritme krijgt de volgende naam
ARcode.setShowOutput(True) #We willen dat het algoritme elke keer een plaatje output met een tekening van de marker
returnint = ARcode.findMarkers(im_array)  #Zoek de markers, en return een integer met hoeveel markers er gevonden zijn

output = ARcode.getFoundMarker(0) #input < returnint! output is een struct met .ID .x en .y informatie
print((output.ID, output.x, output.y))
                    