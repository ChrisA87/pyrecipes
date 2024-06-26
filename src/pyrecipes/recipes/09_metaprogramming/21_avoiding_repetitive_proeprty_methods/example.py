"""
You are writing classes where you are repeatedly having to define
property methods that perform common tasks, such as type-checking.
You would like to simplify the code so there is not so much code
repetition.
"""


def typed_property(name, expected_type):
    storage_name = "_" + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError("{} must be a {}".format(name, expected_type))
        setattr(self, storage_name, value)

    return prop


# Example use
class Person:
    name = typed_property("name", str)
    age = typed_property("age", int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


def main():
    p = Person("Dave", 39)
    p.name = "Guido"
    try:
        p.age = "Old"
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    main()
