#!/usr/bin/env python3
"""
Optimise the photographic assets: downscale to sensible dimensions and emit
WebP, which is ~10-20x smaller than the oversized source PNGs for the sizes
these images actually display at.

Headshots and scene/case photos are converted to .webp and the heavy source
PNG/JPG is removed. The OG social cards (og-*) and the brand logo are left as
PNG on purpose - social scrapers and structured-data consumers want raster
PNG/JPG, not WebP.

Run:  python3 build/optimize.py
"""
import os
import glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# prefix -> max dimension (longest side, px). Tuned to actual display sizes (x2 for retina).
TARGETS = (
    (("exec-", "board-", "reg-", "adv-", "founder-"), 600),   # headshots
    (("scene-", "case-"), 1000),                                # editorial / case photos
)
KEEP_AS_IS = ("og-", "logo")          # social cards + brand logo stay PNG
QUALITY = 80


def target_for(name):
    for prefixes, dim in TARGETS:
        if name.startswith(prefixes):
            return dim
    return None


def main():
    saved = 0
    before = after = 0
    for src in sorted(glob.glob(os.path.join(ASSETS, "*.png")) +
                      glob.glob(os.path.join(ASSETS, "*.jpg"))):
        name = os.path.splitext(os.path.basename(src))[0]
        if name.startswith(KEEP_AS_IS):
            continue
        dim = target_for(name)
        if dim is None:
            continue
        out = os.path.join(ASSETS, f"{name}.webp")
        with Image.open(src) as im:
            im = im.convert("RGB")
            w, h = im.size
            scale = min(1.0, dim / max(w, h))
            if scale < 1.0:
                im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
            im.save(out, "WEBP", quality=QUALITY, method=6)
        src_sz = os.path.getsize(src)
        out_sz = os.path.getsize(out)
        before += src_sz
        after += out_sz
        os.remove(src)            # drop the heavy source; .webp is what we serve
        saved += 1
        print(f"  {name}: {src_sz//1024}KB -> {out_sz//1024}KB webp")
    print(f"\n{saved} images optimised. {before/1e6:.1f}MB -> {after/1e6:.1f}MB "
          f"({100*(1-after/before):.0f}% smaller).")


if __name__ == "__main__":
    main()
