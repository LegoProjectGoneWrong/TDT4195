import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy
img=mpimg.imread('lake.jpg')

plt.imshow(img)
plt.show()
#loopes through all the pixels of the picture

def func1(img): 
  for x in range (0,len(img)):
    for y in range(0,len(img[x])):
      #finds the mean of the 3 colors, and replaces the pixel
      data = img[x][y]
      sum = 0
      for c in range(0,3):
        sum += img[x][y][c]
      color = sum/3;
      color = int(color)
      img[x][y]=[color,color,color]
  return img
plt.imshow(func1(copy.copy(img)))
plt.show()

def func2(img):
  for x in range (0,len(img)):
    for y in range(0,len(img[x])):
      #finds the mean of the 3 colors, and replaces the pixel
      data = img[x][y]
      multi = [0.2126,0.7152,0.0722]
      color = 0;
      for c in range(0,3):
        color  += img[x][y][c]*multi[c]
      img[x][y]=[color,color,color]
  return img
plt.imshow(func2(copy.copy(img)))
plt.show()

