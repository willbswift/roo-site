
/* ==========================================================================
   FRAGMENTS
   Shared HTML fragments are loaded into empty placeholder divs by name:
     <div id="navbar"></div>  -> navbar.html
     <div id="footer"></div>  -> footer.html
     <div id="xxxnav"></div>  -> rooxxxnav.html   (e.g. biologynav -> roobiologynav.html)
   A new page's sub-nav needs only its placeholder div and its rooxxxnav.html
   file; this script doesn't need editing.
   ========================================================================== */
$(function () {
  var fileWarningShown = false;

  function fragmentFile(id) {
    if (id === "navbar" || id === "footer") {
      return id + ".html";
    }
    return "roo" + id + ".html";
  }

  function showLoadError(placeholder, file, xhr) {
    var isFile = location.protocol === "file:";
    if (isFile) {
      if (!fileWarningShown) {
        console.error("ROO: fragments can't load from file://. Serve the site over HTTP, " +
          "e.g. run `python -m http.server 8080` in the site folder and open http://localhost:8080");
        fileWarningShown = true;
      }
    } else {
      console.error("ROO: couldn't load " + file + " (" + xhr.status + " " + xhr.statusText + ")");
    }
    var message = isFile
      ? "Navigation can't load from a local file. Serve the site over HTTP to see it."
      : "Navigation couldn't load. <a href=\"index.html\">Go to the index</a>";
    $(placeholder).html("<p class=\"fragment-error\">" + message + "</p>");
  }

  $("#navbar, #footer, div[id$='nav']").each(function () {
    var placeholder = this;
    var file = fragmentFile(placeholder.id);
    $(placeholder).load(file, function (response, status, xhr) {
      if (status === "error") {
        showLoadError(placeholder, file, xhr);
      }
    });
  });
});

/* ==========================================================================
   SOURCE COLORS
   Clicking a .main block toggles .active, which reveals the source colors
   (see the .active .A-* rules in styles.css). Delegated from document so it
   also works for .main blocks that arrive later inside a fragment.
   ========================================================================== */
$(document).on("click", ".main", function () {
  $(this).toggleClass("active");
});
