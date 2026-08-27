# Reconstruction Specification

Use this normalized representation as an internal planning model before creating Excalidraw elements. It does not need to be saved unless useful for the task.

## Principles

- Store observed, derived, and estimated information separately.
- Never promote an estimate into the exact data array.
- Preserve source semantics before appearance.
- Omit fields the visual does not support rather than guessing them.

## Suggested Schema

```json
{
  "chartType": "vertical-bar",
  "mode": "faithful-clean",
  "source": {
    "kind": "screenshot",
    "aspectRatio": 1.78,
    "perspectiveSkew": "none"
  },
  "text": {
    "title": {"value": "Quarterly Revenue", "confidence": "exact"},
    "subtitle": null,
    "caption": null
  },
  "plot": {
    "x": 0.12,
    "y": 0.15,
    "width": 0.78,
    "height": 0.68
  },
  "axes": {
    "x": {
      "type": "categorical",
      "label": null,
      "categories": ["Q1", "Q2", "Q3", "Q4"]
    },
    "y": {
      "type": "linear",
      "label": "USD millions",
      "min": 0,
      "max": 300,
      "ticks": [0, 50, 100, 150, 200, 250, 300],
      "confidence": "exact"
    }
  },
  "series": [
    {
      "name": "Revenue",
      "kind": "bar",
      "color": "#4c6ef5",
      "values": [120, 150, 205, 250],
      "valueConfidence": ["exact", "exact", "exact", "exact"]
    }
  ],
  "annotations": [],
  "estimatedGeometry": [],
  "uncertainties": []
}
```

## Confidence Values

Use one of:

- `exact` — explicitly legible or directly stated;
- `derived` — mathematically recoverable from readable geometry/scale;
- `estimated` — visually approximated;
- `unknown` — not recoverable.

A field may carry its own confidence when confidence differs across the chart.

## Geometry-Only Reconstruction

When numeric values cannot be recovered, use normalized geometry instead of invented values:

```json
{
  "series": [
    {
      "name": null,
      "kind": "bar",
      "values": null,
      "normalizedHeights": [0.42, 0.67, 0.61, 0.89],
      "valueConfidence": ["unknown", "unknown", "unknown", "unknown"]
    }
  ]
}
```

Normalized values describe visual proportions only. Do not display them as source data.

## Multi-Axis Charts

Assign each series an `axisId`:

```json
{
  "axes": {
    "yLeft": {"type": "linear", "min": 0, "max": 100},
    "yRight": {"type": "linear", "min": 0, "max": 1}
  },
  "series": [
    {"name": "Volume", "kind": "bar", "axisId": "yLeft"},
    {"name": "Conversion", "kind": "line", "axisId": "yRight"}
  ]
}
```

## Uncertainty Notes

Record uncertainties as concrete observations, for example:

```json
{
  "uncertainties": [
    "Second x-axis label is unreadable.",
    "Final point lies between 70 and 75; exact value cannot be derived.",
    "Photo perspective compresses the right side of the plot."
  ]
}
```

Use these notes for verification and the concise user-facing uncertainty summary.
