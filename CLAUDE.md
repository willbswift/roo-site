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
- `images/` holds about 700 images. Extensions are mixed (`.jpg`, `.jpeg`, `.JPG`, `.png`, `.gif`, `.webp`).
- `docwho6.html` and `roo_Dalek_Stuff_near_end.html` are very large legacy and reference files.
  Don't load them whole; grep them instead. Don't edit them unless asked.
- `Tardis Technical Index.pdf` is reference material.

## How pages work

- Fragments are injected with jQuery `.load()` in `rooscript.js`, e.g.
  `$("#navbar").load("navbar.html")`, `$("#biologynav").load("roobiologynav.html")`.
  A new page that needs a sub-nav needs three things: a `<div id="xxxnav">`, a `rooxxxnav.html`
  file, and a `.load()` line in `rooscript.js`.
- Because `.load()` uses XHR, pages must be previewed over HTTP, not `file://`.
  Run `python -m http.server 8080` (or `npx serve`) from the repo root and open
  http://localhost:8080. `.vscode/launch.json` and `.claude/launch.json` (server name `roo-site`)
  already target port 8080. If 8080 is already taken (e.g. a server in the main folder or another
  worktree), that config fails, because its args hardcode 8080 even when the preview tool picks
  another port. In that case, serve the worktree on a free port of its own. Don't stop the other server.
- Every page shares the same `<head>`: normalize.css, the Google Fonts (Russo One, Sarpanch),
  styles.css, the `images/rassilonicon2.png` favicon, and jQuery 4.0.0 from code.jquery.com
  (with its `integrity` hash and `crossorigin="anonymous"`; copy the tag from an existing page).
  Keep new pages consistent with that.
- Every page's `<html>` tag is `<html lang="en" class="no-js">`, and the first line of the inline
  `isMobile` script is
  `document.documentElement.className = document.documentElement.className.replace('no-js', 'js');`.
  New pages need both (see Kompozer edit mode below). The `isMobile` script sits right after
  `<body>` on content pages. It must stay in `<body>` because it writes `document.body.className`.
  On `index.html` the swap line is in its own script in `<head>`, and the `isMobile` part is in `<body>`.
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
  Kompozer: a wide body (2280px), a hidden header, and source colors that are always on.
- In a browser the inline script swaps `no-js` for `js`, so visitors get the normal 1280px layout
  and the click-to-reveal colors.
- Keep the swap line inline and first on the page. Moving it into `rooscript.js` (loaded at the
  end of the page) would flash edit mode before the page switches.
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
