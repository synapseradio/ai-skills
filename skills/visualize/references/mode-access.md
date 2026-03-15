# Access Mode

Build visualizations that work for everyone by making accessibility the foundation.

## When to Use

- Making a chart accessible
- Adding ARIA labels
- Ensuring colorblind safety
- Supporting screen readers
- Adding keyboard navigation
- Checking WCAG compliance
- Fixing contrast issues

## Applicability Check

**In comprehensive mode**: Always runs—accessibility is required for production-ready visualizations.

**Quick check**: Will this visualization be shared with others? If yes → run this mode.

## Core Principle

Accessibility in data visualization follows WCAG 2.1 guidelines adapted for graphical content. The goal is making visual data perceivable, operable, understandable, and robust across abilities and assistive technologies. Every visualization should communicate its message through multiple channels—visual, textual, and interactive—so no single ability becomes a barrier.

## Instructions

### 1. Establish the Accessibility Foundation

Before writing visualization code, determine the accessibility requirements:

**Identify your audience constraints**:

- Will screen reader users consume this visualization?
- Must the visualization work without color perception?
- Is keyboard-only navigation required?
- What devices and assistive technologies must be supported?

**Set your compliance target**:

- WCAG 2.1 Level AA is the standard baseline for most applications
- Level AAA provides enhanced accessibility for specialized contexts
- Government and enterprise applications may have specific mandates

**Plan your accessibility layers**:

1. Base layer: Semantic structure and text alternatives
2. Color layer: Colorblind-safe palettes and sufficient contrast
3. Interaction layer: Keyboard navigation and focus management
4. Assistive technology layer: ARIA roles, labels, and live regions

### 2. Design Color for Universal Perception

Color conveys meaning in visualization, but approximately 8% of males and 0.5% of females have some form of color vision deficiency. Design for everyone.

**Apply colorblind-safe palettes**:

Use established palettes designed for color vision deficiency:

- **Viridis**: Perceptually uniform, remains distinguishable in grayscale
- **ColorBrewer**: Offers sequential, diverging, and qualitative palettes with colorblind-safe options
- **Okabe-Ito**: Eight colors designed for maximum distinguishability across all color blindness types

**Avoid relying on color alone** (WCAG SC 1.4.1):

Every color-encoded distinction needs a secondary channel:

- Add patterns or textures to differentiate data series
- Use shapes (circles, squares, triangles) alongside colors
- Apply direct labels that identify data without requiring legend lookup
- Include icons or symbols that encode the same information

**Ensure sufficient contrast** (WCAG SC 1.4.3, 1.4.11):

| Element | Minimum Contrast Ratio |
|---------|------------------------|
| Normal text (<18pt) | 4.5:1 against background |
| Large text (>=18pt or 14pt bold) | 3:1 against background |
| Graphical objects (bars, lines, icons) | 3:1 against adjacent colors |
| UI components and focus indicators | 3:1 against adjacent colors |

Test contrast using the relative luminance formula or automated tools. Light gray lines on white backgrounds fail silently—verify every element.

**Test with color vision simulations**:

- Protanopia (red deficiency): ~1% of males
- Deuteranopia (green deficiency): ~6% of males
- Tritanopia (blue deficiency): rare, <0.01%
- Achromatopsia (complete color blindness): very rare

Run your visualization through simulation tools before shipping. If data series become indistinguishable, add non-color differentiators.

### 3. Build Semantic SVG Structure

SVG provides rich accessibility hooks when structured properly. Screen readers parse SVG elements and ARIA attributes to convey structure and meaning.

**Add accessible names and descriptions**:

Every SVG that conveys information needs accessible labeling:

```svg
<svg role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Monthly Revenue Trends</title>
  <desc id="chart-desc">
    Bar chart showing revenue from January to December.
    Revenue peaked in November at $2.4M and was lowest
    in February at $1.1M.
  </desc>
  <!-- chart content -->
</svg>
```

**Structure elements for screen readers**:

For decorative SVGs that don't convey information:

```svg
<svg aria-hidden="true">
  <!-- decorative content hidden from screen readers -->
</svg>
```

For complex data visualizations, group related elements:

```svg
<g role="list" aria-label="Data series: Sales by Region">
  <g role="listitem" aria-label="Northeast: $1.2M, 24% of total">
    <rect ... />
    <text>Northeast</text>
  </g>
  <g role="listitem" aria-label="Southeast: $0.9M, 18% of total">
    <rect ... />
    <text>Southeast</text>
  </g>
</g>
```

