# ROO Website — Code Review Findings

**Date:** 2026-11-13
**Scope:** All live pages (`index.html`, the `roo*.html` pages and nav fragments), `navbar.html`, `footer.html`, `css/styles.css`, `javascript/rooscript.js` and `images/`. `docwho6.html` and `roo_Dalek_Stuff_near_end.html` were excluded, as agreed.
**Version reviewed:** `4a2b5a7`, which is identical to `origin/master`, so every finding applies to the published site.
**This is a findings report only.** It contains no fix plan.

## Summary

| # | Severity | Area | Finding |
|---|---|---|---|
| 1 | **High** | Correctness | Source colors are always visible, so the click-to-reveal toggle does nothing |
| 2 | **High** | Correctness | The footer's styles are silently discarded by a stray `*/` |
| 3 | **High** | Security / Correctness | Two jQuery versions load on every page, and the older, vulnerable 3.2.1 wins |
| 4 | **High** | Correctness | 11 image references 404 on GitHub Pages because of filename case |
| 5 | Medium | Correctness | `index.html` throws a TypeError on phones and tablets (mobile detection runs before `<body>` exists) |
| 6 | Medium | Correctness | Body `max-width` is 2280px instead of 1280px (leftover "editing mode" line) |
| 7 | Medium | Correctness | Broken in-site anchors, plus a "Top / Table of Contents" link that only works on the home page |
| 8 | Medium | Correctness | Duplicate element IDs on every page, caused by fragment wrappers |
| 9 | Medium | Data integrity | Malformed source classes (`A-tv&quot;`, `A-TV`) silently drop source coloring |
| 10 | Low | Correctness | Invalid HTML structure in the navbar; podcast subtitle text disappears; obsolete tags |
| 11 | Low | Correctness | Fonts named in the CSS are never loaded, and `san-serif` is misspelled |
| 12 | Medium | Architecture | The fragment loader is a hard-coded list of 19 IDs that runs on every page (violates Open/Closed) |
| 13 | Medium | Architecture | The `<head>` and page shell are copy-pasted into 20 pages and have already drifted |
| 14 | Low | Architecture | `index.html` loads all 19 fragments |
| 15 | Medium | Maintainability | CSS uses toggle-by-commenting "edit modes" and massive duplication |
| 16 | Medium | Maintainability | Pages are huge, with pasted word-processor markup (10,355 inline styles on one page) |
| 17 | Low | Maintainability | Large commented-out legacy blocks are shipped to every visitor |
| 18 | Low | Maintainability | Duplicate page titles, missing meta descriptions, a stale copyright |
| 19 | Low | Maintainability | No automated checks, and the case-sensitivity bugs can't be seen on Windows |
| 20 | Medium | Performance | 74 MB images folder: 147 unused images (36 MB), 23 images over 500 KB, no lazy loading |
| 21 | Low | Performance | Render-blocking fonts and scripts, and late fragment loading |
| 22 | Low | Accessibility | Missing `alt` text, a toggle that only works by mouse click, color-only meaning, hover-only menus, no phone navigation |
| 23 | Low | Security / Privacy | No SRI on CDN scripts, `target="_blank"` without `rel`, a plain-text email, `http://` links |

---

## Correctness & bug risk

### 1. [High] Source colors are always visible, so the click-to-reveal toggle does nothing
- **Where:** `css/styles.css:855-892`
- **Evidence:** The comment on line 855 opens and closes on the same line (`/* Activate the classes below ... */`). The block of base rules `.A-tv { background:black; color:red }` … `.A-fanon {...}` that follows is therefore **live CSS**. Its closing `} */` on line 892 has no opening `/*`.
- **Verified in the browser:** on `roobiology.html`, the computed style of `.main .A-tv` is `color: rgb(255,0,0); background: rgb(0,0,0)` both **before and after** clicking `.main`. The `.active` class does toggle (`active: true`), but nothing changes visually.
- **Impact:** The site's core feature, "click on paragraphs to see color coding for sources", is broken. Every page shows full color coding all the time. On narrow screens the `@media (max-width: 900px)` block (lines 1019-1054) and the `.mobile` rules (lines 941-976) force the same result.

