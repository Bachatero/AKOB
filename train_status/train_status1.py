#!/usr/bin/env /python


"""train_status1.py: Scrapes a web page and sorts trains by their delay. """


__author__      = "Bachatero aka Sir Lancelot"
__copyright__ =  "What Also Floats In Water? 2014"
__credits__ = ["Stefan Urbanek aka stiivi", "Arthur, King of the Britons"]
__license__ = "All Monty Python FC Fans"

from bs4 import BeautifulSoup
from operator import itemgetter

import requests
import re

req = requests.get("http://poloha.vlaku.sk")
data = req.text

pagesource = BeautifulSoup(data)

tuple_riadok=()
ListOfTuples=list()
status_flag=None
time_minutes=0

for tr in pagesource.find_all('tr')[2:]:
   tds = tr.find_all('td')
   # print "Vlak: %s, Nazov: %s, Blabala: %s" % \
   train_code = tds[1].text  #train code
   train_name = tds[2].text  #train name
   time_minutes  = tds[6].find_all('strong') #minutes of delay or minutes ahead of scheduled time
   if time_minutes:  # has delay or is ahead of time

     time_minutes = int(time_minutes[0].text)

     #if tds[6].find(text=re.compile('skok')): #string "ma naskok"
     if re.search('skok',tds[6].text): #string "ma naskok"

       status_flag = -1 # is ahead of scheduled time

     #elif tds[6].find(text=re.compile('me')): #string "meska"
     elif re.search('me',tds[6].text): #string "meska"

       status_flag = 1 # has delay

   else: # on time
     time_minutes = 0
     status_flag = 0

   time_minutes = time_minutes * status_flag
   tuple_riadok =   time_minutes,train_code
   ListOfTuples.append(tuple_riadok)

sorted_L = sorted(ListOfTuples,key=itemgetter(0),reverse=True)
for i in sorted_L: 
   if i[0] == 0 :
     print i[1]," on time"
   elif i[0] > 0:
     print i[1], " delay:",i[0],"min." 
   elif i[0] < 0:
     print i[1]," ahead:",abs(i[0]),"min."
 
exit(0)
