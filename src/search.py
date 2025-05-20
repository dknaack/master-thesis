from sage.all import *

def frac(x):
    return x - floor(x)

def pivot(x, *indices):
    y = [0 for _ in x]
    for l in indices:
        assert frac(x[l]) != 0, "xl cannot be zero"
        for i in range(len(x)):
            if i == l:
                y[i] = 1 / frac(x[i])
            else:
                y[i] = frac(x[i]) / frac(x[l])
    return tuple(y)

def unpivot(x, a):
    d = len(x)

    # Determine the pivot, which is the maximum element
    l = None
    for i in range(d):
        if l is None or x[l] < x[i]:
            l = i

    # Unpivot using x[l]
    y = [0 for _ in range(d)]
    for i in range(d):
        if i == l:
            y[i] = a[i] + 1 / x[i]
        else:
            y[i] = a[i] + x[i] / x[l]

    return tuple(y)

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

def deterministic_search(x, N, strat):
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

def nondeterministic_search(x, N, strat):
    """
    Searches only multiple possible sequences using the given strategy to find a
    periodic representation of the given input.

    INPUT:
    
    - ``x`` -- tuple; The input tuple that is to be represented. It should
      contain only algebraic numbers with the same degree as its length. For
      example, (a, a^2) for an algebraic number a.

    - ``N`` -- integer; The maximum search depth

    - ``strat`` -- function; The strategy to be used when searching. It is
      given the original input and one of the possible sequence. It should
      output a list of indices, which are appended to the create longer
      sequences.

    OUTPUT: Either

    - a tuple for the preperiod and period of the indices required to create an
      MDCF for the original input vector or

    - `None` if no periodic representation was found.
    """
    d = len(x)
    sequences = [[]]
    for n in range(N):
        new_sequences = []
        for L in sequences:
            y = x
            seen = {y: 0}
            for l in L:
                y = pivot(y, l)
                seen[y] = i + 1
            for l in strat(x, L):
                z = pivot(y, l)
                if z in seen:
                    j = seen[z]
                    start = L[:j]
                    period = L[j:i+1]
                    return start, period
                else:
                    new_sequences.append(L + [l])
        sequences = new_sequences
