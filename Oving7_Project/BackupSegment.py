import numpy as np
from scipy import ndimage as ndi, misc
from skimage import feature,filters,io,morphology,transform
import matplotlib.pyplot as plt
from PIL import Image as Im
import os #to check if file exists
import queue
import glob
import random
COLOUMNS = 8
ROWS = 5
SEGMENT_GRADE = 2
K_VALUE = 10
EDGE_TRESHOLD = 100
BOX_W = (180,180,180) #WHITE
TRIANGLE = (160,50,100) #PURPLE
SQUARE = (100,150,80) #GREEN
BOX_B = (50,30,30) #BLACK
WEIRD = (190,170,30) #Yellow
STAR = (50,50,100) #BLUE
PACMAN = (180,40,40)#RED
COLORS = [STAR,PACMAN,WEIRD,TRIANGLE,SQUARE,BOX_B,BOX_W]
  
  
path = "images/difficult01";
img = Im.open(path+".png")
WIDTH,HEIGHT = img.size

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

def perform_erosion(m,k): 
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

def padd_color_matrix(m,n):
  #padds the matrix with n 0's in each direcetion
  M = [[(0,0,0) for y in range(len(m[0])+2*n)]for x in range(len(m)+2*n)]
  for x in range(len(m)):
    for y in range(len(m[0])):
        M[x+n][y+n] = m[x][y]
  return M

def padd_matrix(m,n=2):
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

def convert_to_255(img, color=False):
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
  part = np.asarray(img) 
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

def sick_parts(parts):
  new_parts = []
  for x in range(len(parts)):
    new_parts.append([])
    for y in range(len(parts[0])):
      img = sick_transform_canny_ich(parts[x][y])
      new_parts[x].append(img)
  save_parts(new_parts,path,"_canny") 

def segment_color_matrix(m,n,seeds,d=SEGMENT_GRADE,multiple=False): 
  M = [[None for y in range(len(m[0]))]for x in range(len(m))]
  ln,ln2= len(n),int(len(n)/2)
  q = queue.Queue()
  if multiple:
    for s in seeds:
      q.put((s,m[s[0]][s[1]]))
  else:
    q.put((seeds,m[seeds[0]][seeds[1]]))
  k = 0 
  while not q.empty():
    k+=1
    s = q.get()
    x,y = s[0]
    r,g,b = s[1]
    start_x,start_y = x-ln2,y-ln2
    for i in range(ln):
      for j in range(ln): 
        if n[i][j]==1: #if kernel
          x,y = start_x + i, start_y + j 
          if M[x][y]==None: #if not already checked
            R,G,B = m[x][y]
            check_R = (R>r-d and R<r+d)
            check_G = G>g-d and G<g+d
            check_B = (B>b-d and B<b+d)
            if check_R and check_B and check_G:
              M[x][y]=255
              p = ((x,y),(R,G,B))
              q.put(p)
            else:
              M[x][y]=0
  if k<K_VALUE:
    return segment_color_matrix(m,n,(random.randint(0,len(m)),random.randint(0,len(m[0]))),d,multiple)
  for x in range(len(M)):
    for y in range(len(M[0])):
        if M[x][y]==None:
          M[x][y]=0;
  return M

def isolate_object(part):
  part = np.asarray(part)
  #part = filters.gaussian(part,3)
  #part = convert_to_255(part)
  part = padd_color_matrix(part,2)
  part = segment_color_matrix(part,Moore(),(45,45),10)
  part = perform_closure(part,Disc(5))
  part = convert_to_255(part)
  img = Im.fromarray(np.asarray(part)).convert("L")
  return img

def isolate_objects(parts,save=True):
  new_parts = []
  for x in range(len(parts)):
    new_parts.append([])
    for y in range(len(parts[0])):
      img = isolate_object(parts[x][y])
      new_parts[x].append(img)
  if save: save_parts(new_parts,path,"_seg") 
  return new_parts

def get_spesific_files(path,spec = "canny"):
  files = glob.glob(path+"/*.png")
  cannies = [[] for x in range(COLOUMNS)]
  print(cannies)
  i = 0
  for file in files:
    arr = file.split("_")
    if len(arr)>3:
      if arr[3]==spec+".png":
        print(file)
        cannies[int(i/ROWS)].append(Im.open(file))
        i+=1
  return cannies

