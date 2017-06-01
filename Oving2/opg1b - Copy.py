from PIL import Image as Im
import numpy as np
import math
import matplotlib.pyplot as plt



def image_2_matrix(img):
  m = [[img.getpixel((x,y)) for y in range(img.size[1])] for x in range(img.size[0])]
  return m

def matrix_2_image(m,mode="L"):
  print(m[10][10])
  lx, ly = len(m),len(m[0])
  img = Im.new(mode,(lx,ly))
  for x in range(lx):
    for y in range(ly):
      img.putpixel((x,y), int(m[x][y]))
  return img

def matrix_2_gray(m):
  xl,yl = len(m),len(m[0])
  return [[int(np.mean(m[x][y])) for y in range(yl)] for x in range(xl)]

def padd_matrix(m):
  print(m[0][0])
  xl,yl = len(m),len(m[0])
  hxl,hyl = int(xl/2),int(yl/2)
  M = [[0 for x in range(2*xl)]for y in range(2*yl)]
  print(M[0][0])
  for x in range(xl):
    for y in range(yl):
      M[x+hyl][y+hyl]=m[x][y]
  print(M[hxl][hyl])
  return M

def remove_padding(m):
  xl,yl = int(len(m)/2),int(len(m[0])/2)
  hxl,hyl = int(xl/2),int(yl/2)
  M = []
  for x in range(xl):
    M.append([])
    for y in range(yl):
      M[x].append(m[x+hxl][y+hyl])
  return M


def padd_kernel(m,k):
  kl = len(k)
  xl,yl=len(m),len(m[0])
  print(xl," ",yl)
  K = [[0 for y in range(yl)]for x in range(xl)]

  for x in range(kl):
    for y in range(kl):
      K[x][y] = k[x][y]
  print(len(K))
  return K


def create_kernel(nxn,q=1):
  k = []
  e = math.e
  c = int(nxn/2)
  q2 = math.pow(q,2)
  s = 0
  for u in range(nxn):
    k.append([])
    for v in range(nxn):
      exp = (math.pow(u-c,2) + math.pow(v-c,2))/(2*q2)
      value = 1/((2*math.pi)*q2*math.pow(e,exp))
      k[u].append(value)
      s += value
  print(s)
  K = [[(k[x][y]/s) for y in range(len(k))] for x in range(len(k))]
  return K

def kernel_highpass():
  k = [[-1,-1,-1]
      ,[-1,9,-1]
      ,[-1,-1,-1]]
  return k

def kernel_lowpass(n=3):
  return [[1/(n**2) for i in range(n)]for j in range(n)]


def add_matrixes(m,n):
  M=[]
  for x in range(len(m)):
    M.append([])
    for y in range(len(m[0])):
        M[x].append(m[x][y]+n[x][y])
  return M


def FFT(m):
  return np.fft.fft2(m)

def IFFT(m):
  return np.fft.ifft2(m)

def pointwise_multiplication(m,k):
  mxl, myl = len(m),len(m[0])
  kxl, kyl = len(k),len(k[0])
  print(mxl,myl,kxl,kyl)
  if(mxl!=kxl or myl!=kyl):
    return false

  M = []
  for x in range(mxl):
    M.append([])
    for y in range(myl):
      M[x].append(m[x][y]*k[x][y])

  return M
  

if __name__ == "__main__":
 
  img = Im.open("bricks.tiff")
  m1 = image_2_matrix(img)

  img = Im.open("Bush.tiff")


  m_gray = matrix_2_gray(m)
  grayImg = matrix_2_image(m_gray)
  grayImg.save("jelly_grey.bmp","bmp")

  m_padded = padd_matrix(m_gray)
  k1 = kernel_laplacian()
  k1_padded = padd_kernel(m_padded,k1)

  m_fft = FFT(m_padded)
  k1_fft = FFT(k1_padded)

  G1=pointwise_multiplication(m_fft,k1_fft)
  g1 = IFFT(G1)
  gAdded = add_matrixes(m_padded,g1)
  g1_unpadded = remove_padding(gAdded)
  Img1 = matrix_2_image(g1_unpadded)
  Img1.save("jelly_laplacian.bmp","bmp")





  

