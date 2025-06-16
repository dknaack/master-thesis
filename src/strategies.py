from search import pivot, unpivot, floor_list
from sage.all import *
import random

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
                conv = unpivot(cf)
                q = lcm([x.denominator() for x in conv])

                # Check if the convergent is a good simultaneous approximation
                approx_rate = max([abs(x - p) for x, p in zip(xs, conv)])
                if approx_rate <= self.threshold/q**(1+1/d):
                    yield l

#
# Deterministic Strategies
#

def frac(x):
    return x - floor(x)

def fracmin(x, n):
    l = None
    for i, xi in enumerate(x):
        if frac(xi) == 0:
            continue
        if l is None or xi < x[l]:
            l = i
    return l

def fracmax(x, n):
    l = None
    for i, xi in enumerate(x):
        if frac(xi) == 0:
            continue
        if l is None or xi > x[l]:
            l = i
    return l

def jacobi_perron(x, n):
    return n % len(x)

def modified_jpa(x, n):
    def frac(x):
        return x - floor(x)
    a = frac(x[0])/frac(sum(x))
    b = frac(x[1])/frac(sum(x))
    return 0 if a > b else 1

def random_strategy(x, n):
    d = len(x)
    indices = list(range(d))
    return random.choice(indices)

def fixed_strategy(sequence):
    return lambda x, n: sequence[n % len(sequence)]

def regular_strategy(offset):
    return lambda x, n: (n + offset) % len(x)

def tamura_yasutomi(d):
    def frac(x):
        return x - floor(x)

    def strat(x, n):
        y = list(x)
        for i in range(d):
            y[i] = frac(x[i])**(d+1) / abs(frac(x[i]).norm())
        return y.index(max(y))

    return strat

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
            approx = unpivot(self.conv + [floor_list(y)])
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
        y = pivot(x, min)
        a = floor_list(y)
        self.conv.append(a)
        return min

class MinCost:
    def __init__(self, x, norm):
        self.input = x
        self.conv = [floor_list(x)]
        self.norm = norm

    def __call__(self, x, n):
        # Compute the distances for the next convergents
        d = len(x)
        cost = [0] * d
        for l in range(d):
            y = pivot(x, l)
            approx = unpivot(self.conv + [floor_list(y)])
            cost[l] = max([max(xi.numerator(), xi.numerator()) for xi in approx])

        # Find the minimum
        min = 1
        for l in range(1, d):
            if cost[min] >= cost[l]:
                min = l
        y = pivot(x, l)
        a = floor_list(y)
        self.conv.append(a)
        return min
