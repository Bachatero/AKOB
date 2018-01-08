#!/usr/bin/env /python


"""train_status1.py: Scrapes a web page and sorts trains by their respective delay. """


__author__      = "Bachatero aka Sir Lancelot"
__copyright__ =  "What Also Floats In Water? 2014"
__credits__ = ["Stefan Urbanek aka stiivi", "Arthur, King of the Britons"]
__license__ = "All Monty Python FC Fans"

from bs4 import BeautifulSoup
from operator import itemgetter

import requests
import re
import psycopg2
import sys


DSN = 'dbname=mydebe'

if len(sys.argv) > 1:
  DSN = sys.argv[1]
  print DSN

try:
   conn = psycopg2.connect(DSN)
except:
   print "Unable to connect to database " + DSN

#print "Encoding for this connection is", conn.encoding

curs = conn.cursor()

req = requests.get("http://poloha.vlaku.sk/en")
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
     if re.search('advance',tds[6].text): #string "ma naskok"

       status_flag = -1 # is ahead of scheduled time

     #elif tds[6].find(text=re.compile('me')): #string "meska"
     elif re.search('late',tds[6].text): #string "meska"

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
 
   #curs.execute('INSERT INTO t_train_delay(train, delay, rundate) VALUES(%s,%s,%s)', (i[1],i[0],now()))
   # single insert
   curs.execute('INSERT INTO t_train_delay(train, delay, rundate) VALUES(%s,%s,current_timestamp)', (i[1],i[0],))

#cur.executemany("""INSERT INTO bar(first_name,last_name) VALUES (%(first_name)s, %(last_name)s)""", namedict)
# bulk load
curs.executemany('INSERT INTO t_train_delay(delay,train,rundate) VALUES(%s,%s,current_timestamp)', sorted_L)

# or insert list to file and use copy from file to load database table
 
conn.commit()
conn.close()
exit(0)
