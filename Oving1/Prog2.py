import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy

def inverte(img): #The function that invertes the picture
  for x in range (0,len(img)): 
    for y in range(0,len(img[x])):
      #Loopes through the pixels.
      #Invertes the value of the pixel
      value = img[x][y]
      img[x][y] = 255 - value
  return img

#Loads up the picture
img=mpimg.imread('stinkbug.png')

#Shows the original
plt.imshow(img)
plt.show()
#Shows the new inverted image
plt.imshow(inverte(copy.copy(img)))
plt.show()



