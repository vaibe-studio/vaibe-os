#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Pillow>=10.0.0",
#   "vtracer>=0.6.0",
# ]
# ///
"""
png_to_svg — pixel-accurate raster → SVG converter

Modes:
  embed  <in> <out>  Wraps PNG/JPG as base64 inside SVG. Pixel-perfect.
  trace  <in> <out>  Full-color vector trace via vtracer. Scalable SVG.
  mono   <in> <out>  Monochrome trace via potrace/Inkscape. Best for logos.

Examples:
  uv run .vaibe/skills/png-to-svg/scripts/png_to_svg.py embed image.png output.svg
  uv run .vaibe/skills/png-to-svg/scripts/png_to_svg.py trace infographic.png infographic.svg
  uv run .vaibe/skills/png-to-svg/scripts/png_to_svg.py mono logo.png logo.svg
"""

from __future__ import annotations

import sys
import os
import base64
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple


def _image_dimensions(path: str) -> Tuple[int, int]:
    """Return (width, height) using Pillow or fallback to identify/file."""
    try:
        from PIL import Image
        with Image.open(path) as img:
            return img.size  # (width, height)
    except ImportError:
        pass
    # Fallback: parse PNG header directly
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] == b"\x89PNG\r\n\x1a\n":
        import struct
        w, h = struct.unpack(">II", header[16:24])
        return w, h
    return 800, 600  # safe default


def mode_embed(input_path: str, output_path: str) -> None:
    """
    Embed the raster image as base64 inside an SVG wrapper.
    Pixel-perfect: the browser renders the original raster.
    """
    inp = Path(input_path)
    if not inp.exists():
        sys.exit(f"[png_to_svg] Input file not found: {input_path}")

    mime = "image/png" if inp.suffix.lower() == ".png" else "image/jpeg"
    with open(inp, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    w, h = _image_dimensions(str(inp))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
        f'  <image href="data:{mime};base64,{b64}" '
        f'x="0" y="0" width="{w}" height="{h}" '
        f'image-rendering="crisp-edges"/>\n'
        f'</svg>\n'
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    size_kb = os.path.getsize(output_path) // 1024
    print(f"[embed] Done → {output_path}  ({size_kb} KB, {w}×{h})")


def mode_trace(input_path: str, output_path: str) -> None:
    """
    Full-color vector trace using vtracer.
    Produces real SVG <path> elements — infinitely scalable.
    """
    try:
        import vtracer
    except ImportError:
        sys.exit(
            "[png_to_svg] vtracer not installed. Run: pip3 install vtracer"
        )

    inp = Path(input_path)
    if not inp.exists():
        sys.exit(f"[png_to_svg] Input file not found: {input_path}")

    # If JPG, convert to PNG first (vtracer requires PNG)
    work_path = str(inp)
    if inp.suffix.lower() in (".jpg", ".jpeg"):
        try:
            from PIL import Image
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            Image.open(inp).save(tmp.name)
            work_path = tmp.name
            print(f"[trace] Converted JPG → temp PNG: {tmp.name}")
        except ImportError:
            sys.exit(
                "[png_to_svg] Pillow required for JPG input. "
                "Run: pip3 install Pillow"
            )

    vtracer.convert_image_to_svg_py(
        work_path,
        output_path,
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,       # remove <4px specks; preserves small text
        color_precision=6,      # good color detail without too many layers
        layer_difference=16,    # merge near-identical color layers
        corner_threshold=60,
        length_threshold=4.0,
        splice_threshold=45,
        path_precision=5,       # fewer decimal places → smaller file
    )

    if work_path != str(inp):
        os.unlink(work_path)

    size_kb = os.path.getsize(output_path) // 1024
    print(f"[trace] Done → {output_path}  ({size_kb} KB)")
    print("[trace] Result: true scalable vector SVG (no embedded raster)")


def mode_mono(input_path: str, output_path: str) -> None:
    """
    Monochrome trace via Inkscape (which uses potrace internally).
    Best for logos, icons, line art with 1-2 colors.
    """
    inkscape = "inkscape"
    # Check inkscape availability
    result = subprocess.run(
        ["which", inkscape], capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit("[png_to_svg] inkscape not found. Install: sudo apt install inkscape")

    inp = Path(input_path)
    if not inp.exists():
        sys.exit(f"[png_to_svg] Input file not found: {input_path}")

    # Inkscape trace action: select all → trace bitmap (potrace, brightness)
    actions = (
        "file-open:{inp};"
        "select-all;"
        "org.inkscape.effect.trace;"
        "export-filename:{out};"
        "export-type:svg;"
        "export-plain-svg;"
        "export-do"
    ).format(inp=str(inp.resolve()), out=str(Path(output_path).resolve()))

    proc = subprocess.run(
        [inkscape, "--actions", actions],
        capture_output=True,
        text=True,
    )

    if not Path(output_path).exists():
        # Fallback: embed if trace failed
        print("[mono] Inkscape trace failed, falling back to embed mode")
        print(f"[mono] stderr: {proc.stderr[:400]}")
        mode_embed(input_path, output_path)
        return

    size_kb = os.path.getsize(output_path) // 1024
    print(f"[mono] Done → {output_path}  ({size_kb} KB)")


MODES = {
    "embed": mode_embed,
    "trace": mode_trace,
    "mono": mode_mono,
}


def main() -> None:
    args = sys.argv[1:]
    if len(args) != 3 or args[0] not in MODES:
        print(__doc__)
        print("Available modes:", ", ".join(MODES))
        sys.exit(1)

    mode, input_path, output_path = args
    MODES[mode](input_path, output_path)


if __name__ == "__main__":
    main()
