from .search import pivot, unpivot
from sage.all import *

def floor_list(list):
    return [floor(elem) for elem in list]

class MDCF:
    def __init__(self, dim, int_part):
        self.indices = []
        self.coeffs = [int_part]
        self.dim = dim

    def __repr__(self):
        result = '[' + str(self.coeffs[0])
        for l, a in zip(self.indices, self.coeffs[1:]):
            result += '; ' + str(l) + ', ' + str(a)
        result += ']'
        return result

    def append(self, l, a):
        assert len(a) == self.dim
        self.indices.append(l)
        self.coeffs.append(a)

    def value(self):
        x = self.coeffs[-1]
        for a, l in zip(self.coeffs[-2::-1], self.indices[::-1]):
            x = unpivot(x, a, l)
        return x

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
            mdcf = MDCF(d, floor_list(xs))
            ys = xs
            for i in new_seq:
                if frac(ys[l]) == 0:
                    break
                ys = pivot(ys, i)
                mdcf.append(i, floor_list(ys))
            else:
                conv = mdcf.value()
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

def regular_strategy(offset):
    return lambda x, n: (n + offset) % len(x)

class ConvergentStrategy:
    def __init__(self, x, norm):
        self.input = x
        self.convergent = floor_list(x)
        # TODO: Set norm

    def dist(self, a, b):
        return sum([(ai - bi)**2 for ai, bi in zip(a, b)])

    def __call__(self, x, n):
        closest_l = None
        for l in range(d):
            new_convergent = ...
            new_dist = self.dist(x, new_convergent)
            if closest_l is None or new_dist < closest_dist:
                closest_convergent = new_convergent
                closest_dist = new_dist
                closest_l = l
        return closest_l
