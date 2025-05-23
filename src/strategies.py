from search import pivot, unpivot
from sage.all import *
import random

def floor_list(list):
    return [floor(elem) for elem in list]

def mdcf(coeffs):
    if len(coeffs) == 0:
        raise ValueError("The list is empty")
    elif len(coeffs) == 1:
        return coeffs[0]
    else:
        return unpivot(mdcf(coeffs[1:]), coeffs[0])

#
# Nondeterministic Strategies
#

class ApproxStrategy:
    def __init__(self, threshold):
        self.threshold = threshold

    def __call__(self, xs, seq):
        d = len(xs)
        for l in range(d):
            # Construct an MDCF from the new sequence
            new_seq = seq + [l]
            cf = [floor_list(xs)]
            ys = xs
            for i in new_seq:
                if frac(ys[l]) == 0:
                    break
                ys = pivot(ys, i)
                cf += [floor_list(ys)]
            else:
                conv = mdcf(cf)
                q = lcm([x.denominator() for x in conv])

                # Check if the convergent is a good simultaneous approximation
                approx_rate = max([abs(x - p) for x, p in zip(xs, conv)])
                if approx_rate <= self.threshold/q**(1+1/d):
                    yield l

#
# Deterministic Strategies
#

def min_strategy(x, n):
    l = None
    for i, xi in enumerate(x):
        if frac(xi) == 0:
            continue
        if l is None or xi < x[l]:
            l = i
    return l

def max_strategy(x, n):
    l = None
    for i, xi in enumerate(x):
        if frac(xi) == 0:
            continue
        if l is None or xi > x[l]:
            l = i
    return l

def jpa_strategy(x, n):
    return n % len(x)

def random_strategy(x, n):
    d = len(x)
    indices = list(range(d))
    return random.choice(indices)

def fixed_strategy(sequence):
    return lambda x, n: sequence[n % len(sequence)]

def regular_strategy(offset):
    return lambda x, n: (n + offset) % len(x)

def tamura_yasutomi(x, n):
    def frac(x):
        return x - floor(x)
    a = frac(x[0])**2 / frac(x[0]).norm()
    b = frac(x[1])**2 / frac(x[1]).norm()
    return 0 if a > b else 1

class BestConvergentStrategy:
    def __init__(self, x, norm):
        self.input = x
        self.conv = [floor_list(x)]
        self.norm = norm

    def __call__(self, x, n):
        # Compute the distances for the next convergents
        d = len(x)
        dist = [0] * d
        for l in range(d):
            y = pivot(x, l)
            approx = mdcf(self.conv + [floor_list(y)])
            diff = [abs(xi - yi) for xi, yi in zip(self.input, approx)]
            if self.norm == 'max':
                dist[l] = max(diff)
            else:
                # We do not need sqrt, because we're only comparing distances
                dist[l] = sum([d*d for d in diff])

        # Find the minimum
        min = 1
        for l in range(1, d):
            if dist[min] >= dist[l]:
                min = l
        y = pivot(x, l)
        a = floor_list(y)
        self.conv.append(a)
        return min
