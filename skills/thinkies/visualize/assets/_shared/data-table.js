// Root-scoped data-table renderer. It builds the `<details>` fallback table
// inside one fragment, locating the mount by class within the fragment root
// rather than by a document-global id, so two fragments each render their own
// table. The assembler inlines this once on the shared `window.VizHelpers`
// namespace.
//
// Usage from a fragment's script:
//   VizHelpers.renderDataTable(root, rows, ["Col A", "Col B"])
// where `root` is the `<section class="viz">` and the mount is the
// `.data-table` element inside it.
VizHelpers.renderDataTable = function (root, rows, columns) {
  const container = root.querySelector(".data-table");
  if (!container) return;
  const table = document.createElement("table");
  table.setAttribute("role", "table");
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  columns.forEach(function (col) {
    const th = document.createElement("th");
    th.scope = "col";
    th.textContent = col;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);
  const tbody = document.createElement("tbody");
  rows.forEach(function (row) {
    const tr = document.createElement("tr");
    row.forEach(function (cell) {
      const td = document.createElement("td");
      td.textContent = cell != null ? String(cell) : "";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  container.appendChild(table);
};
