Unix-like CMD Tools for Windows
===============================

This directory contains a collection of command line tools that 
**run on Windows**. It contains unix tools for Windows (located in `unix/`),
binaries compiled from Python scripts (located in `dist/`[^1]), and batch files
(`.bat`) that exposes the aformentioned binaries' paths to Windows cmd (located 
in `batch/`).

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
hence big5/cp950 encoded. If the `.bat` files do not work, recoding these `.bat`
files to the native encoding of your computer might help.


## Unix Tools Included

- sed
- iconv


## Tested Programs

```sh
body compile.sh 1 3
# body prints lines with specified range in a file.
# Call as:
#   body <file> <#from> <#to>

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

daff 
```
