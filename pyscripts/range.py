
print range(3)


n = [3, 5, 7]

def total(numbers):
    result = 0
    for i in range(len(numbers)):
        result += numbers[i]
    return result

print total(n)

#######################################

board=list()
for i in range(0,5):
    board.append(["O"] * 5)
    print board[i] 

board=list()
for i in range(5):
    board.append(["O"] * 5)
    #print board[i]
#print board

def print_board(board):
        for basmeg in board:
                print " ".join(basmeg)

print_board(board)

from random import randint

def random_row(board):
    return randint(0, len(board) -1)

def random_col(board):
    return randint(0, len(board) -1)

ship_row = random_row(board)
ship_col = random_col(board)

print random_row(board)
print random_col(board)

# guess ship's position on the board
guess_row = int(raw_input("Guess Row:"))
guess_col = int(raw_input("Guess Col:"))

if guess_row == ship_row and guess_col == ship_col:
    print "Congratulations! You sank my battleship"
else:
    if guess_row not in range(len(board)) or guess_col not in range(len(board)):
        print "Oops, that's not even in the ocean."
    else:
        print "You missed my battleship!"
        board[guess_row][guess_col] = "X"
        print_board(board)


if guess_row == ship_row and guess_col == ship_col:
    print "Congratulations! You sank my battleship"
elif guess_row not in range(len(board)) or guess_col not in range(len(board)):
        print "Oops, that's not even in the ocean."
elif board[guess_row][guess_col] == "X":
        print "You guessed that one already."
else:
    print "You missed my battleship!"
    board[guess_row][guess_col] = "X"
    print_board(board)
