# Annotation Patterns

Practical techniques for implementing annotations in data visualizations. This reference covers structural patterns, positioning strategies, and technology-specific approaches.

## Annotation Anatomy

Every annotation has three structural components:

### 1. Subject

The data element being annotated. Can be:

- **Point**: A single data point (x, y coordinate)
- **Region**: An area (circle around a point, rectangle around a cluster)
- **Range**: A span along an axis (time period, value range)
- **Line**: A threshold, trend, or reference line
- **Pattern**: Multiple elements forming a shape (trend, anomaly)

Subject type determines connector style and note positioning.

### 2. Connector

Visual link between note and subject. Types include:

- **Line**: Straight path from note to subject
- **Elbow**: Right-angle bend (horizontal then vertical, or vice versa)
- **Curve**: Smooth arc avoiding other elements
- **Arrow**: Directional indicator (points toward subject)
- **Bracket**: Spans a range (typically for duration or comparison)
- **None**: Note positioned directly on or adjacent to subject

Connector choice affects visual weight and clarity:

- Lines are minimal and precise
- Elbows maintain grid alignment
- Curves feel organic but take more space
- Arrows add directional emphasis
- Brackets emphasize extent rather than point

### 3. Note

The text content. Components include:

- **Title**: Bold or larger text for primary message (optional)
- **Label**: The annotation text itself
- **Badge**: Compact identifier (number, icon, initial)

Note length guidelines:

- Badges: 1-3 characters
- Labels: 3-10 words
- Labels with title: Title 2-5 words, label 5-20 words
- Extended callouts: 1-2 sentences maximum

Beyond these limits, content belongs in captions, legends, or supporting text rather than annotations.

## Positioning Strategies

### Quadrant Placement

For point annotations, divide space around the subject into quadrants:

```
     |
  2  |  1
-----|-----
  3  |  4
     |
```

Default preference: Quadrant 1 (upper right) for left-to-right reading cultures. Note appears above and to the right of subject.

Fallback order: 1 → 2 → 4 → 3

Adjust based on:

- Available space (avoid chart edges)
- Other annotations (avoid overlap)
- Data elements (avoid crossing lines)
- Visual hierarchy (important annotations get preferred positions)

### Leader Line Direction

When multiple annotations cluster, use consistent leader line direction:

**Radial pattern**: All lines emanate from a central point

- Works for: Crowded single regions
- Maintains: Clear association between notes and subjects

**Parallel pattern**: All lines exit in same direction before diverging

- Works for: Sequential annotations (timeline events)
- Maintains: Visual order and reading flow

**Perpendicular pattern**: Lines exit perpendicular to data trend

- Works for: Annotations along a line or curve
- Maintains: Clear distinction from data itself

### Collision Avoidance

When annotations would overlap:

**Manual adjustment**: Specify dx/dy offsets to nudge notes apart. Most precise but requires attention at each data update.

**Automatic displacement**: Algorithm pushes overlapping notes apart. Libraries like d3-annotation provide this. Less precise but handles dynamic data.

**Layering**: Only show subset of annotations; others appear on interaction. Reduces collision by reducing density.

**Aggregation**: Combine nearby annotations into single note listing multiple subjects. Reduces collision by reducing count.

### Responsive Positioning

Annotations that work at desktop widths may overlap on mobile. Strategies:

**Reduce density**: Show fewer annotations at smaller widths. Prioritize by importance.

**Reposition**: Stack annotations vertically instead of distributing around subjects. Accept longer connectors.

**Toggle mode**: Replace inline annotations with numbered markers; show notes in separate panel or on tap.

**Simplify**: Use badges instead of full labels; provide detail on interaction.

## Annotation Types by Purpose

### Labeling (identification)

Purpose: Name or identify elements
Note type: Label or badge
Connector: Short line or none
Example: "Seattle" next to a point on a map

Best practices:

- Position consistently (all above, all right, etc.)
- Keep text horizontal when possible
- Match label size to element importance

### Callout (explanation)

Purpose: Explain why something matters
Note type: Title + label
Connector: Line or elbow with clear origin
Example: "Record high—Unprecedented demand during heat wave"

Best practices:

- Use when the data point's significance isn't self-evident
- Title states the fact; label provides context
- Visual emphasis (bold, color) on most important word

### Comparison (relationship)

Purpose: Show relationship between elements
Note type: Label with bracket or dual connector
Connector: Bracket spanning compared elements
Example: "2x growth" with bracket spanning two bars

Best practices:

- Bracket should clearly span exactly the compared elements
- Note positioned at bracket center or endpoint
- Quantify the relationship (not just "higher" but "2x" or "+47%")

### Context (external reference)

Purpose: Connect data to external events
Note type: Label with optional icon
Connector: Line to relevant data region
Example: "Product launch" with line to inflection point

Best practices:

- Place along time axis for temporal context
- Use consistent treatment for all context annotations
- Distinguish visually from insight annotations (lighter weight)

### Threshold (reference line)

Purpose: Mark meaningful value level
Note type: Label along the line
Connector: None (note attached to line)
Example: "Target: 80%" along horizontal reference line

Best practices:

- Line should be visually distinct from data (dashed, lighter color)
- Label at line endpoint or where it doesn't occlude data
- Include value in label

## D3-Annotation Implementation

The d3-annotation library by Susie Lu provides structured annotation support for D3.js visualizations.

### Installation

```bash
npm install d3-annotation
```

