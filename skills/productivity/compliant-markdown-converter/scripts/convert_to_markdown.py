#!/usr/bin/env python3
"""
convert_to_markdown.py — Batch PDF/DOCX/EPUB → 508-compliant markdown.

Handles large volumes: accepts a single file or a directory (optionally recursive)
and emits one clean .md per input, with Section 508 accessibility hygiene applied.
"""

import argparse
import html
import os
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Dependency guards (lazy imports so --help works even if libs are missing)
# --------------------------------------------------------------------------- #
def _require(modname, pipname):
    try:
        return __import__(modname)
    except ImportError:
        print(f"[ERROR] Missing dependency '{pipname}'. Install with: pip install {pipname}",
              file=sys.stderr)
        sys.exit(2)

# --------------------------------------------------------------------------- #
# 508 / hygiene helpers
# --------------------------------------------------------------------------- #

# Regexes for common extraction artifacts to strip from PDF/DOCX/EPUB output.
PAGE_MARKER = re.compile(
    r"^\s*\d+\s+of\s+\d+\s*$"            # "54 of 164"
)
TIMESTAMP_LINE = re.compile(
    r"^\s*\d{1,2}/\d{1,2}/\d{4},\s+\d{1,2}:\d{2}(:\d{2})?\s*(AM|PM)?\s*$"
)
BARE_URL = re.compile(r"(?<!\]\()https?://[^\s\)]+")

# A standalone bare integer (page number), e.g. "2", "43", "164".
PAGE_NUM_ONLY = re.compile(r"^\s*\d{1,4}\s*$")

# Simple repeated-running-header detector: lines that recur verbatim across many
# "pages" are artifacts. We handle this heuristically in the caller.

def strip_page_artifacts(text):
    """Remove running headers/footers, page markers, and timestamps."""
    lines = text.splitlines()
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            out.append("")
            continue
        if PAGE_MARKER.match(s):
            continue
        if TIMESTAMP_LINE.match(s):
            continue
        out.append(line)
    return "\n".join(out)


def collapse_repeated_headers(text, min_repeats=3):
    """
    A running header/footer (e.g. "Revised 508 Standards and 255 Guidelines")
    repeats on every page. If a non-empty line appears >= min_repeats times and
    counts for a large fraction of lines, drop it entirely.
    """
    lines = text.splitlines()
    from collections import Counter
    counts = Counter(l.strip() for l in lines if l.strip())
    total = max(1, len(lines))
    to_drop = set()
    for line, n in counts.items():
        if n >= min_repeats and n / total >= 0.08:
            to_drop.add(line)
    return "\n".join(l for l in lines if l.strip() not in to_drop)


def collapse_blank_lines(text):
    """Never more than two consecutive blank lines."""
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def linkify_bare_urls(text):
    """Wrap bare URLs in markdown link syntax, but never double-wrap URLs
    that are already inside a markdown link (avoids `[[x](x](x))` nesting)."""
    # Mask existing markdown links/images first so their inner URLs are untouched.
    existing = []
    def _mask(m):
        existing.append(m.group(0))
        return f"\x00L{len(existing) - 1}\x00"
    text = re.sub(r"!?\[[^\]]*\]\([^\)]*\)", _mask, text)

    def repl(m):
        url = m.group(0).rstrip(".,;:")  # don't swallow trailing punctuation
        return f"[{url}]({url})"
    text = BARE_URL.sub(repl, text)

    for i, link in enumerate(existing):
        text = text.replace(f"\x00L{i}\x00", link)
    return text


def ensure_utf8(text):
    """Normalize to valid UTF-8 (replace lone surrogates / bad bytes)."""
    return text.encode("utf-8", errors="replace").decode("utf-8")


def apply_508_hygiene(text):
    text = strip_page_artifacts(text)
    text = collapse_repeated_headers(text)
    text = linkify_bare_urls(text)
    text = collapse_blank_lines(text)
    return ensure_utf8(text)


