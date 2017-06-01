import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy
import math

def convolutionMagnitude(H,Fx,Fy): #The function that invertes the picture
  
  hx = copy.copy(H) #makes aa copy of the image to write over
  hy = copy.copy(H) #makes aa copy of the image to write over
  h = copy.copy(H) #makes aa copy of the image to write over
  print(hx[100][100])
  o = int(float(len(Fx)/2)) #The offsett of the filter
  print(o)
  for x in range (o,len(H)-o): 
    for y in range(o,len(H[x])-o):
      hx[x][y]=0 #Sets the current color at current pixel to zero
      hy[x][y]=0
      for i in range (0,len(Fx)):
        for j in range(0,len(Fx[i])):        
            #adds the filters multiplier to the neighboorhood and adds it to the color
            hx[x][y][0] += H[x-o+i][y-o+j][0]*Fx[i][j]
            hy[x][y][0] += H[x-o+i][y-o+j][0]*Fy[i][j]
      #Calculates the new values
      vx = math.pow(hx[x][y][0],2)
      vy = math.pow(hy[x][y][0],2)
      v = vx + vy
      m=float(math.sqrt(v))#adds them into the return matrix
      for k in range(3):
        h[x][y][k]=m
  return h

Fx = [[1,0,1]
    ,[2,0,-2]
    ,[1,0,-1]]

Fy = [[1,2,1]
    ,[0,0,0]
    ,[-1,-2,-1]]

#Loads up the picture
img=mpimg.imread('boxes.jg')

#Shows the original
plt.imshow(img)
plt.show()
#Shows the new inverted image
plt.imshow(convolutionMagnitude(copy.copy(img),Fx,Fy))
plt.show()