**Apply ARIA roles and properties**:

| Role | Use For |
|------|---------|
| `role="img"` | Static charts treated as images |
| `role="graphics-document"` | Complex, structured visualizations |
| `role="graphics-object"` | Individual data points or elements |
| `role="list"` / `role="listitem"` | Series of comparable data items |
| `role="group"` | Related elements that form a unit |

Key ARIA properties for SVG:

- `aria-label`: Concise accessible name
- `aria-labelledby`: Reference to element(s) providing the name
- `aria-describedby`: Reference to element(s) providing description
- `aria-hidden="true"`: Hide decorative or redundant elements

### 4. Implement Keyboard Navigation

All interactive elements must be operable via keyboard alone (WCAG SC 2.1.1).

**Enable keyboard focus**:

SVG elements are not focusable by default. Add `tabindex` to interactive elements:

- `tabindex="0"`: Include in natural tab order
- `tabindex="-1"`: Focusable programmatically but not in tab order

```svg
<circle tabindex="0" role="button" aria-label="Data point: Q3 2024, Revenue $1.8M" />
```

**Design logical tab order**:

Follow a predictable sequence that matches visual scanning patterns:

1. Chart title and summary
2. Legend items (if interactive)
3. Data points in reading order (left to right, top to bottom for Western locales)
4. Controls (filters, zoom, export)

**Provide visible focus indicators** (WCAG SC 2.4.7):

Focus states must be visually apparent with 3:1 contrast:

```css
.data-point:focus {
  outline: 3px solid #005FCC;
  outline-offset: 2px;
}
```

Avoid using color alone for focus—combine with outline, ring, or size change.

**Implement keyboard interactions**:

Standard keyboard patterns for interactive visualizations:

| Key | Action |
|-----|--------|
| Tab | Move focus to next interactive element |
| Shift+Tab | Move focus to previous interactive element |
| Enter/Space | Activate focused element (toggle selection, open details) |
| Arrow keys | Navigate within a group (between data points in a series) |
| Escape | Close popups, cancel operations |
| Home/End | Jump to first/last item in a series |

For D3.js, attach keyboard handlers alongside mouse events:

```javascript
selection
  .on('keydown', function(event) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleActivation(this);
    }
  });
```

### 5. Support Screen Readers

Screen readers convert visual information to speech or braille. Visualizations need text alternatives that convey meaning, not just structure.

**Write effective alt text**:

Good alt text describes the insight, not the implementation:

- Poor: "Bar chart with blue bars"
- Better: "Bar chart showing monthly revenue"
- Best: "Monthly revenue chart showing steady growth from $1.1M in January to $2.4M in November, with a slight dip to $2.1M in December"

For complex visualizations, provide layered descriptions:

1. Brief title: What is this chart?
2. Summary: What's the key takeaway?
3. Detailed data: Available on demand for users who need specifics

**Provide data tables as alternatives**:

Screen reader users often prefer tabular data over navigating complex graphics. Offer an accessible data table:

```html
<details>
  <summary>View data table</summary>
  <table aria-label="Monthly Revenue Data">
    <thead>
      <tr>
        <th scope="col">Month</th>
        <th scope="col">Revenue</th>
        <th scope="col">Change</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>January</td>
        <td>$1.1M</td>
        <td>Baseline</td>
      </tr>
      <!-- additional rows -->
    </tbody>
  </table>
</details>
```

**Use ARIA live regions for dynamic content**:

When data updates asynchronously, announce changes:

```html
<div aria-live="polite" aria-atomic="true" class="visually-hidden">
  Chart updated: New data point added for December showing $2.1M revenue
</div>
```

Choose announcement priority:

- `aria-live="polite"`: Wait for pause in user activity (most updates)
- `aria-live="assertive"`: Interrupt immediately (critical alerts only)

### 6. Handle Responsive and Zoom Requirements

Users with low vision may zoom up to 400% (WCAG SC 1.4.10). Visualizations must remain functional.

**Design for reflow**:

At 400% zoom, content should not require horizontal scrolling for standard viewports. Consider:

- Simplified layouts at smaller effective sizes
- Collapsible legends that become dropdowns
- Data tables as fallback for highly zoomed states

**Preserve text legibility**:

- Use relative units (em, rem) for font sizes where possible
- Ensure text scales with browser zoom settings
- Avoid text embedded in raster images—use SVG text elements

