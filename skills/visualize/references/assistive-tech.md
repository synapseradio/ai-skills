# Assistive Technology Reference

Detailed guidance for making visualizations work with screen readers, keyboard navigation, and other assistive technologies.

## Screen Reader Fundamentals

Screen readers traverse the DOM (or SVG structure), announcing elements based on their semantic meaning and ARIA attributes. Understanding this traversal model is essential for accessible visualization design.

### How Screen Readers Parse SVG

Screen readers process SVG elements differently than HTML:

**Native SVG semantics**: `<title>` and `<desc>` elements provide accessible names and descriptions when properly structured.

**ARIA augmentation**: SVG elements need explicit ARIA roles because most SVG elements lack semantic meaning to assistive technology.

**Text elements**: `<text>` elements are announced; `<tspan>` elements within them are typically combined.

**Grouping**: `<g>` elements provide structure but need roles to convey meaning.

### Screen Reader Modes

Users navigate in different modes:

**Browse mode**: Reading content linearly or by heading/landmark navigation.

**Focus mode**: Interacting with form controls, buttons, and other interactive elements.

**Application mode**: When `role="application"` is set, standard shortcuts are passed to the page (use sparingly).

For visualizations, most users will be in browse mode, navigating by landmarks, headings, or list items depending on how the SVG is structured.

## SVG Accessibility Patterns

### Pattern 1: Static Chart (Image Role)

For non-interactive visualizations that present fixed data:

```svg
<svg role="img" aria-labelledby="chart-title chart-desc"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 600 400">

  <title id="chart-title">Quarterly Revenue by Region</title>
  <desc id="chart-desc">
    Bar chart showing Q4 revenue. Northeast leads at $2.1M,
    followed by West ($1.8M), Southeast ($1.5M), and
    Midwest ($1.2M). Total revenue was $6.6M.
  </desc>

  <!-- Chart content -->
</svg>
```

**Key elements**:

- `role="img"` tells screen readers to treat the entire SVG as a single image
- `<title>` provides the accessible name (equivalent to alt text)
- `<desc>` provides extended description with data insights
- `aria-labelledby` references both elements for complete context

**Best for**: Simple charts where the key insight can be summarized in text.

### Pattern 2: Navigable Data (Document Role)

For complex visualizations where users benefit from exploring structure:

```svg
<svg role="graphics-document" aria-labelledby="chart-title"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 600 400">

  <title id="chart-title">Sales Performance Dashboard</title>

  <g role="group" aria-label="Revenue by quarter">
    <g role="graphics-object" aria-label="Q1: $1.2M, 18% of annual">
      <rect ... />
    </g>
    <g role="graphics-object" aria-label="Q2: $1.5M, 23% of annual">
      <rect ... />
    </g>
    <!-- Additional quarters -->
  </g>

  <g role="group" aria-label="Regional breakdown">
    <!-- Regional data -->
  </g>
</svg>
```

**Key elements**:

- `role="graphics-document"` indicates navigable graphical content
- Nested `role="group"` creates logical sections
- `role="graphics-object"` marks individual data elements

**Best for**: Dashboards, multi-series charts, or visualizations where users need to explore different aspects.

### Pattern 3: Interactive Elements (List + Listitem)

For interactive visualizations where users select or activate data points:

```svg
<svg role="img" aria-labelledby="chart-title"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 600 400">

  <title id="chart-title">Select a region to view details</title>

  <g role="list" aria-label="Regions">
    <g role="listitem" tabindex="0"
       aria-label="Northeast: $2.1M. Press Enter for details.">
      <rect ... />
    </g>
    <g role="listitem" tabindex="0"
       aria-label="West: $1.8M. Press Enter for details.">
      <rect ... />
    </g>
    <!-- Additional items -->
  </g>
</svg>
```

**Key elements**:

- `role="list"` with `role="listitem"` children enables list navigation
- `tabindex="0"` makes items keyboard-focusable
- `aria-label` on each item provides complete context including available actions

**Best for**: Clickable charts, filterable data, drill-down interfaces.

## Keyboard Navigation Implementation

### Focus Management Principles

**Only focusable elements receive focus**: Add `tabindex="0"` to elements that users should be able to reach.

**Logical focus order**: Tab order should follow visual scanning patterns (typically left-to-right, top-to-bottom for Western locales).

**Focus trap avoidance**: Users must be able to tab past the visualization to continue navigating the page.

