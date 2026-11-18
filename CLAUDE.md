# ROO Website — Rassilon, Omega and that Otherguy

A static fan-reference site about Doctor Who's Gallifrey and the Time Lords
(biology, culture, government, technology, history), by William B. Swift.
Published on GitHub Pages: https://willbswift.github.io/roo-site/index.html
Repo: https://github.com/willbswift/roo-site (branch `master`).

There is no build step, no framework and no package manager. It's plain HTML, CSS and jQuery.

## Layout

- `index.html` is the home page and full index of every page and sub-section.
- `rooXXX.html` is a content page (biology, gallifrey, government, lifedeath, tech,
  children, appendix, timeline1–8, podcast, construction).
- `rooXXXnav.html` is the in-page sub-navigation fragment for the matching content page.
- `navbar.html` and `footer.html` are shared fragments used on every page.
- `css/styles.css` holds the site styles; `css/normalize.css` is third-party and shouldn't be edited.
- `javascript/rooscript.js` loads the fragments and toggles source colors.
- `tools/check_shell.py` checks that every page's shared head and body-start match the standard (see below).
- `images/` holds about 700 images. Extensions are mixed (`.jpg`, `.jpeg`, `.JPG`, `.png`, `.gif`, `.webp`).
- `docwho6.html` and `roo_Dalek_Stuff_near_end.html` are very large legacy and reference files.
  Don't load them whole; grep them instead. Don't edit them unless asked.
- `Tardis Technical Index.pdf` is reference material.

## How pages work

- `rooscript.js` fills empty placeholder divs with jQuery `.load()`, picking the file from the id
  by naming convention: `#navbar` → `navbar.html`, `#footer` → `footer.html`, and any
  `<div id="xxxnav">` → `rooxxxnav.html`. A new page that needs a sub-nav needs only a
  `<div id="xxxnav">` and a matching `rooxxxnav.html` file. Don't edit the script for it, and don't
  give other elements an id ending in `nav`. If a fragment fails to load, the placeholder shows
  a `.fragment-error` note and the error is logged to the console.
- The `.main` click handler (source colors) is delegated from `document`, so it also works on
  content that arrives later.
- Because `.load()` uses XHR, pages must be previewed over HTTP, not `file://`.
  Run `python -m http.server 8080` (or `npx serve`) from the repo root and open
  http://localhost:8080. `.vscode/launch.json` and `.claude/launch.json` (server name `roo-site`)
  already target port 8080. If 8080 is already taken (e.g. a server in the main folder or another
  worktree), that config fails, because its args hardcode 8080 even when the preview tool picks
  another port. In that case, serve the worktree on a free port of its own. Don't stop the other server.
- Every page (index.html and the roo*.html content pages) shares one standard "shell": everything
  from `<!DOCTYPE html>` to the `isMobile` script at the top of `<body>`. It's defined in `STANDARD`
  in `tools/check_shell.py`. In order, the `<head>` holds: charset, `<title>`, author, description,
  viewport, normalize.css, the Google Fonts (Russo One, Sarpanch; `%7C`, not a raw `|`), styles.css,
  the `images/rassilonicon2.png` favicon, the inline no-js swap script, then jQuery 4.0.0 from
  code.jquery.com (with its `integrity` hash and `crossorigin="anonymous"`). Only the title, author,
  description and `<body>` tag vary per page. There's no `<style>` block in the head.
- After changing any page's shell, or after the author has edited pages in Kompozer, run
  `python tools/check_shell.py`. It reports drift and never edits files. Build a new page's shell
  by copying an existing page's, then running the check.
- `Beijing SSI` and `CCTimelordSolid` in the styles.css font stacks are deliberately not
  embedded (commercial, no web license). They show only where installed locally, and visitors
  get the fallbacks. Don't add `@font-face` for them unless the author supplies licensed files.
- Every page's `<html>` tag is `<html lang="en" class="no-js">`, and the `<head>` has an inline
  script whose only line is
  `document.documentElement.className = document.documentElement.className.replace('no-js', 'js');`.
  It comes before the jQuery tag, so the swap doesn't wait for the download. New pages need both
  (see Kompozer edit mode below). The separate `isMobile` script sits right after `<body>`. It must stay
  in `<body>` because it writes `document.body.className`.
