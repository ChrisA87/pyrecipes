"""
You've learned about function argument annotations and you have thought
that you might be able to use them to implement multiple-dispatch
(method overloading) based on types. However, you're not quite sure
what's involved (or if it's even a good idea).
"""

import inspect
import types


def example_1():
    class MultiMethod:
        """
        Represents a single multimethod.
        """

        def __init__(self, name):
            self._methods = {}
            self.__name__ = name

        def register(self, meth):
            """
            Register a new method as a multimethod
            """
            sig = inspect.signature(meth)

            # Build a type-signature from the method's annotations
            types = []
            for name, parm in sig.parameters.items():
                if name == "self":
                    continue
                if parm.annotation is inspect.Parameter.empty:
                    raise TypeError(
                        "Argument {} must be annotated with a type".format(name)
                    )
                if not isinstance(parm.annotation, type):
                    raise TypeError(
                        "Argument {} annotation must be a type".format(name)
                    )
                if parm.default is not inspect.Parameter.empty:
                    self._methods[tuple(types)] = meth
                types.append(parm.annotation)

            self._methods[tuple(types)] = meth

        def __call__(self, *args):
            """
            Call a method based on type signature of the arguments
            """
            types = tuple(type(arg) for arg in args[1:])
            meth = self._methods.get(types, None)
            if meth:
                return meth(*args)
            else:
                raise TypeError("No matching method for types {}".format(types))

        def __get__(self, instance, cls):
            """
            Descriptor method needed to make calls work in a class
            """
            if instance is not None:
                return types.MethodType(self, instance)
            else:
                return self

    class MultiDict(dict):
        """
        Special dictionary to build multimethods in a metaclass
        """

        def __setitem__(self, key, value):
            if key in self:
                # If key already exists, it must be a multimethod or callable
                current_value = self[key]
                if isinstance(current_value, MultiMethod):
                    current_value.register(value)
                else:
                    mvalue = MultiMethod(key)
                    mvalue.register(current_value)
                    mvalue.register(value)
                    super().__setitem__(key, mvalue)
            else:
                super().__setitem__(key, value)

    class MultipleMeta(type):
        """
        Metaclass that allows multiple dispatch of methods
        """

        def __new__(cls, clsname, bases, clsdict):
            return type.__new__(cls, clsname, bases, dict(clsdict))

        @classmethod
        def __prepare__(cls, clsname, bases):
            return MultiDict()

    # Some example classes that use multiple dispatch
    class Spam(metaclass=MultipleMeta):
        def bar(self, x: int, y: int):
            print("Bar 1:", x, y)

        def bar(self, s: str, n: int = 0):
            print("Bar 2:", s, n)

    # Example: overloaded __init__
    import time

    class Date(metaclass=MultipleMeta):
        def __init__(self, year: int, month: int, day: int):
            self.year = year
            self.month = month
            self.day = day

        def __init__(self):
            t = time.localtime()
            self.__init__(t.tm_year, t.tm_mon, t.tm_mday)

    s = Spam()
    s.bar(2, 3)
    s.bar("hello")
    s.bar("hello", 5)
    try:
        s.bar(2, "hello")
    except TypeError as e:
        print(e)

    # Overloaded __init__
    d = Date(2012, 12, 21)
    print(d.year, d.month, d.day)
    # Get today's date
    e = Date()
    print(e.year, e.month, e.day)


def example_2():
    class multimethod:
        def __init__(self, func):
            self._methods = {}
            self.__name__ = func.__name__
            self._default = func

        def match(self, *types):
            def register(func):
                ndefaults = len(func.__defaults__) if func.__defaults__ else 0
                for n in range(ndefaults + 1):
                    self._methods[types[: len(types) - n]] = func
                return self

            return register

        def __call__(self, *args):
            types = tuple(type(arg) for arg in args[1:])
            meth = self._methods.get(types, None)
            if meth:
                return meth(*args)
            else:
                return self._default(*args)

        def __get__(self, instance, cls):
            if instance is not None:
                return types.MethodType(self, instance)
            else:
                return self

    # Example use
    class Spam:
        @multimethod
        def bar(self, *args):
            # Default method called if no match
            raise TypeError("No matching method for bar")

        @bar.match(int, int)
        def bar(self, x, y):
            print("Bar 1:", x, y)

        @bar.match(str, int)
        def bar(self, s, n=0):
            print("Bar 2:", s, n)

    s = Spam()
    s.bar(2, 3)
    s.bar("hello")
    s.bar("hello", 5)
    try:
        s.bar(2, "hello")
    except TypeError as e:
        print(e)


def main():
    example_1()
    example_2()


if __name__ == "__main__":
    main()
