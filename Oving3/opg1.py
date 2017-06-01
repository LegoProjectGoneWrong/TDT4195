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

def matrix_2_binary(m, t=128):
  #Creates a binary matrix of matrix, threshold default = 128
  M = copy.copy(m)
  for x in range(len(m)):
    for y in range(len(m[0])):
      if(m[x][y]>T):
        M[x][y]=255
      else:
        M[x][y]=0
  return M


def padd_matrix(m,n):
  #padds the matrix with n 0's in each direcetion
  M = [[0 for y in range(len(m[0])+2*n)]for x in range(len(m)+2*n)]
  for x in range(len(m)):
    for y in range(len(m[0])):
        M[x+n][y+n] = m[x][y]
  return M

def get_threshold(s,T=128, dT=1):
  #Finds the threshold in the set by using numpys mean function
  Tp = 0
  while(abs(T-Tp)>dT):
      m1, m2 =  np.mean([p for p in s if p>T]),np.mean([p for p in s if p<=T])
      Tp, T = T,int((m1+m2)/2)
  print("Threshold ",T)
  return T
      
def segment_matrix(m,n,T,seed): 
  #Segments the matrix with structure n from seed with treshold = T
  M = [[0 for y in range(len(m[0]))]for x in range(len(m))]
  ln,ln2= len(n),int(len(n)/2)
  print("seed: ",m[seed[0]][seed[1]])
  q = [seed]
  i = 0 
  while(i<len(q)):
    start_x,start_y = (q[i][0]-ln2),(q[i][1]-ln2)
    for a in range(ln):
      for b in range(ln): 
        if(n[a][b]==1):
          x,y = start_x + a, start_y + b 
          if(m[x][y]>T):
            M[x][y]=255
            p = (x,y)
            if p not in q: q.append(p)
    i+=1
  return M

def Neumann():
  #returns the Neumann Neighboorhood Structure
  n = [[0,1,0]
      ,[1,0,1]
      ,[0,1,0]]
  return n

def Moore():
  #returns the Moore Neighboorhod structure
  n = [[1,1,1]
      ,[1,0,1]
      ,[1,1,1]]
  return n

if __name__  == "__main__":
  img = Im.open("images/noisy.tiff")
  m = image_2_matrix(img) #creates matrix of image
  m = matrix_2_gray(m) #turns to grayscale
  

  l = matrix_2_list(m) #creates list to find the treshold
  T = get_threshold(l) #finds treshold

  m = matrix_2_binary(m,T)
  matrix_2_image(m).save("images/noisy_binary.bmp","bmp")

  m = padd_matrix(m,3) #padds the image
  seed = (200,150) #sets seed to x=200,y=150
  M = segment_matrix(m,Neumann(),T,seed) #segments the picture with Neumann structure at seed

  img2 = matrix_2_image(M)
  img2.save("images/noisy_seg.bmp","bmp")
