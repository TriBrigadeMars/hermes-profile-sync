# Contrast Ratio Reference (WCAG)

Relative luminance: for each channel c in {r,g,b} normalized to 0–1:
`c' = c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)^2.4`
L = 0.2126*r' + 0.7152*g' + 0.0722*b'
Contrast ratio = (L_light + 0.05) / (L_dark + 0.05)

## Verified Tailwind pairs (computed, session 2026-08-27)

| Pair | Ratio | WCAG AA (4.5 normal / 3 large) |
|---|---|---|
| gray-500 (#6b7280) on white | 4.83 | PASS both |
| gray-600 (#4b5563) on white | 7.56 | PASS |
| gray-700 (#374151) on white | 10.31 | PASS |
| blue-600 (#2563eb) text on white | 5.17 | PASS |
| blue-500 (#3b82f6) text on white | 3.68 | FAIL normal text — use only ≥18pt/14pt bold |
| white on blue-600 bg | 5.17 | PASS |

## Print stylesheet snippet (validated)

```css
@media print {
  nav, footer { display: none !important; }
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #374151;
  }
  body { background: #fff !important; color: #000 !important; }
}
```

## Reduced-motion base layer (move from inline <style> to src/input.css)

```css
@layer base { html { scroll-behavior: smooth; } }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## JSON-LD Person notes

- `"email"` must be the bare address, no `mailto:` prefix.
- Keep `sameAs` pointing at canonical profile URLs.
- Add `<link rel="canonical">` separately in <head>; og:url alone is not a substitute.
