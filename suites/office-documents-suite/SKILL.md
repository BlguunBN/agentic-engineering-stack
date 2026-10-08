---
name: office-documents-suite
description: "Master unified Office & document processing suite. Consolidates PDF reading/extraction/forms/OCR (`pdf`), Microsoft Word `.docx` authoring (`docx`), and Excel `.xlsx` spreadsheets modeling (`xlsx`). Preserves exact formatting and formulas."
category: "creative-and-media"
tools:
  - python
---

# Office Documents Suite (Unified Master Skill)

A unified processing center for generating, parsing, and modifying business documents (PDF, DOCX, XLSX).

## 1. Document Format Routing Ladder

```
[Need to generate, read, or edit a document]
   |
   +---> Is it a PDF document?
   |        └──> Use `pdf` / `pdf-official`: PyMuPDF / pdfplumber for text & tables, ReportLab for creation, OCR for scans.
   |
   +---> Is it a Microsoft Word document (.docx)?
   |        └──> Use `docx` / `docx-official`: `python-docx` with XML manipulation for headers, tables, and styles.
   |
   +---> Is it a spreadsheet (.xlsx / .csv)?
            └──> Use `xlsx` / `xlsx-official`: `openpyxl` / `pandas` for formulas, multi-sheet models, and charts.
```

## 2. Python Tool Selection by Format

### PDF Processing
- **Text & Table Extraction:** Use `pdfplumber` or `pypdf`.
- **High-Fidelity Rendering / Page Images:** Use `fitz` (`PyMuPDF`).
- **Generation:** Use `reportlab` with exact point coordinates or HTML-to-PDF (`weasyprint` / headless Chrome).

### Word (.docx) Processing
- Always manipulate document structure via `python-docx`.
- Preserve existing document XML formatting when performing search-and-replace or redlining.

### Excel (.xlsx) Processing
- Always use uppercase standard formula names (`SUM`, `AVERAGE`, `VLOOKUP`, `XLOOKUP`).
- Use `openpyxl` with `data_only=False` to preserve user formulas, or `data_only=True` to read calculated values.

## 3. Quick Reference Recipes

### Read PDF Text & Tables
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

### Create Styled Excel Spreadsheet
```python
import openpyxl
from openpyxl.styles import Font, PatternFill

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Financial Model"

ws["A1"] = "Revenue"
ws["B1"] = 10000
ws["A2"] = "Expenses"
ws["B2"] = 4000
ws["A3"] = "Net Income"
ws["B3"] = "=B1-B2"

header_font = Font(bold=True)
ws["A3"].font = header_font
ws["B3"].font = header_font
wb.save("model.xlsx")
```
