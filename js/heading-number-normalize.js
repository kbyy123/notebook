// (function () {
//   function trimHeadingNumbering() {
//     // Heading text is prefixed by enumerate-headings spans.
//     var headingSpans = document.querySelectorAll(
//       ".md-content h1 .enumerate-headings-plugin, .md-content h1 .enumerate-heading-plugin, " +
//         ".md-content h2 .enumerate-headings-plugin, .md-content h2 .enumerate-heading-plugin, " +
//         ".md-content h3 .enumerate-headings-plugin, .md-content h3 .enumerate-heading-plugin, " +
//         ".md-content h4 .enumerate-headings-plugin, .md-content h4 .enumerate-heading-plugin, " +
//         ".md-content h5 .enumerate-headings-plugin, .md-content h5 .enumerate-heading-plugin, " +
//         ".md-content h6 .enumerate-headings-plugin, .md-content h6 .enumerate-heading-plugin"
//     );

//     headingSpans.forEach(function (span) {
//       var heading = span.closest("h1, h2, h3, h4, h5, h6");
//       if (!heading) return;

//       var level = parseInt(heading.tagName.slice(1), 10);
//       var text = (span.textContent || "").trim();

//       if (level === 1) {
//         // Hide H1 numbering completely.
//         span.textContent = "";
//         return;
//       }

//       // Convert: 1.1 -> 1, 1.2.3 -> 2.3
//       var m = text.match(/^\d+\.(\d+(?:\.\d+)*)$/);
//       if (m) {
//         span.textContent = m[1];
//       }
//     });
//   }

//   function trimTocNumbering() {
//     var tocLinks = document.querySelectorAll('.md-nav--secondary a[href^="#"]');

//     tocLinks.forEach(function (link) {
//       var href = link.getAttribute("href");
//       if (!href || href.length < 2) return;

//       var id = decodeURIComponent(href.slice(1));
//       var heading = document.getElementById(id);
//       if (!heading) return;

//       var level = parseInt(heading.tagName.slice(1), 10);
//       var txt = link.textContent || "";

//       if (level === 1) {
//         link.textContent = txt.replace(/^\s*\d+\.\s*/, "").trim();
//         return;
//       }

//       // Convert: "1.1 Title" -> "1 Title", "1.2.3 Title" -> "2.3 Title"
//       link.textContent = txt.replace(/^\s*\d+\.(\d+(?:\.\d+)*)\s+/, "$1 ").trim();
//     });
//   }

//   function run() {
//     trimHeadingNumbering();
//     trimTocNumbering();
//   }

//   if (document.readyState === "loading") {
//     document.addEventListener("DOMContentLoaded", run);
//   } else {
//     run();
//   }
// })();
