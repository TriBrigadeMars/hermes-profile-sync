---
name: excalidraw-chart-reconstructor
description: Use for chart images needing editable Excalidraw output.
version: 0.1.0
metadata:
  hermes:
    tags: [excalidraw, charts, graphs, vision, reconstruction]
    related_skills: [excalidraw]
---
# Excalidraw Chart Reconstructor

Convert an existing visual chart, graph, sketch, screenshot, scan, or photographed drawing into a clean, editable Excalidraw chart.

This skill is a companion to the bundled `excalidraw` skill. It owns **visual interpretation and chart reconstruction**. The bundled `excalidraw` skill owns **Excalidraw scene construction conventions and file output**.

## When to Use

Use this skill when the user supplies or points to a visual and asks to:

- recreate a chart or graph in Excalidraw;
- turn a screenshot, sketch, whiteboard drawing, scan, or photo into an editable chart;
- convert a visual graph into editable bars, lines, points, labels, axes, legends, or annotations;
- clean up a hand-drawn chart while preserving its meaning;
- make an existing chart editable rather than embedding it as an image.

Typical trigger phrases include: "convert this chart to Excalidraw", "recreate this graph", "make this chart editable", "turn this sketch into a graph", "trace this chart", and "rebuild this drawing as an Excalidraw chart".

## Do Not Use

- For a diagram or chart created from text/data with no source visual: use the bundled `excalidraw` skill directly.
- For a generic flowchart, architecture diagram, sequence diagram, or concept map created from instructions: use `excalidraw`.
- For simple image embedding where editability is not required: do not reconstruct the chart.
- Do not replace or duplicate the bundled `excalidraw` skill.

## Core Contract

The final result must be a **native editable Excalidraw scene**, not a screenshot pasted into Excalidraw.

Prefer semantic reconstruction over pixel tracing:

- bars -> separate rectangles;
- axes/gridlines -> line elements;
- line-series -> editable line/polyline elements;
- data points -> small ellipses when visible;
- labels/titles/ticks -> text elements;
- legends -> editable marker + text pairs;
- annotations/callouts -> native shapes, arrows, and text;
- chart metadata -> `customData` where useful and safe.

Never invent exact numeric values, labels, units, categories, or series names that cannot be supported by the source visual.

## Workflow

### 1. Confirm the task is visual reconstruction

Identify the source visual and the requested outcome.

If the source is an attached image, use the image information already available to the active vision-capable model. When a closer or explicit inspection is useful and `vision_analyze` is available, use it on the image/path. Hermes handles native-vision versus auxiliary-vision routing automatically.

If no visual is actually available, do not pretend to have inspected one. Ask for the visual only when it is genuinely required to proceed.

### 2. Analyze the source before drawing

Extract a reconstruction model before writing Excalidraw elements. Capture as much of the following as the source supports:

- chart family: vertical bar, horizontal bar, grouped bar, stacked bar, line, scatter, histogram, area, pie/donut, mixed, or unknown;
- title, subtitle, source note, caption;
- plot-area bounds and approximate aspect ratio;
- x/y axis orientation;
- axis labels, units, tick labels, minimum/maximum, zero position;
- scale type: linear, logarithmic, categorical, date/time, or unknown;
- categories or x-values;
- series names and legend mapping;
- exact data labels when visible;
- values derivable from readable axes;
- series colors, markers, line styles, fill styles;
- gridlines, baselines, reference lines, confidence bands, annotations;
- intentionally truncated/non-zero axes;
- visual uncertainty or unreadable regions.

Use `references/reconstruction-spec.md` for the normalized reconstruction representation.

### 3. Assign fidelity and confidence

Classify extracted information into three confidence levels:

- **exact** — explicitly readable in the source;
- **derived** — reliably computable from readable ticks/geometry;
- **estimated** — inferred from relative geometry only.

Rules:

1. Preserve exact values exactly.
2. Derived values may be used when the mapping is unambiguous.
3. Estimated values must never be presented as exact source data.
4. If values are unreadable but geometry is clear, reproduce the geometry and omit unsupported numeric labels.
5. If a label is unreadable, prefer omitting it or using an explicit neutral placeholder only when a placeholder is necessary for structure. Never guess a plausible label.

### 4. Choose reconstruction mode

Default to **faithful-clean** unless the user specifies otherwise.

- **faithful** — preserve source layout, proportions, labels, colors, and irregularities as closely as practical.
- **faithful-clean** — preserve data and meaning while normalizing alignment, spacing, label placement, and obvious hand-drawn noise.
- **structural** — reproduce chart structure and relative geometry when exact values/text are unavailable.

Do not silently "improve" a non-zero baseline, log scale, unusual ordering, or other meaningful design choice into a conventional chart.

### 5. Build a normalized chart specification

Create an internal chart specification following `references/reconstruction-spec.md` before scene construction.

The specification is the source of truth for the reconstruction. Separate:

- observed facts;
- derived values;
- estimates;
- unresolved uncertainties.

Do not mix visual guesses into exact data arrays.

### 6. Load the bundled Excalidraw skill

Before constructing the final scene, load the bundled skill with `skill_view("excalidraw")` unless its instructions are already active.

Follow that skill's current rules for:

