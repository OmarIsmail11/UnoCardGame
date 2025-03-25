class Card:
    def __init__(self, type, colour, number, imagepath):
        self._type = type
        self._colour = colour
        self._number = number
        self._imagePath = imagepath
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

    @property
    def imagePath(self):
        return self._imagePath

    @imagePath.setter
    def imagePath(self, imagepath):
        self._imagePath = imagepath
