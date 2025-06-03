from search import *
from strategies import *
from itertools import product

N = 2000
d = 2

def tsv_print(f, *args):
    print(*args, sep='\t', file=f)

with open('tables/comparison.tsv', 'w') as f:
    tsv_print(f, 'Strategy', 'Polynomial', 'Preperiod', 'Period')

    strategies = {
        'Min': fracmin,
        'Max': fracmax,
        'JPA': jacobi_perron,
        'JPA*': modified_jpa,
        'TY': tamura_yasutomi(d),
        #'CC∞': BestConvergentStrategy(x, 'euclidean'),
        #'CC2': BestConvergentStrategy(x, 'max'),
    }

    success_rate = {name: 0 for name in strategies}

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
