# Vega-Lite Spec Patterns

Comprehensive reference for building Vega-Lite JSON specifications. Vega-Lite is a high-level grammar of interactive graphics that compiles to full Vega specs. Use it for standard chart types where the defaults are acceptable and you want concise, declarative code.

## Grammar Overview

Every Vega-Lite spec is a JSON object with these top-level properties:

| Property | Required | Purpose |
|----------|----------|---------|
| `$schema` | Yes | Schema URL for validation. Use `https://vega.github.io/schema/vega-lite/v6.json` |
| `data` | Yes | Inline values, URL reference, or named dataset |
| `mark` | Yes | Visual element type (bar, line, point, etc.) |
| `encoding` | Yes | Maps data fields to visual channels (x, y, color, etc.) |
| `transform` | No | Data transformations before encoding |
| `params` | No | Interactive parameters (selections, variables) |
| `config` | No | Theme-level defaults (fonts, colors, axes) |
| `title` | No | Chart title (string or object with subtitle) |
| `description` | No | Accessible text description (becomes SVG `<desc>`) |
| `width` | No | Chart width in pixels or `"container"` for responsive |
| `height` | No | Chart height in pixels |

Minimal working spec:

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "data": { "values": [{"a": 1}, {"a": 2}, {"a": 3}] },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "quantitative"}
  }
}
```

## Data Types

Every encoding channel requires a data type. The type determines scale, axis formatting, and default behavior.

| Type | Keyword | Use for | Default scale |
|------|---------|---------|---------------|
| Quantitative | `"quantitative"` | Continuous numbers (revenue, temperature) | Linear |
| Nominal | `"nominal"` | Unordered categories (country, product name) | Ordinal (point) |
| Ordinal | `"ordinal"` | Ordered categories (rating: low/med/high, month names) | Ordinal (point) |
| Temporal | `"temporal"` | Dates and times (ISO 8601 strings, timestamps) | Time |

```json
{"field": "revenue", "type": "quantitative"}
{"field": "category", "type": "nominal"}
{"field": "rating", "type": "ordinal"}
{"field": "date", "type": "temporal"}
```

## Mark Types

### Simple Marks

Each mark type produces a different visual element. The mark property accepts a string shorthand or an object with additional properties.

**arc** -- Pie charts, donut charts, radial gauges.

```json
{
  "mark": {"type": "arc", "innerRadius": 0, "stroke": "white", "strokeWidth": 2, "tooltip": true},
  "encoding": {
    "theta": {"field": "value", "type": "quantitative", "stack": true},
    "color": {"field": "category", "type": "nominal"}
  }
}
```

Set `innerRadius` to a positive value (e.g., 50) for a donut chart.

**area** -- Filled regions emphasizing cumulative magnitude over time.

```json
{
  "mark": {"type": "area", "line": true, "opacity": 0.7, "interpolate": "monotone", "tooltip": true},
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "value", "type": "quantitative", "stack": true}
  }
}
```

Set `"stack": "normalize"` on the y encoding for 100% stacked area.

**bar** -- Categorical comparison, histograms, stacked composition.

```json
{
  "mark": {"type": "bar", "tooltip": true, "cornerRadiusTopLeft": 2, "cornerRadiusTopRight": 2},
  "encoding": {
    "x": {"field": "category", "type": "nominal", "sort": "-y"},
    "y": {"field": "value", "type": "quantitative", "scale": {"zero": true}}
  }
}
```

Y-axis baseline MUST start at zero for bar charts. Bar length encodes magnitude.

**circle** -- Alias for `point` with `filled: true` and circle shape. Useful for bubble charts.

```json
{
  "mark": {"type": "circle", "opacity": 0.7, "tooltip": true},
  "encoding": {
    "x": {"field": "x", "type": "quantitative"},
    "y": {"field": "y", "type": "quantitative"},
    "size": {"field": "magnitude", "type": "quantitative"}
  }
}
```

**geoshape** -- Geographic regions (choropleth maps). Requires projection config.

```json
{
  "mark": {"type": "geoshape", "tooltip": true},
  "projection": {"type": "albersUsa"},
  "encoding": {
    "color": {"field": "rate", "type": "quantitative", "scale": {"scheme": "blues"}}
  }
}
```

**image** -- Render images at data-driven positions.

```json
{
  "mark": {"type": "image", "width": 50, "height": 50},
  "encoding": {
    "x": {"field": "x", "type": "quantitative"},
    "y": {"field": "y", "type": "quantitative"},
    "url": {"field": "imageUrl", "type": "nominal"}
  }
}
```

**line** -- Trends over time for continuous phenomena.

```json
{
  "mark": {"type": "line", "point": true, "interpolate": "monotone", "tooltip": true},
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "value", "type": "quantitative"},
    "color": {"field": "series", "type": "nominal"}
  }
}
```

Interpolation options: `"linear"` (straight segments), `"monotone"` (smooth, no overshoots), `"step"` (discrete aggregations), `"step-after"`, `"step-before"`, `"basis"`, `"cardinal"`, `"natural"`.

**point** -- Scatterplots, dot plots.

```json
{
  "mark": {"type": "point", "filled": true, "opacity": 0.6, "size": 60, "tooltip": true},
  "encoding": {
    "x": {"field": "x", "type": "quantitative", "scale": {"zero": false}},
    "y": {"field": "y", "type": "quantitative", "scale": {"zero": false}},
    "color": {"field": "category", "type": "nominal"},
    "shape": {"field": "type", "type": "nominal"}
  }
}
```

**rect** -- Heatmaps, 2D binned plots, calendar views.

```json
{
  "mark": {"type": "rect", "tooltip": true},
  "encoding": {
    "x": {"field": "hour", "type": "ordinal"},
    "y": {"field": "day", "type": "ordinal"},
    "color": {"field": "value", "type": "quantitative", "scale": {"scheme": "blues"}}
  }
}
```

**rule** -- Reference lines, range lines, error bars (manual).

```json
{
  "mark": {"type": "rule", "color": "red", "strokeDash": [4, 4]},
  "encoding": {
    "y": {"datum": 50}
  }
}
```

Use `datum` (not `field`) for constant values. For range rules, use `y` and `y2`.

**square** -- Alias for `point` with `filled: true` and square shape.

```json
{
  "mark": {"type": "square", "size": 100, "tooltip": true},
  "encoding": {
    "x": {"field": "col", "type": "ordinal"},
    "y": {"field": "row", "type": "ordinal"},
    "color": {"field": "value", "type": "quantitative"}
  }
}
```

**text** -- Data labels, annotations.

```json
{
  "mark": {"type": "text", "fontSize": 11, "dy": -8},
  "encoding": {
    "x": {"field": "category", "type": "nominal"},
    "y": {"field": "value", "type": "quantitative"},
    "text": {"field": "value", "type": "quantitative", "format": ",.0f"}
  }
}
```

**tick** -- Strip plots, distribution previews along an axis.

```json
{
  "mark": {"type": "tick", "thickness": 2},
  "encoding": {
    "x": {"field": "value", "type": "quantitative"},
    "color": {"field": "group", "type": "nominal"}
  }
}
```

**trail** -- Lines with variable width encoding a third variable.

```json
{
  "mark": {"type": "trail", "tooltip": true},
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "price", "type": "quantitative"},
    "size": {"field": "volume", "type": "quantitative"}
  }
}
```

### Composite Marks

Composite marks are shorthand for multi-layer statistical visualizations.

**boxplot** -- Five-number summary with outlier detection.

```json
{
  "mark": {
    "type": "boxplot",
    "extent": 1.5,
    "tooltip": true,
    "median": {"color": "#1a365d"},
    "outliers": {"color": "#e53e3e"}
  },
  "encoding": {
    "x": {"field": "group", "type": "nominal"},
    "y": {"field": "value", "type": "quantitative", "scale": {"zero": false}},
    "color": {"field": "group", "type": "nominal", "legend": null}
  }
}
```

`extent: 1.5` uses Tukey's rule (1.5x IQR). Set `extent: "min-max"` for min/max whiskers (not recommended -- hides outliers).

**errorband** -- Confidence intervals or uncertainty ranges around a trend.

```json
{
  "mark": {"type": "errorband", "extent": "ci"},
  "encoding": {
    "x": {"field": "date", "type": "temporal"},
    "y": {"field": "value", "type": "quantitative"}
  }
}
```

`extent` options: `"ci"` (95% confidence interval), `"stderr"`, `"stdev"`, `"iqr"`.

**errorbar** -- Point-level uncertainty.

```json
{
  "mark": {"type": "errorbar", "extent": "stderr"},
  "encoding": {
    "x": {"field": "group", "type": "nominal"},
    "y": {"field": "value", "type": "quantitative"}
  }
}
```

For pre-computed error values, use `y`, `yError`, and `yError2` fields.

## Encoding Channels

### Position Channels

| Channel | Purpose | Example |
|---------|---------|---------|
| `x` | Horizontal position | `{"field": "date", "type": "temporal"}` |
| `y` | Vertical position | `{"field": "value", "type": "quantitative"}` |
| `x2` | Secondary horizontal (range end) | `{"field": "high"}` |
| `y2` | Secondary vertical (range end) | `{"field": "close"}` |
| `xOffset` | Sub-position within band (grouped bars) | `{"field": "series", "type": "nominal"}` |
| `yOffset` | Sub-position within band (grouped rows) | `{"field": "series", "type": "nominal"}` |

### Mark Property Channels

| Channel | Purpose | Example |
|---------|---------|---------|
| `color` | Fill and stroke color | `{"field": "category", "type": "nominal", "scale": {"scheme": "tableau10"}}` |
| `opacity` | Transparency (0-1) | `{"field": "confidence", "type": "quantitative"}` |
| `size` | Point/circle area, trail width | `{"field": "population", "type": "quantitative", "scale": {"range": [50, 3000]}}` |
| `shape` | Point shape (circle, square, triangle, etc.) | `{"field": "type", "type": "nominal"}` |
| `strokeDash` | Line dash pattern | `{"field": "projected", "type": "nominal"}` |
| `strokeWidth` | Line/border thickness | `{"field": "importance", "type": "quantitative"}` |

### Text and Tooltip Channels

| Channel | Purpose | Example |
|---------|---------|---------|
| `text` | Text mark content | `{"field": "label", "type": "nominal"}` |
| `tooltip` | Hover tooltip (single or array) | `[{"field": "name", "title": "Name"}, {"field": "value", "format": "$,.0f"}]` |

### Facet Channels

| Channel | Purpose | Example |
|---------|---------|---------|
| `row` | Small multiples vertically | `{"field": "region", "type": "nominal"}` |
| `column` | Small multiples horizontally | `{"field": "year", "type": "ordinal"}` |
| `facet` | Wrapping small multiples | `{"field": "category", "type": "nominal", "columns": 3}` |

### Detail and Order

| Channel | Purpose | Example |
|---------|---------|---------|
| `detail` | Group data without visual encoding | `{"field": "id"}` -- creates separate lines per id without coloring |
| `order` | Sort order for stacking/layering | `{"field": "series", "type": "nominal"}` |

## Encoding Properties

Every encoding channel supports these properties:

```json
{
  "field": "revenue",
  "type": "quantitative",
  "title": "Revenue (USD)",
  "axis": {
    "format": "$,.0f",
    "grid": true,
    "gridDash": [2, 2],
    "gridColor": "#e5e7eb",
    "labelAngle": -45,
    "labelAlign": "right",
    "tickCount": 10
  },
  "scale": {
    "zero": true,
    "nice": true,
    "domain": [0, 100],
    "range": [0, 500],
    "scheme": "blues"
  },
  "legend": {
    "title": "Category",
    "orient": "top"
  }
}
```

Use `"datum": 50` instead of `"field"` for constant values (reference lines, annotations).

## Scale Configuration

Scales map data values to visual values. Key properties:

```json
{
  "scale": {
    "zero": true,
    "nice": true,
    "domain": [0, 100],
    "range": [0, 500],
    "type": "log",
    "scheme": "tableau10",
    "clamp": true,
    "reverse": false
  }
}
```

| Property | Purpose | Common values |
|----------|---------|---------------|
| `zero` | Include zero in domain | `true` for bars (mandatory), `false` for scatter/line |
| `nice` | Round domain to clean values | `true` (default for quantitative) |
| `domain` | Explicit data range | `[0, 100]`, or data-driven (omit to auto-compute) |
| `range` | Output pixel/visual range | `[50, 3000]` for size, color values for color |
| `type` | Scale function | `"linear"`, `"log"`, `"sqrt"`, `"pow"`, `"symlog"`, `"time"` |
| `scheme` | Named color scheme | See color schemes table below |
| `clamp` | Clamp out-of-domain values | `true` to prevent overflow |
| `reverse` | Reverse scale direction | `true` for inverted axes |

### Color Schemes

| Category | Schemes | Use case |
|----------|---------|----------|
| Categorical | `tableau10`, `set2`, `pastel1`, `category10` | Nominal categories (up to 10) |
| Sequential | `blues`, `greens`, `viridis`, `plasma`, `cividis` | Unidirectional quantitative |
| Diverging | `redblue`, `redgrey`, `purplegreen`, `blueorange` | Data with meaningful midpoint |

`viridis` is perceptually uniform and works in grayscale. `cividis` is optimized for color vision deficiency. `tableau10` is the safest default for categorical data.

## Composition

### Layer -- Overlay multiple marks on the same axes.

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "data": {"values": [...]},
  "layer": [
    {
      "mark": {"type": "rule", "tooltip": true},
      "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "low", "type": "quantitative"},
        "y2": {"field": "high"}
      }
    },
    {
      "mark": {"type": "bar", "width": 12},
      "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "open", "type": "quantitative"},
        "y2": {"field": "close"}
      }
    }
  ]
}
```

