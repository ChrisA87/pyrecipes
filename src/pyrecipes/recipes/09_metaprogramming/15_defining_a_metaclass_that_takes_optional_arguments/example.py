"""
You want to define a metaclass that allows class definitions to supply
optional arguments, possiblly to control or configure aspects of processing
during type creation.
"""

from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass


class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # Custom processing
        ...
        return super().__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        ...
        super().__new__(cls, name, bases, ns)

    # Required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        # Custom processing
        super().__init__(name, bases, ns)


class Spam(metaclass=MyMeta):
    debug = True
    synchronize = True
    ...


def main():
    pass


if __name__ == "__main__":
    main()
