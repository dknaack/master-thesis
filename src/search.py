from sage.all import *
from sys import stdout

def frac(x):
    return x - floor(x)

def pivot(x, *indices):
    for l in indices:
        y = list(x)
        assert frac(x[l]) != 0, "xl cannot be zero"
        for i in range(len(x)):
            if i == l:
                y[i] = 1 / frac(x[i])
            else:
                y[i] = frac(x[i]) / frac(x[l])
        x = tuple(y)
    return x

def unpivot(coeffs):
    x = coeffs.pop()
    d = len(x)

    while len(coeffs) > 0:
        # Determine the pivot, which is the maximum element
        l = None
        for i in range(d):
            if l is None or x[l] < x[i]:
                l = i

        # Unpivot using x[l]
        a = coeffs.pop()
        y = list(x)
        for i in range(d):
            if i == l:
                y[i] = a[i] + 1 / x[i]
            else:
                y[i] = a[i] + x[i] / x[l]
        x = y

    return tuple(x)

def floor_list(x):
    return [floor(xi) for xi in x]

def convergent(x, *indices):
    a = floor_list(x)
    coeffs = [tuple(a)]
    for l in indices:
        x = pivot(x, l)
        a = floor_list(x)
        coeffs.append(tuple(a))
    return coeffs

def convergent_matrix(x, *indices):
    d = len(x)

    def reflect(pivot, d=d):
        result = identity_matrix(d+1)
        result.swap_columns(0, pivot+1)
        return result

    def skew(a, d=d):
        result = identity_matrix(d+1)
        result.set_column(0, [1, *a])
        return result

    result = identity_matrix(d+1)
    a = floor_list(x)
    result *= skew(a)
    for l in indices:
        x = pivot(x, l)
        a = floor_list(x)
        result *= reflect(l)
        result *= skew(a)
    return result

def brute_force_search(x, N):
    """
    Searches all possible sequences of a given maximum length to find a
    periodic representation of the given input.

    INPUT:
    
    - ``x`` -- tuple; The input tuple that is to be represented. It should
      contain only algebraic numbers with the same degree as its length. For
      example, (a, a^2) for an algebraic number a.

    - ``N`` -- integer; The maximum search depth

    OUTPUT: Either

    - a tuple for the preperiod and period of the indices required to create an
      MDCF for the original input vector or

    - `None` if no periodic representation was found.
    """
    from itertools import product

    d = len(x)
    indices = list(range(d))
    for n in range(N):
        for L in product(indices, repeat=n):
            y = x
            seen = {y: 0}
            for i in range(n):
                y = pivot(y, L[i])
                if y in seen:
                    j = seen[y]
                    start = L[:j]
                    period = L[j:i+1]
                    return start, period
                else:
                    seen[y] = i + 1

def deterministic_search(x, N, strat, name='Unknown'):
    """
    Searches only one possible sequences of a given maximum length to find a
    periodic representation of the given input.

    INPUT:
    
    - ``x`` -- tuple; The input tuple that is to be represented. It should
      contain only algebraic numbers with the same degree as its length. For
      example, (a, a^2) for an algebraic number a.

    - ``N`` -- integer; The maximum search depth

    - ``strat`` -- function; The strategy to be used when searching. It is
      given the current input and should only output one index.

    OUTPUT: Either

    - a tuple for the preperiod and period of the indices required to create an
      MDCF for the original input vector or

    - `None` if no periodic representation was found.
    """
    d = len(x)
    y = x
    L = []
    seen = {y: 0}
    for n in range(N):
        if (n & 31) == 1:
            print(name, n, end='\r')
            stdout.flush()

        l = strat(y, n)
        L.append(l)
        y = pivot(y, l)
        if y in seen:
            j = seen[y]
            start = L[:j]
            period = L[j:n+1]
            return start, period
        else:
            seen[y] = n + 1
