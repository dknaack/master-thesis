from search import *
from strategies import *
from contextlib import redirect_stdout
from sys import argv, stderr
from sage.all import *

def str_list(xs):
    return [str(x) for x in xs]

def generate_period_table(output):
    with redirect_stdout(output):
        print('$n^3$', 'Pre-period', 'Period')
        numbers = set(range(2, 31)) - set([x**3 for x in range(5)])
        for r in numbers:
            K = NumberField(x^3 - r, embedding=RR(1))
            a = K.gen()
            xs = (a, a^2)
            start, period = brute_force_search(xs, 24)

            start_str = ','.join(str_list(start))
            period_str = ','.join(str_list(period))
            print(r, start_str, period_str, sep='\t')

def min_fib(d, n, mem={}):
    if n < d:
        mem[(d, n)] = 1
    elif n not in mem:
        mem[(d, n)] = sum([min_fib(d, n - 1 - i) for i in range(d + 1)])
    return mem[(d, n)]

def max_fib(d, n, mem={}):
    if n < d:
        mem[(d, n)] = 1
    elif n not in mem:
        mem[(d, n)] = max_fib(d, n - 1) + max_fib(d, n - 1 - d)
    return mem[(d, n)]

def generate_fibonacci(output, F):
    n_max = 10
    d_max = 7
    with redirect_stdout(output):
        print('d', 'phi', *[f'F({i})' for i in range(n_max)], sep='\t')
        for d in range(1, d_max):
            phi = F(d, 20) / F(d, 19)
            print(d, round(phi, 5), *[F(d, i) for i in range(n_max)], sep='\t')

def generate_strategy_comparison():
    R = QQ['x']
    x = R.gen()
    for r in range(2, 51):
        p = x^3 - r
        if not p.is_irreducible():
            continue
        K = NumberField(p, embedding=RR(1))
        a = K.gen()
        deterministic_search((a, a^2), 10000, jpa_strategy)

if __name__ == '__main__':
    if len(argv) < 2:
        print("not enough arguments")
    elif argv[1] == 'cubics':
        with open('tables/cubics.tsv', 'w') as f:
            generate_period_table(f)
    elif argv[1] == 'fibonacci':
        with open('tables/min-fibonacci.tsv', 'w') as f:
            generate_fibonacci(f, min_fib)
        with open('tables/max-fibonacci.tsv', 'w') as f:
            generate_fibonacci(f, max_fib)
