import sys
import shutil
import subprocess
from pathlib import Path
from pandas import read_excel, DataFrame
from jc.parsers.asciitable import parse as jc_parse

DOC = '''
diffxl can produce and apply tabular diffs.
Call as:
  diffxl a.csv b.csv
  diffxl a.txt b.txt                (ascii table)
  diffxl a.tsv b.tsv --output       (write HTML output to current dir)
  diffxl a.xls b.xls                (1st sheet of a.xls vs. 1st sheet of b.xls)
  diffxl a.xls 1 b.xls 3            (1st sheet of a.xls vs. 3rd sheet of b.xls)
  diffxl a.xlsx 1 3                 (1st vs. 3rd sheet of a.xlsx)
  diffxl a.xls 1 --c1=A:D --c2=E:H  (columns A:D vs. column E:H within a sheet)
  diffxl a.xls 1 --c1=A:D --c2=E:   (column E:H will be inferred if H left out)
'''

CALLED = 0

def main():
    args = [ x.strip() for x in sys.argv if x.strip() not in ["", '--output', '-o'] ]
    output = True if ('--output' in sys.argv or '-o' in sys.argv) else False
    # print(sys.argv)
    if len(args) == 2 and (args[1].endswith('help') or args[1] == '-h'):
        print_help()
        return
    
    if any(x.startswith('--c1') for x in args):
        # diffxls a.xls 1 --c1=A:D --c2=E:H
        xls, n = Path(args[1]), int(args[2])
        opts = sorted(x for x in args if x.startswith('--c'))
        c1, c2 = opts[0].split('=')[-1], opts[1].split('=')[-1]
        if c2.endswith(":"):
            s1, e1 = c1.split(":")
            diff = alpha2num(e1) - alpha2num(s1)
            s2 = alpha2num(c2.rstrip(":"))
            e2_alpha = num2alpha(s2 + diff)
            c2 += e2_alpha
        fp1 = to_csv(xls, sheet_name=n - 1, usecols=c1)
        fp2 = to_csv(xls, sheet_name=n - 1, usecols=c2)
        fin_id = f"{xls.stem}_{n}_{c1.replace(':', '2')}-{c2.replace(':', '2')}"
    elif len(args) == 3:
        # Use case: diffsheet <file1.xls> <file2.xls>
        xls1, xls2 = Path(args[1]), Path(args[2])
        fp1 = to_csv(xls1, 0)
        fp2 = to_csv(xls2, 0)
        fin_id = f"{xls1.stem}-{xls2.stem}"
    elif len(args) == 4:
        # Use case: diffsheet <file.xls> <num1> <num2>
        xls, n1, n2 = Path(args[1]), int(args[2]), int(args[3])
        fp1 = to_csv(xls, n1 - 1)
        fp2 = to_csv(xls, n2 - 1)
        fin_id = f"{xls.stem}_{n1}-{n2}"
    elif len(args) == 5:
        # Use case: diffsheet <file1.xls> <num1> <file2.xls> <num2>
        xls1, xls2 = Path(args[1]), Path(args[3])
        n1, n2 = int(args[2]), int(args[4])
        fp1 = to_csv(xls1, n1 - 1)
        fp2 = to_csv(xls2, n2 - 1)
        fin_id = f"{xls1.stem}_{n1}-{xls2.stem}_{n2}"
    else:
        return
    
    if output:
        outfp = f"diff.{fin_id}.html"
        subprocess.run(["daff", "--output", outfp, "--index", fp1, fp2])
        open_in_browser(outfp)
    else:
        subprocess.run(["daff", "--www", "--index", fp1, fp2])
    Path(fp1).unlink()
    Path(fp2).unlink()


def to_csv(fin, sheet_name=0, usecols=None):
    global CALLED
    CALLED += 1

    tmpf = (Path("~") / f"diffxls.py_{fin.stem}_{sheet_name}_{CALLED}.csv").expanduser().as_posix()
    
    if fin.suffix == ".xlsx" or fin.suffix == ".xls":
        read_excel(fin, sheet_name=sheet_name, usecols=usecols).to_csv(tmpf)
    else: 
        if fin.suffix == ".tsv" or fin.suffix == ".csv":
            shutil.copyfile(fin, tmpf)
        # Treat as ASCII table
        else:
            result = jc_parse(read_file(fin))
            DataFrame(result).to_csv(tmpf, index=False, header=True)


    return tmpf

#%%
from pathlib import Path
s = Path("a.x")
#%%

def alpha2num(s):
    """ Convert base26 column string to number. """
    expn = 0
    col_num = 0
    for char in reversed(s.upper()):
        col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1

    return col_num - 1

def num2alpha(num):
    num = num + 1
    return num2alpha_r(num)

def num2alpha_r(num, res = ""):
    return num2alpha_r(
        (num - 1) // 26, 
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[(num - 1) % 26] + res
    ) if num > 0 else res


#%%
def open_in_browser(fp):
    fp = Path(fp).absolute().as_posix()
    # webbrowser.open(f"file:///{fp}")
    subprocess.run(["explorer", f"file:///{fp}"])


def print_help():
    global DOC
    print(DOC.strip())


def read_file(fp):
    with open(fp) as f:
        return f.read()



if __name__ == '__main__':
    main()



# %%
# ['a', 'c'].index('c')