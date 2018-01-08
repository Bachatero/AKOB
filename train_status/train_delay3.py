from bs4 import BeautifulSoup
from operator import itemgetter

import requests
import operator

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

for tr in pagesource.find_all('tr')[2:]:
   tds = tr.find_all('td')
   #cislo = tr.find_all('strong')
   # print "Vlak: %s, Nazov: %s, Blabala: %s" % \
   #nazov = tds[2].find(text=True)
   code = tds[1].text
   train_name = tds[2].text
   meskanie  = tds[6].find_all('strong') 
   if meskanie: 
     #print meskanie[0].text
     #riadok = nazov + ',' + meskanie[0].text
     meskanie = meskanie[0].text
   else:
     meskanie = "0"
     #meskanie.encode("ascii")
     #meskanie = int(meskanie[0].text)
     #riadok = '[\'' + code + '\'' + ',' + '\'' + train_name + '\'' + ',' + meskanie + '],'
     #riadok = code + ',' + train_name + ',' + meskanie 
     #riadok = meskanie +  ',' + train_name + ',' + code 
     #riadok = meskanie + ',' +  train_name + ',' + code 
   riadok =   meskanie.encode('ASCII') + ',' + code.encode('ASCII')
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
sorted_L = sorted(L, key = lambda  x: int(x[0]), reverse=True) 
for i in sorted_L:
   if int(i[0]) == 0 :
     print i[1]," on time"
   else:
     print i[1], " delay:",i[0],"min." 
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
