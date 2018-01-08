

while True:
  line = raw_input('>')
  if line == "done":
    break
  print line
print "done!"


while True:
  line = raw_input('>')
  if line[0] == "$":
    continue
  if line == "done":
    break
  print line
print "done!"


largest_so_far = -5

for numero in [3,33,43,2,222,32,55,168]:
  if numero > largest_so_far:
    largest_so_far = numero
  print largest_so_far, numero

print "largest number:", largest_so_far

###########################################################

choice = raw_input('Enjoying the course? (y/n)')

while not(choice == "y" or choice == "n"):  # Fill in the condition (before the colon)
    choice = raw_input("Sorry, I didn't catch that. Enter again: ")


###########################################################

from random import randint

# Generates a number from 1 through 10 inclusive
random_number = randint(1, 10)
print "basmeg, guess three time or you go to hell! "
guesses_left = 3
print random_number
# Start your game!
while guesses_left > 0:
    guess = int(raw_input("Your guess:"))
    if guess == random_number:
        print "You win!"
        break
    guesses_left -= 1
else:
    print "You loose."


###########################################################

word = "Marble"
for char in word:
    print char,

The example above iterates through each character in word and, in the end, prints out M a r b l e.

The , character after our print statement means that our next print statement keeps printing on the same line.

###########################################################

choices = ['pizza', 'pasta', 'salad', 'nachos']

print 'Your choices are:'
for index, item in enumerate(choices):
    print index + 1 , item

###########################################################
#Multiple lists

#It's also common to need to iterate over two lists at once. This is where the built-in zip function comes in handy.

#zip will create pairs of elements when passed two lists, and will stop at the end of the shorter list.

#zip can handle three or more lists as well!


st_a = [3, 9, 17, 15, 19]
list_b = [2, 4, 8, 10, 30, 40, 50, 60, 70, 80, 90]

for a, b in zip(list_a, list_b):
    # Add your code here!
    if a > b: 
        print a
    else:
        print b
    

###########################################################
#Multiple lists


