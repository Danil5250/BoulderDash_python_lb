class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.parent = None

    @property
    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f < other.f
