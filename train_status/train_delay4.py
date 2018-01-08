from bs4 import BeautifulSoup
from operator import itemgetter

import requests
import operator
import re

def sort_table(table, col=0):
    return sorted(table, key=operator.itemgetter(col))

#url = ("poloha.vlaku.sk") 
#raw_input("Enter a website to extract the URL's from: ")

#r  = requests.get("http://" +url)
req = requests.get("http://poloha.vlaku.sk")
data = req.text

pagesource = BeautifulSoup(data)

#for link in soup.find_all('a'):
#    print(link.get('href'))

L=list()
status_flag=None

for tr in pagesource.find_all('tr')[2:]:
   tds = tr.find_all('td')
   #cislo = tr.find_all('strong')
   # print "Vlak: %s, Nazov: %s, Blabala: %s" % \
   #nazov = tds[2].find(text=True)
   train_code = tds[1].text  #train code
   train_name = tds[2].text  #train name
   #meskanie  = tds[6].find_all('strong') 
   time_minutes  = tds[6].find_all('strong') 
   if time_minutes:  # has delay or is ahead of time
     #print meskanie[0].text
     #riadok = nazov + ',' + meskanie[0].text
     #meskanie = meskanie[0].text
     time_minutes = time_minutes[0].text
     #if tds[6].find('skok'):
     ##
     #print tds[6].find_all('skok')
     #blabla=tds[6].find(text=re.compile('skok')):
     if tds[6].find(text=re.compile('skok')):
       print "ma naskok"
     #text=re.compile('kok)
       status_flag="-1"  # is ahead of time
     #meska
     elif tds[6].find(text=re.compile('me')):
     #else:
       print "meska"
       status_flag="1" # has delay
   else:
     time_minutes = "0"
     status_flag="0"
     #meskanie = "0"
     #meskanie.encode("ascii")
     #meskanie = int(meskanie[0].text)
     #riadok = '[\'' + code + '\'' + ',' + '\'' + train_name + '\'' + ',' + meskanie + '],'
     #riadok = code + ',' + train_name + ',' + meskanie 
     #riadok = meskanie +  ',' + train_name + ',' + code 
     #riadok = meskanie + ',' +  train_name + ',' + code 
   #riadok =   time_minutes.encode('ASCII') + ',' + train_code.encode('ASCII')
   riadok =   time_minutes.encode('ASCII') + ',' + train_code.encode('ASCII') + ',' + status_flag
   riadok1 = riadok.split(',')
    #L.append(meskanie[0].text)
   L.append(riadok1)
     # riadok1
     #riadok1 = str(riadok1)
     #print riadok1
     #print map(lambda x: x.encode('ascii'), riadok1)
     #L.append(meskanie)
     #L.append(nazov,int(meskanie))
#L.sort(key=int,reverse=True)
#for i in L:
#  print i
print "                BLABLA "
print "                BLABLA "
print "                BLABLA "
#  print i[0], i[1], i[2], i[3]
#L.sort(key=itemgetter(0))
#sorted_L = sorted(L,key=itemgetter(0))
##sorted_L = sorted(L, key = lambda  x: int(x[0]), reverse=True) 


#sorted_L = sorted(L, key = lambda  x: int(x[0]), reverse=True) 
sorted_L = sorted(L, key = lambda  x: (int(x[2]),int(x[0])), reverse=True) 
for i in sorted_L:
   if i[2] == "0" :
     print i[1]," on time"
   elif i[2] == "1":
     print i[1], " delay:",i[0],"min." 
   elif i[2] =="-1":
     print i[1]," ahead:",i[0],"min."
    #print i[0],  i[1]
   #print str(i)[1:-1]


#L.sort(key=lambda x: int(x[0]), reverse=True)
#for i in L:
#  print i


#   if meskanie: 
   #print meskanie[0].text
   #print meskanie
     #blala = sorted(meskanie, key=operator.itemgetter(1,2))
#`     blala = sorted(meskanie, key = lambda x : (x[0], -x[1]))
#    print tds[1].text, tds[2].text, meskanie[0].text
#   else:
#     print tds[1].text, "on time"
#     basmeg = tds[2].text + meskanie[0].text
#     basmeg = basmeg.split(',')
#     print basmeg[0]
#for td in tds 
#print tds[2]
#   print td
   #print(sorted(tds))
   #print(sorted(nazov), key=lambda basmeg: basmeg[1])
   #print nazov, meskanie


#   if meskanie: 
   #print meskanie[0].text
   #print meskanie
     #blala = sorted(meskanie, key=operator.itemgetter(1,2))
#`     blala = sorted(meskanie, key = lambda x : (x[0], -x[1]))
#    print tds[1].text, tds[2].text, meskanie[0].text
#   else:
#     print tds[1].text, "on time"
#     basmeg = tds[2].text + meskanie[0].text
#     basmeg = basmeg.split(',')
#     print basmeg[0]
#for td in tds 
#print tds[2]
#   print td
   #print(sorted(tds))
   #print(sorted(nazov), key=lambda basmeg: basmeg[1])
   #print nazov, meskanie

#   print "%s %s %s" % \
#     (tds[1].text, tds[2].text.strip(' \t\n\r'), tds[6].text)
#   print cislo[0].text
	#sorted(tds[6], key=lambda elem: elem.text)
         #  for td6 in tds[6].text :
          #    text = td6.string 
    #print "vlak:" %s" % \ 
    #(tds[0].text)
