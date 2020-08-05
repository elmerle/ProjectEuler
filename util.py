from math import sqrt, factorial
from collections import defaultdict, Counter
from functools import wraps
from itertools import repeat, chain, count

PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def cube(n):
    root = int(n ** (1/3) + .9)
    return root ** 3 == n

def sq(n):
    root = int(n ** .5 + .9)
    return root ** 2 == n 

# M*n-N (M=1000, N=111, L=3)
# L = 3 ** l
# M = 10 ** L
# N = int('1' * L)
# ??????
def repunit(n, M=None, N=None, L=None):
    L = L or 3 ** (len(str(n)) - 1)
    M = M or 10 ** L
    N = N or int('1' * L)
    ones = 1
    ret = 1
    first = []
    sfirst = set()
    for i in range(L):
        first.append(ones)
        sfirst.add(ones)
        if ones == 0:
            return ret
        ones = (10 * ones + 1) % n
        ret += 1        
    while True:
        if ones in sfirst:
            return ret - first.index(ones) - 1 
        ones = (M * ones + N) % n
        ret += L

def gcd(n, m):
    while m != 0:
        n, m = m, n % m
    return n

def gcd_ex(n, m):
    (_r, r) = (n, m)
    (_s, s) = (1, 0)
    (_t, t) = (0, 1)
    while r != 0:
        q = _r // r
        (_r, r) = (r, _r - q * r)
        (_s, s) = (s, _s - q * s)
        (_t, t) = (t, _t - q * t)

    return _r, _s, _t 

def mod_inv(mod, n):
    return gcd_ex(n, mod)[1] % mod

def c(n, m):
    return factorial(n) // factorial(m) // factorial(n-m)

def prod(vals):
    if vals:
        return reduce(lambda x, y: x * y, vals)
    return 1

def palindrome(num):
    return str(num) == str(num)[::-1]

def memoize(fn):
    memo = {}
    
    @wraps(fn)
    def wrapper(*n):
        if n not in memo:
            memo[n] = fn(*n)
        return memo[n]
    
    return wrapper

def divisors(n):
    for i in range(1, n):
        if n % i == 0:
            yield i

def is_prime_dumb(n):
    if n <= 1:
        return False
    if n in (2,3,5,7):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in xrange(6, min(int(sqrt(n))+2, n), 6):
        if n % (i-1) == 0 or n % (i+1) == 0:
            return False
    return True

def _factorize():
    cache = {}
    @memoize
    def factorize(n_):
        if n_ == 1:
            return []

        n = n_
        result = []
        bound = sqrt(n)

        if n in cache:
            while n in cache:
                p = cache[n]
                result.append(p)
                n //= p
            assert n == 1
        else:
            #print 'f', n_
            for p in chain([2,3], count(5, 6)):

                if p > bound:
                    break
                while n % p == 0: 
                    result.append(p)
                    cache[n] = p
                    n //= p

                    if n in cache:
                        while n in cache:
                            p = cache[n]
                            result.append(p)
                            n //= p
                        assert n == 1
                    
                    bound = sqrt(n)

                if p > 3:
                    p += 2
                    if p > bound:
                        break
                    while n % p == 0: 
                        result.append(p)
                        cache[n] = p
                        n //= p

                        if n in cache:
                            while n in cache:
                                p = cache[n]
                                result.append(p)
                                n //= p
                            assert n == 1
                        
                        bound = sqrt(n)

            if n > 1:
                result.append(n)
                cache[n] = n

            if len(result) == 1:
                cache[n_] = result[0]

        #assert result == sorted(result), str(n_) + str(cache) + str(result)
        return result
    return factorize

factorize = _factorize()

def num_factors(n):
    if n == 1:
        return 1
    return product([exponent + 1 for exponent in Counter(factorize(n)).values()])

def divisors(n):
    primes = Counter(factorize(n))
    # todo finish

class _Prime(object):

    SIEVE_JUMP = 1000

    def __init__(self):
        self.primes = set([2])
        self.iter = [2]
        self.max_prime = 2
        self.extend(100, jump=0)

    def extend(self, num, jump=SIEVE_JUMP):
        if num > self.max_prime:
            start = self.max_prime        

            # Initial sieve. Start the sieve at one more than the largest 
            # known prime. For example, if max_prime is 7, sieve[0] represents 8.
            sieve = list(repeat(True, num - start + jump))

            # Filter all multiples of known primes.
            for p in self.primes:
                for mult in range(((start-1) // p + 1) * p, num + 1 + jump, p):
                    sieve[mult - start - 1] = False

            # Filter multiples of newly discovered primes in the sieve's range.
            for idx in range(len(sieve)):
                if not sieve[idx]:
                    continue
                p = idx + 1 + start
                for mult in range(2 * p, num + 1 + jump, p):
                    sieve[mult - start - 1] = False

            # Add newly discovered primes to our list.
            for idx in range(len(sieve)):
                if not sieve[idx]:
                    continue
                p = idx + 1 + start
                self.iter.append(p)
                self.primes.add(p)
                self.max_prime = p

    def is_prime(self, num):
        self.extend(num)
        return num in self.primes

    def prime_it(self, start=2):
        self.extend(start)
        inc = self.SIEVE_JUMP
        cur = 0
        while self.iter[cur] < start:
            cur += 1
            
        while True:
            # Yield everything we can.
            while cur < len(self.iter):
                yield self.iter[cur]
                cur += 1

            # Increase inc until we get more primes.
            while cur >= len(self.iter):
                self.extend(self.max_prime + inc)
                inc *= 2
            inc = self.SIEVE_JUMP

_p = _Prime()
is_prime = _p.is_prime
prime_it = _p.prime_it
