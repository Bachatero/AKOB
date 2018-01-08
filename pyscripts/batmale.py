#!/usr/bin/env python


def c2f(c):
   "converts centigrade to farenheit"
   return 32 + (9/5)*c


FILE = 'mydata01.txt'

fd = open(FILE,'r')

for LINE in fd:
    LINE = LINE.strip()
    #print(LINE)
    mylist = LINE.split(':')
    print(mylist)

#print(mylist)

#for LINE in fd:
for LINE in open(FILE,'r'):
    name, profession, status, country = LINE.split(":")
    lastname, firstname = name.split(", ")
    print( firstname, lastname, 'is or was a ', profession, ' from ', country) 


print c2f(30) 
