from util import *
from collections import Counter
from itertools import product, repeat, count, permutations, combinations
from math import sqrt, factorial
from fractions import Fraction

def main():
    print(p138())

# Problems before p134 are lost to time. 
# And I don't feel like going back and re-solving all of them
# just for completeness.

def p138():
    i = 16
    Ls = 0
    while True:
        L = 5*i**2//4+i*2+1 
        if sq(L):
            print(i//2, i+1, int(sqrt(L)))
            i = int(17*i)
        else:
            L = 5*i**2//4-i*2+1
            if sq(L):
                print(i//2, i-1, int(sqrt(L)))
                i = int(17*i)
            else:
                i += 2


# 6.854 found by experimentation...
# Turns out this can be expressed in terms of A, and it
# ends up as a quadratic 0=Ax^2+(A+1)x-A.
def p137():
    i = 1
    while True:
        if sq((i+1)**2+4*(i**2)):
            print(i)
            i = int(i*6.854)
        else:
            i += 1

# Runs kinda slowly, but it works...
def p136():
    # Copied from p135
    def dd(n, x):
        d4 = n//x + x
        if d4 % 4 != 0:
            return None
        return d4 // 4

    ans = 0
    for n in range(1, 50000000):
        sols = 0
        for x in divisors(n):
            d = dd(n, x)
            if d is None or d >= x:
                continue
            sols += 1
            if sols == 2:
                break
        if sols == 1:
            ans += 1
            
    return ans

def p135():
    def dd(n, x):
        d4 = n//x + x
        if d4 % 4 != 0:
            return None
        return d4 // 4

    ans = 0

    for n in range(1155, 1000001):
        sols = 0
        for x in divisors(n):
            d = dd(n, x)
            if d is None or d >= x:
                continue
            sols += 1
        if sols == 10:
            ans += 1

    return ans

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



