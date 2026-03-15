# Color Accessibility Reference

Detailed guidance for designing visualizations that communicate effectively regardless of color perception.

## Understanding Color Vision Deficiency

Color vision deficiency affects perception in predictable ways. Design accounts for these variations rather than requiring normal color vision.

### Types and Prevalence

| Type | Affected Colors | Prevalence (Male) | Prevalence (Female) |
|------|-----------------|-------------------|---------------------|
| Deuteranomaly | Green weakness | ~5% | ~0.4% |
| Deuteranopia | Green blindness | ~1% | <0.01% |
| Protanomaly | Red weakness | ~1% | <0.01% |
| Protanopia | Red blindness | ~1% | <0.01% |
| Tritanopia | Blue-yellow blindness | <0.01% | <0.01% |
| Achromatopsia | Complete color blindness | 0.003% | 0.003% |

Red-green deficiency (protanopia and deuteranopia combined) affects approximately 8% of males. This is the primary concern for most visualization design.

### Problematic Color Combinations

Colors that appear distinct to typical vision may become indistinguishable:

**Avoid these pairs without differentiation**:

- Red and green (classic problem, affects ~8% of males)
- Blue and purple (difficult for tritanopia)
- Green and brown (merge for deuteranopia)
- Light green and yellow (indistinguishable in multiple deficiency types)
- Red and brown (merge for protanopia)
- Pink and gray (problematic at low saturation)

**Generally safe pairs**:

- Blue and orange (distinguishable across most deficiencies)
- Blue and yellow (high contrast, safe for red-green deficiency)
- Black and white (maximum contrast)
- Purple and yellow (safe for most types)

## Colorblind-Safe Palettes

Established palettes have been tested across color vision deficiencies.

### Categorical Palettes

For distinguishing discrete categories:

**Okabe-Ito Palette** (8 colors):

```
#E69F00  Orange
#56B4E9  Sky Blue
#009E73  Bluish Green
#F0E442  Yellow
#0072B2  Blue
#D55E00  Vermillion
#CC79A7  Reddish Purple
#000000  Black
```

Designed specifically for scientific visualization. Each color remains distinguishable under all common color vision deficiencies.

**IBM Color Blind Safe** (8 colors):

```
#648FFF  Ultramarine Blue
#785EF0  Indigo
#DC267F  Magenta
#FE6100  Orange
#FFB000  Gold
#000000  Black
#FFFFFF  White
#808080  Gray
```

Optimized for digital displays with high contrast between adjacent colors.

### Sequential Palettes

For continuous data ranging from low to high:

**Viridis** (matplotlib/D3):
Perceptually uniform colormap that:

- Remains readable in grayscale
- Distinguishes values across full range
- Works for all color vision deficiencies

**Cividis**:
Optimized specifically for deuteranopia and protanopia. Blue-to-yellow gradient avoids problematic red-green channels entirely.

**ColorBrewer Sequential**:
Multiple options with colorblind-safe variants marked. Use the "colorblind safe" filter when selecting palettes.

### Diverging Palettes

For data with a meaningful center point:

**Blue-Orange Diverging**:
Safe choice—blue and orange remain distinguishable across color vision types.

**Purple-Green Diverging**:
Avoid—green becomes problematic for red-green deficiency.

**Brown-Teal Diverging**:
Generally safe alternative to purple-green.

## Contrast Requirements

WCAG defines minimum contrast ratios using relative luminance.

### Calculating Contrast

Relative luminance formula:

```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
```

Where R, G, B are linearized color values (after gamma correction).

Contrast ratio:

```
ratio = (L1 + 0.05) / (L2 + 0.05)
```

Where L1 is the lighter color's luminance and L2 is the darker.

### Required Ratios by Element Type

| Element | WCAG Level AA | WCAG Level AAA |
|---------|---------------|----------------|
| Normal text | 4.5:1 | 7:1 |
| Large text (18pt+ or 14pt bold) | 3:1 | 4.5:1 |
| Graphical objects | 3:1 | — |
| UI components | 3:1 | — |
| Focus indicators | 3:1 | — |

### Common Contrast Failures

**Light gray on white**: #999 on #FFF = 2.9:1 (fails 3:1)
**Medium gray on white**: #767676 on #FFF = 4.5:1 (passes AA text)

**Gridlines and axes**: Often set too light. Ensure 3:1 minimum.

**Data labels on colored backgrounds**: Calculate contrast for every label/background combination.

**Legend swatches**: Small color samples need higher effective contrast to compensate for size.

## Pattern and Texture Strategies

When color alone cannot differentiate, add visual patterns.

### SVG Pattern Definitions

```svg
<defs>
  <!-- Horizontal stripes -->
  <pattern id="stripe-h" patternUnits="userSpaceOnUse"
           width="8" height="8">
    <line x1="0" y1="4" x2="8" y2="4"
          stroke="currentColor" stroke-width="2"/>
  </pattern>

  <!-- Diagonal stripes -->
  <pattern id="stripe-d" patternUnits="userSpaceOnUse"
           width="8" height="8">
    <line x1="0" y1="8" x2="8" y2="0"
          stroke="currentColor" stroke-width="1.5"/>
  </pattern>

  <!-- Dots -->
  <pattern id="dots" patternUnits="userSpaceOnUse"
           width="8" height="8">
    <circle cx="4" cy="4" r="2" fill="currentColor"/>
  </pattern>

  <!-- Crosshatch -->
  <pattern id="crosshatch" patternUnits="userSpaceOnUse"
           width="8" height="8">
    <line x1="0" y1="4" x2="8" y2="4"
          stroke="currentColor" stroke-width="1"/>
    <line x1="4" y1="0" x2="4" y2="8"
          stroke="currentColor" stroke-width="1"/>
  </pattern>
</defs>
```

