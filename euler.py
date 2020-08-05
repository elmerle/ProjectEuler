from util import *
from collections import Counter
from itertools import product, repeat, count, permutations, combinations
from math import sqrt, factorial
from fractions import Fraction

def main():
    print(p134())

# Problems before p134 are lost to time. 
# And I don't feel like going back and re-solving all of them
# just for completeness.

def p134():
    s = 0
    q = 5

    is_prime(1000100)

    def solve(q, p):
        pten = 10 ** len(str(q))
        return (p - q) * mod_inv(p, pten) % p

    for p in prime_it(7):
        n = int(str(solve(q, p)) + str(q))
        s += n

        q = p
        if p > 1000000:
            break

    return s

if __name__ == '__main__':
    main()



