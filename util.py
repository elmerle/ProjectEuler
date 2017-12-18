from math import sqrt
from collections import defaultdict, Counter
from functools import wraps
from itertools import repeat, chain

PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def product(vals):
    return reduce(lambda x, y: x * y, vals)

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

def _factorize():
    cache = {}
    def factorize(n):
        result = []
        bound = sqrt(n)
        for p in PRIMES_100:
            if p > bound:
                break
            while n % p == 0:
                result.append(p)
                n /= p
        p = 101
        while n in cache:
            p = cache[n]
            result.append(p)
            n /= p

        bound = sqrt(n)
        while p <= bound:
            while n % p == 0:
                result.append(p)
                cache[n] = p
                n /= p
                bound = sqrt(n)
            p += 2

        if n > 1:
            result.append(n)

        assert result == sorted(result), str(result)
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

    SIEVE_JUMP = 20

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
                for mult in range(((start-1) / p + 1) * p, num + 1 + jump, p):
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
