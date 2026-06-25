"""Remove baked-in checker background from Nano-Banana icon PNGs."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage


def clean(src: Path, dst: Path) -> None:
    img = np.array(Image.open(src).convert("RGB"))
    r, g, b = img[..., 0].astype(int), img[..., 1].astype(int), img[..., 2].astype(int)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn

    # Strong foreground = clearly darker than any checker square OR colored (saturated).
    fg_core = (mn < 150) | (sat > 30)
    # Drop pixel-level noise.
    fg_core = ndimage.binary_opening(fg_core, iterations=1)
    # Keep only large connected components (filters out residual checker artifacts).
    labels, n = ndimage.label(fg_core)
    if n > 0:
        sizes = ndimage.sum(fg_core, labels, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, dtype=bool)
        keep[1:] = sizes >= 200
        fg_core = keep[labels]
    # Dilate to recover anti-aliasing halo around strokes.
    fg = ndimage.binary_dilation(fg_core, iterations=5)
    # Second connected-component pass on the dilated mask to drop any stragglers.
    labels2, n2 = ndimage.label(fg)
    if n2 > 0:
        sizes2 = ndimage.sum(fg, labels2, index=np.arange(1, n2 + 1))
        keep2 = np.zeros(n2 + 1, dtype=bool)
        keep2[1:] = sizes2 >= 400
        fg = keep2[labels2]

    # Inside the dilated halo, keep only pixels darker than any checker square —
    # this drops checker remnants that ended up next to real strokes.
    halo_bg = fg & ~fg_core & (mn >= 185) & (sat < 20)
    alpha = np.clip((255 - mn) * (255 / 95), 0, 255).astype(np.uint8)
    alpha[~fg] = 0
    alpha[halo_bg] = 0

    out = np.dstack([img, alpha]).astype(np.uint8)
    Image.fromarray(out, mode="RGBA").save(dst, optimize=True)
    print(f"{src.name} -> {dst.name}")


if __name__ == "__main__":
    pairs = list(zip(sys.argv[1::2], sys.argv[2::2]))
    for s, d in pairs:
        clean(Path(s), Path(d))
