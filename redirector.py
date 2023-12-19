'''redirector.py generates HTML files for redirection.

Example:
    redirector out.html -t https://example.com

Usage:
    redirector FILE -t URL
    redirector FILE --target URL

Options:
    -h --help   Print this screen.
    --version   Show version.
    -t --target The target URL to redirect to.
'''
VERSION = "2023.12.19"

from pathlib import Path
from docopt import docopt


def main():
    args = docopt(__doc__, version=VERSION)
    # print(args)
    
    # Write output
    target_url = args["--target"]
    outfp = args["FILE"]
    html = template(target_url)
    write_file(html, outfp)


def write_file(string, outfp):
    outfp = Path(outfp)
    if not outfp.parent.exists(): outfp.parent.mkdir(parents=True)
    with open(outfp, "w", encoding="utf-8") as f:
        f.write(string)
    print(f"HTML written to: {outfp.absolute()}")


def template(target_url):
    html = '''
    <!doctype html>
    <html lang=en-us>

    <head>
        <title>{{ TARGET_URL }}</title>
        <meta name=robots content="noindex">
        <meta charset=utf-8>
        <meta http-equiv=refresh content="0; url={{ TARGET_URL }}">
    </head>
    <body>
        <p>
            Redirecting to <a href="{{ TARGET_URL }}">{{ TARGET_URL }}</a>
        </p>
    </body>
    </html>
    '''
    return html.replace("{{ TARGET_URL }}", target_url)


if __name__ == "__main__":
    main()
