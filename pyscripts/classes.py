class Animal(object):
    """Makes cute animals."""
    is_alive = True
    health = "good"
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # Add your method here!
    def description(self):
        print self.name
        print self.age
    
hippo = Animal("Bazmeg",111)
hippo.description()
sloth = Animal("Idiot",21)
ocelot = Animal("Elton",33)
print hippo.health
print sloth.health
print ocelot.health
