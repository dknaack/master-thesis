from sage.all import *

def frac(x):
    return x - floor(x)

def pivot(xs, *indices):
    xs = list(xs[:])
    d = len(xs)
    for l in indices:
        xl = xs[l]
        assert frac(xl) != 0, "xl cannot be zero"
        for i in range(d):
            if i == l:
                xs[i] = 1 / frac(xs[i])
            else:
                xs[i] = frac(xs[i]) / frac(xl)
    return tuple(xs)

def sequences(base, max_digits):
    """
    Iterator for all sequences of length `max_digits` with digits in `base`.
    """
    seq = []
    while True:
        # Increment the sequence
        carry = 1
        for i in range(len(seq) - 1, -1, -1):
            seq[i] += carry
            if seq[i] == base:
                seq[i] = 0
                carry = 1
            else:
                carry = 0
                break

        if carry:
            if len(seq) < max_digits:
                seq.insert(0, 1)
            else:
                break

        yield seq

def periodic_sequences(xs, max_depth):
    d = len(xs)
    for L in sequences(d, max_depth):
        index = {xs: 0}
        ys = xs
        for i, l in enumerate(L):
            ys = pivot(ys, l)
            if ys in index:
                j = index[ys]
                start = L[:j]
                period = L[j:i+1]
                yield start, period
            else:
                index[ys] = i + 1

def brute_force_search(xs, max_depth):
    for start, period in periodic_sequences(xs, max_depth):
        return start, period

def euclidean(A, b, *indices):
    xs = A.solve_right(b)
    for l in indices:
        assert frac(xs[l]) != 0, "pivot cannot be zero"
        c = A * vector([frac(x) for x in xs])
        b = A[l]
        A.set_column(l, c)
        xs = A.solve_right(b)
    return (A, xs, b)

def get_values(xs, indices):
    for l in indices:
        yield xs
        xs = pivot(xs, l)

def get_coeffs(xs, indices):
    """
    Returns a list of coefficients from each iteration.
    """
    yield tuple([floor(xi) for xi in xs])
    for xs in get_values(xs, indices):
        yield tuple(floor(xi) for xi in xs)

def get_decrease(xs, *indices):
    """
    Gets the total decrease when pivoting xs with the specified indices.

    Returns:
    - decrease: The total decrease over all indices.
    """
    decrease = 1
    for l, ys in zip(indices, get_values(xs, indices)):
        decrease *= frac(ys[l])
    return decrease

def get_period(xs, indices):
    """
    Returns the period if it exists.
    """
    inputs = []
    for i, ys in enumerate(get_values(xs, indices)):
        try:
            repeat_start = inputs.index(ys)
            init = indices[:repeat_start]
            repeat = indices[repeat_start:i]
            return init, repeat
        except ValueError:
            inputs.append(ys)
    return [indices, []]

def get_convergent(xs, indices):
    a = [floor(xi) for xi in xs]
    if len(indices) == 0:
        return a

    l, *indices = indices
    next = get_convergent(pivot(xs, l), indices)
    curr = [0] * len(xs)

    pl, ql = next[l].numerator(), next[l].denominator()
    for i, ai in enumerate(a):
        pi, qi = next[i].numerator(), next[i].denominator()
        if i == l:
            curr[i] = (ai * pl + ql) / pl
        else:
            curr[i] = (ai * qi * pl + pi * ql) / (qi * pl)

    return curr

def repeat_list(list, n):
    """
    Repeats a list such that it has length n.

    Parameters:
    - list: The list to repeat.
    - n: The length of the target list

    Returns:
    - A list of length n.
    """
    return list * (n // len(list)) + list[:n % len(list)]

def increment_nary(number, base, max_digits):
    """
    Increments an n-ary number represented as a list.

    Parameters:
    - number (list): A list of digits representing the number in base `base`.
    - base (int): The base of the number system.
    - max_digits (int): The maximum number of digits allowed.

    Returns:
    - list: The incremented number as a list of digits, or None if overflow occurs.
    """
    # Create a copy to avoid modifying the input
    number = number[:]

    carry = 1
    for i in range(len(number) - 1, -1, -1):
        number[i] += carry
        if number[i] == base:
            number[i] = 0
            carry = 1
        else:
            carry = 0
            break

    if carry:
        if len(number) < max_digits:
            number.insert(0, 1)
        else:
            return None

    return number

def get_leaves(xs, max_depth):
    if max_depth == 0:
        return [[]]

    leaves = []
    fracs = [floor(y) for y in xs]
    for l in range(len(xs)):
        if frac(xs[l]) != 0:
            ys = pivot(xs, l)
            leaves += [[fracs, *leaf] for leaf in get_leaves(ys, max_depth - 1)]
    return leaves

#
# Utility functions for displaying the output
#

def pivot_table(xs, indices):
    rows = []
    values = get_values(xs, indices)
    coeffs = get_coeffs(xs, indices)
    for l, xs, c in zip(indices, values, coeffs):
        rows.append(tuple([l, *xs, *c]))

    header_row = [r'$\ell$', '$x_1$', '$x_2$', '$x_1$', '$x_2$', '$a_1$', '$a_2$']
    return table(rows, header_row=header_row)

def real_list(values):
    return [round(RR(a), 4) for a in values]

def real_matrix(matrix):
    return [real_list(row) for row in matrix]

def pretty_continued_fraction(init, repeat):
    repeat_str = r'\overline{' + ', '.join([str(e) for e in repeat]) + '}'
    return LatexExpr('[' + ', '.join([str (e) for e in init] + [repeat_str]) + ']')

def periodic_pivot_table(xs, init, repeat):
    return pivot_table(xs, init + repeat + [repeat[0]])

#
# Selection Functions
#

def select_min(xs):
    j = None
    for i in range(len(xs)):
        if j == None or xs[i] < xs[j]:
            j = i
    return j

def select_min2(xs):
    min_pair = None
    min_cost = 1
    for i, xi in enumerate(xs):
        for j, xj in enumerate(xs):
            if i == j:
                cost = frac(xi) * frac(1/frac(xi))
            else:
                cost = frac(xi) * frac(frac(xj)/frac(xi))
            if cost < min_cost:
                min_cost = cost
                min_pair = (i, j)
    return min_pair
