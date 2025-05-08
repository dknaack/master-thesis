from src.search import pivot

table = [
        (2,  [1], [0,1]),
        (3,  [0,1], [0,1]),
        (4,  [0], [0,1,0,0,1,1,0,0]),
        (5,  [0], [0,0,1,1,1,0,0,0]),
        (6,  [0], [0,0,1,1,1,0,0,0]),
        (7,  [0], [0,1,0,1,0,0]),
        (9,  [0,1], [0,1]),
        (10, [0], [1,1,0,0]),
        (11, [0], [1,1,0,0]),
        (12, [1], [0,1,1,1,0,1,1,1,0,1]),
        (13, [0,0], [0,1,0,0,0,0]),
        (14, [0,1,0,1], [0,1,0,1]),
        (15, [0,0,1], [0,0,1,0,0,1]),
        (16, [0], [0,1,0,0,1,0,0,1,0,1,0,1,0,0]),
        (17, [0,0,0], [1,1,1,1,0,0,0,0]),
        (18, [0,0,0,0,0,1], [0,0,0,0,0,1]),
        (19, [0,0,1], [1,1,0,0,0,1]),
        (20, [0], [0,1,1,0,0,1,0,0]),
        (21, [0,0,0], [1,1,0,0,1,0,0,0]),
        (22, [0,0,1,0,0,1], [0,0,1,0,0,1]),
        (23, [0], [0,0,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0,1,0,0]),
        (24, [0], [0,0,1,0,1,1,0,0]),
        (25, [1], [0,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1]),
        (26, [0,0,0], [1,0,0,0]),
        (28, [0,1], [0,1]),
        (30, [0], [1,1,0,0]),
        (31, [1,1,0,0], [1,1,0,1,0,0]),
        (32, [1], [0,0,1,0,0,0,0,1,0,0,1,1,0,1]),
]

def format_vector(x):
    return r'\begin{matrix}' \
            + r' \\ '.join(str(xi) for xi in x)  \
            + r' \\ \end{matrix}\,\, '

def print_table(table):
    print(r'\begin{minipage}{0.48\textwidth}')
    print(r'\footnotesize')
    print(r'\begin{tabular}{ll}')
    print(r'\uzlhline')
    print(r'\uzlemph{$x$} & \uzlemph{MDCF} \\ \hline')
    for r, start, period in table:
        x = var('x')
        K.<a> = NumberField(x^3 - r, embedding=RR(1))
        x = (a, a^2)
        args = (tuple([floor(xi) for xi in x]),)
        print(rf'$\sqrt[3]{{{r}}}$', r'& $\left[')
        print(format_vector([''] + [floor(xi) for xi in x]), sep=', ')

        for l in start[:-1]:
            x = pivot(x, l)
            print(format_vector([l+1] + [floor(xi) for xi in x]), sep=', ')

        print(r'\overline{')
        for l in start[-1:] + period[:-1]:
            x = pivot(x, l)
            print(format_vector([l+1] + [floor(xi) for xi in x]), sep=', ')
        print(r'}\right]$ \\')
    print(r'\uzlhline')
    print(r'\end{tabular}')
    print(r'\end{minipage}')

print_table(table[:len(table)//2])
print_table(table[len(table)//2:])
