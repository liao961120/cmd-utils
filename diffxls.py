#%%
import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path

DOC = '''
diffxls can produce and apply tabular diffs.
Call as:
  diffxls a.csv b.csv
  diffxls a.tsv b.tsv
  diffxls a.xls b.xls                (1st sheet of a.xls vs. 1st sheet of b.xls)
  diffxls a.xls 1 b.xls 3            (1st sheet of a.xls vs. 3rd sheet of b.xls)
  diffxls a.xlsx 1 3                 (1st vs. 3rd sheet of a.xlsx)
  diffxls a.xls 1 --c1=A:D --c2=E:H  (columns A:D vs. column E:H within a sheet)
'''

# Usage: diffxls <file1.csv> <file2.csv>
#        diffxls <file1.xls> <file2.xls>
#        diffxls <file.xls> <num1> <num2>
#        diffxls <file1.xls> <num1> <file2.xls> <num2>

CALLED = 0

def main():
    args = [ x.strip() for x in sys.argv if x.strip() != "" ]
    print(sys.argv)
    if len(args) == 2 and (args[1].endswith('help') or args[1] == '-h'):
        print_help()
        return
    
    if any(x.startswith('--c1') for x in args):
        # diffxls a.xls 1 --c1 A:D --c2 E:H
        xls, n = args[1], int(args[2])
        opts = sorted(x for x in args if x.startswith('--c'))
        c1, c2 = opts[0].split('=')[-1], opts[1].split('=')[-1]
        fp1 = to_csv(xls, sheet_name=n - 1, usecols=c1)
        fp2 = to_csv(xls, sheet_name=n - 1, usecols=c2)
    elif len(args) == 3:
        # Use case: diffsheet <file1.xls> <file2.xls>
        xls1, xls2 = args[1], args[2]
        fp1 = to_csv(xls1, 0)
        fp2 = to_csv(xls2, 0)
    elif len(args) == 4:
        # Use case: diffsheet <file.xls> <num1> <num2>
        xls, n1, n2 = args[1], int(args[2]), int(args[3])
        fp1 = to_csv(xls, n1 - 1)
        fp2 = to_csv(xls, n2 - 1)
    elif len(args) == 5:
        # Use case: diffsheet <file1.xls> <num1> <file2.xls> <num2>
        xls1, xls2 = args[1], args[3]
        n1, n2 = int(args[2]), int(args[4])
        fp1 = to_csv(xls1, n1 - 1)
        fp2 = to_csv(xls2, n2 - 1)
    else:
        return
    
    print("running")
    subprocess.run(["daff", "--www", "--index", fp1, fp2])
    Path(fp1).unlink()
    Path(fp2).unlink()


def to_csv(fin, sheet_name=0, usecols=None):
    global CALLED
    CALLED += 1

    tmpf = (Path("~") / f"diffxls.py_{fin}_{sheet_name}_{CALLED}.csv").expanduser().as_posix()
    
    if fin.endswith(".xlsx") or fin.endswith(".xls"):
        pd.read_excel(fin, sheet_name=sheet_name, usecols=usecols).to_csv(tmpf)
    else: 
        #fin.lower().endswith(".tsv") or fin.lower().endswith(".csv"):
        # pd.read_csv(fin).to_csv(tmpf)
        shutil.copyfile(fin, tmpf)
    
    return tmpf


def print_help():
    global DOC
    print(DOC.strip())


if __name__ == '__main__':
    main()



# %%
# ['a', 'c'].index('c')