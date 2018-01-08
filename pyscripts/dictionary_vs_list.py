residents = {'Puffin' : 104, 'Sloth' : 105, 'Burmese Python' : 106}

print residents['Puffin'] # Prints Puffin's room number

# Your code here!
print residents['Sloth']
#print residents['Sloth','Burmese Python']
print dir(residents)


#dictionary {}
backpack = {'xylophone':1, 'dagger':2, 'tent':3, 'bread loaf':4}
del backpack["dagger"] # remove item from a dictionary
print backpack


#dictionary vs list []
backpack = ['xylophone', 'dagger', 'tent', 'bread loaf']
backpack.remove("dagger") # remove item from a list


#######################################################################    
#    Add a key to inventory called 'pocket'
#    Set the value of 'pocket' to be a list consisting of the strings 'seashell', 'strange berry', and 'lint'
#    .sort() the items in the list stored under the 'backpack' key
#    Then .remove('dagger') from the list of items stored under the 'backpack' key
#    Add 50 to the number stored under the 'gold' key



inventory = {
    'gold' : 500,
    'pouch' : ['flint', 'twine', 'gemstone'], # Assigned a new list to 'pouch' key
    'backpack' : ['xylophone','dagger', 'bedroll','bread loaf']
}

# Adding a key 'burlap bag' and assigning a list to it
inventory['burlap bag'] = ['apple', 'small ruby', 'three-toed sloth']

# Sorting the list found under the key 'pouch'
inventory['pouch'].sort() 

# Your code here
inventory["pocket"] = ["seashell","strange berry","lint"]
inventory["backpack"].sort()
inventory["backpack"].remove("dagger")
inventory["gold"] = inventory["gold"] + 50
print inventory["gold"]

########################################################################################

lloyd = {
    "name": "Lloyd",
    "homework": [],
    "quizzes": [],
    "tests": []
}
alice = {
    "name": "Alice",
    "homework": [100.0, 92.0, 98.0, 100.0],
    "quizzes": [82.0, 83.0, 91.0],
    "tests": [89.0, 97.0]
}
tyler = {
    "name": "Tyler",
    "homework": [0.0, 87.0, 75.0, 22.0],
    "quizzes": [0.0, 75.0, 78.0],
    "tests": [100.0, 100.0]
}
for i in (90.0, 97.0, 75.0, 92.0):
    lloyd["homework"].append(i)
for i in (88.0, 40.0, 94.0):
    lloyd["quizzes"].append(i)
for i in (75.0, 90.0): 
    lloyd["tests"].append(i)
    
students=[lloyd,alice,tyler]

for student in students:
    print student["name"]
    print student["homework"]
    print student["quizzes"]
    print student["tests"]

########################################################################################

def average(numbers):
    total = float(sum(numbers))
    return total / len(numbers) 
   
def get_average(student):
    homework = average(student["homework"])
    quizzes = average(student["quizzes"])
    tests = average(student["tests"])
    
    return 0.1 * homework + 0.6 * tests + 0.3 * quizzes 

def get_letter_grade(score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"    
        elif score >= 60:
            return "D"
        else:
            return "F"
            
print get_letter_grade(get_average(lloyd))   

def get_class_average(students):
    results= list()
    for student in students:
        results.append(get_average(student))
    return average(results)


students=[lloyd,alice,tyler]
print get_class_average(students)
print get_letter_grade(get_class_average(students))  


#####################################################################

n.pop(index) will remove the item at index from the list and return it to you:

n = [1, 3, 5]
n.pop(1)
# Returns 3 (the item at index 1)
print n
# prints [1, 5]

    n.remove(item) will remove the actual item if it finds it:

n.remove(1)
# Removes 1 from the list,
# NOT the item at index 1
print n
# prints [3, 5]

    del(n[1]) is like .pop in that it will remove the item at the given index, but it won't return it:

del(n[1])
# Doesn't return anything
print n
# prints [1, 5]

#####################################################################
