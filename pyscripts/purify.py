#Define a function called purify that takes in a list of numbers, removes all odd numbers in the list, and returns the result.

#For example, purify([1,2,3]) should return [2].

#Do not directly modify the list you are given as input; instead, return a new list with only the even numbers.

def purify(list_of_nos):
        clean_list=list()
	for item in list_of_nos:
	    if item % 2 == 0:
	        clean_list.append(item)

	return clean_list

print purify([1,2,3])