- `navbar.html` markup: each dropdown is `<li class="dropdown"><span class="dropbtn">Label</span>
  <ul class="dropdown-content"><li>…</li></ul></li>`, and the color key is
  `<li class="dropdown innerlink">`. Put only `<li>` directly inside a `<ul>`, with no `<div>` or `<br>`.
  The vertical spacing comes from the `.nav .dropdown-content li` rules in styles.css.
  The extra gap above the `?`/`??` lines comes from `li.key-gap`.
- Don't use the obsolete `<center>`, `<big>` or `<font>` tags. Use `<div class="centered">`,
  `<span class="big-text">` and `<span class="smaller-text">` instead (styles.css). Kompozer may write
  the old tags back. Convert them when you come across them, and keep any `A-*` class on the element
  (e.g. `class="big-text A-fanon"`). Note that the existing `.center` class is a styled box, not
  plain centering.

## Kompozer edit mode

The author edits pages in Kompozer. Its editing view doesn't run JavaScript (confirmed in
Kompozer), so the navbar and footer fragments never load there either.
- The rules under `.no-js` in the "KOMPOZER EDIT MODE" section of styles.css apply only in
  Kompozer: a hidden header and source colors that are always on.
- In a browser the inline script swaps `no-js` for `js`, so visitors get the normal layout
  and the click-to-reveal colors.
- Keep the swap line inline and as the first script on the page (in `<head>`, before jQuery). Moving it
  into `rooscript.js` (loaded at the end of the page) would flash edit mode before the page switches.
- Don't go back to switching modes by commenting CSS in and out (the old `321` toggles). That
  approach left stray `*/` markers that broke the live site's styles.
- Visitors with JavaScript disabled also see edit mode. That's accepted.

## Source color coding (core feature — preserve it)

Content text is wrapped in spans whose class names the source of the fact:
`A-tv`, `A-audiobook`, `A-licensed`, `A-game`, `A-behind`, `A-notbbc`, `A-fanon`,
`A-alternate`, `A-infinity`.
Clicking a `.main` block toggles `.active`, which reveals the colors (see `.active .A-*` in
styles.css). When editing text:
- Never strip, merge or reassign these classes. A sentence's source class is data.
- Keep the edit inside the existing span. If text from two sources is merged, keep separate spans.
- If you add a new source class, copy the existing `A-tv` rules in styles.css. There are
  `.active`, `::selection`, `.innerlink` (color key), `.no-js` (Kompozer edit mode), `.mobile` and
  `@media (max-width: 900px)` versions. Also add the class to the color key / SOURCES explanation.
- Class names are case-sensitive and must be exact: `A-TV` or `A-tv"` silently lose their color.

## Writing and spelling conventions

- `ROOWords.txt` is the list of in-universe and proper-noun spellings (Lineacrux, Kastria,
  Otherstide, Whoniverse, ...). Treat them as correct; never "fix" them.
- Episode, story, book and audio titles, and direct quotes (`<div class="quote">` and quoted
  dialogue), must stay verbatim. Don't correct spelling or tense inside quotes.
- Fix spelling, grammar and tense in the author's own narrative text only.
- Tense convention: timeline entries (`rootimeline1`–`8.html`) are written mostly in the
  simple present tense, e.g. "Rassilon founds the Time Lords", not "founded" or "has founded".
  When fixing tenses on timeline pages, convert narrative verbs to simple present unless the
  sentence describes something earlier than the entry's own event (keep past or past
  perfect there), or the text is a quote or title.
- Keep the author's voice. Make light-touch edits, not rewrites.

## Working rules

- Make small, reviewable changes. Content pages are large (100 KB–800 KB), so edit the
  specific section and don't rewrite whole files.
- After changing HTML, check that tags are still balanced and that every `<span class="A-...">`
  is still closed.
- Check image references against the real filenames. Case matters on GitHub Pages
  (`.JPG` is not `.jpg`).
- New images should be web-optimized (aim for under ~500 KB) to keep the repo small.
- Don't commit or push unless asked.

## Git notes

- The working copy lives in Dropbox. Dropbox syncing `.git` can cause lock-file and corruption
  problems. If git reports `index.lock` or "File exists" errors, check for Dropbox conflicted copies.
  "unable to write new index file" has also happened. It was a brief Dropbox lock, and retrying
  the command worked.
- Claude sessions work in worktrees under `.claude/worktrees/` on `claude/...` branches. `master`
  is checked out in the main folder, so merge with `git merge --ff-only <branch>` run there.
- Pages use CRLF line endings, and `core.autocrlf` is on. "LF will be replaced by CRLF" warnings
  are normal.
- `.vs/` (Visual Studio cache) was committed in the past and is now in `.gitignore`.
