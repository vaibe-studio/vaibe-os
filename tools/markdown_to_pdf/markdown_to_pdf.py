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
    pass


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


def render_markdown_to_pdf(
    md_text: str,
    output_path: Path,
    *,
    title: str | None = None,
    author: str | None = None,
    main_font: FontFiles | None = None,
    mono_font_path: Path | None = None,
) -> None:
    if main_font is None:
        main_font = detect_windows_font_family()
    if mono_font_path is None:
        mono_font_path = detect_windows_mono_font()

    pdf = PDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=15)
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

    def set_main(size: int, style: str = "") -> None:
        pdf.set_font(main_family, style=_safe_style(style, available_main_styles), size=size)

    def write_paragraph(text: str, *, indent_mm: float = 0.0, size: int = 12, style: str = "") -> None:
        set_main(size, style)
        x0 = pdf.get_x()
        if indent_mm:
            pdf.set_x(x0 + indent_mm)
        line_h = max(5, int(round(size * 0.45)))
        pdf.multi_cell(0, line_h, text)
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

    lines = md_text.splitlines()
    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip() == "<!-- pagebreak -->":
            pdf.add_page()
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF (minimal, Unicode via Windows fonts).")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    parser.add_argument("--title", type=str, default=None, help="PDF title metadata")
    parser.add_argument("--author", type=str, default=None, help="PDF author metadata")
    args = parser.parse_args(argv)

    md_text = args.input.read_text(encoding="utf-8")
    render_markdown_to_pdf(md_text, args.output, title=args.title, author=args.author)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

