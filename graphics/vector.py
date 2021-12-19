
class Vector:
    def __init__(x, y, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __add__(self, other):
        return Vector()