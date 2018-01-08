def is_prime(x):
  for i in range(2,abs(x)-1):
     print i
     if x % i == 0:
        return False
	break
  return True


print is_prime(-7)

	
# negative numbers are not prime
def is_prime(x):
    if x < 0:
        return False
        exit
    if x in [0,1]:
        return False
        exit
    for i in range(2,abs(x)-1):
        if x % i == 0:
            return False
            break
    return True

print is_prime(-7)
print is_prime(5)
print is_prime(11)
print is_prime(4)
print is_prime(18)
print is_prime(21)
