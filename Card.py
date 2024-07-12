class Card:
    def __init__(self, type, colour, number):
        self._type = type
        self._colour = colour
        self._number = number

    def __str__(self):
        return f"({self._type}, {self._colour}, {self._number})"
    
    def __repr__(self):
        return f"(Type: {self._type}, Colour: {self._colour}, Number: {self._number})"
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        self._type = type   
    
    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, colour):
        self._colour = colour 

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, number):
        self._number = number 