- `.excalidraw` envelope and JSON structure;
- valid element fields;
- bound text;
- arrow bindings;
- z-order;
- font sizing;
- colors and contrast;
- output file creation and optional upload.

If this skill and the bundled `excalidraw` skill disagree about Excalidraw JSON mechanics, **the bundled `excalidraw` skill wins**. This skill remains authoritative only for reconstruction semantics.

### 7. Map the chart specification to editable elements

Use `references/chart-mapping.md` for chart-specific geometry.

General requirements:

- every meaningful chart component should remain individually editable;
- keep data marks separate from labels when practical;
- preserve meaningful ordering and relative scale;
- create a true zero/reference baseline when the source has one;
- preserve negative values and truncated axes correctly;
- keep legend order aligned with series order;
- use source colors when they are distinguishable and readable;
- if source colors are uncertain, use a coherent accessible palette rather than inventing near-matches;
- avoid decorative complexity that makes the chart harder to edit.

For reconstructed data marks, add `customData` when useful. Suggested shape:

```json
{
  "chartRole": "bar",
  "series": "Revenue",
  "category": "Q1",
  "value": 120,
  "valueConfidence": "exact"
}
```

Only include `value` when a value is exact or reliably derived. For geometry-only reconstructions, use role/series/category metadata without fabricated values.

### 8. Preserve editability over visual imitation

Do not flatten the source visual into one image element.

A source image may be used only as a temporary visual reference during reconstruction. The deliverable should consist of native Excalidraw elements unless the user explicitly asks to retain the source image as a reference layer.

When the source contains logos, photographs, textures, or decorative artwork that is not necessary to understand the chart, omit it by default or simplify it into a neutral annotation. The chart's information structure has priority.

### 9. Save the output

Save the result as a `.excalidraw` file using the bundled `excalidraw` skill's current file-writing procedure.

Use a descriptive filename based on the source or chart title. Avoid overwriting an existing source file unless the user explicitly requests replacement.

### 10. Report reconstruction uncertainty briefly

When uncertainty materially affects the result, tell the user what was reconstructed exactly and what was approximated. Keep this concise.

Examples:

- "Axis labels and bar values were readable and preserved exactly."
- "The axis numbers were unreadable, so bar heights preserve relative proportions without invented values."
- "Series labels were preserved, but two point positions are approximate because the photo was skewed."

## Chart-Type Handling

### Bar / Column Charts

Support vertical, horizontal, grouped, stacked, diverging, and histogram-style bars. Each bar should be an editable rectangle. Respect non-zero baselines and negative values.

### Line Charts

Use editable linear elements for each series. Recreate visible point markers as ellipses. Preserve breaks/gaps instead of interpolating missing values unless the source clearly connects them.

### Scatter Plots

Use one editable point element per visible observation when practical. Preserve logarithmic axes, quadrants, and reference lines when identifiable.

### Area Charts

Prioritize the boundary lines and axis semantics. Add filled regions only when they can be represented reliably with native editable elements. Do not sacrifice editability for a perfect raster-like fill.

### Pie / Donut Charts

Preserve slice ordering, labels, and percentages when readable. Reconstruct slices with editable native geometry when practical. If exact filled sector geometry cannot be produced reliably, prefer a simplified editable pie structure with radial dividers and labels over an embedded image.

### Mixed / Dashboard Graphics

Treat each plot region as a separate chart subsystem. Preserve shared legends and axes only when the source clearly indicates they are shared.

## Verification

Before finishing, verify all of the following:

1. The file is valid JSON and uses the current `.excalidraw` envelope from the bundled skill.
2. The final scene does not depend on an embedded screenshot for the chart itself.
3. Major chart components are individually editable.
4. Titles, labels, units, legend names, and exact visible values match the source.
5. Estimated values are not represented as exact facts.
6. Axis minima/maxima, zero positions, truncated baselines, and log scales are preserved when visible.
7. Data geometry is internally consistent with the reconstructed scale.
8. Bars/points/lines do not overlap labels unintentionally.
9. Legend markers match the intended series.
10. Text remains readable at normal viewing size.
11. Z-order keeps gridlines behind data marks and labels above marks.
12. If uncertainty remains, the final response identifies it briefly.

## Pitfalls

- **Pixel tracing instead of reconstruction:** do not reproduce anti-aliasing, compression artifacts, or hand jitter when a cleaner editable shape conveys the same information.
- **Inventing values:** relative bar height is not permission to fabricate a precise number.
- **Assuming zero baseline:** many source charts intentionally use truncated axes.
- **Missing log scales:** equal visual spacing can represent multiplicative rather than additive changes.
- **Photo perspective:** prioritize semantic relationships and readable values over literal skew unless the user explicitly wants the photographed perspective.
- **Legend confusion:** do not infer series identity from color alone when labels are ambiguous.
- **Stacked bars:** reconstruct segment boundaries independently; do not mistake cumulative height for segment value.
- **Dual-axis charts:** keep each series tied to the correct axis.
- **Missing values:** preserve gaps when the source shows gaps.
- **Decorative infographics:** extract the actual quantitative structure first; decoration is secondary.
- **Overlapping skill scope:** visual interpretation belongs here; Excalidraw JSON mechanics belong to the bundled `excalidraw` skill.
