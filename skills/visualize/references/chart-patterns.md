# Chart-Specific D3 Patterns

D3.js implementation patterns organized by data relationship category. Each pattern shows the core scale setup and mark rendering for its chart type. Verify D3 scale and layout API usage against the current D3 documentation before implementing.

## Comparisons (Bar Charts)

```javascript
// Band scale for categories
const xScale = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, width])
  .padding(0.2);

// Linear scale for values (start at 0)
const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0])
  .nice();

// Bars
svg.selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", d => xScale(d.category))
  .attr("y", d => yScale(d.value))
  .attr("width", xScale.bandwidth())
  .attr("height", d => height - yScale(d.value))
  .attr("fill", colors[0]);
```

## Distributions (Histograms)

```javascript
// Bin the data
const bins = d3.bin()
  .value(d => d.value)
  .domain(xScale.domain())
  .thresholds(20)
  (data);

// Rectangles for each bin
svg.selectAll("rect")
  .data(bins)
  .join("rect")
  .attr("x", d => xScale(d.x0) + 1)
  .attr("width", d => Math.max(0, xScale(d.x1) - xScale(d.x0) - 1))
  .attr("y", d => yScale(d.length))
  .attr("height", d => height - yScale(d.length))
  .attr("fill", colors[0]);
```

## Relationships (Scatter Plots)

```javascript
// Linear scales for both axes
const xScale = d3.scaleLinear()
  .domain(d3.extent(data, d => d.x))
  .range([0, width])
  .nice();

const yScale = d3.scaleLinear()
  .domain(d3.extent(data, d => d.y))
  .range([height, 0])
  .nice();

// Points
svg.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", 5)
  .attr("fill", d => colorScale(d.category))
  .attr("opacity", 0.7);
```

## Temporal (Line Charts)

```javascript
// Time scale for x-axis
const xScale = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

// Line generator
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value));

// Path
svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", colors[0])
  .attr("stroke-width", 2)
  .attr("d", line);
```

## Compositions (Pie/Donut)

```javascript
// Pie layout
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

// Arc generator
const arc = d3.arc()
  .innerRadius(0)  // 0 for pie, >0 for donut
  .outerRadius(Math.min(width, height) / 2);

// Slices
svg.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colors[i % colors.length])
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

## Pattern Selection Guide

| Data Relationship | Primary Pattern | When to Use |
|-------------------|-----------------|-------------|
| Category comparison | Bar chart | Comparing quantities across discrete categories |
| Value distribution | Histogram | Showing frequency distribution of continuous data |
| Two-variable correlation | Scatter plot | Exploring relationships between variables |
| Change over time | Line chart | Showing trends in values over continuous time |
| Part-to-whole | Pie/Donut | Showing proportions (max 5-7 slices) |

## Sources

- D3.js documentation — https://d3js.org/getting-started
- D3 API Reference — https://github.com/d3/d3/blob/main/API.md