**Focus restoration**: After closing modals or tooltips, return focus to the triggering element.

### Implementing Tab Navigation

Basic focusable element:

```svg
<g tabindex="0" role="button"
   aria-label="Data point: January, $1.2M revenue">
  <circle cx="50" cy="100" r="8" />
</g>
```

### Implementing Arrow Key Navigation

For groups of related elements, use arrow keys within the group:

```javascript
function setupArrowNavigation(container) {
  const items = container.querySelectorAll('[role="listitem"]');

  items.forEach((item, index) => {
    item.addEventListener('keydown', (event) => {
      let targetIndex;

      switch (event.key) {
        case 'ArrowRight':
        case 'ArrowDown':
          targetIndex = (index + 1) % items.length;
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          targetIndex = (index - 1 + items.length) % items.length;
          break;
        case 'Home':
          targetIndex = 0;
          break;
        case 'End':
          targetIndex = items.length - 1;
          break;
        default:
          return;
      }

      event.preventDefault();
      items[targetIndex].focus();
    });
  });
}
```

### Roving Tabindex Pattern

For complex widgets, use roving tabindex so only one element in a group is in the tab order:

```javascript
function setupRovingTabindex(container) {
  const items = container.querySelectorAll('[role="listitem"]');

  // Only first item is in tab order initially
  items.forEach((item, index) => {
    item.setAttribute('tabindex', index === 0 ? '0' : '-1');
  });

  items.forEach((item, index) => {
    item.addEventListener('keydown', (event) => {
      if (['ArrowRight', 'ArrowDown', 'ArrowLeft', 'ArrowUp'].includes(event.key)) {
        event.preventDefault();

        // Remove current from tab order
        item.setAttribute('tabindex', '-1');

        // Calculate next index
        const direction = ['ArrowRight', 'ArrowDown'].includes(event.key) ? 1 : -1;
        const nextIndex = (index + direction + items.length) % items.length;

        // Add next to tab order and focus
        items[nextIndex].setAttribute('tabindex', '0');
        items[nextIndex].focus();
      }
    });
  });
}
```

### Focus Indicators

CSS for visible focus states:

```css
[tabindex]:focus {
  outline: 3px solid #005FCC;
  outline-offset: 2px;
}

/* For SVG elements that don't support outline well */
[tabindex]:focus rect,
[tabindex]:focus circle,
[tabindex]:focus path {
  stroke: #005FCC;
  stroke-width: 3;
}

/* High contrast mode support */
@media (forced-colors: active) {
  [tabindex]:focus {
    outline: 3px solid CanvasText;
  }
}
```

## ARIA Live Regions

For dynamic content updates, announce changes to screen readers.

### Implementation Pattern

```html
<!-- Hidden announcement region -->
<div id="chart-announcements"
     aria-live="polite"
     aria-atomic="true"
     class="visually-hidden">
</div>
```

CSS for visually hidden but screen reader accessible:

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

JavaScript to announce updates:

```javascript
function announce(message) {
  const region = document.getElementById('chart-announcements');
  region.textContent = message;
}

// Usage
announce('Chart filtered to show only Q4 data. 4 regions displayed.');
announce('Northeast selected. Revenue: $2.1 million, 32% of total.');
```

### Announcement Best Practices

**Be concise**: Long announcements interrupt users. Summarize key information.

**Use polite priority**: `aria-live="polite"` waits for a pause. Use "assertive" only for critical alerts.

**Avoid redundancy**: If the action is obvious from context (button clicked, focus moved), don't over-announce.

**Include actionable context**: "Press Escape to close" is more useful than just announcing content.

## Data Tables as Alternatives

Screen reader users often prefer tabular data. Provide accessible table alternatives.

### Collapsible Table Pattern

```html
<details>
  <summary>View data as table</summary>

  <table>
    <caption>Quarterly Revenue by Region (in millions)</caption>
    <thead>
      <tr>
        <th scope="col">Region</th>
        <th scope="col">Q1</th>
        <th scope="col">Q2</th>
        <th scope="col">Q3</th>
        <th scope="col">Q4</th>
        <th scope="col">Total</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Northeast</th>
        <td>$1.8</td>
        <td>$1.9</td>
        <td>$2.0</td>
        <td>$2.1</td>
        <td>$7.8</td>
      </tr>
      <!-- Additional rows -->
    </tbody>
  </table>
</details>
```

### Table Accessibility Requirements

