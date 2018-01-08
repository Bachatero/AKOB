stringg = "basmeg shut up"
stuff = stringg.split()
print stuff
print dir(stuff)
print type(stuff)

stringg = "basmeg;shut;up;          pliz"
print stringg
stuff = stringg.split(';')
print stuff

stringg = "basmeg shut up         pliz"
print stringg
stuff = stringg.split()
print stuff