Data can be specified at the top level (shared) or per layer (independent).

### Horizontal and Vertical Concatenation

```json
{
  "hconcat": [
    {"mark": "bar", "encoding": {...}},
    {"mark": "point", "encoding": {...}}
  ]
}
```

```json
{
  "vconcat": [
    {"mark": "line", "encoding": {...}, "height": 300},
    {"mark": "bar", "encoding": {...}, "height": 100}
  ]
}
```

Use `"resolve": {"scale": {"x": "shared"}}` to sync axes across concatenated views.

### Facet -- Small multiples from a single dataset.

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "data": {"values": [...]},
  "facet": {"field": "region", "type": "nominal", "columns": 3},
  "spec": {
    "mark": "line",
    "encoding": {
      "x": {"field": "date", "type": "temporal"},
      "y": {"field": "value", "type": "quantitative"}
    },
    "width": 200,
    "height": 150
  }
}
```

Alternatively, use `row` and `column` encoding channels for inline faceting.

### Repeat -- Same spec with different fields.

```json
{
  "repeat": {"column": ["revenue", "profit", "growth"]},
  "spec": {
    "mark": "bar",
    "encoding": {
      "x": {"field": "category", "type": "nominal"},
      "y": {"field": {"repeat": "column"}, "type": "quantitative"}
    },
    "width": 200,
    "height": 200
  }
}
```

## Interactivity

### Point Selection

Select individual data points by clicking.

```json
{
  "params": [
    {
      "name": "highlight",
      "select": {"type": "point", "fields": ["category"]}
    }
  ],
  "mark": {"type": "bar", "tooltip": true},
  "encoding": {
    "opacity": {
      "condition": {"param": "highlight", "value": 1},
      "value": 0.3
    }
  }
}
```

### Interval Selection

Select a range by click-dragging.

```json
{
  "params": [
    {
      "name": "brush",
      "select": {"type": "interval", "encodings": ["x"]}
    }
  ],
  "mark": "point",
  "encoding": {
    "color": {
      "condition": {"param": "brush", "field": "category", "type": "nominal"},
      "value": "grey"
    }
  }
}
```

### Bind to Input Widgets

Create sliders, dropdowns, and other HTML controls.

```json
{
  "params": [
    {
      "name": "minRevenue",
      "value": 0,
      "bind": {"input": "range", "min": 0, "max": 100000, "step": 1000, "name": "Min Revenue: "}
    },
    {
      "name": "selectedRegion",
      "bind": {"input": "select", "options": [null, "North", "South", "East"], "name": "Region: "}
    }
  ],
  "transform": [
    {"filter": "datum.revenue >= minRevenue"},
    {"filter": "selectedRegion == null || datum.region == selectedRegion"}
  ]
}
```

### Conditional Encoding

Apply different encodings based on selection state or data conditions.

```json
{
  "color": {
    "condition": {"param": "highlight", "field": "category", "type": "nominal"},
    "value": "lightgray"
  }
}
```

Data-driven condition (no selection):

```json
{
  "color": {
    "condition": {"test": "datum.value > 100", "value": "red"},
    "value": "steelblue"
  }
}
```

## Data Transforms

Transforms modify data before encoding. Applied in array order.

### filter -- Remove rows.

```json
{"filter": "datum.value > 0"}
{"filter": {"field": "category", "oneOf": ["A", "B", "C"]}}
{"filter": {"field": "date", "timeUnit": "year", "equal": 2024}}
```

### calculate -- Add computed fields.

```json
{"calculate": "datum.revenue - datum.cost", "as": "profit"}
{"calculate": "datum.open <= datum.close", "as": "bullish"}
{"calculate": "format(datum.value / datum.total * 100, '.1f') + '%'", "as": "pctLabel"}
```

### aggregate -- Group and summarize.

```json
{
  "aggregate": [
    {"op": "mean", "field": "value", "as": "avgValue"},
    {"op": "count", "as": "rowCount"}
  ],
  "groupby": ["category"]
}
```

Aggregate operations: `count`, `sum`, `mean`, `median`, `min`, `max`, `stdev`, `stderr`, `q1`, `q3`, `ci0`, `ci1`, `distinct`, `valid`, `missing`.

### bin -- Discretize continuous values.

```json
{"bin": true, "field": "value", "as": "binned_value"}
{"bin": {"maxbins": 20}, "field": "value", "as": "binned_value"}
{"bin": {"step": 5}, "field": "value", "as": "binned_value"}
```

Can also be set directly in encoding: `"x": {"field": "value", "bin": true}`.

### fold -- Unpivot wide-format data to long format.

```json
{
  "fold": ["revenue", "cost", "profit"],
  "as": ["metric", "amount"]
}
```

Converts `{revenue: 100, cost: 60, profit: 40}` into three rows with `metric` and `amount` fields.

### flatten -- Expand array-valued fields.

```json
{"flatten": ["tags"]}
```

Converts `{name: "A", tags: ["x", "y"]}` into two rows.

### window -- Running calculations.

```json
{
  "window": [
    {"op": "rank", "as": "rank"},
    {"op": "sum", "field": "value", "as": "cumulative"}
  ],
  "sort": [{"field": "value", "order": "descending"}],
  "groupby": ["category"]
}
```

Window operations: `row_number`, `rank`, `dense_rank`, `percent_rank`, `cume_dist`, `ntile`, `lag`, `lead`, `first_value`, `last_value`, plus all aggregate ops as running calculations.

### joinaggregate -- Add aggregate values as new columns without collapsing rows.

```json
{
  "joinaggregate": [
    {"op": "mean", "field": "value", "as": "groupMean"},
    {"op": "max", "field": "value", "as": "groupMax"}
  ],
  "groupby": ["category"]
}
```

Adds the group-level aggregate to every row in that group. Useful for computing deviations from group mean or normalizing within groups.

### density -- Kernel density estimation.

```json
{
  "density": "value",
  "bandwidth": 5,
  "groupby": ["category"],
  "as": ["value", "density"]
}
```

Use for violin-like overlays. Bandwidth controls smoothing.

## Responsive Sizing

### Container-Relative Width

```json
{
  "width": "container",
  "height": 400
}
```

Requires the parent HTML element to have a defined width. The chart fills the container and resizes with the window.

### Autosize

```json
{
  "autosize": {
    "type": "fit",
    "contains": "padding",
    "resize": true
  }
}
```

`type` options: `"pad"` (default, expands to fit content), `"fit"` (shrink content to fit dimensions), `"fit-x"` / `"fit-y"` (fit one dimension), `"none"`.

## Common Patterns

### Sorting

Sort axis by value (descending):

```json
{"field": "category", "type": "nominal", "sort": "-y"}
```

Sort by explicit order:

```json
{"field": "day", "type": "ordinal", "sort": ["Mon", "Tue", "Wed", "Thu", "Fri"]}
```

Sort by another field:

```json
{"field": "category", "sort": {"field": "revenue", "op": "sum", "order": "descending"}}
```

### Conditional Color

Color based on data value:

```json
{
  "color": {
    "condition": {"test": "datum.change > 0", "value": "#26a269"},
    "value": "#e01b24"
  }
}
```

### Layered Chart with Shared Data

Combine marks on the same dataset (e.g., line + points + labels):

```json
{
  "data": {"values": [...]},
  "layer": [
    {"mark": "line", "encoding": {"x": {...}, "y": {...}}},
    {"mark": {"type": "point", "filled": true}, "encoding": {"x": {...}, "y": {...}}},
    {"mark": {"type": "text", "dy": -10}, "encoding": {"x": {...}, "y": {...}, "text": {"field": "value"}}}
  ]
}
```

### Grouped Bars via xOffset

```json
{
  "encoding": {
    "x": {"field": "quarter", "type": "nominal"},
    "xOffset": {"field": "region", "type": "nominal"},
    "y": {"field": "sales", "type": "quantitative"},
    "color": {"field": "region", "type": "nominal"}
  }
}
```

### Tooltip Array

Show multiple fields in tooltip:

```json
{
  "tooltip": [
    {"field": "name", "type": "nominal", "title": "Company"},
    {"field": "revenue", "type": "quantitative", "title": "Revenue", "format": "$,.0f"},
    {"field": "growth", "type": "quantitative", "title": "Growth", "format": ".1%"}
  ]
}
```

### Histogram with Automatic Binning

```json
{
  "mark": "bar",
  "encoding": {
    "x": {"field": "value", "type": "quantitative", "bin": true, "title": "Score"},
    "y": {"aggregate": "count", "type": "quantitative", "title": "Frequency"}
  }
}
```

### Normalized Stacked Bar (100%)

```json
{
  "encoding": {
    "y": {"field": "value", "type": "quantitative", "stack": "normalize"}
  }
}
```

### Selection-Driven Filtering Across Views

```json
{
  "vconcat": [
    {
      "params": [{"name": "brush", "select": {"type": "interval", "encodings": ["x"]}}],
      "mark": "area",
      "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "value", "type": "quantitative"}
      },
      "height": 60
    },
    {
      "mark": "area",
      "encoding": {
        "x": {"field": "date", "type": "temporal", "scale": {"domain": {"param": "brush"}}},
        "y": {"field": "value", "type": "quantitative"}
      },
      "height": 300
    }
  ]
}
```

### Axis Formatting

```json
{
  "axis": {
    "format": "$,.0f",
    "formatType": "number",
    "tickCount": 10,
    "grid": true,
    "gridDash": [2, 2],
    "gridColor": "#e5e7eb",
    "labelAngle": -45,
    "labelAlign": "right",
    "labelColor": "#6b7280",
    "titleColor": "#374151",
    "tickColor": "#d1d5db",
    "domainColor": "#d1d5db"
  }
}
```

Common format strings: `",.0f"` (integer with commas), `"$,.2f"` (currency), `".1%"` (percentage), `"%b %Y"` (month year), `"%b %d"` (month day).

## Config Object

The `config` object sets theme-level defaults. Every property set here applies to all marks, axes, and legends unless overridden.

```json
{
  "config": {
    "view": {"stroke": null},
    "axis": {
      "labelFontSize": 12,
      "titleFontSize": 13,
      "labelColor": "#6b7280",
      "titleColor": "#374151",
      "tickColor": "#d1d5db",
      "domainColor": "#d1d5db"
    },
    "legend": {
      "labelFontSize": 11,
      "titleFontSize": 12
    },
    "title": {
      "fontSize": 16,
      "subtitleFontSize": 12,
      "subtitleColor": "#666"
    },
    "bar": {
      "continuousBandSize": 20
    },
    "point": {
      "filled": true
    }
  }
}
```

`"view": {"stroke": null}` removes the default border around the chart area.

## Common Pitfalls

**Pitfall: Bar chart y-axis does not start at zero.** Bar length encodes magnitude. A non-zero baseline truncates the visual encoding, making small differences look large. Always set `"scale": {"zero": true}` for bar charts. Exception: price charts (candlestick, line) where the full range matters more.

**Pitfall: Using `field` instead of `datum` for constants.** To draw a reference line at y=50, use `"y": {"datum": 50}`, not a filter-and-field approach.

**Pitfall: Missing `type` on encoding.** Every field encoding requires a type. Omitting it produces undefined behavior. Use `"quantitative"`, `"nominal"`, `"ordinal"`, or `"temporal"`.

**Pitfall: Stacked bars with negative values.** Standard stacking cannot handle negative values. Use `"stack": null` to disable stacking, or use a diverging stacked bar pattern with separate positive/negative layers.

**Pitfall: Too many categories in color encoding.** Beyond 10 categories, colors become indistinguishable. Aggregate small categories into "Other" or use faceting instead of color.

**Pitfall: Temporal axis with non-ISO dates.** Vega-Lite parses dates as UTC by default. Use ISO 8601 format (`"2024-01-15"` or `"2024-01-15T10:30:00"`). Ambiguous formats like `"01/15/2024"` may parse incorrectly across locales.

**Pitfall: `width: "container"` has no effect.** The parent HTML element must have a defined width. If the chart renders at 0 width, the container has no explicit dimensions.

## Sources

- Vega-Lite documentation -- https://vega.github.io/vega-lite/docs/
- Vega-Lite examples -- https://vega.github.io/vega-lite/examples/
- Vega-Lite schema v6 -- https://vega.github.io/schema/vega-lite/v6.json
