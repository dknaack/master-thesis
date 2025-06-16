from sage.all import *
from search import pivot
from sys import stdout

class ApproxStrategy:
    """
    The approximation strategy only outputs sequences,
    whose convergent satisfies the approximation bound. 
    """

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
        print('iteration', n, len(sequences))
        new_sequences = []
        for L in sequences:
            y = x
            for i, l in enumerate(L):
                y = pivot(y, l)
            for l in strat(x, L):
                new_sequences.append(L + [l])
        sequences = new_sequences
        if not sequences:
            raise ValueError('No more sequences')

# The search tests every MCF for the number of convergents that satisfy the
# approximation bound from Dirichlet's approximation theorem.
# The output is a series of instructions. They are roughly structured like:
#
# - root r
#   - approximation c 
#     - iteration n
#     - success, fail or nothing
#
# These can then be parsed to only output approximations with c = 1 or only
# approximations that fail, etc.

d = 2
N = 20

R = QQ['x']
x = R.gen()
for r in range(2, 101):
    # Generate the (d+1)-th root of r
    p = x**(d+1) - r
    if not p.is_irreducible():
        continue
    a = NumberField(p, names=('x'), embedding=RR(1)).gen()
    # Create an input vector for the search
    xs = tuple([a**i for i in range(1, d+1)])

    print('root', r)
    for c in range(1, 6):
        print('approximation', c)
        try:
            if nondeterministic_search(xs, N, ApproxStrategy(c)):
                print('success')
            break
        except ValueError:
            print('fail')
        stdout.flush()
