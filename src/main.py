from math import floor

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

class Rat:
    def __init__(self, num, denom=1):
        if denom < 0:
            num = -num
            denom = -denom

        g = gcd(abs(num), denom)
        self.num = num // g
        self.denom = denom // g
        assert self.denom != 0

    def __repr__(self):
        if self.denom == 1:
            return f"{self.num}"
        else:
            return f"{self.num}/{self.denom}"

    def __hash__(self):
        return hash((self.num, self.denom))

    def __add__(self, other):
        if isinstance(other, Rat):
            num = self.num * other.denom + other.num * self.denom
            denom = self.denom * other.denom
            return Rat(num, denom)
        elif isinstance(other, int):
            return Rat(self.num + self.denom * other, self.denom)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Rat):
            num = self.num * other.denom - other.num * self.denom
            denom = self.denom * other.denom
            return Rat(num, denom)
        elif isinstance(other, int):
            return Rat(self.num - other * self.denom, self.denom)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return Rat(other * self.denom - self.num, self.denom)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Rat):
            return Rat(self.num * other.num, self.denom * other.denom)
        elif isinstance(other, int):
            return Rat(self.num * other, self.denom)
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Rat(self.num * other.denom, self.denom * other.num)

    def __rtruediv__(self, other):
        if isinstance(other, int):
            return Rat(other * self.denom, self.num)
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Rat):
            return self.num == other.num and self.denom == other.denom
        elif isinstance(other, int):
            return self.num == other and self.denom == 1
        else:
            return NotImplemented

    def __lt__(self, other):
        return self.num * other.denom < other.num * self.denom

    def __neg__(self):
        return Rat(-self.num, self.denom)

    def frac(self):
        return Rat(self.num % self.denom, self.denom)

class Poly:
    def __init__(self, *coeffs):
        if isinstance(coeffs[0], list) or isinstance(coeffs[0], tuple):
            self.coeffs = coeffs[0]
        else:
            self.coeffs = coeffs

    def __repr__(self):
        result = ''
        first = True

        for i, a in enumerate(self.coeffs):
            if a == 0: 
                continue

            if first: 
                first = False
                if a < 0:
                    result += '-'
                    a = -a
            elif a >= 0:
                result += ' + '
            else:
                a = -a
                result += ' - '

            if i == 0 or a != 1:
                result += str(a)
            if i != 0:
                result += 'x'
            if i > 1:
                result += '^' + str(i)

        return result

    def __call__(self, x):
        """
        Evaluate the polynomial at x.
        """

        return sum([c * x ** i for i, c in enumerate(self.coeffs)], 0)

    @property
    def deriv(self):
        return Poly([(i + 1) * c for i, c in enumerate(self.coeffs[1:])])

    def root(f, x=0, steps=100):
        df = f.deriv
        for i in range(steps):
            y = f(x)
            dy = df(x)

            if abs(y) < 0.001:
                return x
            if dy == 0:
                raise ValueError('Derivative is zero.')

            x -= y / dy

        raise ValueError('Could not find root with enough accuracy')

    def reflect(self):
        return Poly([c for c in reversed(self.coeffs)])

    def neg(self):
        return Poly([-c for c in self.coeffs])

class LinearRec:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    @classmethod
    def from_poly(cls, p):
        """
        Convert a characteristic polynomial back to its linear recurrence.
        """

        if p.coeffs[-1] != 1:
            raise ValueError(f"Last coefficient must be 1")

        return LinearRec([-c for c in p.coeffs[:-1]])

    def __call__(self, n):
        """
        Evaluate the linear recurrence.
        """

        order = len(self.coeffs) - 1
        xs = [0] * order + [1]
        for _ in range(n):
            x = sum([c * x for c, x in zip(self.coeffs, xs)])
            xs = xs[1:] + [x]
        return xs[0]

    def __repr__(self):
        result = f'F(n + {len(self.coeffs)}) = '
        for i, a in enumerate(self.coeffs):
            if a == 0:
                continue
            if a == -1:
                result += '-'
            elif a != 1:
                result += str(a)
            if i == 0:
                result += f'F(n) + '
            else:
                result += f'F(n + {i}) + '

        return result[:-3]

    @property
    def char_poly(self):
        """
        Returns the characteristic polynomial of the linear recurrence.
        """

        return Poly([-c for c in self.coeffs] + [1])

