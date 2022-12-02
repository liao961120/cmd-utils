#%%
import sys
import pandas as pd
from pathlib import Path

DOC = """
xl2csv converts an excel file to csv(s).
Call as:
  xl2csv <a.xlsx>        (Convert the 1st sheet of a.xlsx to a csv file)
  xl2csv <a.xlsx> 2      (Convert the 2nd sheet of a.xlsx to a csv file)
  xl2csv <a.xlsx> 1,3    (Convert the 1st & 3rd sheet of a.xlsx to csv files)
  xl2csv <a.xlsx> all    (Convert each sheet of a.xlsx to a csv file)
  xl2csv <a.csv>         (Recode cp950 to utf8)
"""

def main():
    args = [ x.strip() for x in sys.argv if x.strip() != "" ]
    fin = Path(args[1])

    if '--help' in args:
        print_help()
        return

    if fin.suffix != ".xls" and fin.suffix != ".xlsx":
        outfp = recode_file(fin)
        print_output([outfp])
        return

    if len(args) == 2:
        # xl2csv file.xls
        outfps = to_csv(fin, sheet_name=[0], usecols=None)
    elif len(args) == 3:
        a2 = args[2]
        if a2 == "all" or a2 == "a" or a2 == "--all" or a2 == "-a":
            outfps = to_csv(fin, sheet_name=None, usecols=None)
        else:
            sheets = [int(x) - 1 for x in a2.split(",")]
            outfps = to_csv(fin, sheet_name=sheets, usecols=None)

    else:
        print("Unexpected inputs.")
        print("  Type in `xl2csv --help` for instructions.")
        return
    
    print_output(outfps)

#%%
#%%

def to_csv(fin, sheet_name=0, usecols=None):
    outfps = []
    if sheet_name is None or isinstance(sheet_name, list):
        sheets = pd.read_excel(fin, 
            sheet_name=sheet_name, 
            usecols=usecols,
            header=None)
        for i, df in sheets.items():
            outfp = f"{fin.stem}_{i+1}{fin.suffix}.csv"
            df.to_csv(outfp, header=False, index=False)
            outfps.append(outfp)
    else:
        print("unexpected input")

    return outfps


def recode_file(fin):
    with open(fin, encoding="cp950") as f:
        content = f.read()
    fout = fin.parent / f"{fin.stem}.utf8{fin.suffix}"
    with open(fout, "w", encoding="utf-8") as f:
        f.write(content)
    return fout


def print_help():
    global DOC
    print(DOC.strip())


def print_output(fps):
    if len(fps) == 1:
        print(f"Output: `{fps[0]}`")
        return
    print("Outputs: ")
    for fp in fps:
        print(f"  `{fp}`")



if __name__ == '__main__':
    main()
