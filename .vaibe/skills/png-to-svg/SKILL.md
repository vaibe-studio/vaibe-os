---
name: png-to-svg
description: Convert raster images (PNG/JPG) to pixel-accurate SVG using local tools. Use when asked to "embed", "convert" or "vectorize" an image into SVG or HTML — never manually redraw with <path> elements. Triggers: png to svg, jpg to svg, векторизация, конвертация изображения, вставить картинку в svg, embed image, pixel-perfect svg, точная копия изображения.
license: MIT
---

# Purpose

Convert raster images to SVG without information loss. The goal is **exact reproduction**, not approximation.

**Critical rule:** Never manually redraw a raster image with hand-written `<path>`, `<circle>`, `<rect>` elements. This always produces "похожее, но не точное" (similar but not exact). Use conversion tools instead.

# When to use

- User shows a PNG/JPG and wants it in HTML/SVG
- User says "встроить картинку", "конвертировать в SVG", "сделать как на изображении"
- User compares result to reference image and finds it "not the same"
- Any infographic, diagram, illustration from a raster file needs to be placed on a web page

# Tools available (pre-installed)

`png_to_svg` is a `uv` project; below `$P` = `.vaibe/skills/png-to-svg/scripts/png_to_svg`.

| Tool | Type | Best for | Command |
|---|---|---|---|
| `vtracer` (Python) | True vector trace | Color illustrations, infographics | `uv run --project $P --extra trace $P/main.py trace` |
| `inkscape` | Base64 embed | Any image, pixel-perfect, preserves raster | `uv run --project $P $P/main.py embed` |
| `potrace` | Mono trace | Logos, icons, line art (single color) | via Inkscape or direct |

# Decision flowchart

```
User wants image in HTML/SVG
        │
        ├─ "Pixel-perfect, exact copy" → MODE: embed
        │    Result: <svg><image href="data:image/png;base64,..."/></svg>
        │    Size: ~1.3× the PNG. Scales 1:1. Browser renders raster.
        │
        ├─ "Scalable vector, zoom without blur" → MODE: trace
        │    Result: True SVG paths via vtracer. ~2× PNG size. Infinitely scalable.
        │    Best for: illustrations, infographics, flat-style images
        │
        └─ "Logo / icon / line art (1-2 colors)" → MODE: mono
             Result: potrace monochrome SVG. Smallest size.
```

# Procedure

## Step 1 — Identify the source file

Confirm the path to the PNG/JPG. Accept paths from:
- `Проекты/*/Задачи/*/` (task attachments)
- IDE image-paste location (e.g. Cursor `~/.cursor/projects/*/assets/`)
- Any absolute path the user provides

## Step 2 — Choose mode

Ask or infer from context:
- **embed** — when "pixel-perfect" or "exact" is required, or image has complex gradients/photos
- **trace** — when scalable SVG is needed, or image is illustration/diagram style
- **mono** — when image is a simple logo or black-and-white icon

## Step 3 — Run conversion

```bash
P=.vaibe/skills/png-to-svg/scripts/png_to_svg

# EMBED MODE (pixel-perfect, raster in SVG wrapper)
uv run --project $P $P/main.py embed /path/to/image.png /path/to/output.svg

# TRACE MODE (true vector via vtracer — needs the 'trace' extra)
uv run --project $P --extra trace $P/main.py trace /path/to/image.png /path/to/output.svg

# MONO MODE (potrace via Inkscape)
uv run --project $P $P/main.py mono /path/to/image.png /path/to/output.svg
```

## Step 4 — Integrate into HTML

For embedding in a web page, prefer the **inline SVG** or **img tag** approach:

```html
<!-- Option A: direct image (simplest, always pixel-perfect) -->
<img src="path/to/image.png" alt="description" style="width:100%;height:auto;">

<!-- Option B: inline SVG wrapper with base64 (SVG context required) -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" style="width:100%">
  <image href="data:image/png;base64,BASE64_HERE" width="1024" height="1024"/>
</svg>

<!-- Option C: external SVG file (from trace mode) -->
<img src="output.svg" alt="description" style="width:100%">
<!-- or inline: -->
<object data="output.svg" type="image/svg+xml" style="width:100%"></object>
```

## Step 5 — Verify

Open in browser. Compare side-by-side with the original reference image.

# Anti-patterns (NEVER do this)

- ❌ Writing SVG `<path d="M...">` manually to "redraw" what's in a PNG
- ❌ Using `<rect>`, `<circle>`, `<text>` to approximate an infographic from a screenshot
- ❌ Saying "это похожее, но точнее нельзя" without first trying vtracer or embed
- ❌ Converting a complex illustration to SVG by describing it to an LLM

These approaches always produce "similar but not pixel-accurate" results.

# Quality bar

- [ ] Conversion done by a tool (vtracer / inkscape / potrace), not by hand
- [ ] Result compared to reference in browser before declaring done
- [ ] Mode (embed/trace/mono) explicitly chosen and justified
- [ ] If embed mode: file size is acceptable for context (web page weight)
- [ ] Output SVG opens and renders correctly without errors

# Known limitations

| Issue | Cause | Fix |
|---|---|---|
| vtracer SVG is 2-3× the PNG size | Many path nodes for complex images | Use embed mode instead, or compress with SVGO |
| vtracer loses thin text < 10px | Speckle filter removes small details | Lower `filter_speckle` to 1-2 |
| embed SVG doesn't scale like true vector | It IS still a raster inside | Expected; for infinite scaling use trace mode |
| potrace loses colors | Mono-only tool | Use vtracer for color images |

# Related tools

- `.vaibe/skills/png-to-svg/scripts/png_to_svg/` — CLI wrapper (embed / trace / mono modes)
- `.vaibe/scripts/markdown_to_pdf` — PDF generation
- `vtracer` docs: https://github.com/visioncortex/vtracer
