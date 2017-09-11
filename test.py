import math

      
      
      
def eratosthenes (n):
    primes = []
    multiples = []
    j = 2
    for i in xrange(j, n + 1, j * j):
        if i != 2 and i % 2 == 0:
          continue
          
        if i not in multiples:
            primes.append(i)
            multiples.extend(xrange(i * i, n + 1, i))
        j = i
    return (primes, multiples)
  
  
    
    
def primes_sieve2(limit):
    a = [True] * limit                          # Initialize the primality list
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in xrange(i*i, limit, i):     # Mark factors non-prime
                a[n] = False

#print eratosthenes(10000000000)
print primes_sieve2(10000000000)