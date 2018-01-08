

#x =3
#if x < 2:
#	print "less than 2"
#elif x < 10:
#	print "less than 10"


str=raw_input('number')
try:
  ival = int(str)
except:
  ival = -1

if ival>0:
  print "number"
else:
  print "not_number"
