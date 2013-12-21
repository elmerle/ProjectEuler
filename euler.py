import util

def getRing(n):
    s = n**2
    d = n-1
    return [s-3*d, s-2*d, s-d]

def main():
    l = 3
    total = 1.0
    primes = 0
    while True:
        total += 4
        primes += len([p for p in getRing(l) if util.isPrime(p)])
        if primes / total < .1:
            print l
            break
        l += 2

if __name__ == '__main__':
    main()