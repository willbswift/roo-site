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
  http://localhost:8080. `.vscode/launch.json` already targets port 8080.
- Every page shares the same `<head>`: normalize.css, the Google Fonts (Russo One, Sarpanch),
  styles.css, the `images/rassilonicon2.png` favicon, and jQuery 3.5.1 from code.jquery.com.
  Keep new pages consistent with that.

## Source color coding (core feature — preserve it)

Content text is wrapped in spans whose class names the source of the fact:
`A-tv`, `A-audiobook`, `A-licensed`, `A-game`, `A-behind`, `A-notbbc`, `A-fanon`,
`A-alternate`, `A-infinity`.
Clicking a `.main` block toggles `.active`, which reveals the colors (see `.active .A-*` in
styles.css). When editing text:
- Never strip, merge or reassign these classes. A sentence's source class is data.
- Keep the edit inside the existing span. If text from two sources is merged, keep separate spans.
- If you add a new source class, add both the base rule and the `.active` rule in styles.css,
  and add it to the color key / SOURCES explanation.

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
- `.vs/` (Visual Studio cache) was committed in the past and is now in `.gitignore`.
