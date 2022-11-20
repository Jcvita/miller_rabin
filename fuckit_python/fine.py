from random import randint
from math import sqrt
from timeit import timeit
from threading import Thread

#calculat s and d where n - 1 = (2^d) * s
def calc_s_d(n):
    s = 0
    d = n - 1
    # if the next division results in a fraction, use the previous s, d values
    while (d / 2).is_integer():
        s += 1
        d /= 2
    return s, int(d)

# (in theory) faster modular exponentiation using square multiply method
# python is slow so it's not faster
def sqm(base,exponent,modulus):
    #Converting the exponent to its binary form
    binaryExponent = []
    while exponent != 0:
        binaryExponent.append(exponent%2)
        exponent = exponent/2
    #Application of the square and multiply algorithm
    result = 1
    binaryExponent.reverse()
    for i in binaryExponent:
        if i == 0:
            result = (result*result) % modulus
        else:
            result = (result*result*base) % modulus
        #print i,"\t",result
    return result

#miller rabin implementation
def miller_rabin(n, k, a=None, use_sqm=True):
    if n < 3 or n % 2 == 0:
        return False
    s, d = calc_s_d(n)
    a = a if a else randint(1, n-1)
    # print(a)
    b = sqm(a, d, n) if use_sqm else pow(a, d, n)
    if b == 1:
        return True
    for _ in range(k):
        if b == n-1:
            return True
        b = sqm(b, 2, n) if use_sqm else pow(b, 2, n)
    return False

#determine if a number is prime via brute force
def brute_prime(n):
    if n % 2 == 0:
        return False
    for x in range(2, int(sqrt(n) + 1), 2):
        if (n / (x + 1)).is_integer():
            return False
    return True

#determine if a number is prime faster
def faster_prime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

#calculate the error rate for a mr composite
def mr_error_rate(n, use_sqm=False):
    errors = 0
    trials = range(2, n-1)
    k = 2
    comp = not faster_prime(n)
    if not comp:
        return (n, 0)
    for a in trials:
        result = miller_rabin(n, k, a, use_sqm)
        if result:
            errors += 1
    return (n, errors/len(trials))

#get the highest error value from a block of errors
def highest_error(start, end, storage):
    highest = (0, 0)
    print(f'started block {start}')
    for x in range(start, end):
        result = mr_error_rate(x)
        if result[1] > highest[1]:
            highest = result
    storage.append(highest)
    print(f'finished block {start}')
    return highest

def main():
    errors = []
    threads = []
    
    # multithread to chop it up into parallel blocks of 1000
    for x in range(85001, 99002, 1000):
        threads.append(Thread(target=highest_error, args=(x, x + 1000, errors)))
    for x in threads:
        x.start()
    mx = (0, 0)
    for x in errors:
        if x[1] > mx[1]:
            mx = x
    for x in threads:
        x.join()

    print(f'highest error = {mx[0]}\nrate = {mx[1]}')
    # [print(f'error rate for {n}: {mr_error_rate(n, False)}') for n in range(85001, 100000, 2)] 
    
    
if __name__ == '__main__':
    main()