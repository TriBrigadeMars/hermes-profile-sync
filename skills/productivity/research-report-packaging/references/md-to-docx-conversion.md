# Markdown-to-DOCX Conversion Pattern

A reusable pattern for converting markdown with rich inline formatting to a properly formatted .docx using python-docx.

## Why Custom Script (Not docx_create.py JSON Spec)

The `docx_create.py` approach requires pre-parsing markdown into a JSON block structure. This works for simple documents but becomes cumbersome when the markdown has:
- Inline italic formatting (`*Journal Name*`) mixed with regular text
- Bold text (`**text**`) within paragraphs
- References with alternating italic/normal runs

A custom python-docx script handles these cases directly.

## Conversion Script Pattern

```python
#!/usr/bin/env python3
"""Convert markdown to .docx with proper formatting."""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_LINE_SPACING

def setup_document():
    """Create and configure the document with proper styles."""
    doc = Document()
    
    # Set 1-inch margins all sides
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    
    # Set document properties
    doc.core_properties.language = "en-US"
    doc.core_properties.title = "Document Title"
    
    # Configure Normal style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    
    # Configure Title style (one per document, distinct from Heading 1)
    title_style = doc.styles['Title']
    title_style.font.name = 'Arial'
    title_style.font.size = Pt(16)
    title_style.font.bold = True
    title_style.font.color.rgb = RGBColor(0, 0, 0)
    title_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Configure headings (Heading 1, 2, 3)
    for level, size in [(1, 14), (2, 13), (3, 12)]:
        style = doc.styles[f'Heading {level}']
        style.font.name = 'Arial'
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    
    return doc

def parse_inline_formatting(para, text):
    """Parse markdown inline formatting and add runs to paragraph.
    
    Handles: *italic*, **bold**, ***bold italic***
    """
    # Split on ***bold italic*** first
    parts = re.split(r'\*\*\*(.*?)\*\*\*', text)
    for i, part in enumerate(parts):
        if i % 2 == 1:  # bold italic
            run = para.add_run(part)
            run.bold = True
            run.italic = True
        else:
            # Split on **bold**
            sub_parts = re.split(r'\*\*(.*?)\*\*', part)
            for j, sub_part in enumerate(sub_parts):
                if j % 2 == 1:  # bold
                    run = para.add_run(sub_part)
                    run.bold = True
                else:
                    # Split on *italic*
                    italic_parts = re.split(r'\*(.*?)\*', sub_part)
                    for k, italic_part in enumerate(italic_parts):
                        if k % 2 == 1:  # italic
                            run = para.add_run(italic_part)
                            run.italic = True
                        else:
                            if italic_part:
                                run = para.add_run(italic_part)
    
    # Set font for all runs
    for run in para.runs:
        if not run.font.name:
            run.font.name = 'Arial'
        if not run.font.size:
            run.font.size = Pt(12)

def parse_references(text):
    """Parse a reference line, yielding ('italic', text) or ('normal', text)."""
    parts = re.split(r'\*([^*]+)\*', text)
    for i, part in enumerate(parts):
        if i % 2 == 1:  # italic part (journal name)
            yield ('italic', part)
        else:
            yield ('normal', part)

def convert_md_to_docx(md_path, output_path, exclude_pattern=None):
    """Main conversion function."""
    doc = setup_document()
    title_used = False  # Track whether Title style has been applied
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Exclude HTML comments if specified
    if exclude_pattern:
        lines = [l for l in lines if exclude_pattern not in l]
    
    for line in lines:
        line = line.rstrip('\n')
        
        # Skip empty lines
        if not line.strip():
            continue
        
        # Headings — APA 7 mapping:
        # # (first) → Title style (document title)
        # ## → Heading 1 (APA Level 1: major sections)
        # ### → Heading 2 (APA Level 2: subsections)
        # #### → Heading 3 (APA Level 3: sub-subsections)
        if line.startswith('#### '):
            para = doc.add_heading(line[5:].strip(), level=3)
        elif line.startswith('### '):
            para = doc.add_heading(line[4:].strip(), level=2)
        elif line.startswith('## '):
            para = doc.add_heading(line[3:].strip(), level=1)
        elif line.startswith('# '):
            # First # becomes Title style; subsequent #s become Heading 1
            if not title_used:
                para = doc.add_paragraph(line[2:].strip(), style='Title')
                title_used = True
            else:
                para = doc.add_heading(line[2:].strip(), level=1)
        # Bullet lists
        elif line.startswith('- '):
            para = doc.add_paragraph(style='List Bullet')
            parse_inline_formatting(para, line[2:].strip())
        # Regular paragraph (including references)
        else:
            para = doc.add_paragraph()
            # Check if this is a reference (starts with known author names)
            if any(line.startswith(name) for name in ['Azagba', 'Bauermeister', 'Budenz', 'CDC', 'Corey', 'Crankshaw', 'Donaldson', 'Fahey', 'Gentzke', 'Graham', 'Hendlin', 'Krueger', 'Mann', 'Mereish', 'Parchem', 'Perry', 'Regalado', 'Romm', 'Soneji', 'Tan', 'Theis', 'U.S.', 'Vogel']):
                for run_type, run_text in parse_references(line):
                    if run_type == 'italic':
                        run = para.add_run(run_text)
                        run.italic = True
                    else:
                        run = para.add_run(run_text)
                    run.font.name = 'Arial'
                    run.font.size = Pt(12)
            else:
                parse_inline_formatting(para, line)
        
        # Set line spacing for all paragraphs
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    
    doc.save(output_path)

# Usage:
# convert_md_to_docx('input.md', 'output.docx', exclude_pattern='<!--style-pass-notes-->')
```

## Key Patterns

### 1. Italic Journal Names in References

References use `*Journal Name*` for italics. The `parse_references()` function splits on `*` and alternates between normal and italic runs:

```python
for run_type, run_text in parse_references(line):
    if run_type == 'italic':
        run = para.add_run(run_text)
        run.italic = True
    else:
        run = para.add_run(run_text)
    run.font.name = 'Arial'
```

### 2. HTML Comment Exclusion

Strip lines containing the pattern before processing:

```python
lines = [l for l in lines if '<!--style-pass-notes-->' not in l]
```

### 3. Heading Style Override

After adding headings, override the default font:

```python
para = doc.add_heading(text, level=1)
for run in para.runs:
    run.font.name = 'Arial'
    run.font.color.rgb = RGBColor(0, 0, 0)
```

### 4. Line Spacing on All Paragraphs

Set double-spacing on every paragraph, including headings:

```python
para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
```

## Verification After Conversion

```python
from docx import Document

doc = Document('output.docx')
print(f'Paragraphs: {len(doc.paragraphs)}')
print(f'Tables: {len(doc.tables)}')

# Check fonts
fonts = set()
for para in doc.paragraphs:
    for run in para.runs:
        if run.font.name:
            fonts.add(run.font.name)
print(f'Fonts: {fonts}')

# Check line spacing
spacings = set()
for para in doc.paragraphs:
    if para.paragraph_format.line_spacing_rule:
        spacings.add(str(para.paragraph_format.line_spacing_rule))
print(f'Line spacings: {spacings}')

# Check margins
section = doc.sections[0]
print(f'Margins: {section.top_margin.inches}" all sides')
```
