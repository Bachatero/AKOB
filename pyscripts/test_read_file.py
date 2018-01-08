
#fname=raw_input("Enter file name:")
#fhandle=open(fname)

fhandle=open("test.txt","r")
inputdata = fhandle.read()

print len(inputdata)

print inputdata[:7]

print ""
print "2nd part\n"

fhandle=open("test.txt","r")
for line in fhandle:
   line = line.rstrip()
   if line.startswith("d"):
      print line
print ""
print "3d part\n"

fhandle=open("test.txt","r")
for line in fhandle:
   line = line.rstrip()
   if line.startswith("d"):
      continue
   print "not d lines"



print ""
print "4th part\n"

fhandle=open("test.txt","r")
for line in fhandle:
   line = line.rstrip()
   if not "@" in line:
      continue
   print " @ in line"
   print line
   print "yada yada"


print ""
print "5th part\n"

fname=raw_input("Enter file name:")
try:
  fhandle=open(fname)
except:
  print "file cannot be opened: ",fname
  exit()
for line in fhandle:
   line = line.rstrip()
   if not "@" in line:
      continue
   print " @ in line"
   print line
   print "yada yada"


print ""
print "6th part\n"

fname=raw_input("Enter file name:")
try:
  fh=open(fname)
except:
  print "file cannot be opened: ",fname
  exit()
for line in fh:
   print line.upper()



