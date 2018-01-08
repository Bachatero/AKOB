largest = None
smallest = None
while True:
    try:
      numb = raw_input("Enter a number: ")
      if numb == "done" :
        break
      num = int(numb)
      if smallest is None:
        smallest = num
        print "s1 ",smallest
      elif num < smallest:
        smallest = num 	
        print "s2 ", smallest
      elif largest is None:
        largest = num
        print "p1 ",largest
      elif num > largest:
        largest = num
        print "p2 ",largest
      #print num
    except:
      print "Invalid input"
print "Maximum", largest
print "Minimum", smallest
