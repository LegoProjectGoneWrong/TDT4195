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

def image_2_gray(img):
  return matrix_2_image(matrix_2_gray(image_2_matrix(img)))

def image_2_list(img):
  return [img.getpixel((x,y)) for y in range (img.size[1]) for x in range(img.size[0])]

def matrix_2_list(m):
  return [m[x][y] for y in range(len(m[0])) for x in range(len(m))]

def matrix_2_binary(m): #returns a binary matrix, (0 or 255)
  M=copy.copy(m)
  for x in range(len(m)):
    for y in range(len(m[0])):
      if(m[x][y]>128):
        M[x][y]=255
      else:
        M[x][y]=0
  return M


def padd_matrix(m,n): #padds the matrixs with n 0's in each direction
  M = [[0 for y in range(len(m[0])+2*n)]for x in range(len(m)+2*n)]
  for x in range(len(m)):
    for y in range(len(m[0])):
        M[x+n][y+n] = m[x][y]
  return M
        

def get_treshold(s,T=128, dT=1): #returns treshold with global treshold alhorithm
  Tp = 0
  while(abs(T-Tp)>dT):
      m1, m2 =  np.mean([p for p in s if p>T]),np.mean([p for p in s if p<=T])
      Tp, T = T,int((m1+m2)/2)
  print("Treshold ",T)
  return T      

def perform_erosion2(m,k,i): #Applies kernel through dilation on matrix, returns matrix 
  M = copy.copy(m)
  lx,ly,lk,lk2= len(M),len(M[0]),len(k),int(len(k)/2)
  for x in range(lk2,lx-lk2):
    for y in range(lk2,ly-lk2):
      if(m[x][y]==255):
        #Cheks wheter the reference pixel is still high
        while(True): 
          #If any of the surrounding pixels are 0, the reference get set to zero.
          for a in range(lk):
            for b in range(lk):
              pos_x,pos_y = x-lk2+a,y-lk2+b
              if k[a][b]==1 and m[pos_x][pos_y]<i:
                #sets the pixel to the current iteration if its supposed to be 0
                M[x][y]=i 
                break
          break
  return M

def still_pixels(m): #returns true if there are any pixels above 200
  for l in m:
    for p in l:
      if(p>200):
        return True
  return False

def distance_transform(m,k): #applies distance transofmraton
  M= copy.copy(m)
  i=0
  while(still_pixels(M)): #Applies transformation till all pixels are belove gone
    i+=1
    print("Performing erosion: ",i)
    M = perform_erosion2(M,k,i)
   
  value = 255/i #scales the pixels
  for x in range(len(M)):
    for y in range(len(M[0])):
      M[x][y]=M[x][y]*value
  return M

def Disc(n=3): #returns disc structuring element with diameter n
  c = int(n/2)
  k = [[0 for i in range(n)]for j in range(n)]
  for x in range(n):
    for y in range(n):
      if (x-c)**2 + (y-c)**2 <= c**2: k[x][y]=1
  return k
def Box(n=3): #returns box structuring element with diameter n
  return [[1 for i in range(n)]for j in range(n)]

if __name__  == "__main__":
  img = Im.open("images/noisy_fix.bmp") 
  m = image_2_matrix(img)
  m = matrix_2_gray(m)
  m = matrix_2_binary(m)
  
  m = distance_transform(m,Box())

  img =  matrix_2_image(m)
  img.save("images/noisy_distance_box.bmp","bmp")
  


  
 
