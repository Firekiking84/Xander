class Coords:
    def __init__(self, x=0, y=0, i=0, width=3):
        self.x = x
        self.y = y
        self.i = i
        self.width = width

    def set(self, x=None, y=None, i=None):
        if i is not None:
            self.i = i
            self.x = int(i % self.width)
            self.y = int(i / self.width)
        else:
            if x is not None:
                self.x = x
            if y is not None:
                self.y = y
            self.i = self.y * self.width + self.x

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, index: {self.i}, width: {self.width}"

    def copy(self):
        return Coords(self.x, self.y, self.i, self.width)