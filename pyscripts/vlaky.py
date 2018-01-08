from bs4 import BeautifulSoup

import requests

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
#    print(sorted(tds[1]), key=lambda x: x[1])
   print "%s %s %s" % \
     (tds[1].text, tds[2].text.strip(' \t\n\r'), tds[6].text)
#   print cislo[0].text
	#sorted(tds[6], key=lambda elem: elem.text)
         #  for td6 in tds[6].text :
          #    text = td6.string 
    #print "vlak:" %s" % \ 
    #(tds[0].text)
