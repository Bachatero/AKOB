# Write a program to read through the mbox-short.txt and figure out who has the sent the greatest number of mail messages. The program looks for 'From ' lines and takes the second word of those lines as the person who sent the mail. The program creates a Python dictionary that maps the sender's mail address to a count of the number of times they appear in the file. After the dictionary is produced, the program reads through the dictionary using a maximum loop to find the most prolific committer.

name = raw_input("Enter file:")
if len(name) < 1 : 
   name = "mbox-short.txt"
handle = open(name)

heavy_sender=dict()
prolific_addresser=None
big_mailcount=None

for line in handle:
    if not line.startswith("From "):
	continue 
    line=line.split()
    #print line[1]
    heavy_sender[line[1]] = heavy_sender.get(line[1],0) + 1
    #print  heavy_sender[line[1]]
    print  heavy_sender.items()
    print  heavy_sender

#for address,count in heavy_sender.items():
#    if big_mailcount is None or count > big_mailcount:
#	big_mailcount=count 
#	prolific_addresser=address

#print prolific_addresser, big_mailcount
    

