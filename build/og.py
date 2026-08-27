#!/usr/bin/env python3
"""
Render assets/og-image.svg to a real raster assets/og-image.png (1200x630).

Social platforms (Facebook, LinkedIn, Slack, iMessage, X) generally do NOT
render SVG og:image files, so a raster is required for link previews to work.
Uses the pre-installed Chromium binary headlessly - no extra dependencies.

Run:  python3 build/og.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def render(svg_name="og-image.svg", png_name="og-image.png", w=1200, h=630):
    svg_path = os.path.join(ASSETS, svg_name)
    out_path = os.path.join(ASSETS, png_name)
    with open(svg_path) as f:
        svg = f.read()
    html = (
        '<!doctype html><html><head><meta charset="utf-8"><style>'
        '*{margin:0;padding:0}html,body{width:%dpx;height:%dpx;overflow:hidden}'
        'svg{display:block;width:%dpx;height:%dpx}</style></head><body>%s</body></html>'
        % (w, h, w, h, svg)
    )
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ASSETS) as tf:
        tf.write(html)
        tmp = tf.name
    try:
        subprocess.run([
            CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={w},{h}", f"--screenshot={out_path}",
            "file://" + tmp,
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.remove(tmp)
    size = os.path.getsize(out_path)
    print(f"Rendered {png_name} ({size:,} bytes, {w}x{h}).")


if __name__ == "__main__":
    import glob
    for svg in sorted(glob.glob(os.path.join(ASSETS, "og-*.svg"))):
        base = os.path.splitext(os.path.basename(svg))[0]
        render(base + ".svg", base + ".png", 1200, 630)
    render("logo.svg", "logo.png", 512, 512)
    render("logo.svg", "logo-192.png", 192, 192)
