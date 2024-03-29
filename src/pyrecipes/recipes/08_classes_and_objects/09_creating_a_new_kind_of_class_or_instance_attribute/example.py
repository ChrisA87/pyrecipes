"""
You want to create an entirely new attribute type with some
extra functionality in the form of a descriptor class.
"""


class Integer:
    """Descriptor attribute for an integer type-checked attribute"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            print("Expected an int")
        else:
            instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Point:
    x = Integer("x")
    y = Integer("y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    p = Point(1, 2)
    print(p.x)
    print(p.y)
    p.x = 6
    print(p.x)
    p.y = 8.2
    del p.x


if __name__ == "__main__":
    main()