# --------------------------------------------------------------------------- #
# PDF conversion
# --------------------------------------------------------------------------- #
def convert_pdf(path: Path, engine: str = "pymupdf") -> str:
    if engine == "marker":
        return _convert_pdf_marker(path)
    if engine == "llm":
        return _convert_pdf_llm(path)
    return _convert_pdf_pymupdf(path)


def _convert_pdf_pymupdf(path: Path) -> str:
    """Plain pymupdf text extraction with per-page cleanup: strips running
    headers/footers, page numbers, and reflows hard-wrapped paragraphs."""
    pymupdf = _require("pymupdf", "pymupdf")
    doc = pymupdf.open(str(path))
    if doc.needs_pass:
        return ""  # password-protected; caller reports skip
    pages_text = []
    for page in doc:
        try:
            pages_text.append(page.get_text())
        except Exception:  # noqa: BLE001
            continue

    if not any(p.strip() for p in pages_text):
        # Empty text layer — likely a scanned PDF.
        try:
            _require("marker", "marker-pdf")
            print(f"  [SCAN] {path.name}: empty text layer, falling back to marker-pdf",
                  file=sys.stderr)
            return _convert_pdf_marker(path)
        except SystemExit:
            print(f"  [SKIP] {path.name}: scanned PDF and marker-pdf not installed. "
                  f"Install with: pip install marker-pdf", file=sys.stderr)
            return ""

    artifacts = _detect_running_headers_footers(pages_text)

    cleaned = []
    for pt in pages_text:
        kept = []
        for line in pt.splitlines():
            s = line.strip()
            if not s:
                continue
            if PAGE_NUM_ONLY.match(s):
                continue  # bare page number
            if s in artifacts:
                continue  # running header/footer
            kept.append(line.rstrip())
        cleaned.append(_reflow_paragraphs("\n".join(kept)))

    return "\n\n".join(p for p in cleaned if p.strip())


def _detect_running_headers_footers(pages_text):
    """Lines appearing at the top or bottom of a majority of pages are artifacts."""
    from collections import Counter
    top = Counter()
    bottom = Counter()
    n = max(1, len(pages_text))
    for pt in pages_text:
        lines = [l.strip() for l in pt.splitlines() if l.strip()]
        if not lines:
            continue
        for l in dict.fromkeys(lines[:4]):      # first 4 non-empty lines
            top[l] += 1
        for l in dict.fromkeys(lines[-4:]):     # last 4 non-empty lines
            bottom[l] += 1
    threshold = max(2, int(n * 0.5))
    return {l for l, c in top.items() if c >= threshold} | \
           {l for l, c in bottom.items() if c >= threshold}


def _looks_like_heading(s):
    s = s.strip()
    if not s:
        return False
    if re.match(r"^(Rule|Part|Section|CHAPTER|Chapter|Appendix|APPENDIX)\b", s):
        return True
    if s.isupper() and len(s) <= 60:
        return True
    return False


def _is_para_end(prev):
    """A line ends a paragraph if it carries terminal punctuation."""
    return bool(re.search(r"[.!?:;\u201d\u2019)]$", prev))


def _reflow_paragraphs(text):
    """Join hard-wrapped lines into flowing paragraphs, respecting headings and
    de-hyphenating words split across lines."""
    out = []
    for line in text.splitlines():
        s = line.rstrip()
        stripped = s.strip()
        if not stripped:
            out.append("")
            continue
        if not out or out[-1] == "":
            out.append(s)
            continue
        prev = out[-1]
        # Never merge into/out of a heading line.
        if _looks_like_heading(prev.strip()) or _looks_like_heading(stripped):
            out.append(s)
            continue
        # De-hyphenate: prev ends with '-' and next starts lowercase.
        if prev.endswith("-") and stripped[0].islower():
            out[-1] = prev[:-1] + stripped
            continue
        # Join mid-sentence continuation.
        if not _is_para_end(prev):
            out[-1] = prev + " " + stripped
        else:
            out.append(s)
    return "\n".join(out)


