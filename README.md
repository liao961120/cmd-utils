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
