# 7.1 Write a program that prompts for a file name, then opens that file and reads through the file, and print the contents of the file in upper case. Use the file words.txt to produce the output below.

#You can download the sample data at http://www.pythonlearn.com/code/words.txt

fname=raw_input("Enter file name:")
try:
  fh=open(fname)
except:
  print "file cannot be opened: ",fname
  exit()
for line in fh:
   print line.rstrip().upper()

