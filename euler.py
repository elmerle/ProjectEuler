from util import *
from collections import Counter
from itertools import product, repeat, count, permutations, combinations
from math import sqrt, factorial
from fractions import Fraction

def d(p):
    seen = set()
    n = 1
    while n not in seen:
        seen.add(n)
        n = (n * 10 + 1) % p 


def main():
    is_prime(100100)

    ps = []

    for p in prime_it():
        if p > 100000:
            break
        if p in (2, 5):
            continue
        a = repunit(p)
        if set(factorize(a)) <= set([2, 5]):
            pass
        else:
            ps.append(p)

    print ps, sum(ps)


if __name__ == '__main__':
    main()

