# 7.2 Write a program that prompts for a file name, then opens that file 
#and reads through the file, looking for lines of the form:

#X-DSPAM-Confidence:    0.8475
#
#Count these lines and extract the floating point values from each 
#of the lines and compute the average of those values and produce an output as shown below.

#You can download the sample data at http://www.pythonlearn.com/code/mbox-short.txt when you are testing below enter mbox-short.txt as the file name.


# Use the file name mbox-short.txt as the file name

no_lines = 0
sumarum = 0
fname = raw_input("Enter file name: ")
fh = open(fname)
for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"): 
       continue
    #print line
    blank = line.find(" ")
    numero=float(line[blank:].lstrip())
    sumarum = sumarum + numero
    no_lines += 1

#print "Done"
#print no_lines
print  "Average spam confidence:", sumarum / no_lines
