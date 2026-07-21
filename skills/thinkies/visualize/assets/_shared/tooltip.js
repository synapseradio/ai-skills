// Root-scoped tooltip helpers. Every function takes the fragment's own root
// element (the `<section class="viz">`) and finds the tooltip inside it, so two
// fragments on one page each drive their own tooltip rather than fighting over a
// single document-global `#tooltip`. The assembler inlines this once and hangs
// the functions on the shared `window.VizHelpers` namespace.
VizHelpers.showTooltip = function (root, event, html) {
  const tip = root.querySelector(".tooltip");
  if (!tip) return;
  tip.style.opacity = "1";
  tip.innerHTML = html;
  tip.style.left = event.pageX + 12 + "px";
  tip.style.top = event.pageY - 28 + "px";
};
VizHelpers.hideTooltip = function (root) {
  const tip = root.querySelector(".tooltip");
  if (tip) tip.style.opacity = "0";
};
