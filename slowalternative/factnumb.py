#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Попытка переписать fact.py с использованием массивов numpy и ускорением numba jit
Работает. Но очень медленно.
Даже без нахождения кратностей на N = 1 000 000 в ~5 раз медленнее, в ~3 с jit
"""

import numpy as np
from numba import jit, i4, prange
from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:%r took: %2.3f sec' % (f.__name__, te-ts))
        return result
    return wrap


@timing
@jit("i4[:,:](i4)", locals={'i': i4, 'j': i4, 'k': i4})
def factorize(n):
    """
    finds prime multipliers for each of [1,...,N]
    returns 2D array F[i, j]
    where F[i-1:] is an array of prime multipliers for i (ends with zeros)
    """
    F = np.zeros((n, int(np.sqrt(n))))

    # numba does not work with cycles within if: else: constructions
    i = 2
    while i < n+1:
        while F[i-1,0] != 0:
            if i == n:
                break
            i += 1
        for k in prange (2*i, n+1, i):
            j = 0
            while F[k-1, j] != 0:
                j = j + 1
            F[k-1,j] = i
        i += 1

    return F


if __name__ == '__main__':
    n = int(input('n: '))
    f = factorize(n)
    print(f)
