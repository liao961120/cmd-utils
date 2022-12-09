BATCH_DIR=/c/Users/rd/AppData/Local/Microsoft/WindowsApps
SRC_DIR='C:\Users\rd\bin\dist'
NATIVE_ENC=cp950

# Print Doc
if [[ $1 = "" ]]; then
    printf "Compile python script to .exe and create a .bat file on PATH\n\n"
    printf '  bash compile.sh <file.py>\n'
    exit 0
fi

# Build binary
fp=${1%.*}
[[ -d "dist/${fp}" ]] && rm -r "dist/${fp}"
printf "Compiling $fp.py ...\n\n"
pyinstaller "${fp}.py"

# Make .bat
echo "@ECHO OFF
${SRC_DIR}\\${fp}\\${fp}.exe %*
" > tmp.bat
iconv -f UTF-8 -t $NATIVE_ENC tmp.bat > batch/"${fp}.bat"
unix2dos.exe batch/"${fp}.bat"

# Copy .bat to directory on PATH
[[ -e "$BATCH_DIR"/"${fp}.bat" ]] && rm "$BATCH_DIR"/"${fp}.bat"
cp batch/"${fp}.bat" "$BATCH_DIR"/"${fp}.bat"

# Clean up
rm tmp.bat "${fp}.spec"
[[ -d build ]] && rm -r build
