#!/usr/bin/env python3
"""
Restyle an uploaded photo into a clean corporate headshot that matches the rest
of the team, using Gemini's image-editing model. Keeps the person's identity,
puts/keeps them in a business suit, and swaps the background for a neutral studio.

Usage:  GEMINI_API_KEY=... python3 build/suit.py "assets/src.jpg=adv-1" ...
        (each arg is  <source path>=<output basename>, output -> assets/<base>.webp)
"""
import os, sys, json, base64, subprocess, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
MODEL = os.environ.get("IMAGE_MODEL", "gemini-2.5-flash-image")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

PROMPT = (
    "Restyle this into a professional corporate headshot for a company leadership page, "
    "matching a clean studio style. Keep the man's face, identity, bone structure, eyes, "
    "skin and hairline exactly the same - do not change who he is. Keep him in a smart "
    "dark business suit with a collared shirt (neaten it; a plain look is fine). "
    "Replace the entire background with a clean, softly-lit neutral studio backdrop in cool "
    "grey-blue - remove any office, screens, other people, text and logos. Tight head-and-"
    "shoulders framing, looking at camera, calm confident professional expression. "
    "Remove any name badge, name tag, lapel pin or bow tie from the jacket entirely. "
    "Photorealistic, natural studio lighting. No text, no numbers, no logos, no watermark."
)


def edit(src, out_png):
    b64 = base64.b64encode(open(src, "rb").read()).decode()
    body = {"contents": [{"parts": [{"text": PROMPT},
            {"inline_data": {"mime_type": "image/jpeg", "data": b64}}]}],
            "generationConfig": {"responseModalities": ["IMAGE"]}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        json.dump(body, tf); req = tf.name
    resp = req + ".resp"
    try:
        for attempt in range(1, 4):
            subprocess.run(["curl", "-s", "-X", "POST", URL, "-H", "Content-Type: application/json",
                            "--data-binary", "@" + req, "-o", resp], check=True)
            d = json.load(open(resp))
            for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                img = p.get("inline_data") or p.get("inlineData")
                if img and img.get("data"):
                    open(out_png, "wb").write(base64.b64decode(img["data"]))
                    return True
            print(f"    attempt {attempt}: no image ({json.dumps(d)[:120]})")
    finally:
        for f in (req, resp):
            if os.path.exists(f): os.remove(f)
    return False


def main():
    if not KEY: sys.exit("Set GEMINI_API_KEY")
    for arg in sys.argv[1:]:
        src, base = arg.split("=")
        out_png = os.path.join(ASSETS, base + "-suit.png")
        print(f"{base}: editing {os.path.basename(src)} ...")
        if not edit(src, out_png):
            print(f"  FAILED {base}"); continue
        im = Image.open(out_png).convert("RGB")
        w, h = im.size; s = 600 / max(w, h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        webp = os.path.join(ASSETS, base + ".webp")
        im.save(webp, "WEBP", quality=82, method=6)
        print(f"  -> {base}.webp ({os.path.getsize(webp)//1024}KB, {im.size})")


if __name__ == "__main__":
    main()
