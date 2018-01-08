#smallest_so_far = 0

int_list=[3,33,43,2,222,32,-10,55,168]
#for numero in [3,33,43,2,222,32,55,168]:
for indx, value in enumerate(int_list):
  print indx, value
  if indx == 0:
    smallest_so_far = value
  elif  value < smallest_so_far:
    smallest_so_far=value 
print "smallest number:", smallest_so_far

### OR


smallest_so_far = None

for numero in [3,33,43,2,222,32,55,168]:
  if smallest_so_far is None:
    smallest_so_far = numero
  elif numero < smallest_so_far:
    smallest_so_far = numero
  print smallest_so_far, numero

print "smallest number:", smallest_so_far


n = 5
while n > 0 :
    print n
print 'All done'
