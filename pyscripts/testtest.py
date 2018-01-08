import re
m = re.search('(?<=abc)def', 'abcdef')
m.group(0)

print m.group(0)


jjj  = [1,1,2,2,1]
print sum(jjj)


shits = '9: from fairest creatures we desire increase'
#10: that thereby beautys rose might never die
#11: but as the riper should by time decease
#12: his tender heir might bear his memory
#13: but thou contracted to thine own bright eyes
#14: feedst thy lights flame with selfsubstantial fuel

print shits.split(" ")
