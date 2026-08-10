# mr-pythoneer.github.io

Personal engineering record — a blueprint-style index of my work.

**Live:** https://mr-pythoneer.github.io

## Design notes

Single self-contained `index.html`. No build step, no dependencies, no external
network requests of any kind — system fonts, inline CSS, inline SVG, inline JS.
Works identically opened from `file://` or served over HTTP.

- **Diagram** — nodes are real HTML; traces are a decorative SVG overlay whose
  paths are generated at runtime by a Manhattan (right-angle) router that
  measures live element geometry. Because it measures rather than assumes, the
  same router handles the desktop ring and the mobile spine with no special cases.
- **Console** — the `boot` module accepts real commands (`help`, `ls`,
  `filter <domain>`, `open <project>`, `contact`, `status`, `clear`).
  `filter` and `open` genuinely drive the diagram.
- **Accessibility** — the SVG is `aria-hidden`; all content lives in semantic
  HTML, so nothing is trapped in the drawing. Motion is gated behind
  `prefers-reduced-motion`.
- **Print** — `@media print` linearises the page into a plain resume handout.
