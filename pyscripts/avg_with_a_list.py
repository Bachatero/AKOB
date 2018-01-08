
listtt = list()

while True:
	getinput=raw_input("enter number:")
        if getinput=="done": break
	value=float(getinput)
	listtt.append(value)

print "average:",sum(listtt)/len(listtt)