def scan_binary(img):
  img = np.asarray(img)
  i = 0
  for x in range(len(img)):
    for y in range(len(img[0])):
      if img[x][y]>0:
        i+=1
  return i

def create_canny_parts(path):
  create_gray_path(path) #converts to gray if it doesnt exists
  canny = misc.imread(path+"_gray.png")
  canny = feature.canny(canny,1)
  misc.imsave(path+"_canny.png",canny)
  canny = Im.open(path+"_canny.png")
  canny_parts = segregate_image(canny,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  save_parts(canny_parts,path,"_canny")
  return canny_parts

def create_gray_parts(path):
  create_gray_path(path) #converts to gray if it doesnt exists
  gray = Im.open(path+"_gray.png")
  parts_gray = segregate_image(gray,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  save_parts(parts_gray,path,"_gray")
  return parts_gray

def check_corners(m):
  print(m)
  m = np.asarray(m)
  w = len(m)
  h = len(m[0])
  points = ((10,10),(10,h-10),(w-10,10),(w-10,h-10))
  corners = 0
  for p in points:
    corners += m[p[0]][p[1]]
  return corners>2

def invert_image(img):
  m = np.asarray(img)
  lx, ly = len(m),len(m[0])
  img2 = Im.new("L",(lx,ly))
  for x in range(lx):
    for y in range(ly):
      if m[x][y]==0: img2.putpixel((y,x), 255)
  return img2

def find_object(part):
  obj = isolate_object(part)
  obj.show()
  if check_corners(obj):
    print("flipping")
    obj = np.invert(obj)
  return obj

def scan_binaries(parts,t = EDGE_TRESHOLD):
  lx,ly = len(parts),len(parts[0])
  scanned = set()
  for x in range(ly):
    for y in range(ly):
      part = parts[x][y]
      if scan_binary(part)>t:
          scanned.add((x,y))
  return scanned

def classify_touple(touple):
  R,G,B,= touple
  for t in range(0,50,5):
    for i in range(len(COLORS)):
      color = COLORS[i]
      if (color[0]>R-t and color[0]<R+t) and (color[1]>G-t and color[1]<G+t) and (color[2]>B-t and color[2]<B+t):
        return i;
  return -1
   
def remove_padding(img,n=3):
  w,h = img.size
  return img.crop((n,n,w-n,h-n))

def find_seed_from_canny(m,d=10):
  lx,ly = len(m),len(m[0])
  M = [[0 for y in range(ly)] for x in range(lx)]
  for x in range(lx):
    start_y = False
    for y in range(ly):
      if(m[x][y]>0):
        if not start_y:
          print("found x: %d %d" %(x,y))
          start_Y = y
        elif start_y:
          if y-start_y>d:
            #kprint("ending x: %d %d" %(x,y))
            mid_y = (y+start_y)/2
            M[x][mid_y]=1
          else:
            print("Not valid distance between %d %d"%(start_y,y))
            start_x=False
  print(M)
  return np.asarray(M)
         

def classify_picture(path):
  parts = segregate_image(img,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  save_parts(parts,path)
  gray_parts = create_gray_parts(path)
  canny_parts = create_canny_parts(path)
  #objects = scan_binaries(canny_parts)

  part = canny_parts[1][4] 
  #part.show()
  part = np.asarray(part)
  part = find_seed_from_canny(part)

  Im.fromarray(part).show()
  #seg_parts = isolate_objects(parts,save=True)
   



  """
  part = parts[6][1]
  part = np.asarray(part)
  print(classify_touple(part[40][40]))"""


def main():
  classify_picture(path)


  
  
"""
  #canny_parts = get_spesific_files(path,"canny")
  #print(scan_binary(canny_parts[1][1]))
  for x in range(len(canny_parts)):
    for y in range(len(canny_parts[0])):
      print("%d %d %d" %(x,y,scan_binary(canny_parts[x][y])))
"""
if __name__ == "__main__":
  main()
