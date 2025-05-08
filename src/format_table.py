import csv

opts = {'sep': ' & ', 'end': ' \\\\\n'}
with open('tables/cubics.tsv', 'r') as file:
    file_without_comments = filter(lambda line: not line.startswith('#'), file)
    reader = csv.reader(file_without_comments, delimiter='\t')
    header = next(reader)
    print(r'\begin{tabular}{ll}')
    print(r'\uzlhline')
    print(r'\uzlemph{$p(x)$}', r'\uzlemph{Index Sequence}', **opts)
    print(r'\hline')
    for i, row in enumerate(reader):
        if row[1] != '-':
            preperiod = ''.join([str(int(s) + 1) for s in row[1].split(',')])
            period = ''.join([str(int(s) + 1) for s in row[2].split(',')])
            print(row[0], '$' + preperiod + r'\overline{' + period + '}$', **opts)
        else:
            print(row[0], '-', **opts)
    print(r'\uzlhline')
    print(r'\end{tabular}')
