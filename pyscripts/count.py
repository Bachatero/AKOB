# print number of occurences of an item in a sequence/list
def count(sequence,item):
    no = 0 
    for element in sequence:
       if element == item:
          no +=1
    return no 

print count([1,2,1,1],2)

# or use list.count(x) method
#return sequence.count(item)
