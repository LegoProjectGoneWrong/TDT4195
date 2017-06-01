import numpy as np
from scipy import ndimage as ndi, misc
from skimage import feature,filters,io,morphology,transform
import matplotlib.pyplot as plt
from PIL import Image as Im
import os #to check if file exists

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

def save_parts(parts,filepath,ending=""):
  print("Saving")
  for x in range(len(parts)):
      for y in range(len(parts[0])):
        name = filepath+"/Slot_"+str(x)+"_"+str(y)+ending+".png"
        parts[x][y].save(name,"png")

def segregate_image(img,n_x,n_y,w,h,o=0):
    pix_x = w/n_x
    pix_y = h/n_y
    parts = []
    for x in range(n_x):
      parts.append([])
      for y in range(n_y):
        part = img.crop((x*pix_x+o,y*pix_y+o,(x+1)*pix_x-o,(y+1)*pix_y-o));
        parts[x].append(part)
    return parts;
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

def padd_matrix(m,n):
  #padds the matrix with n 0's in each direcetion
  M = [[0 for y in range(len(m[0])+2*n)]for x in range(len(m)+2*n)]
  for x in range(len(m)):
    for y in range(len(m[0])):
        M[x+n][y+n] = m[x][y]
  return M
        
def segment_matrix(m,n,seed): 
  #Segments the matrix with structure n from seed with treshold = T
  T = m[seed[0]][seed[1]]
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
          if(T-10<m[x][y]<T+10):
            M[x][y]=255
            p = (x,y)
            if p not in q: q.append(p)
    i+=1
  return M

def segment_matrix_color(m,n,seed): 
  #Segments the matrix with structure n from seed with treshold = T
  s = m[seed[0]][seed[1]]
  M = [[False for y in range(len(m[0]))]for x in range(len(m))]
  ln,ln2= len(n),int(len(n)/2)
  print("seed: ",m[seed[0]][seed[1]])
  q = Qeue.queue()
  q.put(s)
  i = 0 
  while(i<len(q)):
    s = q.pop()
    start_x,start_y = (q[i][0]-ln2),(q[i][1]-ln2)
    for a in range(ln):
      for b in range(ln): 
        if(n[a][b]==1):
          x,y = start_x + a, start_y + b 
          cR = R
          if(T-10<m[x][y]<T+10):
            M[x][y]=255
            p = (x,y)
            if p not in q: q.append(p)
    i+=1
  return M

def create_gray_path(path):
  if not os.path.isfile(path+"_gray.png"):
    print("Creating gray")
    img = Im.open(path+".png")
    image_2_gray(img).save(path+"_gray.png","png")
  else:
    print("gray exists")

def normalize(img):
  max_p= 0
  min_p=255
  for x in range(len(img)):
    for y in range(len(img[0])):
      p = img[x][y]
      if p>max_p: max_p=p
      if p<min_p: min_p=p
  print("min: %d, max: %d" %(min_p,max_p))
  diff = max_p - min_p
  for x in range(len(img)):
    for y in range(len(img[0])):
      img[x][y]=(img[x][y]-min_p)/diff
  return img

def convert_to_255(img):
  for x in range(len(img)):
    for y in range(len(img[0])):
      img[x][y]=img[x][y]*255.0
  return img

def get_treshold(s,T=128, dT=1): #returns treshold with global treshold alhorithm
  Tp = 0
  while(abs(T-Tp)>dT):
      m1, m2 =  np.mean([p for p in s if p>T]),np.mean([p for p in s if p<=T])
      Tp, T = T,int((m1+m2)/2)
  print("Treshold ",T)
  return T      

def make_binary(data,T=128):
  m = []
  for x in range(len(data)):
    m.append([])
    for y in range(len(data[0])):
      if data[x][y]>=T:
        m[x].append(255)
      else:
        m[x].append(0)
  return m

def sick_transform_canny_ich(img):
  part = image_2_matrix(img) 
  part = normalize(part)
  #c = feature.canny(part) need dtype attribute

  #part = convert_to_255(part)
  part = filters.gaussian(np.asarray(part),5)
  #part = morphology.erosion(part)
  edges = filters.sobel(part)
  #edges = convert_to_255(edges)
  T = filters.threshold_otsu(edges)
  binary = make_binary(edges,T)
  img = np.asarray(binary)
  img = convert_to_255(img)
  return Im.fromarray(img)



def main():
  path = "images/easy02"
  create_gray_path(path)
  img = Im.open(path+"_gray.png")
  w,h = img.size
  parts = segregate_image(img,8,5,w,h,5)
  save_parts(parts,path,"_gray")



  new_parts = []
  for x in range(len(parts)):
    new_parts.append([])
    for y in range(len(parts[0])):
      part =sick_transform_canny_ich(parts[x][y])
      new_parts[x].append(part)
  new_parts[7][3].show()
  save_parts(new_parts,path,"_sick")




  #h,theta,d = transform.hough_line(binary)
  #segment = segment_matrix(part,kernel,(50,50))
  #matrix_2_image(segment).show()
if __name__ == "__main__":
  main()
