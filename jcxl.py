#%%
import jc
import sys
import pandas as pd
from pathlib import Path

DOC = '''
jcxl converts ASCII tables to Excel (or CSV).

Call as:
  jcxl a.txt -o a.xlsx
  jcxl a.txt -o a.csv
  jcxl a.txt b.txt -o merged.xlsx

Note:
  jcxl expects input text files with a native encoding (i.e. Big5/cp950 on most
  Windows machines in Taiwan). Output CSV files would be UTF-8 encoded. The 
  header row in the input text files must be ASCII characters, else they would 
  be replaced with empty string.
'''

def main():
    if print_help(sys.argv) == 1: return
    
    outfp = "jcxl.out.xlsx"
    args = [ '-o' if x == '--output' else x for x in sys.argv[1:] ]
    if '-o' in args:
        outfp = args.index("-o") + 1
        outfp = args[outfp]
    fps = [ x for x in args if x not in (outfp, '-o') ]
    outtype = Path(outfp).suffix
    if outtype not in [".xlsx", ".xls", ".csv"]:
        print("Unsupported format for output.")
        print("Only `.xlsx`, `.xls`, and `.csv` are supported.")
        return

    if len(fps) == 1:
        fp = fps[0]
        result = jc.parse("asciitable", read_file(fp))
        d = pd.DataFrame(result)
        if outtype == '.csv':
            d.to_csv(outfp, index=False, header=True)
        else:
            d.to_excel(outfp, index=False, header=True)
    else:
        dfs = []
        for fp in fps:
            result = jc.parse("asciitable", read_file(fp))
            d = pd.DataFrame(result)
            dfs.append(d)
        if outtype == '.csv':
            print("Cannot create multiple sheets in .csv plaintext!")
            print("Use Excel (.xlsx) as output format!")
            print("Exiting...")
            return
        with pd.ExcelWriter(outfp) as writer:
            for fp, df in zip(fps, dfs):
                df.to_excel(writer, sheet_name=fp, index=False, header=True)


def read_file(fp):
    with open(fp) as f:
        return f.read()


def print_help(args):
    if '--help' in args or '-h' in args:
        global DOC
        print(DOC.strip())
        return 1
    return 0




if __name__ == '__main__':
    main()

#%%
