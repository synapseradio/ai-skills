# Observable Plot Patterns

Observable Plot is a high-level visualization library built on D3. Use it for rapid prototyping and when D3's low-level control isn't needed.

## When to Use Plot vs D3

**Use Observable Plot when**:

- You need a standard chart type quickly
- The defaults are acceptable
- You want concise, declarative code
- Rapid iteration matters more than pixel-perfect control

**Use D3 directly when**:

- You need custom interactions beyond tooltips
- Standard mark types don't fit your design
- You need fine-grained animation control
- The visualization is highly custom

## Basic Pattern

```javascript
import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

const chart = Plot.plot({
  marks: [
    Plot.barY(data, {x: "category", y: "value"})
  ]
});

document.getElementById("chart").appendChild(chart);
```

Plot returns an SVG element that you append to the DOM.

## Common Chart Types

### Bar Chart

```javascript
Plot.plot({
  marks: [
    Plot.barY(data, {
      x: "category",
      y: "value",
      fill: "steelblue"
    }),
    Plot.ruleY([0])  // Zero baseline
  ]
})
```

### Horizontal Bar Chart

```javascript
Plot.plot({
  marks: [
    Plot.barX(data, {
      x: "value",
      y: "category",
      fill: "steelblue"
    })
  ],
  marginLeft: 100  // Room for category labels
})
```

### Line Chart

```javascript
Plot.plot({
  marks: [
    Plot.lineY(data, {
      x: "date",
      y: "value",
      stroke: "steelblue"
    })
  ]
})
```

### Multi-Series Line Chart

```javascript
Plot.plot({
  color: { legend: true },
  marks: [
    Plot.lineY(data, {
      x: "date",
      y: "value",
      stroke: "series"  // Color by series
    })
  ]
})
```

### Scatterplot

```javascript
Plot.plot({
  marks: [
    Plot.dot(data, {
      x: "xValue",
      y: "yValue",
      fill: "category",
      r: 5
    })
  ]
})
```

### Area Chart

```javascript
Plot.plot({
  marks: [
    Plot.areaY(data, {
      x: "date",
      y: "value",
      fill: "steelblue",
      fillOpacity: 0.5
    }),
    Plot.lineY(data, {
      x: "date",
      y: "value",
      stroke: "steelblue"
    })
  ]
})
```

### Histogram

```javascript
Plot.plot({
  marks: [
    Plot.rectY(data, Plot.binX({y: "count"}, {x: "value"})),
    Plot.ruleY([0])
  ]
})
```

### Box Plot

```javascript
Plot.plot({
  marks: [
    Plot.boxY(data, {
      x: "category",
      y: "value"
    })
  ]
})
```

### Heatmap

```javascript
Plot.plot({
  color: { scheme: "Blues" },
  marks: [
    Plot.cell(data, {
      x: "column",
      y: "row",
      fill: "value"
    })
  ]
})
```

## Faceting (Small Multiples)

```javascript
Plot.plot({
  facet: {
    data: data,
    x: "category"  // Create column for each category
  },
  marks: [
    Plot.lineY(data, {
      x: "date",
      y: "value"
    })
  ]
})
```

## Annotations

### Text Labels

```javascript
Plot.plot({
  marks: [
    Plot.barY(data, {x: "category", y: "value"}),
    Plot.text(data, {
      x: "category",
      y: "value",
      text: d => d.value,
      dy: -5
    })
  ]
})
```

### Reference Lines

```javascript
Plot.plot({
  marks: [
    Plot.lineY(data, {x: "date", y: "value"}),
    Plot.ruleY([average], {stroke: "red", strokeDasharray: "4"}),
    Plot.text([{label: "Average"}], {
      x: data[0].date,
      y: average,
      text: "label",
      dy: -5
    })
  ]
})
```

## Styling Options

### Dimensions

```javascript
Plot.plot({
  width: 800,
  height: 400,
  marginTop: 40,
  marginRight: 30,
  marginBottom: 50,
  marginLeft: 60,
  marks: [...]
})
```

### Axes

```javascript
Plot.plot({
  x: {
    label: "Date",
    tickFormat: d3.timeFormat("%b %Y")
  },
  y: {
    label: "Value ($)",
    grid: true,
    domain: [0, 1000]
  },
  marks: [...]
})
```

### Colors

```javascript
Plot.plot({
  color: {
    scheme: "Tableau10",  // Categorical
    // or
    scheme: "Blues",      // Sequential
    // or
    type: "diverging",
    scheme: "RdBu"        // Diverging
  },
  marks: [...]
})
```

## Tooltips

Plot has built-in tooltip support:

```javascript
Plot.plot({
  marks: [
    Plot.dot(data, {
      x: "xValue",
      y: "yValue",
      title: d => `${d.name}: ${d.value}`,  // Tooltip text
      fill: "category"
    })
  ]
})
```

For richer tooltips, use the `tip` mark:

```javascript
Plot.plot({
  marks: [
    Plot.dot(data, {x: "x", y: "y"}),
    Plot.tip(data, Plot.pointer({
      x: "x",
      y: "y",
      title: d => `${d.name}\nValue: ${d.value}`
    }))
  ]
})
```

## Complete Standalone Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Observable Plot Example</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 20px; }
    #chart { max-width: 800px; }
  </style>
</head>
<body>
  <h1>Monthly Sales</h1>
  <div id="chart"></div>

  <script type="module">
    import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

    const data = [
      { month: "Jan", sales: 100 },
      { month: "Feb", sales: 120 },
      { month: "Mar", sales: 90 },
      { month: "Apr", sales: 150 },
      { month: "May", sales: 200 },
      { month: "Jun", sales: 180 }
    ];

    const chart = Plot.plot({
      y: { grid: true, label: "Sales ($)" },
      marks: [
        Plot.barY(data, {
          x: "month",
          y: "sales",
          fill: "steelblue"
        }),
        Plot.text(data, {
          x: "month",
          y: "sales",
          text: d => d.sales,
          dy: -8
        }),
        Plot.ruleY([0])
      ]
    });

    document.getElementById("chart").appendChild(chart);
  </script>
</body>
</html>
```

## When to Drop Down to D3

Plot delegates to D3, so you can mix them:

```javascript
// Create Plot chart
const chart = Plot.plot({...});

// Then modify with D3
d3.select(chart)
  .selectAll("rect")
  .on("click", function(event, d) {
    // Custom interaction
  });
```

This lets you use Plot for layout while adding D3 interactions.
