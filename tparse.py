from sys import argv

DOC = '''
tparse parses plaintext tables and exports them to csv/excel.

  Call as:
  python tparse.py table.txt output.csv
  python tparse.py table.txt output.xlsx

  In Python
  from tparse import tparse
  table = tparse("table.txt")  # tparse() returns a 2D list

  Note:
  `tparse` scans through each line of the table to determine
  the columns that are spanned with values. Hence, blank 
  columns between values are required for successful parsing.
  
  A table that could be parsed by `tparse` is shown below.
  Note that the character `|` are replaced with space during 
  parsing, and "dashed" lines with `-` spanning the full 
  table are ignored by `tparse`.

  |Score   Used   %    % |  Meas  Meas  MnSq | Residual |
  -------------------------------------------------------
  |  4       .5   2%   2%|  -.59  -1.28  1.2 |          |
  |  6      3.5  14%  18%|  -.78   -.32  1.6 |      2.0 |
  |  7      1.5   6%  24%|  -.74   -.75   .3 |          |
  | 10      2.5  10%  48%|  -.05   -.14   .3 |       .6 |
  | 11      1.0   4%  52%|   .00    .00   .6 |      -.9 |
  | 18       .5   2% 100%|   .59*  1.28  1.2 |          |
  -------------------------------------------------------
'''


def main():
    # Command line utilities
    if any(x == '-h' or x == '--help' for x in argv):
        help()
        return
    try:
        INPUT = argv[1]
        OUTPUT = argv[2]
    except:
        help()
        return

    # Parse table
    table = tparse(INPUT)

    # Export to excel
    if OUTPUT.endswith(".xlsx"):
        from pandas import DataFrame
        DataFrame(table).to_excel(
            OUTPUT, index=False, header=True
        )
    # Export to csv
    else:
        import csv
        with open(OUTPUT, "w", encoding="UTF-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(table)


def tparse(fp):
    with open(fp) as f:
        file = []
        for line in f:
            line = line.rstrip().replace("|", " ")
            if " " not in line: continue
            file.append(line)

    value_cols = []
    m = get_column_filled(file)
    for i, col in enumerate(t(m)):
        if sum(col) > 0:
            value_cols.append(1)
        else:
            value_cols.append(0)

    table = []
    for i, line in enumerate(file):
        new_line = []
        term = ""
        for j, col in enumerate(line):
            if value_cols[j] == 1:
                term += col
            else:
                new_line.append(term.strip())
                term = ""
        table.append(new_line)

    # Remove empty columns
    idx = get_empty_col_idx(table)
    table2 = []
    for line in table:
        new_line = []
        for j, col in enumerate(line):
            if j in idx: continue
            new_line.append(col)
        table2.append(new_line)

    return table2



def t(x):
    """Transpose 2d list"""
    return list(map(list, zip(*x)))


def get_column_filled(file):
    filled = []
    for line in file:
        filled.append([ 
            0 if x == " " else 1 for x in line 
        ])
    return filled


def get_empty_col_idx(file):
    empty = []
    for i, c in enumerate(t(file)):
        if all(x == "" for x in c):
            empty.append(i)
    return empty


def help():
    print(DOC.strip())


if __name__ == '__main__':
    main()
