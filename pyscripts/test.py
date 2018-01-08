basmeg=list() 
strng="1, djdj jdjj, kkkk k k"
print strng.split(',') 
for i in range(0,10):
  print i
  basmeg.append(strng)
  print basmeg

sorted_L = sorted(basmeg, key = lambda  x: int(x[0]))
for i in sorted_L:
  print i
