class Tecla:
    def __init__(self, x, y, char, shift):
        self.coords = (x,y)
        self.character = char
        self.shift = shift

    def get_coords(self):
        return self.coords

    def y(self):
        return self.coords[1]
    def x(self):
        return self.coords[0]
    
    def get_char(self):
        return self.character
    def get_shift(self):
        return self.shift

    def to_str(self):
        return '<(%d, %d)>  - %s:%s' % (self.coords[0], self.coords[1], self.get_char(),
                                        self.get_shift())

