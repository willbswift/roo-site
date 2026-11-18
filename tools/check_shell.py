"""Check that every page's shell matches the site standard.

The "shell" is everything from <!DOCTYPE html> to the end of the isMobile
<script> near the top of <body>. Pages are copy-pasted, so this
script catches drift after editing in Kompozer. It only reports; it never
changes files.

Usage (from the repo root):
    python tools/check_shell.py            # check every page
    python tools/check_shell.py rootech.html roobiology.html

Whitespace and line breaks are ignored. Each page keeps its own <title>,
author, description and <body> tag; everything else must match STANDARD below.
Exit code is 1 if any page has a problem, 0 otherwise (warnings don't count).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Legacy/reference files that aren't site pages.
EXCLUDED = {"roo_Dalek_Stuff_near_end.html", "docwho6.html"}

JQUERY = ('<script src="https://code.jquery.com/jquery-4.0.0.min.js" '
          'integrity="sha384-fgGyf7Mo7DURSOMnOy7ed+dkq5Job205Gnzu6QIg0BOHKaqt4D76Dt8VlDCzcMHV" '
          'crossorigin="anonymous"></script>')

STANDARD = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
	<meta charset="utf-8">
	<title>{title}</title>
	<meta name="author" content="{author}">
	<meta name="description" content="{description}">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="css/normalize.css" type="text/css" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css?family=Russo+One%7CSarpanch" rel="stylesheet">
	<link href="css/styles.css" type="text/css" rel="stylesheet">
	<link rel="shortcut icon" type="image/png" href="images/rassilonicon2.png">
	<script>
		document.documentElement.className = document.documentElement.className.replace('no-js', 'js');
	</script>
	""" + JQUERY + """
</head>

{body_tag}
	<script>
		var isMobile = /(iPhone|iPod|iPad|Android)/.test(navigator.userAgent) ||
			(/Macintosh/.test(navigator.userAgent) && navigator.maxTouchPoints > 1);
		if (isMobile) {{
			document.body.className += ' ' + 'mobile';
		}}
	</script>"""

ROOSCRIPT = '<script src="javascript/rooscript.js" type="text/javascript"></script>'

# Up to the end of the first <script> in <body> that mentions isMobile, so any
# stray scripts before it (e.g. a misplaced jQuery tag) count as shell drift.
SHELL_END = re.compile(r"<body\b[^>]*>.*?\bisMobile\b.*?</script>", re.S | re.I)
EMPTY_STYLE = re.compile(r"<style>\s*</style>", re.I)
# Kompozer rewrites <html lang="en" class="no-js"> as <html class="no-js" lang="en">
# when it saves. Attribute order doesn't matter, so accept either one.
HTML_TAG_KOMPOZER = re.compile(r'<html\s+class="no-js"\s+lang="en"\s*>', re.I)
HTML_TAG_STANDARD = '<html lang="en" class="no-js">'


def page_files():
    return sorted(p for p in ROOT.glob("*.html")
                  if (p.name == "index.html" or p.name.startswith("roo"))
                  and not p.name.endswith("nav.html")
                  and p.name not in EXCLUDED)


def split_shell(text):
    """Return (shell, rest) or None if no <body>...isMobile...</script> is found."""
    m = SHELL_END.search(text)
    if not m:
        return None
    return text[:m.end()], text[m.end():]


def page_fields(shell):
    def find(pattern):
        m = re.search(pattern, shell, re.S | re.I)
        return m.group(1) if m else None
    return {
        "title": find(r"<title>(.*?)</title>"),
        "author": find(r'<meta\s+name="author"\s+content="([^"]*)"'),
        "description": find(r'<meta\s+name="description"\s+content="([^"]*)"'),
        "body_tag": find(r"(<body\b[^>]*>)"),
    }


def expected_shell(fields):
    return STANDARD.format(**fields)


def squash(s):
    """Normalize whitespace so formatting differences don't count."""
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*(<|>)\s*", r"\1", s)
    return s.strip()


def tokens(s):
    return [t + ">" for t in squash(s).split(">") if t]


def check(path):
    """Return (problems, warnings) for one page."""
    text = path.read_text(encoding="utf-8")
    problems, warnings = [], []
    parts = split_shell(text)
    if not parts:
        return ["no <body> ... isMobile <script> found"], warnings
    shell, rest = parts

    if EMPTY_STYLE.search(shell):
        warnings.append("empty <style></style> in <head> (Kompozer may add this; harmless)")
        shell = EMPTY_STYLE.sub("", shell)
    shell = HTML_TAG_KOMPOZER.sub(HTML_TAG_STANDARD, shell, count=1)

    fields = page_fields(shell)
    for name in ("title", "author", "description"):
        if not fields[name] or not fields[name].strip():
            problems.append(f"missing or empty {name}")
            fields[name] = fields[name] or ""
    if not fields["body_tag"]:
        fields["body_tag"] = "<body>"

    got, want = tokens(shell), tokens(expected_shell(fields))
    if got != want:
        # Report the first point where the shell differs, with a little context.
        i = next((k for k, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))
        problems.append("shell differs from the standard at:\n"
                        f"        found:    {' '.join(got[i:i + 2])[:160] or '(end)'}\n"
                        f"        expected: {' '.join(want[i:i + 2])[:160] or '(end)'}")

    if rest.count(ROOSCRIPT) != 1:
        problems.append(f"expected exactly one rooscript.js tag after the shell, found {rest.count(ROOSCRIPT)}")
    if "jquery-" in rest:
        problems.append("a second jQuery <script> appears later in the page")
    if re.search(r"\bisMobile\b|replace\('no-js'", rest):
        problems.append("a second isMobile or no-js swap script appears later in the page")
    return problems, warnings


def main(argv):
    paths = [ROOT / a for a in argv] if argv else page_files()
    failed = 0
    for path in paths:
        problems, warnings = check(path)
        if problems:
            failed += 1
        for p in problems:
            print(f"{path.name}: {p}")
        for w in warnings:
            print(f"{path.name}: warning: {w}")
    print(f"\n{len(paths)} page(s) checked, {failed} with problems.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
