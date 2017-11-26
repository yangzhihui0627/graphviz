# tools.py

import os
import functools

from . import _compat

__all__ = ['attach', 'mkdirs', 'mapping_items', 'multi_contextmanager']


def attach(object, name):
    """Return a decorator doing setattr(object, name) with its argument.

    >>> spam = type('Spam', (object,), {})()
    >>> @attach(spam, 'eggs')
    ... def func():
    ...     pass
    >>> spam.eggs  # doctest: +ELLIPSIS
    <function func at 0x...>
    """
    def decorator(func):
        setattr(object, name, func)
        return func
    return decorator


def mkdirs(filename, mode=0o777):
    """Recursively create directories up to the path of filename as needed."""
    dirname = os.path.dirname(filename)
    if not dirname:
        return
    _compat.makedirs(dirname, mode=mode, exist_ok=True)


def mapping_items(mapping, _iteritems=_compat.iteritems):
    """Return an iterator over the mapping items, sort if it's a plain dict.

    >>> list(mapping_items({'spam': 0, 'ham': 1, 'eggs': 2}))
    [('eggs', 2), ('ham', 1), ('spam', 0)]

    >>> from collections import OrderedDict
    >>> list(mapping_items(OrderedDict(enumerate(['spam', 'ham', 'eggs']))))
    [(0, 'spam'), (1, 'ham'), (2, 'eggs')]
    """
    if type(mapping) is dict:
        return iter(sorted(_iteritems(mapping)))
    return _iteritems(mapping)


def multi_contextmanager(func):
    """

    >>> @multi_contextmanager
    ... def spam():
    ...      yield 'spam'
    ...      print('and')
    ...      yield 'eggs'

    >>> s = spam()
    >>> with s as x:
    ...    print(x)
    spam
    >>> with s as x:
    ...    print(x)
    and
    eggs
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return GeneratorContextmanager(func(*args, **kwargs))
    return wrapper


class GeneratorContextmanager(object):

    def __init__(self, generator):
        self._iter = iter(generator)

    def __enter__(self):
        return next(self._iter)

    def __exit__(self, type, value, tb):
        pass
