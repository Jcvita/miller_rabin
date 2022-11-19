from random import randint

def calc_s_d(n):
    s = 0
    d = n - 1
    while (d / 2).is_integer():
        s += 1
        d /= 2
    return s, int(d)

def miller_rabin(n, k):
    if n % 2 == 0 or n < 3:
        return True
    s, d = calc_s_d(n)
    for _ in range(1, k):
        a = randint(1, n-1)
        x = pow(a, d, n)
        y = 0
        for _ in range(1, s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != (n - 1):
                return False
            x = y
        if y != 1:
            return False
    return True

def main():
    n = 61
    k = 10
    print(f's, d: {calc_s_d(n)}')
    prim = miller_rabin(n, k)
    print(prim)
    # [print(f'{x} is {"prime" if miller_rabin(x, k) else "comp"}') for x in range(20)]
    
if __name__ == '__main__':
    main()