def solution_coeffs(d):
    coeffs = [0] * (d + 2)
    for i in range(d + 2):
        if i == 0:
            coeffs[i] = -1
        elif i == 1:
            coeffs[i] = 1
        elif i == d + 1:
            coeffs[i] = (-1) ** i
        else:
            coeffs[i] = (-1) ** i * 2
    return coeffs

def solution(d):
    p = Poly(solution_coeffs(d))
    r = 1/p.root(2)
    xs = [0] * d
    xs[0] = r
    if d > 1:
        xs[1] = 1 / r - 1
        for i in range(2, d):
            xs[i] = 2 - xs[i - 1] / r

    return xs

def frac(x):
    if isinstance(x, Rat):
        return Rat(x.num % x.denom, x.denom)
    else:
        f = x - floor(x)
        if f < 0.0001:
            return 0
        elif f > 0.9999:
            return 0
        else:
            return f

def min_frac(xs):
    fs = [i for i, x in enumerate(xs) if frac(x) != 0]
    l = min(fs, key=lambda i: xs[i]) if fs else -1
    return l

def pivot(xs, l=None):
    if all(frac(x) == 0 for x in xs):
        return xs

    # Find index with minimum fractionality
    if l is None:
        l = min_frac(xs)

    # Update the vector accordingly
    ys = [0] * len(xs)
    for i, x in enumerate(xs):
        if l == i:
            ys[i] = frac(1 / xs[l])
        else:
            ys[i] = frac(-x / xs[l])
    return tuple(ys)

def update(xs):
    steps = 0
    while any(frac(x) != 0 for x in xs):
        #xs = tuple(sorted(xs))
        steps += 1

        # Only for debugging
        print(f"{steps}.", end='')
        l = min_frac(xs)
        for i, x in enumerate(xs):
            if i == l:
                print(f' [{x}]', end='')
            else:
                print(f' {x}', end='')
        print()

        ys = pivot(xs)

        # Only for debugging
        for i, (x, y) in enumerate(zip(xs, ys)):
            if i == l:
                print(f' [{1 / x}]', end='')
            else:
                print(f' {-x / xs[l]}', end='')
        print()

        # Only for debugging
        for i, (x, y) in enumerate(zip(xs, ys)):
            if i == l:
                print(f' [{1 / x - y}]', end='')
            else:
                print(f' {y + x / xs[l]}', end='')
        print()

        xs = ys

    return steps

def ranges(*args):
    if len(args) == 1:
        for i in range(*args[0]):
            yield (i,)
    else:
        for i in ranges(*args[1:]):
            for j in range(*args[0]):
                yield (j, *i)

def reverse_pivot(ys):
    ys = tuple(sorted(ys))
    for l, yl in enumerate(ys):
        if yl == 0:
            continue

        for a, b in ranges((0, 5), (0, 5)):
            xl = frac(1 / (yl + a))
            xs = [0] * len(ys)
            for i, yi in enumerate(ys):
                if i == l:
                    xs[i] = xl
                else:
                    xs[i] = frac(xl * (b - yi))

            if tuple(sorted(pivot(xs))) == ys:
                yield tuple(sorted(xs))

def cost(xs):
    return max(xs, key=lambda x: x.denom)

def invert_dict(d):
    inverse = {}
    for k, v in d.items():
        inverse.setdefault(v, []).append(k)
    return inverse

def brute_force_search(n):
    steps = {(Rat(0), Rat(0)): 0}
    for i in ranges((1, n), (1,n), (1, n), (1, n)):
        def backtrack(xs):
            if xs in steps:
                return steps[xs]
            else:
                steps[xs] = 1 + backtrack(pivot(xs))
                return steps[xs]

        xs = (frac(Rat(i[3], i[2])), frac(Rat(i[1], i[0])))
        backtrack(xs)

    inputs = invert_dict(steps)

    mins = {k: min(v, key=lambda xs: max(xs[0].denom, xs[1].denom)) for k, v in inputs.items()}

    return steps, inputs, mins

f = LinearRec([-1, -1, -2, +2, -1])