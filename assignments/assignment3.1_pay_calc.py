reg_wrk_hrs = 40
hrs = raw_input("Enter Hours:")
hrs = float(hrs)
rate = float(raw_input("Enter Rate per Hour:"))


if hrs <= reg_wrk_hrs:
	print "Pay:",hrs * rate
else:
	print "Pay incl. overtime:", reg_wrk_hrs * rate + (hrs-reg_wrk_hrs) *rate * 1.5


exit()
