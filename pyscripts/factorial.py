def factorial(x):
   fact = 1
   for i in range(1,x+1):
     print i
     fact *= i
   return fact

print factorial(5)