### 2. [High] The footer's styles are silently discarded
- **Where:** `css/styles.css:892-907`
- **Evidence:** The stray `*/` after `.A-fanon { … }` is parsed as part of the next selector, giving `*/ .footer`. That selector is invalid, so the browser drops the whole `.footer { … }` rule.
- **Verified in the browser:** the computed `.footer` has `background-image: none` and `border-top-width: 0px`. The CSS asks for a radial gradient and a 4px border.
- **Impact:** The footer on every page renders unstyled. Any rule placed just after a stray comment marker is at risk in the same way.

### 3. [High] Two jQuery versions load on every page, and the older, vulnerable one wins
- **Where:** On every content page, `jquery-3.5.1` loads near the top (for example `roobiology.html:15`) and `jquery/3.2.1` loads again just before `rooscript.js` (for example `roobiology.html:1979`). `index.html` loads 3.5.1 (line 13), then 3.2.1 (line 1157), then 3.5.1 again (line 1159).
- **Verified in the browser:** `$.fn.jquery` reports **`3.2.1`** on 19 of 20 pages, and `3.5.1` only on `index.html`.
- **Impact:**
  - jQuery < 3.5.0 has known XSS issues in HTML parsing (CVE-2020-11022 and CVE-2020-11023), plus prototype pollution in versions before 3.4.0 (CVE-2019-11358). The site's `.load()` calls pass fetched HTML through exactly that HTML-parsing path.
  - Each page downloads, parses and executes about 85 KB of redundant JavaScript.
  - The version that actually runs depends on script order, which is fragile.

### 4. [High] Image references that 404 on GitHub Pages because of filename case
- **Where (src → file on disk):**
  - `roobiology.html:372` `brain5.jpg` → `brain5.JPG`
  - `roogallifrey.html:482` `citadelkarn.jpg` → `citadelkarn.JPG`
  - `roogallifrey.html:721` `pazithi2.jpg` → `Pazithi2.jpg`
  - `roogallifrey.html:722` `pazithi3.jpg` → `Pazithi3.jpg`
  - `rootech.html:65` `gallifreycity.jpg` → `GallifreyCity.JPG`
  - `rootech.html:66` `city1.jpg` → `city1.JPG`
  - `rootech.html:67` `city4.jpg` → `city4.JPG`
  - `rootimeline1.html:3890` `fighter.jpg` → `fighter.JPG`
  - `rootimeline1.html:3891` `flier1.jpg` → `flier1.JPG`
- **Verified:** `https://willbswift.github.io/roo-site/images/brain5.jpg` returns **404 Page not found**. All 9 references return 200 on the local Windows server, which is case-insensitive. That is why the problem doesn't show up while editing (see #20).
- **Impact:** These images appear broken to every visitor of the live site.

### 5. [Medium] `index.html` throws a TypeError on mobile devices
- **Where:** `index.html:14-19`
- **Evidence:** The mobile-detection script runs inside `<head>` and does `document.body.className += ...`. At that point `document.body` is `null`. On the other pages the same script sits after `<body>`, so it works there.
- **Verified in the browser:** with a mobile user agent the console shows `Uncaught TypeError: Cannot read properties of null (reading 'className') at index.html:17`. The `mobile` class is never applied (`bodyClass: ""`).
- **Also:** User-agent sniffing (`/(iPhone|iPod|iPad|Android)/`) misses modern iPads, which report a desktop Safari user agent. It also duplicates the work the CSS media queries already do.

### 6. [Medium] Body `max-width` is 2280px instead of 1280px
- **Where:** `css/styles.css:21-22`
- **Evidence:** The "editing mode" line `max-width: 2280px;  */` was left active. Its `*/` has no opener, so the declaration still applies and overrides `max-width: 1280px` on line 15.
- **Verified in the browser:** `getComputedStyle(body).maxWidth` is `"2280px"`.
- **Impact:** On wide monitors the content stretches beyond the intended 1280px layout, while the fixed `.header` (`max-width: 1280px`) does not. The two no longer line up.