### Pattern Usage Guidelines

**Layer patterns over color**: Apply pattern with partial opacity to preserve color while adding texture:

```svg
<rect fill="#0077B6" ... />
<rect fill="url(#stripe-d)" opacity="0.3" ... />
```

**Distinguish pattern types clearly**: Use visually distinct patterns (stripes vs dots vs crosshatch) rather than subtle variations.

**Scale patterns appropriately**: Patterns should remain visible at expected viewing distances. Test at minimum display size.

**Combine with direct labels**: Patterns help in legends and print; direct labels remain the clearest solution.

## Shape Encoding

For scatter plots and point-based visualizations, vary shape alongside color.

### Effective Shape Sets

**5-shape set** (highly distinguishable):

- Circle
- Square
- Triangle (pointing up)
- Diamond
- Cross/Plus

**Extended set** (use with caution):

- Circle, Square, Triangle-up, Diamond, Cross
- Triangle-down, Star, Pentagon
- Hollow variants of above

Hollow and filled variants may become confused at small sizes. Test at minimum display dimensions.

### Shape + Color Combinations

Map each category to both a color AND a shape:

```javascript
const categoryStyles = {
  'Product A': { color: '#0077B6', shape: 'circle' },
  'Product B': { color: '#E69F00', shape: 'square' },
  'Product C': { color: '#009E73', shape: 'triangle' },
  'Product D': { color: '#D55E00', shape: 'diamond' }
};
```

With redundant encoding, users can distinguish categories through either channel.

## Direct Labeling

The most accessible color strategy: label data directly rather than relying on legends.

### Benefits

- Eliminates color lookup entirely
- Works for screen readers
- Survives grayscale printing
- Reduces cognitive load

### Implementation Patterns

**Label lines at endpoint**:

```svg
<text x="line-end-x" y="line-end-y"
      dx="5" dy="4">Product A</text>
```

**Label bars inside or adjacent**:

```svg
<text x="bar-center-x" y="bar-top-y - 5"
      text-anchor="middle">$1.2M</text>
```

**Label pie slices or segments**:
Prefer labels outside the slice connected by leader lines when space is limited inside.

### When Direct Labels Fail

- Dense visualizations with many overlapping elements
- Real-time updating charts where label positions shift
- Very small display sizes

In these cases, use color + pattern + interactive tooltips as backup.

## Testing Color Accessibility

### Browser-Based Simulation

Chrome DevTools: Rendering panel > Emulate vision deficiencies

Firefox: Accessibility panel > Simulate > Color vision

### Online Tools

- **Coblis**: Upload image, view under different deficiency types
- **Sim Daltonism** (macOS): Live screen filter for any application
- **Color Oracle** (Windows/macOS/Linux): System-wide color blindness filter

### Automated Checking

**axe-core**: Flags color contrast failures in HTML/SVG
**Lighthouse**: Audits contrast ratios, identifies text on images

### Manual Verification Checklist

For each visualization:

1. [ ] View under protanopia simulation—can all data series be distinguished?
2. [ ] View under deuteranopia simulation—do any elements merge?
3. [ ] View in grayscale—does the visualization still communicate its message?
4. [ ] Check contrast ratios for all text (4.5:1 minimum)
5. [ ] Check contrast ratios for graphical objects (3:1 minimum)
6. [ ] Verify patterns or shapes provide redundant encoding where needed
7. [ ] Confirm direct labels work without color reference where possible

## Palette Selection Decision Tree

```
Is data categorical or continuous?
├── Categorical (discrete groups)
│   ├── ≤8 categories → Okabe-Ito or IBM Color Blind Safe
│   ├── >8 categories → Reduce categories or use direct labels
│   └── Consider adding shapes/patterns as secondary encoding
│
└── Continuous (range of values)
    ├── Single direction (low→high)
    │   └── Use Viridis, Cividis, or ColorBrewer sequential
    │
    └── Diverging (low←center→high)
        └── Use Blue-Orange or tested diverging palette
```

## Common Mistakes

**Using red for "bad" and green for "good"**: This exact pair is problematic for 8% of males. Use symbols, icons, or alternative colors (blue for positive, orange for negative).

**Assuming tools generate accessible palettes**: Most default color schemes in charting libraries are not colorblind-safe. Always verify or replace with tested palettes.

**Testing only one deficiency type**: Protanopia and deuteranopia are most common, but test tritanopia for visualizations using blue-yellow gradients.

**Ignoring print scenarios**: Visualizations may be printed in grayscale. Test with grayscale filter if print is a use case.

**Relying on hover states for color information**: Hover isn't available for touch, keyboard, or print. Ensure information is accessible without interaction.
