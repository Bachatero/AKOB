print int("1",2)
print int("10",2)
print int("111",2)
print int("0b100",2)
print int(bin(5),2)
# Print out the decimal equivalent of the binary 11001001.
print int("11001001",2)


#bitwise operations:

shift_right = 0b1100 # binary 12
shift_left = 0b1     # binary 1

# Your code here!
shift_right = shift_right >> 2
shift_left = shift_left << 2

print bin(shift_right)
print bin(shift_left)

#0b11    # binary 3
#0b100   # binary 4

print int("1100",2)

# convert dec into binary
print bin(1)

print bin(0b111)


#For practice, print out the result of using | on 0b1110 and 0b101 as a binary string. Try to do it on your own without using the | operator if you can help it.
print bin( 0b1110 | 0b101)
print bin((0b1110 + 0b101) - (0b1110 & 0b101))


#Operator ^:
print bin( 0b1110 ^ 0b101)
print bin((0b1110 + 0b101) - 2*(0b1110 & 0b101))




#Define a function, check_bit4, with one argument, input, an integer.
#It should check to see if the fourth bit from the right is on.
#If the bit is on, return "on" (not print!)
#If the bit is off, return "off"

print "basmeg"

def check_bit4(input):
	   print len(bin(input)) 
	   #print len(input[2:]) 
           #print bin(input)
	   mask = 0b1000 
           result  = input & mask
	   if result > 0:
		return "on"
	   else:
		return "off"
print check_bit4(0b1)
print check_bit4(0b11011)
print check_bit4(0b00010011)


# turn a bit on when it's off or leave it on when it's on
# using or bitwise operation
a = 0b10111011
mask = 0b100
answer = a | mask
print bin(answer)


#slip and slide
def flip_bit(number,n):
    mask = (0b1 << n -1)
    result = number ^ mask
    return result
flip_bit(0b111111111,4)
