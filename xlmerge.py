DOC = '''
xlmerge merges multiple Excel/CSVs into a single Excel workbook

  Call as:
  python xlmerge.py a.xlsx b.xlsx -o merged.xlsx
  python xlmerge.py a.csv b.xlsx -o merged.xlsx
'''
import sys
from pathlib import Path
from pandas import read_csv, read_fwf, read_excel, ExcelWriter


def main():
    """Command line program"""
    args = arg_parse(sys.argv)
    if args == 1:
        help()
        return
    inputs, outfp = args['inputs'], args['outfp']
    merged_tbl = xlmerge(inputs)
    write_merged_excel(merged_tbl, outfp=outfp)
    print(f"Output: {outfp}")


def xlmerge(inputs):
    """Merge multiple Excel/CSV tables into a dictionary of `pd.DataFrame`s.

    Parameters
    ----------
    inputs : list
        A list of `pathlib.Path` objects pointing to the file holding 
        input tables (.xlsx/.csv/.tsv...).

    Returns
    -------
    dict
        A dictionary with pd.DataFrames as values and sheet or file names of
        the input files as keys.
    """
    merged_tbl_dict = {}
    for fp in inputs:
        tbls = read_tables(fp)
        for nm, tbl in tbls.items():
            i = 1; nmo = nm
            while nm in merged_tbl_dict: 
                nm = f"{nmo}_{i}"; i += 1
            merged_tbl_dict[nm] = tbl
    return merged_tbl_dict


def arg_parse(argv):
    out = Path("merged.xlsx")
    if '-o' in argv:
        idx = argv.index('-o') + 1
        try:
            out = Path(argv[idx])
            argv = [ x for i, x in enumerate(argv) if i not in (idx, idx - 1) ]
        except: return 1
    if len(argv) < 2: return 1
    inputs = [ Path(x) for x in argv if not x.endswith(".py") ]
    return { 'outfp': out, 'inputs': inputs }


def write_merged_excel(merged_tbl_dict, outfp):
    with ExcelWriter(outfp) as writer:  
        for nm, df in merged_tbl_dict.items():
            df.to_excel(writer, sheet_name=nm, header=False, index=False)


def read_tables(fp):
    """Reads and returns tables as a dictionary of dataframes"""
    ext = fp.suffix.lower()
    nm = fp.stem
    if ext == '.csv':   tbl = { nm: read_csv(fp, header=None) }
    elif ext == '.tsv': tbl = { nm: read_csv(fp, sep="\t", header=None) }
    elif ext == '.txt': tbl = { nm: read_fwf(fp) }
    elif ext in ('.xlsx', '.xls', 'xlsm', 'xlsb'): 
        tbl = read_excel(fp, sheet_name=None, header=None)
        if len(tbl) == 1:
            if list(tbl.keys())[0].lower() in ( "sheet1", "工作表1" ):
                tbl = { nm: list(tbl.values())[0] }
    else:
        raise Exception("Unsupported input file types.")
    return tbl

def help():
    print(DOC.strip())


if __name__ == '__main__':
    main()
