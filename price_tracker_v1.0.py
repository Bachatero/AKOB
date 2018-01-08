""" 

######################################
 Check price of a product 
######################################

"""

__author__ = 'Bachatero'
__date__ = '2017-08-27'


url = 'https://www.officeshoesonline.sk/products/search'
data = {'q': 'Modesto'}
#data = {'q': 'Symbol'}
price = '65,95'


def getsource(url, data): 

   import requests

   myreq = requests.post(url,data=data)
   #print(myreq.status_code)

   return myreq


def extractdata(reqdata):

   from bs4 import BeautifulSoup

   tag = ['span','price']
   soup = BeautifulSoup(reqdata.text)
   #for mydata in pagesource.find_all(tag[0]):
      #if 'price' in mydata:
      #tds = mydata.find_all(tag[1])
      #print(mydata)
   mydata = soup.find(tag[0], attrs={'class':tag[1]})

   return mydata.text


def evaluateprice(myprice):
   
   if myprice[:-3] <= price:
      print 'Price of', data.values()[0],  'has been marked down to:', myprice

   return None


def testinet():
   
   import sys

   try:

      None
      print "All good"
      #sys.exit(0)
      return True

   except IOError:

      print "Check your internet connection"
      return False
      sys.exit(1)
   
   #return sys.exit(0)


def sendsms(mymessage):

   from twilio.rest import Client
   
   account_sid = "ACf776baefc3df4321637f6ae8ce18c62b"
   auth_token = "56ecb69d6376b0ba20fd2f8ca6308332"
   
   client = Client(account_sid, auth_token)

   message = client.api.account.messages.create(to="+421917896805",
                                             from_="+19284408385",
                                             body=mymessage)
   print(message)




if __name__ == '__main__':
   ##import doctest
   ##doctest.testmod(optionflags=1068)
   testinet()
   request = getsource(url,data)   
   myprice = extractdata(request)
   evaluateprice(myprice)
   #if myprice[:-3] <= price:	
   #   print 'Price of', data.values()[0],  'has been lowered to:', myprice
   #sendsms()
