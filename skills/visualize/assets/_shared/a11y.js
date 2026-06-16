// Root-scoped keyboard navigation. Arrow keys move focus between the focusable
// marks inside one fragment. It scopes its query to the fragment root rather
// than the whole document, so arrow keys in one chart never jump focus into a
// sibling chart on the same page. The assembler inlines this once on the shared
// `window.VizHelpers` namespace.
//
// Usage from a fragment's script: VizHelpers.navigateMarks(root, "ArrowLeft", "ArrowRight")
VizHelpers.navigateMarks = function (root, prevKey, nextKey) {
  if (!root) return;
  root.addEventListener("keydown", function (event) {
    const focusable = Array.from(root.querySelectorAll('[tabindex="0"]'));
    if (focusable.length === 0) return;
    const idx = focusable.indexOf(document.activeElement);
    if (event.key === nextKey && idx < focusable.length - 1) {
      event.preventDefault();
      focusable[idx + 1].focus();
    } else if (event.key === prevKey && idx > 0) {
      event.preventDefault();
      focusable[idx - 1].focus();
    }
  });
};