```javascript
import { annotation, annotationCallout } from 'd3-annotation';
```

### Basic Pattern

```javascript
const annotations = [
  {
    note: {
      label: "Unexpected spike in March",
      title: "Anomaly"
    },
    x: xScale(targetDate),
    y: yScale(targetValue),
    dy: -50,  // vertical offset of note from subject
    dx: 30    // horizontal offset of note from subject
  }
];

const makeAnnotations = annotation()
  .type(annotationCallout)
  .annotations(annotations);

svg.append("g")
  .attr("class", "annotation-group")
  .call(makeAnnotations);
```

### Annotation Types

```javascript
import {
  annotationCallout,      // Line connector with note
  annotationCalloutCircle, // Circle around point, line to note
  annotationCalloutRect,   // Rectangle highlight, line to note
  annotationCalloutElbow,  // Elbow connector
  annotationCalloutCurve,  // Curved connector
  annotationLabel,         // Compact badge
  annotationBadge,         // Circular badge with text
  annotationXYThreshold    // Threshold line with label
} from 'd3-annotation';
```

### Styling

```css
.annotation-group .annotation-note-title {
  font-weight: bold;
  font-size: 14px;
}

.annotation-group .annotation-note-label {
  font-size: 12px;
  fill: #666;
}

.annotation-group .annotation-connector path {
  stroke: #333;
  stroke-width: 1px;
}

.annotation-group .annotation-subject circle {
  fill: none;
  stroke: #333;
  stroke-width: 2px;
}
```

### Data-Driven Annotations

```javascript
// Generate annotations from data conditions
const annotations = data
  .filter(d => d.value > threshold)
  .map(d => ({
    note: {
      label: `${d.value} exceeds threshold`,
      title: d.category
    },
    x: xScale(d.date),
    y: yScale(d.value),
    dy: -40,
    dx: 30
  }));
```

### Responsive Annotations

```javascript
function updateAnnotations() {
  const width = container.clientWidth;

  // Adjust annotation density based on width
  const maxAnnotations = width > 800 ? 5 : width > 500 ? 3 : 1;
  const visibleAnnotations = annotations
    .sort((a, b) => b.importance - a.importance)
    .slice(0, maxAnnotations);

  // Adjust positioning based on width
  visibleAnnotations.forEach(a => {
    a.dx = width > 500 ? 50 : 20;
    a.dy = width > 500 ? -50 : -30;
  });

  svg.select('.annotation-group')
    .call(annotation().annotations(visibleAnnotations));
}

window.addEventListener('resize', updateAnnotations);
```

## Technology-Agnostic Patterns

These patterns apply regardless of implementation technology.

### Annotation Layer Architecture

Separate annotations into a distinct layer:

```
Base layer: Axes, gridlines, reference marks
Data layer: The actual visualization
Annotation layer: Labels, callouts, connectors
Interaction layer: Hover effects, tooltips, selections
```

Benefits:

- Annotations can be toggled without affecting data rendering
- Z-ordering is explicit and predictable
- Different interaction modes for annotations vs data

### Annotation Data Model

Store annotations as structured data:

```typescript
interface Annotation {
  id: string;
  subject: {
    type: 'point' | 'region' | 'range' | 'line';
    coordinates: AnnotationCoordinates;
  };
  note: {
    title?: string;
    label: string;
  };
  connector: {
    type: 'line' | 'elbow' | 'curve' | 'arrow' | 'bracket';
    offset: { dx: number; dy: number };
  };
  style: {
    priority: 'primary' | 'secondary' | 'tertiary';
    visible: boolean;
  };
}
```

Benefits:

- Annotations are serializable (can be saved, loaded, versioned)
- Business logic separate from rendering
- Easy to filter, sort, transform

### Progressive Disclosure Pattern

Layer annotations by detail level:

**Level 0 (always visible)**: Title only
**Level 1 (default)**: Primary insight annotations (1-3)
**Level 2 (on demand)**: Secondary context annotations
**Level 3 (on drill-down)**: All available annotations

Implementation:

- Store priority/level in annotation data model
- Filter visible annotations based on current level
- Provide UI control or automatic level based on zoom/focus

### Annotation-Data Binding

Keep annotations synchronized with data:

**Derived annotations**: Calculate annotation positions from current data. When data updates, annotations update automatically.

```javascript
// Annotation position derived from data
const peakAnnotation = {
  x: xScale(findPeak(data).date),
  y: yScale(findPeak(data).value),
  label: `Peak: ${formatValue(findPeak(data).value)}`
};
```

**Declarative annotations**: Define annotations relative to data properties, not absolute coordinates.

```javascript
// Annotation defined relative to data
const annotations = [
  { dataKey: 'peak', label: 'Highest point' },
  { dataKey: 'trough', label: 'Lowest point' },
  { threshold: 100, label: 'Target exceeded' }
];
```

### Accessibility Patterns

Annotations must have text alternatives:

**Alt text**: Include annotation content in image alt text or SVG description.

**Data table**: Provide table with annotated values and their annotations.

**Screen reader text**: Add visually hidden text that reads annotation content.

**Keyboard navigation**: Allow tabbing through annotations; announce content on focus.

```html
<!-- Example: visually hidden annotation summary -->
<div class="sr-only">
  Chart annotations:
  March 2024 shows record high of 147 units, marked as anomaly.
  Product launch occurred in January 2024.
</div>
```
