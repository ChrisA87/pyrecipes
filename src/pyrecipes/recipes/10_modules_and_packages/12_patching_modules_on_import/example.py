"""
You want to patch or apply decorators to functions in an existing module.
However, you only want to do it if the module actually gets imported and used elsewhere.
"""

# postimport.py

import importlib
import sys
from collections import defaultdict

_post_import_hooks = defaultdict(list)


class PostImportFinder:
    def __init__(self):
        self._skip = set()

    def find_module(self, fullname, path=None):
        if fullname in self._skip:
            return None
        self._skip.add(fullname)
        return PostImportLoader(self)


class PostImportLoader:
    def __init__(self, finder):
        self._finder = finder

    def load_module(self, fullname):
        importlib.import_module(fullname)
        module = sys.modules[fullname]
        for func in _post_import_hooks[fullname]:
            func(module)
        self._finder._skip.remove(fullname)
        return module


def when_imported(fullname):
    def decorate(func):
        if fullname in sys.modules:
            func(sys.modules[fullname])
        else:
            _post_import_hooks[fullname].append(func)
        return func

    return decorate


sys.meta_path.insert(0, PostImportFinder())


def main():
    print(
        """
# Example usage:
from postimport import when_imported

@when_imported('threading')
def warn_threads(mod):
    print('Threads? Are you crazy?')

if __name__ == '__main__':
    import threading

"""
    )

    print(
        """
# Example usage 2
from postimport import when_imported
from functools import wraps


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return wrapper

@when_imported('math')
def add_logging(mod):
    mod.cos = logged(mod.cos)
    mod.sin = logged(mod.sin)

if __name__ == '__main__':
    import math
    print(math.cos(2))
    print(math.sin(2))
    """
    )


if __name__ == "__main__":
    main()
