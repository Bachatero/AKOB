
import re

name = raw_input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

#x='jjjs jjjjs jjj@hshsh.sk jsjsj kakk@akkk.com kkkkw'
#x='From ray@media.berkeley.edu Thu Jan  3 17:07:00 2008'
x='From ray@media.berkeley.edu Thu Jan  3 17:07:00 2008 From bbb@bbb.com ikkk'
y = re.findall('\S+@\S+',x)
print y


y = re.findall('^From (\S+@\S+)',x)   # matching longer string, extracting a smaller part of it
print y


y = re.findall('@([^ ]+)',x)    # [^ ] ... match any non-blank character(single character), given the plus sign, one or many non-blank characters are matched.  do not want the at sign, I want to extract the characters after the at sign (within the parantheses "()")

[^ ] ... caret inside square brackets means NOT, in this case it means "not a blank character"

print y

y = re.findall('@([\S]+)',x)    # does the same thing
print y


y = re.findall('^From .*@([^ ]+)',x)    
print y


numlist=list()

for line in handle:
   line=line.rstrip()
   stuff=re.findall('X-DSPAM-Confidence: ([0-9.]+)',line)
   if len(stuff) == 0:
       continue
   num=float(stuff[0])
   numlist.append(num)

print "maximum:", max(numlist)
