Unix-like CMD Tools for Windows
===============================

This directory contains a collection of command line tools that 
**run on Windows**. It contains unix tools for Windows (located in `unix/`),
binaries compiled from Python scripts (located in `dist/`[^1]), and batch 
files (`.bat`) that exposes the aformentioned binary paths to Windows cmd 
(located in `batch/`).

```
.
|-- README.md
|-- batch\
|-- dist\
|-- unix\
|-- compile.sh
`-- unix.zip
```

[^1]: `compile.sh` compiles Python scripts into .exe binaries in `dist/` and 
creates executable `.bat` files in `batch/`.


## Batch File Encoding

The `.bat` files are designed to work on Windows machines in Taiwan and are 
hence big5/cp950 encoded. If the `.bat` files do not work, recoding these 
`.bat` files to the native encoding of your computer might help.


## Unix Tools Included

- sed
- iconv


## Tested Programs

```sh
body compile.sh 1 3
#> body prints lines with specified range in a file.
#> Call as:
#>   body <file> <#from> <#to>

iconv -f UTF-8 -t cp950 foo.txt > foo.big5.txt
iconv -f big5 -t UTF-8 foo.big5.txt > foo.utf8.txt

jcxl --help
#> jcxl converts ASCII tables to Excel (or CSV).
#> 
#> Call as:
#>   jcxl a.txt -o a.xlsx
#>   jcxl a.txt -o a.csv
#>   jcxl a.txt b.txt -o merged.xlsx
#> 
#> Note:
#>   jcxl expects input text files with a native encoding (i.e. Big5/cp950 on most
#>   Windows machines in Taiwan). Output CSV files would be UTF-8 encoded. The 
#>   header row in the input text files must be ASCII characters, else they would 
#>   be replaced with empty string.

python tparse.py  # (Not compiled yet)
#> tparse parses plaintext tables and exports them to csv/excel.
#> 
#>   Call as:
#>   python tparse.py table.txt output.csv
#>   python tparse.py table.txt output.xlsx
#> 
#>   In Python
#>   from tparse import tparse
#>   table = tparse("table.txt")  # tparse() returns a 2D list
#> 
#>   Note:
#>   `tparse` scans through each line of the table to determine
#>   the columns that are spanned with values. Hence, blank 
#>   columns between values are required for successful parsing.
#>   
#>   A table that could be parsed by `tparse` is shown below.
#>   Note that the character `|` are replaced with space during 
#>   parsing, and "dashed" lines with `-` spanning the full 
#>   table are ignored by `tparse`.
#> 
#>   |Score   Used   %    % |  Meas  Meas  MnSq | Residual |
#>   -------------------------------------------------------
#>   |  4       .5   2%   2%|  -.59  -1.28  1.2 |          |
#>   |  6      3.5  14%  18%|  -.78   -.32  1.6 |      2.0 |
#>   |  7      1.5   6%  24%|  -.74   -.75   .3 |          |
#>   | 10      2.5  10%  48%|  -.05   -.14   .3 |       .6 |
#>   | 11      1.0   4%  52%|   .00    .00   .6 |      -.9 |
#>   | 18       .5   2% 100%|   .59*  1.28  1.2 |          |
#>   -------------------------------------------------------

diffxl --help
#> diffxl can produce and apply tabular diffs.
#> Call as:
#>   diffxl a.csv b.csv
#>   diffxl a.tsv b.tsv --output       (write HTML output to current dir)
#>   diffxl a.xls b.xls                (1st sheet of a.xls vs. 1st sheet of b.xls)
#>   diffxl a.xls 1 b.xls 3            (1st sheet of a.xls vs. 3rd sheet of b.xls)
#>   diffxl a.xlsx 1 3                 (1st vs. 3rd sheet of a.xlsx)
#>   diffxl a.xls 1 --c1=A:D --c2=E:H  (columns A:D vs. column E:H within a sheet)
#>   diffxl a.xls 1 --c1=A:D --c2=E:   (column E:H will be inferred if H left out)
```
