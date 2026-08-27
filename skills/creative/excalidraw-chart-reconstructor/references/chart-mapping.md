# Chart-to-Excalidraw Mapping

This reference covers chart geometry only. For Excalidraw JSON field requirements, text binding, z-order, styling, and saving, load and follow the bundled `excalidraw` skill.

## Coordinate System

Choose a clean chart frame first. A practical default plot area is roughly 900-1100 px wide and 450-650 px high, with additional margins for titles, axes, and legends.

Use source aspect ratio when it matters. Otherwise prioritize readability.

For a linear y-axis with plot top `py`, height `ph`, axis minimum `ymin`, and maximum `ymax`:

```text
y_pixel(value) = py + ph * (ymax - value) / (ymax - ymin)
```

For a linear x-axis with plot left `px`, width `pw`, minimum `xmin`, and maximum `xmax`:

```text
x_pixel(value) = px + pw * (value - xmin) / (xmax - xmin)
```

For a confirmed logarithmic base-10 axis, map `log10(value)` rather than `value`.

Never apply a log transform unless the source indicates a logarithmic scale.

## Layer Order

Recommended chart z-order:

1. background zones/bands;
2. gridlines;
3. reference lines;
4. axes;
5. area fills;
6. bars/lines/points;
7. data labels;
8. annotations/callouts;
9. legend;
10. title/subtitle/source note.

Follow the bundled `excalidraw` skill if its z-order requirements are more specific.

## Vertical Bars

Represent each bar as a rectangle.

For a positive value:

```text
bar_top    = y_pixel(value)
zero_y     = y_pixel(0)
bar_height = zero_y - bar_top
```

For a negative value:

```text
bar_top    = zero_y
bar_height = y_pixel(value) - zero_y
```

Do not force `zero_y` to the bottom of the plot when the source axis is truncated or spans negative values.

For categorical charts, distribute category centers evenly across the plot unless the source uses meaningful unequal spacing.

## Grouped Bars

For each category, allocate a category band and subdivide it by series count. Preserve visible ordering from left to right. Leave a small intra-group gap and a larger inter-category gap.

## Stacked Bars

Compute segment boundaries cumulatively from the actual segment values. A stack's total height is not an individual segment value.

For mixed positive/negative stacks, accumulate positive and negative values independently from the zero baseline.

## Horizontal Bars

Swap x/y mapping logic. Category labels usually sit left of the plot; numerical scale runs along x.

## Histograms

Treat bins as adjacent bars unless the source visibly includes gaps. Preserve bin edge labels rather than converting them to generic categories.

## Line Charts

Map each data point to chart coordinates and create an editable linear/polyline series.

- Preserve point order.
- Preserve gaps in missing data.
- Add point-marker ellipses only when markers exist in the source or improve editability without changing meaning.
- For stepped lines, reproduce steps rather than connecting with diagonals.
- Do not smooth/interpolate a line unless the source is visibly smoothed.

## Scatter Plots

Represent observations as small ellipses or similarly simple native marks.

- Preserve x and y scales independently.
- Preserve visible clusters and outliers.
- For very dense plots, prioritize representative editability and ask before reducing point count if exact point-level recreation is required.

## Area Charts

The boundary line carries the primary data semantics. Recreate it first. If a filled native editable region can be built reliably, add it behind the line with reduced visual emphasis.

For stacked areas, preserve stacking order and cumulative boundaries.

## Reference Lines and Bands

Reference lines should be distinct from data series, typically thinner or dashed. Keep their labels near the line and do not include them in the legend unless the source does.

Reference bands should sit behind data marks.

## Dual Axes

Create and label both axes. Record which series belongs to which axis in `customData` when useful.

Never map all series to one scale just because they share the same plot area.

## Truncated Axes

A source axis beginning above zero is meaningful. Reproduce its stated minimum and resulting geometry. Do not visually imply a zero baseline.

## Pie / Donut Charts

If percentages or values are visible, preserve them exactly. Slice angle is:

```text
angle = 360 * value / total
```

For geometry-only reconstruction, preserve relative slice angles without inventing numeric values.

Prefer editable native sector approximations. If reliable filled sectors are impractical, use:

- a base ellipse;
- radial divider lines;
- labels/leader lines;
- legend markers.

This is preferable to flattening the chart into an image.

## Labels

Preserve the source's semantic hierarchy:

- chart title: largest;
- subtitle: secondary;
- axis titles: clear but subordinate;
- tick/category labels: readable and compact;
- source notes: smallest acceptable text.

Do not rotate text unless the source requires it for density or meaning.

## `customData` Recommendations

Use metadata to make reconstructed elements easier for future agents to understand.

Examples:

```json
{"chartRole":"x-axis","axisId":"x"}
```

```json
{"chartRole":"gridline","axisId":"y","tickValue":100}
```

```json
{
  "chartRole":"bar",
  "series":"Revenue",
  "category":"Q2",
  "value":150,
  "valueConfidence":"derived"
}
```

```json
{
  "chartRole":"point",
  "series":"Conversion",
  "xValue":"2026-06",
  "yValue":0.34,
  "valueConfidence":"exact"
}
```

Do not attach fabricated values to metadata.
