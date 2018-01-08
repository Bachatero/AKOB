score = raw_input("Enter score between 0.0 and 1.0: ")
try:
	score=float(score)
	if score < 0.0 or score > 1.0:
	  print "Score is out of range, it must be between 0.0 and 1.0"
except:
	print "Entered value is not a number"
	quit()

if score <= 1.0:
  if score >= 0.9: 
	print "A"
  elif score >= 0.8:
	print "B"
  elif score >= 0.7:
	print "C"
  elif score >= 0.6:
	print "D"
  elif score < 0.6 and score >=0.0:
	print "F"

