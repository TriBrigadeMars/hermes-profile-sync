---
name: compliant-markdown-converter
description: "Batch-convert PDF/DOCX/EPUB to 508-compliant markdown."
version: 1.0.0
author: Mars Cruz
license: MIT
platforms: [linux, windows]
metadata:
  hermes:
    tags: [PDF, DOCX, EPUB, Markdown, Conversion, 508, Accessibility, Batch]
    related_skills: [ocr-and-documents, docx, pdf, workflow-orchestrator]
---

# Document-to-Markdown Converter (508-Compliant)

Batch-converts PDF, DOCX, and EPUB files into clean, accessible markdown files that meet Section 508 standards.

## When to Use

- User provides PDFs, DOCX, or EPUB files and wants markdown output
- Converting healthcare/law/regulatory documents that must meet Section 508 accessibility
- Processing large batches of mixed-format documents

## Prerequisites

```bash
pip install pymupdf pymupdf4llm ebooklib python-docx lxml
```

For **scanned PDFs** (image-only, no text layer), also install marker-pdf:
```bash
pip install marker-pdf
```

## Quick Start — Single File

```bash
python scripts/convert_to_markdown.py /path/to/document.pdf
python scripts/convert_to_markdown.py /path/to/document.docx
python scripts/convert_to_markdown.py /path/to/document.epub
```

Output is saved in the **same directory** as the source file as `<original_name>.md`.

## Batch Processing — Directory

```bash
python scripts/convert_to_markdown.py /path/to/folder --recursive
```

Recursively finds all `.pdf`, `.docx`, `.doc`, and `.epub` files and converts each. Skips files that already have a `.md` counterpart unless `--overwrite` is passed.

## Output Location Override

```bash
python scripts/convert_to_markdown.py /path/to/files --output_dir "D:\Users\cruzmars\Documents\Converted"
```

All `.md` files go to the specified directory instead of alongside the source.

## Batch Processing via Hermes execute_code

For large volumes (hundreds of files), use `execute_code` to process in controlled batches and avoid timeouts:

```python
from hermes_tools import terminal

# Convert an entire folder with 4 workers
result = terminal(
    'python scripts/convert_to_markdown.py "C:\\Users\\cruzmars\\Downloads" '
    '--recursive --output_dir "D:\\Users\\cruzmars\\Documents\\Converted" --overwrite',
    timeout=600
)
print(result['output'])
```

## Script Flags

| Flag | Description |
|------|-------------|
| `--recursive` | Scan subdirectories |
| `--output_dir DIR` | Save all markdown to DIR (default: same folder as source) |
| `--overwrite` | Overwrite existing `.md` files |
| `--verbose` | Print per-file status |
| `--engine pymupdf` | (default) Plain pymupdf text extraction — instant, never hangs |
| `--engine llm` | pymupdf4llm — higher quality (headings/tables), but can stall on huge PDFs |
| `--engine marker` | Use marker-pdf for scanned PDFs / OCR (requires ~5GB install) |

## Output Quality Rules

The script enforces these 508-compliant markdown standards:

1. **Heading hierarchy** — No heading level skips (e.g., `#` → `##` → `###`)
2. **Alt text on images** — `![descriptive alt](path)` — never empty alt
3. **Tables with headers** — Every table starts with a header row and separator
4. **No bare URLs** — All URLs are proper markdown links: `[text](url)`
5. **Clean whitespace** — No more than two consecutive blank lines
6. **UTF-8 encoding** — Output always UTF-8
7. **No page artifacts** — Page numbers, watermarks, and running headers stripped
8. **Lists properly formatted** — Consistent bullet markers (`-`), proper indentation

## How Conversion Works by Format

### PDF (pymupdf — default, robust)
- Extracts text page-by-page with plain pymupdf — instant, never hangs, handles huge/pathological PDFs (e.g. 76MB web-prints)
- Per-page cleanup: strips running headers/footers (top/bottom lines recurring across a majority of pages), bare page numbers, and timestamps
- Reflows hard-wrapped lines back into flowing paragraphs, and de-hyphenates words split across lines
- Detects empty text layer → falls back to marker-pdf (OCR) if installed, else errors
- **Known limitations:** headings (Rule/Part/Section) are kept as distinct lines but NOT converted to `#` markdown headings; numbered-list markers may land on their own line; multi-line addresses merge onto one line

### PDF (pymupdf4llm — `--engine llm`, UNRELIABLE)
- Higher-quality markdown with headings/tables, **but it stalls/hangs in the Docker sandbox on PDFs of ANY size** (observed on both a 373KB and a 76MB file). Only use it if it is confirmed working in a native (non-sandbox) Python environment.

### DOCX (python-docx)
- Parses the actual XML structure — headings, paragraphs, tables, lists, bold/italic
- Maps Word styles to markdown: `Heading 1` → `#`, `Heading 2` → `##`, etc.
- Images: converts embedded images to base64 inline or notes `[IMAGE: description]`
- Table cells are properly aligned with header rows
- Hyperlinks are preserved as markdown links

### EPUB (ebooklib)
- Parses XHTML content from each chapter
- Strips EPUB-specific wrappers, keeps semantic HTML-to-markdown mapping
- Combines chapters in order with `# Chapter N` headings
- Preserves emphasis, lists, and links from source HTML

## Pitfalls

- **Scanned PDFs** produce empty text with pymupdf. The script detects this and falls back to marker-pdf if installed, otherwise raises an error.
- **Password-protected PDFs** — script skips with a warning.
- **Very large PDFs** (500+ pages) — may take minutes with marker-pdf; pymupdf is instant.
- **Pathological PDFs** (76MB web-prints, thousands of embedded fonts) — extraction can be slow when files sit on a bind-mounted drive (Docker/WSL). Run large batches with `terminal(background=True)` and a generous timeout, not in the foreground.
- **DOCX images** — images are not embedded as files; the script notes `[IMAGE: description]` placeholders.
- **EPUB with DRM** — standard ebooklib cannot process DRM-protected EPUBs.

## Reference Standards

The converter produces markdown that:
- Matches the clean structure of well-formatted documents (proper `#`/`##`/`###` hierarchy, bullet lists, tables, bold terms)
- Strips extraction artifacts (repeated headers/footers, "X of pages" page markers, timestamps)
- Follows standard markdown syntax per The Markdown Guide

**Always ask the user where to save** before running a batch. Default suggestion: `D:\Users\cruzmars\Documents\`.