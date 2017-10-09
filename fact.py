#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from time import time


def timing(f):
    """
    timing decorator
    """
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.3f sec' % (f.__name__, te-ts))
        return result
    return wrap


@timing
def findpowers(mainlst):
    """
    finds powers for prime multipliers
    """
    n = len(mainlst)
    for i in range(3, n):
        if mainlst[i]:
            factdict = dict.fromkeys(mainlst[i])
            for prime in mainlst[i]:
                power = 1
                j = i
                while j % prime == 0:
                    j /= prime
                    power += 1

                factdict[prime] = power - 1

            mainlst[i] = factdict


@timing
def factorize(n):
    """
    prime factorization for each of [1,...,N]
    based on Sieve of Eratosthenes algorithm
    returns list where list[i]=0 if i is prime
    else list[i]=dict{prime: power}
    """
    if n <= 0:
        raise ValueError('N must be greater than 1')
    elif n < 4:
        return [0] * (n+1)

    # initializing
    mainlst = [0, 0, 0, []]
    for i in range(4, n+1, 2):
        mainlst.append([2])
        mainlst.append([])
    if len(mainlst) == n+2:
        mainlst.pop(n+1)

    # sieving
    i = 3
    while i <= n:
        if not mainlst[i]:
            for j in range(i, n + 1, i):
                mainlst[j].append(i)
            mainlst[i] = 0
        i += 1

    # finding powers
    findpowers(mainlst)
    return mainlst


def printfact(factorization):
    """
    prints factorization on the screen
    we consider 1 as a prime number
    """
    n = len(factorization)
    for i in range(1, n):
        line = '%d ' % i
        if not factorization[i]:
            line += 'prime'
        else:
            line += '='
            for prime, power in factorization[i].items():
                line += ' %d^%d *' % (prime, power)
            line = line[:-2]
        print(line)


if __name__ == '__main__':
    try:
        stopnum = int(input('enter N = '))
        fact = factorize(stopnum)
        input('press enter to print')
        printfact(fact)
    except ValueError or TypeError as e:
        print('Error: incorrect input: %s' % str(e))
        exit()