### 7. [Medium] Broken in-site anchors
- **`navbar.html:91`:** "Top / Table of Contents" links to `#hero`. `id="hero"` exists only in `index.html`, so the link does nothing on the other 19 pages.
- **`roogallifreynav.html:34` and `rootimeline1.html:2100`:** `roogallifrey.html#ancient` doesn't exist.
- **`rootimeline1.html:6162, 6606`:** `roolifedeath.html#houses` doesn't exist.
- **`rootimeline2.html:356, 1596, 2931`:** `roogovernment.html#capitol`, `#barriers` and `#citadel` don't exist.
- **`rooconstruction.html`:** There's no `<div id="footer">`, so the navbar's "Contact" link (`#footer`) does nothing there and the page has no footer (verified: `footerLoaded: false`).
- **Impact:** Readers land at the top of the target page instead of the section.

### 8. [Medium] Duplicate element IDs on every page
- **Evidence:** Each fragment repeats its host's ID as its own wrapper. `navbar.html` starts with `<div id="navbar">` and is loaded *into* `<div id="navbar">`. The same is true for `footer.html` and every `*nav.html`. Several fragments also reuse a page section's ID. For example, `roobiologynav.html` has `<div id="biology">` and `<figure id="biology">`.
- **Verified in the browser:** there are 3 duplicate IDs per content page and 19 on `index.html`. `rootimeline1.html` also has `id="child"` three times (lines 3411, 3512, 3552).
- **Impact:** This is invalid HTML. `#id` selectors, anchors and `getElementById` resolve to only the first match. CSS such as `#biology img` hits both elements, whether that's intended or not.

### 9. [Medium] Malformed source classes silently lose their coloring
- **`rooappendix.html:150`:** `<td class="A-tv&quot;">`. The class becomes `A-tv"`, which matches no rule.
- **`rootimeline7.html:2704`:** `<span class="A-TV">`. Class names are case-sensitive, so this matches no rule.
- **Impact:** Per CLAUDE.md, the source class is data. These facts lose their source coloring with no visible error. Nothing in the project detects this kind of typo.

### 10. [Low] Invalid HTML structure, stray tags and lost text
- **`navbar.html`:** `<div class="dropdown">` and `<br>` are placed directly inside `<ul>` (34 occurrences), and `<li class="dropbtn">` sits inside a `div`. These are invalid list content models. Browsers repair them inconsistently, and screen readers announce the list incorrectly.
- **`roopodcast.html:38`:** `<em><My Youtube Podcast on all things Gallifreyan></em>`. The angle brackets are parsed as an unknown `<my>` element, so the text **disappears from the page**. There is also an extra `</div>` at `roopodcast.html:119`.
- **`rootimeline1.html:13`, `rootech.html:13`, `rooweb.html:13`, `rootimeline2.html:13`:** `<script>` (and on rootimeline1, a run of `&nbsp;`) sits directly after `<body>`. The `isMobile` script is in `<body>` on most pages but in `<head>` on `index.html`.
- **`rooconstruction.html:12`:** the favicon `<link>` and an empty `<style>` are placed after the main head block.
- Obsolete tags: there are `<center>` tags in timelines 1–5, 7 and 8 (126 in total), `<big>` in timelines 1–5 and 8, and `<font>` in `rooweb.html`.

### 11. [Low] Fonts named in the CSS are never loaded
- **Where:** `css/styles.css`, throughout.
- **Evidence:** `Beijing SSI` and `CCTimelordSolid` are used in the font stacks, but the CSS has no `@font-face` and no page loads them. They render only on machines that happen to have them installed. `san-serif` is misspelled (it should be `sans-serif`) in 7 places, so that fallback never applies and the browser default is used.

