


name = raw_input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

distrib = dict()

for line in handle:
    if not line.startswith("From "):
	continue


lst = list()
lst = distrib.items()

lst.sort()

	


for key,val in lst:
	print key, val

