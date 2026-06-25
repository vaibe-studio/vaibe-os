#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from fpdf import FPDF


_RE_MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_MD_ITALIC_1 = re.compile(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)")
_RE_MD_ITALIC_2 = re.compile(r"_(?!\s)(.+?)(?<!\s)_")
_RE_MD_INLINE_CODE = re.compile(r"`([^`]+)`")
_RE_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_MD_IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
_RE_TABLE_SEP_CELL = re.compile(r"^:?-{2,}:?$")


def strip_inline_markdown(text: str) -> str:
    text = _RE_MD_LINK.sub(r"\1 (\2)", text)
    text = _RE_MD_INLINE_CODE.sub(r"\1", text)
    text = _RE_MD_BOLD.sub(r"\1", text)
    text = _RE_MD_ITALIC_1.sub(r"\1", text)
    text = _RE_MD_ITALIC_2.sub(r"\1", text)
    return text


@dataclass(frozen=True)
class FontFiles:
    regular: Path
    bold: Path | None = None
    italic: Path | None = None
    bold_italic: Path | None = None


def _first_existing(paths: Iterable[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def detect_windows_font_family() -> FontFiles:
    fonts_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"

    candidates: list[FontFiles] = []
    candidates.append(
        FontFiles(
            regular=fonts_dir / "arial.ttf",
            bold=fonts_dir / "arialbd.ttf",
            italic=fonts_dir / "ariali.ttf",
            bold_italic=fonts_dir / "arialbi.ttf",
        )
    )
    candidates.append(
        FontFiles(
            regular=fonts_dir / "segoeui.ttf",
            bold=fonts_dir / "segoeuib.ttf",
            italic=fonts_dir / "segoeuii.ttf",
            bold_italic=fonts_dir / "segoeuiz.ttf",
        )
    )
    candidates.append(
        FontFiles(
            regular=fonts_dir / "calibri.ttf",
            bold=fonts_dir / "calibrib.ttf",
            italic=fonts_dir / "calibrii.ttf",
            bold_italic=fonts_dir / "calibriz.ttf",
        )
    )

    for c in candidates:
        if c.regular.exists():
            return c

    # Last-resort: pick any TTF available (regular only).
    any_ttf = _first_existing(fonts_dir.glob("*.ttf"))
    if any_ttf is None:
        raise RuntimeError("No .ttf fonts found in Windows Fonts directory; cannot render Unicode text.")
    return FontFiles(regular=any_ttf)


def detect_windows_mono_font() -> Path | None:
    fonts_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    for name in ("consola.ttf", "cour.ttf"):
        p = fonts_dir / name
        if p.exists():
            return p
    return None


class PDF(FPDF):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._footer_logo_path: str | None = None
        self._footer_font_family: str = "Helvetica"
        self._footer_available_styles: set[str] = {""}

    def footer(self) -> None:
        if self._footer_logo_path is None:
            return
        self.set_y(-18)
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        logo = Path(self._footer_logo_path)
        if logo.exists():
            self.image(str(logo), x=self.l_margin, y=self.h - 16, w=18)
        self.set_y(-14)
        self.set_font(
            self._footer_font_family,
            style=_safe_style("", self._footer_available_styles),
            size=8,
        )
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, str(self.page_no()), align="R")
        self.set_text_color(0, 0, 0)


def _add_font_family(pdf: FPDF, family: str, files: FontFiles) -> None:
    pdf.add_font(family, style="", fname=str(files.regular))
    if files.bold and files.bold.exists():
        pdf.add_font(family, style="B", fname=str(files.bold))
    if files.italic and files.italic.exists():
        pdf.add_font(family, style="I", fname=str(files.italic))
    if files.bold_italic and files.bold_italic.exists():
        pdf.add_font(family, style="BI", fname=str(files.bold_italic))


def _safe_style(requested: str, available_styles: set[str]) -> str:
    if requested in available_styles:
        return requested
    if requested == "BI":
        if "B" in available_styles:
            return "B"
        if "I" in available_styles:
            return "I"
    if requested == "B" and "B" not in available_styles:
        return ""
    if requested == "I" and "I" not in available_styles:
        return ""
    return ""


def _is_table_line(line: str) -> bool:
    s = line.strip()
    return bool(s) and s[0] == "|" and s.count("|") >= 2


def _is_separator_row(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return len(cells) >= 1 and all(_RE_TABLE_SEP_CELL.match(c) for c in cells if c)


def _parse_alignments(sep_line: str) -> list[str]:
    cells = [c.strip() for c in sep_line.strip().strip("|").split("|")]
    aligns: list[str] = []
    for c in cells:
        c = c.strip()
        if c.startswith(":") and c.endswith(":"):
            aligns.append("C")
        elif c.endswith(":"):
            aligns.append("R")
        else:
            aligns.append("L")
    return aligns


def _parse_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [strip_inline_markdown(c.strip()) for c in s.split("|")]


def _compute_cell_line_count(pdf: FPDF, text: str, col_width: float) -> int:
    """How many visual lines does *text* occupy in a cell of *col_width* mm?"""
    usable = col_width - 2  # 1 mm padding each side
    if usable <= 0:
        return 1
    words = text.split()
    if not words:
        return 1
    lines = 1
    cur_line = ""
    for w in words:
        test = f"{cur_line} {w}".strip()
        if pdf.get_string_width(test) > usable:
            lines += 1
            cur_line = w
        else:
            cur_line = test
    return lines


def _render_table(
    pdf: FPDF,
    table_lines: list[str],
    main_family: str,
    available_main_styles: set[str],
) -> bool:
    """Render a markdown table with text wrapping, auto font sizing, and alternating row colors.

    Returns True if successfully rendered, False if lines don't form a valid table.
    """
    if len(table_lines) < 3:
        return False
    if not _is_separator_row(table_lines[1]):
        return False

    header = _parse_row(table_lines[0])
    alignments = _parse_alignments(table_lines[1])
    rows = [_parse_row(line) for line in table_lines[2:]]
    n_cols = len(header)

    while len(alignments) < n_cols:
        alignments.append("L")

    avail_w = pdf.w - pdf.l_margin - pdf.r_margin

    font_size = 10
    if n_cols >= 7:
        font_size = 7
    elif n_cols >= 5:
        font_size = 8
    elif n_cols >= 4:
        font_size = 9

    pdf.set_font(main_family, style=_safe_style("B", available_main_styles), size=font_size)
    col_max_w = [0.0] * n_cols
    for i, h in enumerate(header):
        if i < n_cols:
            col_max_w[i] = max(col_max_w[i], pdf.get_string_width(h) + 4)

    pdf.set_font(main_family, style="", size=font_size)
    for row in rows:
        for i in range(n_cols):
            cell_text = row[i] if i < len(row) else ""
            col_max_w[i] = max(col_max_w[i], pdf.get_string_width(cell_text) + 4)

    total_natural = sum(col_max_w)
    if total_natural <= avail_w:
        scale = avail_w / total_natural if total_natural > 0 else 1
        col_w = [w * scale for w in col_max_w]
    else:
        min_col_w = max(14.0, avail_w / n_cols * 0.4)
        col_w = [max(w, min_col_w) for w in col_max_w]
        total_clamped = sum(col_w)
        if total_clamped > avail_w:
            scale = avail_w / total_clamped
            col_w = [w * scale for w in col_w]

    line_h = max(4, int(round(font_size * 0.5)))

    min_table_h = line_h * min(len(rows) + 1, 4)
    remaining = pdf.page_break_trigger - pdf.get_y()
    if remaining < min_table_h:
        pdf.add_page()

    def _draw_wrapped_row(cells: list[str], is_header: bool, fill_color: tuple[int, int, int]) -> None:
        """Draw a single table row with text wrapping in each cell."""
        if is_header:
            pdf.set_font(main_family, style=_safe_style("B", available_main_styles), size=font_size)
        else:
            pdf.set_font(main_family, style="", size=font_size)

        row_line_counts = []
        for i in range(n_cols):
            cell_text = cells[i] if i < len(cells) else ""
            row_line_counts.append(_compute_cell_line_count(pdf, cell_text, col_w[i]))
        max_lines = max(row_line_counts) if row_line_counts else 1
        row_h = line_h * max_lines + 2

        page_remaining = pdf.page_break_trigger - pdf.get_y()
        if page_remaining < row_h:
            pdf.add_page()

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        pdf.set_fill_color(*fill_color)
        for i in range(n_cols):
            pdf.rect(x_start + sum(col_w[:i]), y_start, col_w[i], row_h, style="DF")

        for i in range(n_cols):
            cell_text = cells[i] if i < len(cells) else ""
            align = alignments[i] if i < len(alignments) else "L"
            cell_x = x_start + sum(col_w[:i])
            pdf.set_xy(cell_x + 1, y_start + 1)
            if is_header:
                pdf.set_font(main_family, style=_safe_style("B", available_main_styles), size=font_size)
            else:
                pdf.set_font(main_family, style="", size=font_size)
            pdf.multi_cell(col_w[i] - 2, line_h, cell_text, align=align)

        pdf.set_xy(x_start, y_start + row_h)

    pdf.set_draw_color(180, 180, 180)

    pdf.set_text_color(255, 255, 255)
    _draw_wrapped_row(header, is_header=True, fill_color=(70, 70, 80))

    pdf.set_text_color(50, 50, 50)
    for r_idx, row in enumerate(rows):
        fill = (245, 245, 248) if r_idx % 2 == 0 else (255, 255, 255)
        _draw_wrapped_row(row, is_header=False, fill_color=fill)

    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(2)
    return True


def render_markdown_to_pdf(
    md_text: str,
    output_path: Path,
    *,
    title: str | None = None,
    author: str | None = None,
    main_font: FontFiles | None = None,
    mono_font_path: Path | None = None,
    base_dir: Path | None = None,
    footer_logo: Path | None = None,
) -> None:
    if main_font is None:
        main_font = detect_windows_font_family()
    if mono_font_path is None:
        mono_font_path = detect_windows_mono_font()

    pdf = PDF(format="A4", unit="mm")
    bottom_margin = 22 if footer_logo else 15
    pdf.set_auto_page_break(auto=True, margin=bottom_margin)
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()

    main_family = "Main"
    _add_font_family(pdf, main_family, main_font)
    available_main_styles = {""}
    for s in ("B", "I", "BI"):
        try:
            # fpdf2 doesn't expose style registry; rely on add_font calls above + file existence.
            if getattr(main_font, {"B": "bold", "I": "italic", "BI": "bold_italic"}[s]) is not None:
                available_main_styles.add(s)
        except KeyError:
            pass

    mono_family = None
    if mono_font_path is not None and mono_font_path.exists():
        mono_family = "Mono"
        pdf.add_font(mono_family, style="", fname=str(mono_font_path))

    pdf.set_title(title or output_path.stem)
    if author:
        pdf.set_author(author)

    if footer_logo and footer_logo.exists():
        pdf._footer_logo_path = str(footer_logo)
        pdf._footer_font_family = main_family
        pdf._footer_available_styles = available_main_styles

    def set_main(size: int, style: str = "") -> None:
        pdf.set_font(main_family, style=_safe_style(style, available_main_styles), size=size)

    def write_paragraph(text: str, *, indent_mm: float = 0.0, size: int = 12, style: str = "") -> None:
        set_main(size, style)
        x0 = pdf.get_x()
        if indent_mm:
            pdf.set_x(x0 + indent_mm)
        line_h = max(5, int(round(size * 0.45)))
        pdf.multi_cell(0, line_h, text, align="L")
        pdf.ln(1)
        if indent_mm:
            pdf.set_x(x0)

    def write_hr() -> None:
        y = pdf.get_y()
        x1 = pdf.l_margin
        x2 = pdf.w - pdf.r_margin
        pdf.set_draw_color(180, 180, 180)
        pdf.line(x1, y + 1, x2, y + 1)
        pdf.ln(3)

    in_code = False
    code_lines: list[str] = []
    table_buffer: list[str] = []

    lines = md_text.splitlines()
    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip() == "<!-- pagebreak -->":
            pdf.add_page()
            continue

        img_m = _RE_MD_IMAGE.match(line.strip())
        if img_m:
            img_path_raw = img_m.group(2)
            img_path = Path(img_path_raw)
            if not img_path.is_absolute() and base_dir is not None:
                img_path = base_dir / img_path
            if img_path.exists():
                avail_w = pdf.w - pdf.l_margin - pdf.r_margin
                img_w = min(avail_w * 0.35, 55)
                x_centered = (pdf.w - img_w) / 2
                pdf.image(str(img_path), x=x_centered, w=img_w)
                pdf.ln(5)
            continue

        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
                continue
            # closing fence
            in_code = False
            block = "\n".join(code_lines).rstrip()
            if block:
                if mono_family:
                    pdf.set_font(mono_family, size=10)
                else:
                    set_main(10)
                pdf.set_fill_color(245, 245, 245)
                pdf.multi_cell(0, 5, block, fill=True)
                pdf.ln(2)
            continue

        if in_code:
            code_lines.append(line)
            continue

        if _is_table_line(line):
            table_buffer.append(line)
            continue

        if table_buffer:
            if not _render_table(pdf, table_buffer, main_family, available_main_styles):
                for tl in table_buffer:
                    write_paragraph(strip_inline_markdown(tl))
            table_buffer = []

        if not line.strip():
            pdf.ln(1)
            continue

        if line.strip() == "---":
            write_hr()
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = strip_inline_markdown(m.group(2)).strip()
            sizes = {1: 20, 2: 16, 3: 14, 4: 12}
            remaining = pdf.page_break_trigger - pdf.get_y()
            if remaining < 30:
                pdf.add_page()
            write_paragraph(text, size=sizes.get(level, 12), style="B")
            continue

        # Blockquote
        if line.lstrip().startswith(">"):
            q = line.lstrip()[1:].lstrip()
            q = strip_inline_markdown(q)
            write_paragraph(q, indent_mm=6.0, size=11, style="I")
            continue

        # Bullets
        m = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if m:
            indent = len(m.group(1))
            text = strip_inline_markdown(m.group(2)).strip()
            bullet = "•"
            write_paragraph(f"{bullet} {text}", indent_mm=indent * 1.5, size=12)
            continue

        # Numbered list
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m:
            indent = len(m.group(1))
            n = m.group(2)
            text = strip_inline_markdown(m.group(3)).strip()
            write_paragraph(f"{n}. {text}", indent_mm=indent * 1.5, size=12)
            continue

        # Normal paragraph
        write_paragraph(strip_inline_markdown(line))

    if table_buffer:
        if not _render_table(pdf, table_buffer, main_family, available_main_styles):
            for tl in table_buffer:
                write_paragraph(strip_inline_markdown(tl))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF (minimal, Unicode via Windows fonts).")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    parser.add_argument("--title", type=str, default=None, help="PDF title metadata")
    parser.add_argument("--author", type=str, default=None, help="PDF author metadata")
    parser.add_argument("--footer-logo", type=Path, default=None, help="Logo image for page footer")
    args = parser.parse_args(argv)

    md_text = args.input.read_text(encoding="utf-8")
    render_markdown_to_pdf(
        md_text,
        args.output,
        title=args.title,
        author=args.author,
        base_dir=args.input.parent,
        footer_logo=args.footer_logo,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

