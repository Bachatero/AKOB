#Write a function called censor that takes two strings, text and word, as input. It should return the text with the word you chose replaced with asterisks. 

def censor(text,word):
     sentence = list()
     sentence = text.split() 
     #print type(sentence)
     for  index, item in enumerate(sentence):
	 #print index, item 
         if item == word:
            wordlen = len(word)
	    #print sentence[index]
            sentence[index] = "*" * wordlen
            #print sentence[index]
     return " ".join(sentence)   # join elements of list into one string 


print censor("i have a vewy great fwend in rome called biggus dickus", "dickus")
