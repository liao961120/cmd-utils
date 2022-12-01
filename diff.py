import sys
import webbrowser
from pathlib import Path
from difflib import HtmlDiff

def main():
    f1 = read_file(sys.argv[1])
    f2 = read_file(sys.argv[2])
    outpf = None if len(sys.argv) < 4 else sys.argv[3]
    # if len(sys.argv) < 3:
    #     outfp = tempfile.TemporaryFile(encoding="utf-8")

    html_diff = HtmlDiff().make_file(f1, f2)
    outfp = write_file(html_diff, outpf)
    print(f"File written to `{outfp}`")
    webbrowser.open(f"file:///{outfp}")


def read_file(fp):
    with open(fp, encoding="utf-8") as f: 
        return f.read().split('\n')


def write_file(s, fp=""):
    if fp == "":
        fp = f"diff_{sys.argv[1]}-{sys.argv[2]}.html"
    with open(fp, "w", encoding="utf-8") as f:
        f.write(s)
    return Path(fp).absolute().as_posix()

if __name__ == '__main__':
    main()
