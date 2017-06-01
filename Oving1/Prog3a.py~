import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy

def convolution(H,F): #The function that invertes the picture
  V = 0;
  for i in F:
    for v in i:
      V += v
  h = copy.copy(H) #makes aa copy of the image to write over
  o = int(float(len(F)/2)) #The offsett of the filter
  l = len(F)
  for x in range (o,len(H)-o): 
    for y in range(o,len(H[x])-o):
      h[x][y]=0 #Sets the current color at current pixel to zero
      for i in range (0,len(F)):
        for j in range(0,len(F[i])):        
            #adds the filters multiplier to the neighboorhood and adds it to the color
            h[x][y] += H[x-o+i][y-o+j]*F[i][j]/V 
  return h


Threes=[[1,1,1,]
  ,[1,1,1]
  ,[1,1,1]]

Fives = [[1,4,6,4,1]
    ,[4,16,24,16,4]
    ,[6,24,36,24,6]
    ,[4,16,24,16,4]
    ,[1,4,6,4,1]]


#Loads up the picture
img=mpimg.imread('stinkbug.png')

#Shows the original
plt.imshow(img)
plt.show()
#Shows the new inverted image
plt.imshow(convolution(copy.copy(img),Threes))
plt.show()