def _convert_pdf_llm(path: Path) -> str:
    """High-quality conversion via pymupdf4llm (preserves headings/tables). Can
    stall on pathological PDFs — use only for well-behaved files."""
    pymupdf4llm = _require("pymupdf4llm", "pymupdf4llm")
    md = pymupdf4llm.to_markdown(str(path))
    if not md.strip():
        return _convert_pdf_pymupdf(path)
    return md


def _convert_pdf_marker(path: Path) -> str:
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        converter = PdfConverter(artifact_dict=create_model_dict())
        rendered = converter(str(path))
        return rendered.markdown
    except Exception as e:  # noqa: BLE001
        print(f"  [ERROR] marker-pdf failed for {path.name}: {e}", file=sys.stderr)
        return ""


# --------------------------------------------------------------------------- #
# DOCX conversion
# --------------------------------------------------------------------------- #
def convert_docx(path: Path) -> str:
    docx = _require("docx", "python-docx")
    from docx import Document
    from docx.document import Document as _Doc
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn

    document = Document(str(path))

    def iter_block_items(parent):
        # Yield paragraphs and tables in document order.
        for child in parent.element.body.iterchildren():
            if child.tag == qn("w:p"):
                yield Paragraph(child, parent)
            elif child.tag == qn("w:tbl"):
                yield Table(child, parent)

    def para_to_md(p: Paragraph) -> str:
        text = p.text.strip()
        if not text:
            return ""

        style = (p.style.name or "").lower() if p.style else ""

        # Map Word heading styles to markdown heading levels.
        heading_map = {
            "title": "#", "heading 1": "#", "heading1": "#",
            "heading 2": "##", "heading2": "##",
            "heading 3": "###", "heading3": "###",
            "heading 4": "####", "heading4": "####",
            "heading 5": "#####", "heading5": "#####",
            "heading 6": "######", "heading6": "######",
        }

        # Rebuild runs with inline emphasis (bold/italic).
        parts = []
        for run in p.runs:
            t = run.text
            if not t:
                continue
            if run.bold and run.italic:
                t = f"***{t}***"
            elif run.bold:
                t = f"**{t}**"
            elif run.italic:
                t = f"*{t}*"
            parts.append(t)
        rendered = "".join(parts) or text

        # List items.
        if style.startswith("list bullet") or "bullet" in style:
            return f"- {rendered}"
        if style.startswith("list number") or "number" in style:
            return f"1. {rendered}"

        if style in heading_map:
            return f"{heading_map[style]} {rendered}"

        return rendered

    def table_to_md(tbl: Table) -> str:
        rows = []
        for row in tbl.rows:
            cells = [c.text.strip().replace("\n", " ") for c in row.cells]
            rows.append(cells)
        if not rows:
            return ""
        # Unify column count.
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]

        header = rows[0]
        body = rows[1:] if len(rows) > 1 else []
        lines = ["| " + " | ".join(header) + " |"]
        lines.append("| " + " | ".join(["---"] * width) + " |")
        for r in body:
            lines.append("| " + " | ".join(r) + " |")
        return "\n".join(lines)

    out = []
    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            md = para_to_md(block)
            if md:
                out.append(md)
        elif isinstance(block, Table):
            md = table_to_md(block)
            if md:
                out.append(md)
    return "\n\n".join(out)


# --------------------------------------------------------------------------- #
# EPUB conversion
# --------------------------------------------------------------------------- #
def convert_epub(path: Path) -> str:
    ebooklib = _require("ebooklib", "ebooklib")
    from ebooklib import epub, ITEM_DOCUMENT

    book = epub.read_epub(str(path))

    chapters = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        name = item.get_name()
        if not isinstance(name, str):
            continue
        try:
            body = item.get_content().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue

        title = _epub_item_title(item) or ""
        md = _html_to_markdown(body, title)
        if md.strip():
            chapters.append(md)

    # Preserve spine order when available.
    ordered = []
    try:
        spine = [it.get_name() for it in book.spine]
        by_name = {_epub_item_name(c): c for c in chapters}
        # Re-map: we stored titles; easier: rebuild by iterating spine ids.
    except Exception:  # noqa: BLE001
        pass

    if not chapters:
        return ""

    # Simple header for the whole book, then chapters separated.
    title = ""
    try:
        t = book.get_metadata("DC", "title")
        if t:
            title = t[0][0].strip()
    except Exception:  # noqa: BLE001
        pass

    result = []
    if title:
        result.append(f"# {title}\n")
    for ch in chapters:
        result.append(ch)
    return "\n\n".join(result)


