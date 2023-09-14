from werkzeug.security import check_password_hash

class User:
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
    
    @staticmethod
    def is_authenticated(self):
        "pay attention to this when you are preparing landing page"
        " This would make it work only for authenticated users"
        return True
    
    @staticmethod
    def is_active(self):
        return True
    
    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.firstname
    
    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    def print_stuff(self):
        return (self.firstname + ' ' + self.lastname)
    
    def __repr__(self): 
        "leaving this like this for testing purposes for now"
        return ("my name is {} and my password is {}".format(self.firstname, self.password))


class Driver(User):
  def __init__(self, firstname, lastname, email, password, vehicle_type, available):
    super().__init__(firstname, lastname, email, password)
    self.available = available
    self.vehicle = vehicle_type

class Ride():
    def __init__(self, firstname, current_location, destination, created_by):
        self.firstname = firstname
        self.current_location = current_location 
        self._destination = destination
        self.created_by = created_by
    
    def __repr__(self): 
        "leaving this like this for testing purposes for now"
        return (f"my name is {self.firstname}, location is {self.current_location}, destination is {self.destination}")

    @property
    def destination(self):
        return self._destination
    
    @destination.setter
    def destination(self, new_destination):
        self._destination = new_destination

"""
z = Ride("davis", "lekki", "better_days", "vic")
z.destination = "better beeter days"
print(z)

x = User("dave", "dave", "test", "test")
x.password = "pray"
print(x.password)
print(x)
y = Driver("dave", "david", "damsel", "test", "yes")
print(y.print_stuff())
"""