**Caption**: Identifies the table's purpose.

**Headers**: Use `<th>` with appropriate `scope`:

- `scope="col"` for column headers
- `scope="row"` for row headers

**Simple structure**: Avoid merged cells where possible. Screen readers handle simple tables more reliably than complex layouts.

## Testing with Assistive Technologies

### VoiceOver (macOS)

**Enable**: System Preferences > Accessibility > VoiceOver, or press Cmd+F5.

**Navigate**:

- VO+Right/Left: Move to next/previous element
- VO+Cmd+H: Next heading
- VO+Cmd+L: Next link
- Tab: Next focusable element

**Test checklist**:

1. Navigate to the visualization
2. Verify the chart title is announced
3. Verify the description is available (VO+Shift+H for help menu)
4. Navigate through data elements
5. Test interactive elements with VO+Space

### NVDA (Windows)

**Enable**: Start from system tray icon or desktop shortcut.

**Navigate**:

- Arrow keys: Browse mode reading
- Tab: Focus mode navigation
- H: Next heading
- D: Next landmark

**Test checklist**:

1. Navigate to the visualization
2. Verify role and name are announced
3. Use arrow keys to explore content
4. Tab to interactive elements
5. Activate with Enter or Space

### Common Screen Reader Issues

**Missing accessible name**: Element announced as "graphic" or "group" without context.

- Fix: Add `aria-label` or `aria-labelledby`.

**Incorrect role**: Content read as generic element rather than specific type.

- Fix: Add appropriate `role` attribute.

**Focus never reaches element**: Interactive element cannot be accessed via keyboard.

- Fix: Add `tabindex="0"`.

**Announcement is too verbose**: Every decorative element is announced.

- Fix: Add `aria-hidden="true"` to decorative elements.

**Dynamic updates not announced**: Filter changes or data updates are silent.

- Fix: Use `aria-live` region to announce changes.

## Browser and AT Compatibility

Different browser/screen reader combinations have varying support:

### Tested Combinations

| Browser | Screen Reader | Notes |
|---------|---------------|-------|
| Chrome | NVDA | Good SVG support, use with Windows |
| Firefox | NVDA | Strong ARIA support |
| Safari | VoiceOver | Best macOS combination |
| Chrome | VoiceOver | Works but Safari preferred |
| Edge | NVDA | Chromium-based, similar to Chrome |
| Firefox | JAWS | Good commercial AT support |

### Known Limitations

**Inline vs External SVG**: `aria-labelledby` to hidden elements works reliably only for inline SVG. External SVG files may require `aria-label` instead.

**Graphics roles**: `role="graphics-document"` and `role="graphics-object"` have inconsistent support. Test with target browsers.

**Focus within SVG**: Some browser/AT combinations don't properly announce focused SVG elements. Ensure focus indicators are visible to sighted keyboard users as a fallback.

## Mobile Accessibility

### Touch Navigation

VoiceOver (iOS) and TalkBack (Android) use swipe gestures:

- Swipe right: Next element
- Swipe left: Previous element
- Double-tap: Activate

**Considerations**:

- Ensure tap targets are at least 44x44px
- Provide gesture alternatives for drag operations
- Test with VoiceOver/TalkBack on actual devices

### Responsive Behavior

Visualizations should remain accessible at mobile sizes:

- Simplify layouts rather than shrinking elements too small
- Provide data table alternative when chart becomes cramped
- Maintain touch target sizes even when visual elements shrink

## Accessibility Testing Checklist

### Automated Checks

- [ ] Run axe-core on the page containing the visualization
- [ ] Verify no ARIA errors in browser console
- [ ] Check Lighthouse accessibility score

### Keyboard Testing

- [ ] Tab to every interactive element
- [ ] Use arrow keys within groups
- [ ] Press Enter/Space to activate elements
- [ ] Press Escape to close modals/tooltips
- [ ] Verify focus is visible at all times
- [ ] Verify focus order is logical

### Screen Reader Testing

- [ ] Verify chart title is announced on entry
- [ ] Verify extended description is available
- [ ] Navigate through all data elements
- [ ] Verify each element provides complete context
- [ ] Test interactive elements (selection, activation)
- [ ] Verify dynamic updates are announced

### Cross-Browser Testing

- [ ] Test with VoiceOver + Safari (macOS primary)
- [ ] Test with NVDA + Chrome or Firefox (Windows primary)
- [ ] Test on at least one mobile platform if applicable