def _epub_item_title(item):
    try:
        for t in item.get_metadata("DC", "title"):
            return t[0].strip()
    except Exception:  # noqa: BLE001
        pass
    # Fall back to a heading inside the content.
    try:
        content = item.get_content().decode("utf-8", errors="replace")
        m = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", content, re.I | re.S)
        if m:
            return _strip_html(m.group(1)).strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def _epub_item_name(chapter):
    return chapter


def _strip_html(s):
    return re.sub(r"<[^>]+>", "", s)


def _html_to_markdown(body: str, title: str = "") -> str:
    """Convert a single XHTML chapter to markdown."""
    md = []
    if title:
        md.append(f"## {title}\n")

    # Sequential tag processing with a tiny regex-based approach (no external libs).
    # Handle the common tags: h1-h6, p, li, table rows, strong/b, em/i, a, img.
    s = body

    # Block-level: headings
    for lvl in range(1, 7):
        s = re.sub(
            rf"<h{lvl}[^>]*>(.*?)</h{lvl}>",
            lambda m, l=lvl: f"\n\n{'#' * l} {_inline_to_md(m.group(1)).strip()}\n\n",
            s, flags=re.I | re.S,
        )

    # Lists
    def li_repl(m):
        txt = _inline_to_md(m.group(1)).strip()
        return f"\n- {txt}"
    s = re.sub(r"<li[^>]*>(.*?)</li>", li_repl, s, flags=re.I | re.S)

    # Tables
    def table_repl(m):
        return _html_table_to_md(m.group(0))
    s = re.sub(r"<table[^>]*>.*?</table>", table_repl, s, flags=re.I | re.S)

    # Paragraphs
    def p_repl(m):
        txt = _inline_to_md(m.group(1)).strip()
        return f"\n\n{txt}\n\n" if txt else "\n\n"
    s = re.sub(r"<p[^>]*>(.*?)</p>", p_repl, s, flags=re.I | re.S)

    # Line breaks
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)

    # Any remaining inline formatting
    s = _inline_to_md(s)

    # Strip any leftover tags
    s = re.sub(r"<[^>]+>", "", s)

    # Unescape entities
    s = html.unescape(s)

    return s


def _inline_to_md(s: str) -> str:
    """Convert inline elements: strong/b → **, em/i → *, a → [text](url), img → ![alt](src)."""
    # Images (must come before links)
    def img_repl(m):
        attrs = _parse_attrs(m.group(1))
        alt = attrs.get("alt", "")
        src = attrs.get("src", "")
        if not alt:
            alt = os.path.basename(src) or "image"
        return f"![{alt}]({src})"
    s = re.sub(r"<img\b([^>]*)>", img_repl, s, flags=re.I)

    # Links
    def a_repl(m):
        attrs = _parse_attrs(m.group(1))
        href = attrs.get("href", "")
        txt = _strip_html(m.group(2))
        if not txt:
            txt = href
        if href:
            return f"[{txt}]({href})"
        return txt
    s = re.sub(r"<a\b([^>]*)>(.*?)</a>", a_repl, s, flags=re.I | re.S)

    # Bold / strong
    s = re.sub(r"</?(?:strong|b)>", "**", s, flags=re.I)

    # Italic / emphasis
    s = re.sub(r"</?(?:em|i)>", "*", s, flags=re.I)

    # Code
    s = re.sub(r"</?code>", "`", s, flags=re.I)

    return s


def _parse_attrs(attr_str: str):
    attrs = {}
    for m in re.finditer(r'([\w-]+)\s*=\s*"([^"]*)"', attr_str):
        attrs[m.group(1).lower()] = m.group(2)
    return attrs