**Test across viewport sizes**:

Visualizations should adapt:

- Remove or simplify labels at small sizes
- Provide touch-friendly target sizes (minimum 44x44px) for mobile
- Maintain color and contrast at all sizes

### 7. Network Visualization Accessibility

Force-directed graphs and network visualizations present unique accessibility challenges. The relational nature of the data—nodes connected by edges—requires specific patterns.

**Edge contrast requirements** (WCAG SC 1.4.11):

Edges are graphical objects that must meet 3:1 contrast against the background. Common edge colors that fail on white backgrounds:

| Color | Contrast | Status |
|-------|----------|--------|
| #999 | 2.85:1 | **Fails** |
| #888 | 3.54:1 | Passes (barely) |
| #666 | 5.74:1 | Recommended |

Use #666 or darker for edge strokes. Verify contrast when edges overlay colored nodes.

**Keyboard navigation for nodes**:

Network nodes must be keyboard-accessible. Apply focus management:

```javascript
nodeLayer.selectAll('circle')
  .attr('tabindex', 0)
  .attr('role', 'button')
  .attr('aria-label', d => `${d.label}: ${d.connections} connections`)
  .on('keydown', (event, d) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      highlightConnected(d);
    }
  })
  .on('focus', (event, d) => highlightConnected(d))
  .on('blur', resetHighlight);
```

**Arrow key navigation** between connected nodes:

```javascript
.on('keydown', (event, d) => {
  if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
    const nextNode = getNextConnectedNode(d);
    if (nextNode) nextNode.node().focus();
  }
});
```

**Focus indicators for network nodes**:

Focus states must have 3:1 contrast and not rely on color alone:

```css
.node:focus {
  outline: none;  /* Remove default, provide custom */
}

.node:focus circle {
  stroke: #000;
  stroke-width: 3px;  /* 2x default width */
}
```

**Screen reader alternatives for networks**:

Network graphs cannot be fully conveyed through screen reader navigation. Provide alternative representations:

```html
<details>
  <summary>View connections as table</summary>
  <table aria-label="Topic Connections">
    <caption>Which topics appear together in sessions</caption>
    <thead>
      <tr>
        <th scope="col">Topic A</th>
        <th scope="col">Topic B</th>
        <th scope="col">Shared Sessions</th>
      </tr>
    </thead>
    <tbody>
      <!-- Populated by JS -->
    </tbody>
  </table>
</details>
```

**Interactive feedback announcements**:

When hover highlighting changes visible relationships, announce to screen readers:

```javascript
const liveRegion = d3.select('#live-announcements');

function highlightConnected(node) {
  // Visual highlighting...

  // Screen reader announcement
  const connectedCount = getConnectedNodes(node).length;
  liveRegion.text(`${node.label} is connected to ${connectedCount} other topics`);
}
```

```html
<div id="live-announcements" aria-live="polite" class="visually-hidden"></div>
```

See `network-patterns.md` for complete network accessibility patterns.

### 8. Integrate Testing Throughout Development

Accessibility requires verification, not assumption.

**Automated testing**:

Run accessibility linters during development:

- axe-core for automated WCAG checking
- eslint-plugin-jsx-a11y for React components
- Lighthouse accessibility audits in CI/CD

**Manual testing checklist**:

Automated tools catch approximately 30-40% of accessibility issues. Manual verification is essential:

- [ ] Keyboard-only navigation: Complete all tasks without a mouse
- [ ] Screen reader testing: Navigate with VoiceOver (macOS), NVDA (Windows), or Orca (Linux)
- [ ] Color simulation: View with protanopia, deuteranopia, and grayscale filters
- [ ] Zoom testing: Verify functionality at 200% and 400% zoom
- [ ] Focus management: Confirm focus is visible and logical throughout interaction
- [ ] Text alternatives: Verify all data is accessible via text

**User testing**:

Include users with disabilities in testing when possible. Simulated testing reveals technical issues; actual users reveal workflow barriers.

## Further Reading

For deeper guidance on specific accessibility topics:

- See `color-accessibility.md` for colorblind-safe palettes, contrast requirements, and testing tools
- See `assistive-tech.md` for screen reader patterns, keyboard navigation implementation, and ARIA live regions

## Phase Transition

After ensuring accessibility, consider:

- **Interact** to add keyboard-accessible interactions
- **Refine** to verify accessibility wasn't compromised during other passes
