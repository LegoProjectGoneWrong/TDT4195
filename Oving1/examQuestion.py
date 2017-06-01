def trans(H,F):
  D = []
  for i in range(1,6):
    D.append([])
    for j in range(1,6):
      D[i-1].append([0])
      for a in range(0,3):
        for b in range(0,3):
          value = H[i-1+a][j-i+b]*F[a][b]
          print(value)
  return D
        

H = [[0,0,0,0,0,0,0]
  ,[0,0,0,2,2,6,0]
  ,[0,0,1,1,4,6,0]
  ,[0,3,3,7,2,5,0]
  ,[0,0,0,0,0,0,0]]

F= [[-1,-1,-1]
  ,[-1,8,-1]
  ,[-1,-1,-1]]

T = trans(H,F)
for i in T:
  print(i)
