import numpy as np
from scipy import ndimage as ndi, misc
from skimage import feature,filters,io,morphology,transform,exposure, draw
import matplotlib.pyplot as plt
from PIL import Image as Im
import os #to check if file exists
import queue
import glob
import random
COLOUMNS = 8
ROWS = 5
path = "images/easy01"
img = Im.open(path+".png")
WIDTH,HEIGHT = img.size

SEGMENT_GRADE = 2 #span for segmentation
K_VALUE = 30
EDGE_TRESHOLD = 40
SCAN_DISTANCE = 5 #for eroding binary
CENTRE_DISTANCE = 20
ANALYZE_SAMPLES = 20 #check color of this many pixels


STAR = (80,80,130) #BLUE 0
PACMAN = (180,40,40)#RED  1
WEIRD = (190,170,30) #Yellow  2
TRIANGLE = (160,50,100) #PURPLE 3
SQUARE = (100,150,80) #GREEN    4
BOX_B = (50,30,30) #BLACK 5
BOX_W = (200,200,200) #WHITE  6

COLORS = [STAR,PACMAN,WEIRD,TRIANGLE,SQUARE,BOX_B,BOX_W]
  
  

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

def save_parts_from_lists(parts,indexes,filepath,ending=""):
  print("Saving")
  for i in range(len(parts)):
        x,y = indexes[i]
        name = filepath+"/Slot_"+str(x)+"_"+str(y)+ending+".png"
        parts[i].save(name,"png")

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

def scan_binary(img, d = SCAN_DISTANCE):
  img = np.asarray(img)
  i = 0
  for x in range(d,len(img)-d):
    for y in range(d,len(img[0])-d):
      if img[x][y]>0:
        i+=1
  return i

