import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy

def gamma(img,G): #The function that invertes the picture
  for x in range (0,len(img)): 
    for y in range(0,len(img[x])):
      value = img[x][y]/255 #nomralizes the picture
      img[x][y] = (value**G)*255 #applies the transformation and multiplies it ut againn
  return img

#Loads up the picture
img=mpimg.imread('stinkbug.png')

#Shows the original
plt.imshow(img)
plt.show()
#Shows the new inverted image with gamma = 0.3
#Gamma = 0.3
plt.imshow(gamma(copy.copy(img),0.3))
plt.show()

plt.imshow(gamma(copy.copy(img),0.5))
plt.show()
#Gamma = 0.8
plt.imshow(gamma(copy.copy(img),0.8))
plt.show()
#gamma = 1.5
plt.imshow(gamma(copy.copy(img),1))
plt.show()

#Gamma = 2
plt.imshow(gamma(copy.copy(img),1.2))
plt.show()

#Gamma = 3
plt.imshow(gamma(copy.copy(img),1.5))
plt.show()





