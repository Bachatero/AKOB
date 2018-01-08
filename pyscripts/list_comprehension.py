# generate list of all even numbers from 0 to 50
evens_to_50 = [i for i in range(51) if i % 2 == 0]
print evens_to_50

doubles_by_3 = [x*2 for x in range(1,6) if (x*2) % 3 == 0]

# Complete the following line. Use the line above for help.

#Use a list comprehension to build a list called even_squares in the editor.
#Your even_squares list should include the squares of the even numbers between 1 to 11. Your list should start [4, 16, 36...] and go from there.

even_squares = [i**2 for i in range(1,12) if i**2%2 == 0 ]
print even_squares

#The comprehension should consist of the cubes of the numbers 1 through 10 only if the cube is evenly divisible by four.
cubes_by_four =[i**3 for i in range(1,11) if i**3%4 == 0 ]
print cubes_by_four
