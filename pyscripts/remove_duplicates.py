#Write a function remove_duplicates that takes in a list and removes elements of the list that are the same.

#For example: remove_duplicates([1,1,2,2])
#should return [1,2].

#Do not modify the list you take as input! Instead, return a new list.

def remove_duplicates(lst_of_items):
	new_list=list()
        #dict={}
	for item in lst_of_items:
	   #dict[item]
           if item not in new_list:
	       new_list.append(item)
               #print item

	return new_list

print remove_duplicates([1,3,1,2,2,3,3,3])