def _html_table_to_md(tbl_html: str) -> str:
    def cells_repl(m):
        tag = m.group(1).lower()
        content = _inline_to_md(_strip_html(m.group(2))).strip()
        return (tag, content)

    rows = re.split(r"</tr>", tbl_html, flags=re.I)
    parsed = []
    for row in rows:
        if "<tr" not in row.lower() and "<td" not in row.lower() and "<th" not in row.lower():
            continue
        cells = []
        for m in re.finditer(r"<(th|td)[^>]*>(.*?)</\1>", row, flags=re.I | re.S):
            content = _inline_to_md(_strip_html(m.group(2))).strip()
            cells.append(content)
        if cells:
            parsed.append(cells)
    if not parsed:
        return ""
    width = max(len(r) for r in parsed)
    for r in parsed:
        r += [""] * (width - len(r))
    lines = ["| " + " | ".join(parsed[0]) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for r in parsed[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n\n" + "\n".join(lines) + "\n\n"


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #
def convert_one(src: Path, out_dir: Path, overwrite: bool, engine: str, verbose: bool) -> str:
    ext = src.suffix.lower()
    if ext == ".pdf":
        md = convert_pdf(src, engine)
    elif ext in (".docx", ".doc"):
        md = convert_docx(src)
    elif ext == ".epub":
        md = convert_epub(src)
    else:
        return "skip:unsupported"

    if not md.strip():
        return f"skip:empty:{src.name}"

    md = apply_508_hygiene(md)

    out_file = out_dir / (src.stem + ".md")
    if out_file.exists() and not overwrite:
        return f"skip:exists:{out_file.name}"

    out_file.write_text(md, encoding="utf-8")
    return f"ok:{out_file.name}"


def gather_sources(target: Path, recursive: bool):
    exts = {".pdf", ".docx", ".doc", ".epub"}
    if target.is_file():
        return [target] if target.suffix.lower() in exts else []
    if not target.is_dir():
        print(f"[ERROR] Path not found: {target}", file=sys.stderr)
        sys.exit(1)
    if recursive:
        return [p for p in target.rglob("*") if p.suffix.lower() in exts]
    return [p for p in target.iterdir() if p.suffix.lower() in exts]


def main():
    ap = argparse.ArgumentParser(description="Convert PDF/DOCX/EPUB to 508-compliant markdown.")
    ap.add_argument("target", help="File or directory to convert")
    ap.add_argument("--recursive", action="store_true", help="Scan subdirectories")
    ap.add_argument("--output_dir", default=None, help="Directory for output .md files")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing .md files")
    ap.add_argument("--verbose", action="store_true", help="Print per-file status")
    ap.add_argument("--engine", choices=["pymupdf", "llm", "marker"], default="pymupdf",
                    help="PDF engine (default: pymupdf; llm=pymupdf4llm; marker=OCR)")
    args = ap.parse_args()

    target = Path(args.target)
    sources = sorted(gather_sources(target, args.recursive))
    if not sources:
        print(f"No .pdf/.docx/.doc/.epub files found under {target}")
        return 0

    out_dir = Path(args.output_dir) if args.output_dir else target.parent if target.is_file() else target
    out_dir.mkdir(parents=True, exist_ok=True)

    ok = skipped = failed = 0
    for src in sources:
        try:
            status = convert_one(src, out_dir, args.overwrite, args.engine, args.verbose)
        except Exception as e:  # noqa: BLE001
            status = f"error:{src.name}:{e}"
        if status.startswith("ok"):
            ok += 1
            if args.verbose:
                print(f"[OK]   {src.name} -> {status.split(':',1)[1]}")
        elif status.startswith("skip"):
            skipped += 1
            if args.verbose:
                print(f"[SKIP] {status}")
        else:
            failed += 1
            print(f"[FAIL] {status}", file=sys.stderr)

    print(f"\nDone. {ok} converted, {skipped} skipped, {failed} failed.")
    print(f"Output directory: {out_dir}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())