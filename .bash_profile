cd ~/Desktop

export PATH=$PATH:/c/Users/rd/bin
export PATH=$PATH:/c/Users/rd/AppData/Local/Programs/R/R-4.2.2/bin
export PATH=$PATH:/c/Users/rd/py3.11/Scripts


2utf() {
    # Usage:  cat <file> | 2utf
    stdin=$(</dev/stdin)
    echo "$stdin" > tmp.txt
    powershell -command "Get-Content tmp.txt" > tmp.utf8.txt
    cat tmp.utf8.txt
    rm tmp.txt tmp.utf8.txt
}

body() {
    # body <file.txt> <#from> <#to> 
    # body a.txt 1 10  (print the first 10 lines)
    # body a.txt 3 10  (print L3~L10)
    # body a.txt 3     (print L1 to the last line)
    sed -n "${2-1},${3-\$}p" "${1}"
}

jcxl() {
    # jcxl a.txt -o a.xlsx
    # jcxl a.txt -o a.csv
    # jcxl a.txt b.txt -o merged.xlsx
    python /c/Users/rd/bin/jcxl.py "$@"
}

xl2csv() {
    # xl2csv <a.xlsx>        (Convert the 1st sheet of a.xlsx to a csv file)
    # xl2csv <a.xlsx> 2      (Convert the 2nd sheet of a.xlsx to a csv file)
    # xl2csv <a.xlsx> 1,3    (Convert the 1st & 3rd sheet of a.xlsx to csv files)
    # xl2csv <a.xlsx> all    (Convert each sheet of a.xlsx to a csv file)
    # xl2csv <a.csv>         (Recode cp950 to utf8)
    python /c/Users/rd/bin/xl2csv.py "$1" "$2" "$3"
}

difff() {
    python /c/Users/rd/bin/diff.py "$1" "$2" "$3"
}

diffcsv() {
    # Usage:  difft <tsv1/csv1> <tsv1/csv2> 
    # Output spec: http://paulfitz.github.io/daff-doc/spec.html
    daff --www --index "$1" "$2"
}

diffxl() {
    # Usage: diffxl <file1> <file2>  (supports: .xls .xlsx csv/tsv)
    #        diffxl <file.xls> <num1> <num2>
    #        diffxl <file1.xls> <num1> <file2.xls> <num2>
    python /c/Users/rd/bin/diffxl.py "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8"
}

# Compare two csv (output html in web browser)
# daff --output OUT.html --index --www foo2.csv foo3.csv