def create_canny_parts(path,save=True):
  create_gray_path(path) #converts to gray if it doesnt exists
  canny = misc.imread(path+"_gray.png")
  canny = feature.canny(canny,1)
  misc.imsave(path+"_canny.png",canny)
  canny = Im.open(path+"_canny.png")
  canny_parts = segregate_image(canny,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  if save: save_parts(canny_parts,path,"_canny")
  return canny_parts

def create_gray_parts(path,save = True):
  create_gray_path(path) #converts to gray if it doesnt exists
  gray = Im.open(path+"_gray.png")
  parts_gray = segregate_image(gray,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  if save: save_parts(parts_gray,path,"_gray")
  return parts_gray

def check_corners(m,d=7):
  m = np.asarray(m)
  w = len(m)
  h = len(m[0])
  points = ((d,d),(d,h-d),(w-d,d),(w-d,h-d))
  corners = 0
  for p in points:
    corners += m[p[0]][p[1]]
  return corners>2

def invert_matrix(m):
  lx, ly = len(m),len(m[0])
  img2 = Im.new("L",(lx,ly))
  for x in range(lx):
    for y in range(ly):
      if m[x][y]<1: img2.putpixel((y,x), 255)
      else: img2.putpixel((y,x),0)
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
  print("%d %d"%(lx,ly))
  scanned = []
  for x in range(lx):
    for y in range(ly):
      part = parts[x][y]
      if scan_binary(part)>t:
          scanned.append((x,y))
          print("Sucsess: %d %d"%(x,y))
  return scanned

def classify_tuple(touple):
  R,G,B,= touple
  for t in range(5,50,5):
    for i in range(len(COLORS)):
      color = COLORS[i]
      if (color[0]>R-t and color[0]<R+t) and (color[1]>G-t and color[1]<G+t) and (color[2]>B-t and color[2]<B+t):
        return i;
  return -1
   
def remove_padding(img,n=3):
  w,h = img.size
  return img.crop((n,n,w-n,h-n))

def isolate_object(part,centres=None):
  w,h = part.size
  if centres:
    seeds = get_seeds(centres)

    
  #part = exposure.adjust_sigmoid(part) #contrast
  part = np.asarray(part)
  #part = filters.gaussian(part,3)
  #part = normalize(part)
  part = padd_color_matrix(part,2)
  print("Segmenting")
  part_seg = segment_color_matrix(part,Moore(),seeds.pop(),10)
  attempts = 0
  while(check_corners(part_seg) and seeds and attempts <5):
    attempts+=1
    #part = invert_matrix(part)
    #part = Im.fromarray(np.asarray(part))
    part_seg = segment_color_matrix(part,Moore(),seeds.pop(),10)
  else:
    part = Im.fromarray(np.asarray(part_seg))
  part = remove_padding(part)
  part = perform_closure(np.asarray(part),Disc(5))
  part = convert_to_255(part)
  img = Im.fromarray(np.asarray(part)).convert("L")
  img = img.resize((w,h))
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

def find_centre_from_canny(m,d=CENTRE_DISTANCE):
  lx,ly = len(m),len(m[0])
  M = [[0 for y in range(ly)] for x in range(lx)]
  for x in range(lx):
    start_y = 0
    last_y=0
    for y in range(ly):
      if(m[x][y]>0):
        if start_y==0:
          start_y = y
        else:
          if y-start_y>d:
            last_y=y
            mid_y = int((y+start_y)/2)
            M[x][mid_y]=255
            start_y=0
          elif y-last_y>d:
            start_y=y
          else:
            start_y=0
  for y in range(ly):
    start_x = 0
    for x in range(lx):
      if(m[x][y]>0):
        if start_x==0:
          start_x = x
        else:
          if x-start_x>d:
            mid_x = int((x+start_x)/2)
            M[mid_x][y]=255
            start_x=0
          else:
            start_x=x
  return np.asarray(M)
 
def create_centre_from_canny_parts(parts,path,save=True):
  lx, ly = len(parts),len(parts[0])
  centres = []
  for x in range(lx):
    centres.append([])
    for y in range(ly):
      #parts[x][y].show()
      centre = find_centre_from_canny(np.asarray(parts[x][y]))
      centre = convert_to_255(centre)
      centre = Im.fromarray(centre)
      #centre.show()
      centres[x].append(centre)
  if save: save_parts(centres,path,"_centre")
  return centres

def find_center(m):
  sum_x = 0; sum_y=0; num=0;
  len_x,len_y = len(m),len(m[0])
  for x in range(len_x):
    for y in range(len_y):
      if m[x][y]>0:
        sum_x+=x
        sum_y+=y
        num+=1
  img = np.zeros((len_x,len_y))
  c_x = int(sum_x/num)
  c_y = int(sum_y/num)
  rr,cc = draw.circle(c_x,c_y,5)
  img[rr,cc]=1
  img = convert_to_255(img)
  return c_x,c_y,Im.fromarray(img).convert("RGB")

def get_seeds(m):
  seeds = set([])
  m = np.asarray(m)
  lx,ly = len(m),len(m[0])
  for x in range(lx):
    for y in range(ly):
      if m[y][x]>0:
        seeds.add((x,y))
  return seeds

def blend_images(im1,im2):
  if im1.size!=im2.size:
    print("Wrong size")
    return False
  w,h = im1.size
  im = np.zeros((w,h))
  for x in range(w):
    for y in range(h):
      if im1.getpixel((y,x))[0]>0 or im2.getpixel((y,x))>0:
        im[x][y]=255
  return Im.fromarray(im).convert("LA")

def analyze_segmentation(part,seg):
  seg = np.asarray(seg)
  #seg = perform_erosion(seg,Disc(3))
  seeds = get_seeds(seg)
  options = []
  for i in range(ANALYZE_SAMPLES):
    if seeds:
      x,y = seeds.pop()
      color = part.getpixel((x,y))
      print(color)
      option = classify_tuple(color)
      if option>=0:
        options.append(option)
  if options:
    print(options)
    return np.bincount(options).argmax()
  
  return -1



def classify_picture(path):
  parts = segregate_image(img,COLOUMNS,ROWS,WIDTH,HEIGHT,5)
  save_parts(parts,path)
  gray_parts = create_gray_parts(path,save=False)
  canny_parts = create_canny_parts(path,save=False)
  centre_parts = create_centre_from_canny_parts(canny_parts,path,save=False);
  scans = scan_binaries(canny_parts)
  scans = [(4,0)]
  parts_scanned = []
  isolated_scanned = []
  centre_scanned = []
  canny_scanned = []
  centers = []
  center_c = []
  types = []
  output = []
  for scan in scans:
    x,y = scan
    parts_scanned.append(parts[x][y])
    centre_scanned.append(centre_parts[x][y])
    canny_scanned.append(canny_parts[x][y])
    isolated = isolate_object(parts[x][y],centre_parts[x][y])
    isolated_scanned.append(isolated)
    c_x,c_y,center = find_center(np.asarray(isolated))
    blended = blend_images(center,canny_parts[x][y])
    centers.append(blended)
    center_c.append((c_x,c_y))
    color_type = analyze_segmentation(parts[x][y],isolated)
    string = "%d %d %d\n"%(color_type,x,ROWS-1-y)
    output.append(string)
    parts[x][y].show()
    
  object_file = open("Objects.txt","w")
  for line in output:
    object_file.writelines(line)
  object_file.close()

  save_parts_from_lists(isolated_scanned,scans,path,"_seg")
  save_parts_from_lists(centre_scanned,scans,path,"_centre")
  save_parts_from_lists(canny_scanned,scans,path,"_canny")
  save_parts_from_lists(parts_scanned,scans,path)
  save_parts_from_lists(centers,scans,path,"_points")
   





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
