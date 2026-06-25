#!/usr/bin/env python3
"""
PDF to Markdown Converter

Универсальный скрипт для извлечения текста из PDF и конвертации в Markdown.
Поддерживает как встроенный текст, так и OCR для сканированных документов.

Usage:
    python pdf_to_markdown.py input.pdf -o output.md
    python pdf_to_markdown.py input.pdf -o output.md --ocr
    python pdf_to_markdown.py input.pdf -o output.md --pages 1-5
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies(use_ocr: bool = False) -> bool:
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import pdfplumber
    except ImportError:
        missing.append('pdfplumber')
    
    try:
        import fitz  # PyMuPDF
    except ImportError:
        missing.append('PyMuPDF')
    
    if use_ocr:
        try:
            import pytesseract
        except ImportError:
            missing.append('pytesseract')
        
        try:
            from pdf2image import convert_from_path
        except ImportError:
            missing.append('pdf2image')
    
    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        logger.error("Install with: pip install " + ' '.join(missing))
        return False
    
    return True


def parse_page_range(pages_str: str, total_pages: int) -> list[int]:
    """
    Parse page range string like '1-5,7,10-12' into list of page numbers.
    
    Args:
        pages_str: Page range string
        total_pages: Total number of pages in document
        
    Returns:
        List of 0-indexed page numbers
    """
    pages = set()
    
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start) if start else 1
            end = int(end) if end else total_pages
            pages.update(range(start - 1, min(end, total_pages)))
        else:
            page_num = int(part) - 1
            if 0 <= page_num < total_pages:
                pages.add(page_num)
    
    return sorted(pages)


def extract_text_pdfplumber(pdf_path: Path, pages: Optional[list[int]] = None) -> list[tuple[int, str]]:
    """
    Extract text using pdfplumber (good for tables and structured content).
    
    Args:
        pdf_path: Path to PDF file
        pages: List of 0-indexed page numbers to extract, None for all
        
    Returns:
        List of (page_number, text) tuples
    """
    import pdfplumber
    
    results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        page_indices = pages if pages is not None else range(len(pdf.pages))
        
        for i in page_indices:
            if i >= len(pdf.pages):
                continue
                
            page = pdf.pages[i]
            text = page.extract_text() or ''
            
            # Try to extract tables
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table:
                        text += '\n\n' + format_table_as_markdown(table)
            
            results.append((i + 1, text))
    
    return results


def extract_text_pymupdf(pdf_path: Path, pages: Optional[list[int]] = None) -> list[tuple[int, str]]:
    """
    Extract text using PyMuPDF (fast, good for simple documents).
    
    Args:
        pdf_path: Path to PDF file
        pages: List of 0-indexed page numbers to extract, None for all
        
    Returns:
        List of (page_number, text) tuples
    """
    import fitz
    
    results = []
    
    doc = fitz.open(pdf_path)
    page_indices = pages if pages is not None else range(len(doc))
    
    for i in page_indices:
        if i >= len(doc):
            continue
            
        page = doc[i]
        text = page.get_text()
        results.append((i + 1, text))
    
    doc.close()
    return results


def extract_text_ocr(pdf_path: Path, pages: Optional[list[int]] = None, lang: str = 'rus+eng') -> list[tuple[int, str]]:
    """
    Extract text using OCR (for scanned documents).
    
    Args:
        pdf_path: Path to PDF file
        pages: List of 0-indexed page numbers to extract, None for all
        lang: Tesseract language code
        
    Returns:
        List of (page_number, text) tuples
    """
    import pytesseract
    from pdf2image import convert_from_path
    
    results = []
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    page_indices = pages if pages is not None else range(len(images))
    
    for i in page_indices:
        if i >= len(images):
            continue
            
        image = images[i]
        text = pytesseract.image_to_string(image, lang=lang)
        results.append((i + 1, text))
    
    return results


def format_table_as_markdown(table: list[list[str]]) -> str:
    """
    Convert a table (list of rows) to Markdown format.
    
    Args:
        table: List of rows, each row is a list of cell values
        
    Returns:
        Markdown formatted table string
    """
    if not table or not table[0]:
        return ''
    
    # Clean cells
    cleaned_table = []
    for row in table:
        cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else '' for cell in row]
        cleaned_table.append(cleaned_row)
    
    # Calculate column widths
    num_cols = max(len(row) for row in cleaned_table)
    col_widths = [3] * num_cols  # minimum width
    
    for row in cleaned_table:
        for i, cell in enumerate(row):
            if i < num_cols:
                col_widths[i] = max(col_widths[i], len(cell))
    
    # Build markdown table
    lines = []
    
    # Header row
    if cleaned_table:
        header = cleaned_table[0]
        header_line = '| ' + ' | '.join(
            (header[i] if i < len(header) else '').ljust(col_widths[i])
            for i in range(num_cols)
        ) + ' |'
        lines.append(header_line)
        
        # Separator
        sep_line = '| ' + ' | '.join('-' * w for w in col_widths) + ' |'
        lines.append(sep_line)
        
        # Data rows
        for row in cleaned_table[1:]:
            data_line = '| ' + ' | '.join(
                (row[i] if i < len(row) else '').ljust(col_widths[i])
                for i in range(num_cols)
            ) + ' |'
            lines.append(data_line)
    
    return '\n'.join(lines)


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and artifacts.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove trailing whitespace from lines
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def text_to_markdown(pages_text: list[tuple[int, str]], include_page_markers: bool = True) -> str:
    """
    Convert extracted text to Markdown format.
    
    Args:
        pages_text: List of (page_number, text) tuples
        include_page_markers: Whether to include page markers
        
    Returns:
        Markdown formatted text
    """
    parts = []
    
    for page_num, text in pages_text:
        cleaned = clean_text(text)
        
        if not cleaned:
            continue
        
        if include_page_markers:
            parts.append(f'<!-- Page {page_num} -->\n')
        
        parts.append(cleaned)
        parts.append('\n\n')
    
    return ''.join(parts).strip()


def is_text_meaningful(text: str, min_length: int = 50) -> bool:
    """
    Check if extracted text is meaningful (not empty or garbage).
    
    Args:
        text: Text to check
        min_length: Minimum length to consider meaningful
        
    Returns:
        True if text appears meaningful
    """
    if not text:
        return False
    
    # Remove whitespace and check length
    cleaned = re.sub(r'\s+', '', text)
    if len(cleaned) < min_length:
        return False
    
    # Check for high proportion of readable characters
    readable = re.sub(r'[^\w\s.,!?;:"\'-]', '', text, flags=re.UNICODE)
    if len(readable) < len(text) * 0.5:
        return False
    
    return True


def convert_pdf_to_markdown(
    input_path: str,
    output_path: Optional[str] = None,
    use_ocr: bool = False,
    ocr_lang: str = 'rus+eng',
    pages: Optional[str] = None,
    include_page_markers: bool = True,
    force_ocr: bool = False
) -> str:
    """
    Main function to convert PDF to Markdown.
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to output Markdown file (optional)
        use_ocr: Enable OCR fallback for scanned documents
        ocr_lang: Tesseract language code for OCR
        pages: Page range string (e.g., '1-5,7,10-12')
        include_page_markers: Include page markers in output
        force_ocr: Force OCR even if text extraction works
        
    Returns:
        Extracted Markdown text
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"PDF file not found: {input_path}")
    
    if not check_dependencies(use_ocr=use_ocr):
        raise RuntimeError("Missing required dependencies")
    
    # Get total pages count
    import fitz
    doc = fitz.open(input_path)
    total_pages = len(doc)
    doc.close()
    
    # Parse page range
    page_indices = None
    if pages:
        page_indices = parse_page_range(pages, total_pages)
        logger.info(f"Processing pages: {[p + 1 for p in page_indices]}")
    else:
        logger.info(f"Processing all {total_pages} pages")
    
    # Extract text
    pages_text = []
    
    if not force_ocr:
        # Try pdfplumber first (better for tables)
        logger.info("Extracting text with pdfplumber...")
        pages_text = extract_text_pdfplumber(input_path, page_indices)
        
        # Check if we got meaningful text
        all_text = ' '.join(text for _, text in pages_text)
        
        if not is_text_meaningful(all_text):
            # Try PyMuPDF as backup
            logger.info("pdfplumber extraction insufficient, trying PyMuPDF...")
            pages_text = extract_text_pymupdf(input_path, page_indices)
            all_text = ' '.join(text for _, text in pages_text)
    
    # OCR fallback
    if force_ocr or (use_ocr and not is_text_meaningful(' '.join(text for _, text in pages_text))):
        logger.info(f"Using OCR with language: {ocr_lang}")
        pages_text = extract_text_ocr(input_path, page_indices, ocr_lang)
    
    # Convert to Markdown
    markdown_text = text_to_markdown(pages_text, include_page_markers)
    
    if not markdown_text:
        logger.warning("No text could be extracted from the PDF")
        markdown_text = "<!-- No text could be extracted from this PDF -->"
    
    # Write output
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_text, encoding='utf-8')
        logger.info(f"Saved to: {output_path}")
    
    return markdown_text


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert PDF to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf -o output.md
  %(prog)s input.pdf -o output.md --ocr
  %(prog)s input.pdf -o output.md --pages 1-5,10
  %(prog)s input.pdf --force-ocr --lang rus
        """
    )
    
    parser.add_argument(
        'input',
        help='Input PDF file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output Markdown file path (prints to stdout if not specified)'
    )
    
    parser.add_argument(
        '--ocr',
        action='store_true',
        help='Enable OCR fallback for scanned documents'
    )
    
    parser.add_argument(
        '--force-ocr',
        action='store_true',
        help='Force OCR even if text extraction works'
    )
    
    parser.add_argument(
        '--lang',
        default='rus+eng',
        help='OCR language(s), e.g., "rus", "eng", "rus+eng" (default: rus+eng)'
    )
    
    parser.add_argument(
        '--pages',
        help='Page range to extract, e.g., "1-5", "1,3,5", "1-3,7-10"'
    )
    
    parser.add_argument(
        '--no-page-markers',
        action='store_true',
        help='Do not include page markers in output'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        result = convert_pdf_to_markdown(
            input_path=args.input,
            output_path=args.output,
            use_ocr=args.ocr or args.force_ocr,
            ocr_lang=args.lang,
            pages=args.pages,
            include_page_markers=not args.no_page_markers,
            force_ocr=args.force_ocr
        )
        
        if not args.output:
            print(result)
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
