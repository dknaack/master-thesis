from search import *
from itertools import product

#
# Strategies
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

#
# Main
#

N = 2000
d = 2

def tsv_print(f, *args):
    print(*args, sep='\t', file=f)

with open('comparison.tsv', 'w') as f:
    tsv_print(f, 'Strategy', 'Polynomial', 'Preperiod', 'Period')

    names = [ 'Min', 'Max', 'JPA', 'JPA*', 'TY', 'BC∞', 'BC2', 'WC∞', 'WC2', ]
    success_rate = {name: 0 for name in names}

    total = 0
    R = QQ['x']
    x = R.gen()
    for a in range(2, 1000):
        p = x**(d+1) - a
        if not p.is_irreducible():
            continue
        K = NumberField(p, names=('x'), embedding=RR(1))
        a = K.gen()
        xs = tuple([a**i for i in range(1, d+1)])
        total += 1

        strategies = {
            'Min': fracmin,
            'Max': fracmax,
            'JPA': jacobi_perron,
            'JPA*': modified_jpa,
            'TY': tamura_yasutomi(d),
            'BC∞': BestConvergentStrategy(x, 'euclidean'),
            'BC2': BestConvergentStrategy(x, 'max'),
        }

        for i, name in enumerate(strategies):
            result = deterministic_search(xs, N, strategies[name], name)
            if result:
                success_rate[name] += 1
                print('success', name, p)

                start, period = result
                start_str = ','.join([str(i) for i in start])
                period_str = ','.join([str(i) for i in period])
            else:
                print('fail', name, p)

                start_str = ''
                period_str = ''

            tsv_print(f, name, p, start_str, period_str)
        f.flush()

with open('tables/success-rate.tsv', 'w') as f:
    print('Strategy', 'Success')
    for name, rate in success_rate.items():
        tsv_print(f, name, rate, total)
