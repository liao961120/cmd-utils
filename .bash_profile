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


xl2csv() {
    # Usage xl2csv <input.xls(x)> <optional-sheet-index>
    in2csv.exe -I --write-sheets - "${1}"
    # Optional sheet index
    if [[ $2 != "" ]]; then
        num=$(($2 - 1))
    else
        num=-1
    fi
    
    printf "\n\n"

    bn=$(basename -s .xlsx "$1")
    bn=$(basename -s .xls "$1")
    tmp=$HOME/tmp.csv
    touch $tmp
    for file in "$bn"_*.csv; do
        [ -e "$file" ] || continue  # deal with non-matching
        
        # Skip when sheet num not matching current file
        if [[ $2 != "" ]]; then
            echo "${bn}_${num}".csv
            [[ $file != "${bn}_${num}".csv ]] && continue
        fi

        cat "$file" | 2utf > $tmp
        cat $tmp > "$file"
        echo "Output: \`$file\`"
    done
    rm $tmp

    echo "$file"
}

xl2csv1() {
    # Usage: xl2csv1 <file.xls>
    tmp=$(echo $HOME/tmp.txt)
    # Single sheet version
    in2csv.exe -I "${1}" > "$tmp"
    cat "$tmp" | 2utf > "$1.csv"
    rm "$tmp"
    echo "$1.csv"
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
# diffxls() {
#     # Usage: diffxls <file1.xls> <file2.xls2>
#     f1=$(xl2csv1 "$1")
#     f2=$(xl2csv1 "$2")
#     diffcsv "$f1" "$f2"
# }


# Compare two csv (output html in web browser)
# daff --output OUT.html --index --www foo2.csv foo3.csv