---

## Architecture & SOLID

### 12. [Medium] The fragment loader is a hard-coded registry that runs everywhere (Open/Closed, SRP)
- **Where:** `javascript/rooscript.js:9-65`
- **Evidence:** 19 separate `$(function(){ $("#x").load("x.html") })` blocks, one per fragment. Every page runs all 19, and jQuery quietly does nothing when the ID is missing.
- **Concerns:**
  - **Open/Closed:** Adding a page requires editing the shared script (CLAUDE.md lists this as a required step). The script can't be extended without modifying it.
  - **Single responsibility and coupling:** The script also binds the color-toggle click handler. Unrelated behaviors share one file with no structure, and they're coupled to page IDs by string literals.
  - **No error handling:** `.load()` failures (a 404 or a `file://` preview) fail silently. The page just shows no navbar.
  - **Ordering:** The `.main` click handler is bound at `ready`, while fragments arrive asynchronously. It works today only because `.main` is never inside a fragment.
  - **Runtime dependency:** The page chrome (navigation and footer) only exists after JavaScript and XHR run. With JS disabled, with a slow network, or for crawlers that don't run JS, there's no navigation, and the page shows a layout shift when the header arrives.

### 13. [Medium] The `<head>` and page shell are copy-pasted into 20 pages, and the copies have drifted
- **Evidence:** Every page repeats the normalize, fonts, styles, favicon, jQuery and `isMobile` code, plus the closing jQuery and rooscript tags. With no template or include, the copies have already diverged:
  - The `isMobile` script is in `<head>` on index (and is broken there, #5) but in `<body>` elsewhere.
  - `rooconstruction.html` uses an un-encoded `|` in the Google Fonts URL, while the others use `%7C`.
  - jQuery script order differs on index (#3).
  - Page titles were copied and never updated (#19).
  - Every page has an empty `<style></style>`.
- **Impact:** Any shared change, such as upgrading jQuery, must be made by hand in about 40 places. That is how #3 happened.

### 14. [Low] `index.html` loads every sub-nav fragment
- `index.html` contains all 17 `*nav` host divs and so issues 19 XHR requests. The resulting page has 26 `*nav` elements and 19 duplicate IDs. The home page's layout depends on every content page's fragment.

---

## Maintainability

### 15. [Medium] CSS "edit modes" toggled by commenting, and heavy duplication
- **Toggle by commenting:** Three places (`styles.css:21`, `:108`, `:855`) carry instructions like "USE THE LINE OF TEXT BELOW TO MAKE IT EASY TO EDIT ON KOMPOZER… 321". They expect a person to comment and uncomment code by hand to switch modes. Findings #1, #2 and #6 are exactly this mechanism left half-switched. The mode switch isn't explicit (a class, a separate stylesheet or a flag), so mistakes are invisible.
- **Duplication:**
  - The 9 source colors are hard-coded 5 times each: `.active`, `::selection` ×3, `.innerlink`, the base rules, `.mobile` and the media query.
  - The `-webkit-selection` pseudo-elements don't exist and are dead code. The `-moz-selection` rules haven't been needed since Firefox 62.
  - `a`, `a:visited`, `.dropbtn` and `figcaption a` repeat the same 10 declarations.
  - `#darktimes img`, `#legend img`, `#middle img` and the rest are 9 near-identical blocks that differ only in height.
  - There are no CSS custom properties. `#cdd2ea` appears 31 times and `#6C6BD0` 18 times.
- **Leftovers:** empty rules (`tr:nth-child(even) td {}`, `body {}` in the media query), duplicate declarations in one rule (`.gallifreys li` sets `margin` twice, `thead th` sets `background` twice), `zoom: 1` (an IE7 hack), and commented-out code blocks.
- **Mixed approach:** Page-specific IDs (`#biology`, `#culture`, `#craig`, `#presidentlist`…) are styled in the global sheet. Combined with #8, a change for one page can affect others.

### 16. [Medium] Pages are very large, with pasted word-processor markup
- **Size:** `roochildren.html` is 1.1 MB, with **10,355 inline `style` attributes**. For example, `style="font-size: 20px;"` and `style="font-family: Arial, Helvetica, sans-serif;"` each appear 3,444 times, and `margin: 0in 0in 0.0001pt … Calibri` appears 552 times. `rootimeline1.html` is 817 KB with 1,394 inline styles, and `rootimeline5.html` is 805 KB.
- **DOM size (measured):** `rootimeline1` has 12,316 nodes, `roochildren` 10,809 and `rootimeline5` 9,416.
- **Impact:** Inline styles override the stylesheet, so global design changes don't reach this content. Files this size are hard to diff and review, and editing them risks the span-closing errors CLAUDE.md warns about.

### 17. [Low] Large commented-out legacy blocks shipped to users
- `index.html` keeps the full old header and footer inside HTML comments (from line 27 onward, and around line 1150, including "Copyright 2018 AD"). It also keeps a commented-out loader for a non-existent `nav-bar.html`.
- `roolifedeath.html:2078` has an empty `<script></script>` with a "date calculator" note.
- All of this is downloaded by every visitor and has to be skipped over by every maintainer.

### 18. [Low] Stale, duplicated and missing metadata
- **Titles:** `<title>Appendix</title>` is used by `rooappendix.html`, **`roopodcast.html`** and **`rooconstruction.html`**.
- **Descriptions:** 11 of the 20 pages have no `<meta name="description">`.
- **Footer:** `footer.html:13` hard-codes "Copyright 2024 AD".
- **Navbar:** "Human History", "Dalek Biology & Culture" and "Dalek Timeline" all link to the same `rooconstruction.html`.

### 19. [Low] No automated checks, and the dev setup hides real bugs
- **No checks:** There is no link checker, HTML validator, CSS linter or class-name check. Every finding above was found manually or with ad-hoc scripts.
- **Case-insensitive local preview:** Local preview runs on a case-insensitive Windows filesystem (inside Dropbox), so the case-sensitivity bugs in #4 cannot reproduce locally.
- **Large files in git:** The repository holds `Tardis Technical Index.pdf` (8 MB) and three README screenshots in the root (`Image1–3.jpg`, 1.9 MB). The README references them with absolute paths (`/Image1.jpg`), which resolve against the domain root rather than the repo.

---

## Performance

### 20. [Medium] Image weight and loading
- **Folder size:** `images/` holds 706 files, **74 MB** in total.
- **Unused images:** **147 images (36 MB) aren't referenced** by any page, the CSS, or the excluded legacy files. Examples: `veilnebula.png` (7.3 MB), `nameday.png` (3.5 MB), `drfather.JPG` (2.2 MB), `gallifreybigbig.png` (1.5 MB).
- **Oversized images:** **23 images are over 500 KB** (32.9 MB combined). Some are referenced and shown at `height: 15–23rem`:
  - `milkyway.jpg` (2.1 MB)
  - `kotturuh.jpg` (1.6 MB)
  - `gallifreymapatlas.jpg` (1.3 MB)
  - `sagittariusa.jpeg` (777 KB)
  - `hornsofrassilon.jpg` (745 KB)
- **No lazy loading:** No `<img>` uses `loading="lazy"` (verified: 0 on every page), and none has `width`/`height` attributes. `rootimeline5` requests 104 images and `rootimeline1` 102 on first load, and the layout shifts as each one arrives.
- **No modern formats:** Most images are JPEG/PNG; only a few use WebP.

### 21. [Low] Render-blocking resources
- **CSS:** The Google Fonts request uses the legacy `css?family=` API without `display=swap`, so text can be invisible while the fonts load.
- **JavaScript:** jQuery loads synchronously in the body, twice (#3).
- **Fragments:** The navbar and footer arrive late by XHR (#12), which adds requests and causes a layout shift.

---

## Accessibility

### 22. [Low] Accessibility issues
- **Missing `alt` text:** The timeline pages have many images with no `alt` (measured: `rootimeline5` 91, `rootimeline4` 40, `rootimeline1` 36, `rootimeline2` 29, `rootimeline3` 28, `rootimeline7` 27, `rootimeline8` 25, `rootimeline6` 18). Every page also includes the decorative `#decoration-left` and `#decoration-right` images with no `alt=""`.
- **Click-only toggle:** The color toggle is a `click` handler on a plain `div.main`. It has no `role`, no `tabindex` and no keyboard handler, so keyboard and screen-reader users can't trigger it. The whole page is a single `.main` (measured: one `.main` containing the entire 16,000px content). The navbar text "click on paragraphs" is therefore misleading, because a click toggles the entire page.
- **Color-only meaning:** The source of a fact is shown only by text color. There is no text or icon alternative for color-blind readers.
  - `A-behind` (#993300) on black, used in the always-on base rules, fails WCAG contrast.
  - `A-notbbc` (#999999) and `A-tv` (red) on black are borderline.
- **Hover-only menus:** The dropdowns open only on `:hover` (`styles.css:197`), so keyboard users can't open them. The dropdown "buttons" are `<li>` elements, not focusable controls.
- **Headings:** `index.html` has two `<h1>`. The navbar puts a `<h3>` inside a list item ("click on paragraphs…"), which appears on every page above the page `<h1>`.
- **Hidden navigation on small screens:** At 900px and below, `.header` is hidden (`styles.css:984`). Only a "Return To Master Index" link (`.noshow`) remains, and only on pages that include it. On phones there is no other site navigation.

---

## Security & hosting

### 23. [Low] Security and privacy hygiene
- **No integrity hashes on CDN scripts:** No CDN `<script>` has `integrity` (SRI) or `crossorigin` attributes. If code.jquery.com or cdnjs were compromised, any script could run on the site. This compounds #3.
- **`target="_blank"` without `rel="noopener"`:** 43 links (23 on index, 15 on roopodcast, plus navbar and footer). Modern browsers now default to `noopener`, so the risk is low, but the practice is outdated.
- **Exposed email:** `footer.html:10` publishes a plain-text email address (as a `mailto:` link and as text) on every page, which invites harvesting by spam bots.
- **`http://` links:** Plain `http://` links in `index.html:1035, 1049, 1053` and `roogovernment.html:786`. These are outbound links, not mixed content, so the impact is low.
- **Unencoded URL:** The navbar links to `Tardis Technical Index.pdf` with unencoded spaces. It works, but it depends on browser repair.

---

## How verified
- **Local server:** Served this worktree with `python -m http.server 8080` and loaded all 20 pages in the in-app browser (Chromium).
  - **Measured on each page:** jQuery version, console errors, whether the navbar and footer fragments loaded, duplicate IDs, image counts and lazy loading, DOM size, and the number of `.main` elements.
  - **Desktop, `roobiology.html`:** computed styles of `.A-tv` before and after clicking (#1), plus the `.footer` styles (#2) and the body `max-width` (#6).
  - **Mobile user agent, `index.html`:** checked for the console error (#5).
- **Static checks (Python, read-only):** tag-balance and stray-tag scan, duplicate IDs after fragment injection, `A-*` class inventory, every internal link, anchor and `<img src>` resolved against the real filenames with exact case, orphaned and oversized images, inline-style counts, `alt` text and `target="_blank"` audits.
- **Live check:** `https://willbswift.github.io/roo-site/images/brain5.jpg` returns 404, which confirms #4 in production.
- **Read in full:** `rooscript.js`, `styles.css`, `navbar.html`, `footer.html`, and the head and tail of each page.
- **Limits:**
  - The tag-balance check uses a lenient parser. It catches stray and unclosed tags, but a full W3C validation (deliberately not run) would report more.
  - Excluded: content accuracy, spelling, and the two legacy files.
- No site files were modified. The only file added is this report.
