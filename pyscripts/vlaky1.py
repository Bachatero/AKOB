from bs4 import BeautifulSoup

import requests
import operator

#url = ("poloha.vlaku.sk") 
#raw_input("Enter a website to extract the URL's from: ")

#r  = requests.get("http://" +url)
req = requests.get("http://poloha.vlaku.sk")
data = req.text

pagesource = BeautifulSoup(data)

#for link in soup.find_all('a'):
#    print(link.get('href'))

for tr in pagesource.find_all('tr')[2:]:
   tds = tr.find_all('td')
   #cislo = tr.find_all('strong')
   # print "Vlak: %s, Nazov: %s, Blabala: %s" % \
   #nazov = tds[2].find(text=True)
   #nazov = tds[2].text
   meskanie  = tds[6].find_all('strong') 
   if meskanie: 
   #print meskanie[0].text
   #print meskanie
     print tds[1].text, tds[2].text, meskanie[0].text
   else:
     print tds[1].text, "on time"
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
