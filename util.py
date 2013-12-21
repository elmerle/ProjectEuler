from math import *
from collections import defaultdict
from operator import mul

def factorize(n):
    result = []

    while n % 2 == 0:
        result.append(2)
        n /= 2

    p = 3
    max = sqrt(n)
    while p <= max:
        if n % p == 0:
            result.append(p)
            n /= p
            max = sqrt(n)
        else:
            p += 2

    # optimization for prime n
    if n != 1:
        result.append(n)

    return result

def numDivisors(n):
    primes = factorize(n)
    histogram = defaultdict(int)
    for factor in primes:
        histogram[factor] += 1
    return reduce(mul, [exponent + 1 for exponent in list(histogram.values())])

def isPrime(num):
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False
    if num % 3 == 0:
        return False

    return numDivisors(num) == 2

class _AbstractPrimeTest:
    def isPrime(self, n):
        raise 'Not implemented.'

    def nextPrime(self, n):
        raise 'Not implemented.'

    def getPrimes(self, max):
        raise 'Not implemented.'

    def getType(self):
        raise 'Not implemented.'

class _EratosthenesPrimeTest(_AbstractPrimeTest):
    def __init__(self):
        self._primes = [2, 3]
        self._primeSet = set(self._primes)
    
    def getType(self):
        return 'eratosthenes'

    def isPrime(self, n):
        if n >= self._primes[-1]:
            self._generatePrimes(2 * n)
        return n in self._primeSet

    def nextPrime(self, n):
        if not self.isPrime(n):
            return None
        if n >= self._primes[-1]:
            self._generatePrimes(2 * n)
        return self._primes[self._primes.index(n) + 1]
    
    def getPrimes(self, max):
        self._generatePrimes(max)
        return [prime for prime in self._primes if prime <= max]

    def _generatePrimes(self, max): 
        if max <= self._primes[-1]:
            return
        offset = self._primes[-1] + 1 # first number
        sieve = [True for i in range(offset, max + 1)]
        for prime in self._primes:    
            self._doSieve(sieve, prime, offset)
        prime = offset
        while prime < max:
            if sieve[prime - offset]:
                self._doSieve(sieve, prime, offset)
            prime += 1
        newPrimes = [prime for prime in range(offset, max + 1) if sieve[prime - offset]]
        self._primes += newPrimes
        for prime in newPrimes:
            self._primeSet.add(prime)    
    
    def _doSieve(self, sieve, prime, offset=0):
        nextPrime = max(2 * prime, offset + (prime - offset % prime) % prime)
        for multiple in range(nextPrime, len(sieve) + offset, prime):
            sieve[multiple - offset] = False
    
class _SundaramPrimeTest(_AbstractPrimeTest):
    def __init__(self):
        self._halves = [1]
        self._halvesSet = set(self._halves)
    
    def getType(self):
        return 'sundaram'

    def isPrime(self, n):
        if n > 2 * self._halves[-1] + 1:
            self._generateHalves(n)
        if n == 2:
            return True
        return (n - 1) / 2.0 in self._halvesSet

    def nextPrime(self, n):
        half = (n - 1) / 2
        if not self.isPrime(n):
            return None
        if half >= self._halves[-1]:
            self._generateHalves(n)
        if n == 2:
            return 3
        return 1 + 2 * self._halves[self._halves.index(half) + 1]

    def getPrimes(self, max):
        self._generateHalves(max / 2)
        return [2] + [2 * half + 1 for half in self._halves if 2 * half + 1 <= max]

    def _generateHalves(self, half):
        halves = [True for i in xrange(half + 1)]
        for i in xrange(1, half + 1):
            for j in xrange(i, (half - i) / (2 * i + 1) + 1):
                if i + j + 2 * i * j <= half:
                    halves[i + j + 2 * i * j - 1] = False
        self._halves = [p for p in range(1, half + 1) if halves[p - 1]]
        self._halvesSet = set(self._halves)

def getPrimeTest(type):
    if type == 'eratosthenes':
       return _EratosthenesPrimeTest() 
    elif type == 'sundaram':
        return _SundaramPrimeTest()
    return None