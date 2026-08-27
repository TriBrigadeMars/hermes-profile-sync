# Test Cases

Use these cases to evaluate the skill after installation.

## 1. Exact Labeled Bar Chart

Input: screenshot of a four-bar chart with readable category labels and values.

Prompt:

> Recreate this chart as an editable Excalidraw chart. Preserve the values and labels exactly.

Acceptance:

- separate rectangle per bar;
- readable axes/title;
- exact values preserved;
- no embedded screenshot required;
- `customData` values match visible labels.

## 2. Hand-Drawn Bar Sketch Without Numbers

Input: photo of a whiteboard with five hand-drawn bars and category names but no axis values.

Prompt:

> Clean this up into an editable Excalidraw chart, but do not invent any values.

Acceptance:

- relative bar heights preserved;
- no fabricated numeric labels;
- category names preserved;
- uncertainty note says values were not available.

## 3. Truncated-Axis Line Chart

Input: line chart whose y-axis runs from 80 to 100.

Prompt:

> Rebuild this chart in Excalidraw as faithfully as possible.

Acceptance:

- y-axis begins at 80, not 0;
- line geometry reflects 80-100 scale;
- no false zero baseline.

## 4. Multi-Series Line Chart

Input: chart with two colored lines, point markers, legend, and readable values.

Acceptance:

- each series is independently editable;
- legend mapping is correct;
- point order and gaps are preserved;
- colors remain distinguishable.

## 5. Skewed Photograph

Input: angled phone photo of a printed chart.

Prompt:

> Turn this into a clean editable Excalidraw chart rather than copying the photo perspective.

Acceptance:

- chart is rectified into a clean plot frame;
- semantic values/labels are preserved when readable;
- perspective distortion is not reproduced.

## 6. Ambiguous / Unreadable Labels

Input: low-resolution chart with two unreadable category labels.

Acceptance:

- agent does not guess labels;
- readable portions are reconstructed;
- uncertainty is explicitly noted.

## 7. Scope Boundary

Input: no image. Prompt:

> Make me a quarterly revenue bar chart in Excalidraw from these values: 10, 20, 30, 40.

Acceptance:

- this companion skill should defer to the bundled `excalidraw` skill because no visual reconstruction is needed.
