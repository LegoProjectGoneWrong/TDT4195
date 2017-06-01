from PIL import Image as Im
import numpy as np
import math
import matplotlib.pyplot as plt
import copy



def image_2_matrix(img):
  m = [[img.getpixel((x,y)) for y in range(img.size[1])] for x in range(img.size[0])]
  return m

def matrix_2_image(m,mode="L"):
  lx, ly = len(m),len(m[0])
  img = Im.new(mode,(lx,ly))
  for x in range(lx):
    for y in range(ly):
      img.putpixel((x,y), int(m[x][y]))
  return img

def matrix_2_gray(m):
  xl,yl = len(m),len(m[0])
  return [[int(np.mean(m[x][y])) for y in range(yl)] for x in range(xl)]

def image_2_gray(img):#returns a grayscale of the image
  return matrix_2_image(matrix_2_gray(image_2_matrix(img)))

def image_2_list(img):
  return [img.getpixel((x,y)) for y in range (img.size[1]) for x in range(img.size[0])]

def matrix_2_list(m):
  return [m[x][y] for y in range(len(m[0])) for x in range(len(m))]

def padd_matrix(m,n): #padds the matrixs with n 0's in each direction
  M = [[0 for y in range(len(m[0])+2*n)]for x in range(len(m)+2*n)]
  for x in range(len(m)):
    for y in range(len(m[0])):
        M[x+n][y+n] = m[x][y]
  return M
        
def perform_dilation(m,k): #Applies kernel through dilation on matrix, returns matrix
  M = [[0 for y in range(len(m[0]))]for x in range(len(m))]
  lx,ly,lk,lk2= len(m),len(m[0]),len(k),int(len(k)/2)
  for x in range(lk2,lx-lk2):
    for y in range(lk2,ly-lk2):
      if(m[x][y]>128):
        #If reference node is high, sets all surrounding to highk
        for a in range(lk):
          for b in range(lk):
            pos_x,pos_y = x-lk2+a,y-lk2+b
            if k[a][b]==1:
              M[pos_x][pos_y]=255
  return M

def perform_erosion(m,k,): 
  #Applies kernel through dilation on matrix, returns matrix 
  M = [[0 for y in range(len(m[0]))]for x in range(len(m))]
  lx,ly,lk,lk2= len(m),len(m[0]),len(k),int(len(k)/2)
  for x in range(lk2,lx-lk2):
    for y in range(lk2,ly-lk2):
      if(m[x][y]>128):
        M[x][y]=255
        while(True): 
          #If any of the surrounding pixels are 0, the reference get set to zero.
          #The while causes the algorithm to break after the reference-node gets set to zero
          for a in range(lk):
            for b in range(lk):
              pos_x,pos_y = x-lk2+a,y-lk2+b
              if k[a][b]==1 and m[pos_x][pos_y]==0:
                M[x][y]=0
                break
          break
  return M

def perform_closure(m,k): 
  #Uses perform_dilation and then perform_erosion
  print("Performing closure")
  m = perform_dilation(m,k)
  m = perform_erosion(m,k)
  return m

def perform_opening(m,k):
  #Used perform_erosion and then perform_dilation
  print("Opening picture")
  m = perform_erosion(m,k)
  m = perform_dilation(m,k)
  return m

def Disc(n): #returns disc structuring element with diameter n
  c = int(n/2)
  k = [[0 for i in range(n)]for j in range(n)]
  for x in range(n):
    for y in range(n):
      if (x-c)**2 + (y-c)**2 <= c**2: k[x][y]=1
  return k

def Box(n=3): #returns box structuring element with diameter n
  return [[1 for i in range(n)]for j in range(n)]

if __name__  == "__main__":
  img = Im.open("images/noisy.tiff") 
  m = image_2_matrix(img)
  m = matrix_2_gray(m)

  m = padd_matrix(m,15) #Padds the image, as we are using big structuring elemts
  
  m = perform_opening(m,Disc(15)) #Performs opening, removing all noise
  matrix_2_image(m).save("images/noisy_opened.bmp","bmp")
  
  m = perform_closure(m,Disc(15)) #Performs closure, filling the holes

  img =  matrix_2_image(m)
  img.save("images/noisy_fix.bmp","bmp")
  


  
  
