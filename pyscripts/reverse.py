def reverse(text):
   rtext = ""
   strln = len(text)
   #print strln
   for i in range(1,len(text) + 1):
      rtext = rtext + text[strln - i]  
      #print rtext
   return rtext
   #print rtext

print reverse("basmeg")
