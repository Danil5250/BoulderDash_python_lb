class Coordinates:
    __slots__ = ['__x', '__y']

    def __init__(self, x, y, /):
        self.__x = x
        self.__y = y

    def move_instance(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_element_in_bounds(self, dx, dy, field_height, field_width):
        new_x = self.x + dx
        new_y = self.y + dy
        return 0 <= new_x < field_height and 0 <= new_y < field_width


    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if value >= 0:
            self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if value >= 0:
            self.__y = value