from math import *

primes = [2, 3]
primeSet = set(primes)

def isPrime(n):
    if n > primes[-1]:
        _generatePrimes(2 * n)
    return n in primeSet

def nextPrime(n):
    if not isPrime(n):
        return None
    if n >= primes[-1]:
        _generatePrimes(2 * n)
    return primes[primes.index(n) + 1]

def getPrimes(max):
    _generatePrimes(max)
    return [prime for prime in primes if prime <= max]

def _generatePrimes(max): 
    global primes
    if max < primes[-1]:
        return
    offset = primes[-1] + 1 # first number
    sieve = [True for i in range(offset, max + 1)]
    for prime in primes:    
        _doSieve(sieve, prime, offset)
    prime = offset
    while prime < max:
        if sieve[prime - offset]:
            _doSieve(sieve, prime, offset)
        prime += 1
    newPrimes = [prime for prime in range(offset, max + 1) if sieve[prime - offset]]
    primes += newPrimes
    for prime in newPrimes:
        primeSet.add(prime)    

def _doSieve(sieve, prime, offset=0):
    nextPrime = max(2 * prime, offset + (prime - offset % prime) % prime)
    for multiple in range(nextPrime, len(sieve) + offset, prime):
        sieve[multiple - offset] = False
