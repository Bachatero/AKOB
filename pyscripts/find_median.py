#sorted([5, 2, 3, 1, 4])
#[1, 2, 3, 4, 5]

#Write a function called median that takes a list as an input and returns the median value of the list.

#For example: median([1,1,2]) should return 1.

#    The list can be of any size and the numbers are not guaranteed to be in any particular order.
#    If the list contains an even number of elements, your function should return the average of the middle two.

def median(lst_of_stuff):
    lst_len = len(lst_of_stuff)
    lst_of_stuff.sort()
    #return lst_len
    if lst_len % 2 > 0: # odd
       ret_index = (lst_len - 1 )/2  #value in the middle
       #print lst_of_stuff
       #print ret_index
       #print lst_of_stuff[ret_index]
       return lst_of_stuff[ret_index]
    else:
       #print lst_of_stuff
       ret_index1 = (lst_len / 2 ) - 1 #first value  
       ret_index2 = lst_len / 2 
       #print float(lst_of_stuff[ret_index1] + lst_of_stuff[ret_index2])/2
       return float(lst_of_stuff[ret_index1] + lst_of_stuff[ret_index2])/2
       #print ret_index


print median([2])
print median([1,1,2])
print median([7,3,1,4])
print median([7,3])
print median([7,3,4,5,5,8])
print median([7,3,1,4,5,5,7,9,9])
