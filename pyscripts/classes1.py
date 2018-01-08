class ShoppingCart(object):
    """Creates shopping cart objects
    for users of our fine website."""
    items_in_cart = {}
    def __init__(self, customer_name):
        self.customer_name = customer_name

    def add_item(self, product, price):
        """Add product to the cart."""
        if not product in self.items_in_cart:
            self.items_in_cart[product] = price
            print product + " added."
        else:
            print product + " is already in the cart."

    def remove_item(self, product):
        """Remove product from the cart."""
        if product in self.items_in_cart:
            del self.items_in_cart[product]
            print product + " removed."
        else:
            print product + " is not in the cart."

my_cart = ShoppingCart("Jimmy Carter")
my_cart.add_item("Airship",23000000)


##########################################################
#Inheritance is a tricky concept, so let's go through it step by step.

#Inheritance is the process by which one class takes on the attributes and methods of another, and it's used to express an is-a relationship. For example, a Panda is a bear, so a Panda class could inherit from a Bear class. However, a Toyota is not a Tractor, so it shouldn't inherit from the Tractor class (even if they have a lot of attributes and methods in common). Instead, both Toyota and Tractor could ultimately inherit from the same Vehicle class.


class Customer(object):
    """Produces objects that represent customers."""
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def display_cart(self):
        print "I'm a string that stands in for the contents of your shopping cart!"

class ReturningCustomer(Customer):
    """For customers of the repeat variety."""
    def display_order_history(self):
        print "I'm a string that stands in for your order history!"

monty_python = ReturningCustomer("ID: 12345")
monty_python.display_cart()
monty_python.display_order_history()

##########################################################

#Add a new method called full_time_wage with the arguments self and hours.
#That method should return the result of a super call to the calculate_wage method of PartTimeEmployee's parent class. Use the example above for help.

#Then, after your class:

#Create an instance of the PartTimeEmployee class called milton. Don't forget to give it a name.
#Finally, print out the result of calling his full_time_wage method. You should see his wage printed out at $20.00 per hour! (That is, for 10 hours, the result should be 200.00.)


class Employee(object):
    """Models real-life employees!"""
    def __init__(self, employee_name):
        self.employee_name = employee_name

    def calculate_wage(self, hours):
        self.hours = hours
        return hours * 20.00

# Add your code below!
class PartTimeEmployee(Employee):
    def full_time_wage(self, hours):
        return super(PartTimeEmployee,self).calculate_wage(hours)
    def calculate_wage(self,hours):
        self.hours = hours
        return hours * 12.00

milton=PartTimeEmployee("Milton")
print milton.full_time_wage(10)

##########################################################


#Create a class named Equilateral that inherits from Triangle.
#Inside Equilateral, create a member variable named angle and set it equal to 60.
#Create an __init__() function with only the parameter self, and set self.angle1, self.angle2, and self.angle3 equal to self.angle (since an equilateral triangle's angles will always be 60˚).



class Triangle(object):
    number_of_sides = 3
    def __init__(self,angle1,angle2,angle3):
        self.angle1 = angle1
        self.angle2 = angle2
        self.angle3 = angle3
    def check_angles(self):
        if self.angle1 + self.angle2 + self.angle3 == 180:
            return True
        else:
            return False
class Equilateral(Triangle):
    angle = 60
    def __init__(self):
        self.angle1 = self.angle
        self.angle2 = self.angle
        self.angle3 = self.angle
        
my_triangle = Triangle(90,20,70)
print my_triangle.number_of_sides
print my_triangle.check_angles()

##########################################################

ass Car(object):
    condition = "new"
    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg   = mpg
    
    def display_car(self):
        print "This is a %s %s with %s MPG." % (self.color, self.model, self.mpg) 

my_car = Car("DeLorean", "silver", 88)
#print my_car.condition
#print my_car.model
#print my_car.color
#print my_car.mpg
print my_car.display_car()



##########################################################

#We can modify variables that belong to a class the same way that we initialize those member variables. This can be useful when we want to change the value a variable takes on based on something that happens inside of a class method.
#Instructions

#Inside the Car class, add a method drive_car() that sets self.condition to the string "used".
#Remove the call to my_car.display_car() and instead print only the condition of your car.
#Then drive your car by calling the drive_car() method.
#Finally, print the condition of your car again to see how its value changes.




class Car(object):
    condition = "new"
    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg   = mpg
    
    def display_car(self):
        print "This is a %s %s with %s MPG." % (self.color, self.model, self.mpg) 
        
    def drive_car(self):
        self.condition = "used"

my_car = Car("DeLorean", "silver", 88)
#print my_car.condition
#print my_car.model
#print my_car.color
#print my_car.mpg

print my_car.condition
my_car.drive_car()
print my_car.condition



##########################################################

class Car(object):
    condition = "new"
    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg   = mpg
    
    def display_car(self):
        print "This is a %s %s with %s MPG." % (self.color, self.model, self.mpg) 
        
    def drive_car(self):
        self.condition = "used"

class ElectricCar(Car):
    def __init__(self,model, color, mpg, battery_type):
        self.model = model
        self.color = color
        self.mpg   = mpg
        self.battery_type = battery_type
    
    def drive_car(self):
        self.condition = "like new"

my_car = Car("DeLorean", "silver", 88)
#print my_car.condition
#print my_car.model
#print my_car.color
#print my_car.mpg

#print my_car.condition
#my_car.drive_car()
#print my_car.condition

my_car = ElectricCar("Bazmeg","shitty",2222, "molten salt")

print my_car.condition
my_car.drive_car()
print my_car.condition

##########################################################
