#!/usr/bin/env python3
"""
Generate real photographic headshots for the Clear Sky Consulting team using
Google's Imagen (via the Gemini API), and save them into assets/.

Why this works in the sandbox: the gateway already reaches
generativelanguage.googleapis.com, so no network-policy change is needed -
only a real API key.

Setup:
  1. Get a key at https://aistudio.google.com/apikey (billing enabled - Imagen is paid).
  2. Export it (or add it to the environment):  export GEMINI_API_KEY=...
  3. Run:  python3 build/photos.py
  4. Then re-run the site generator; portraits will switch to the photos
     (generate.py prefers assets/<img>.jpg over the .svg when present).

Prompts are tuned per person to the cast's inferred gender / age / heritage,
so the team reads as a believable, diverse leadership page.
"""
import os, sys, json, base64, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
MODEL = os.environ.get("IMAGEN_MODEL", "imagen-4.0-generate-001")
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict"

# img, gender, heritage, age, glasses, beard, extra
PEOPLE = [
    ("exec-1", "man",   "Anglo-Australian",       52, False, False, ""),
    ("exec-2", "woman", "Chinese",                48, False, False, ""),
    ("exec-3", "man",   "Scottish",               50, False, False, ""),
    ("exec-4", "woman", "South Indian",           45, False, False, ""),
    ("exec-5", "woman", "Scandinavian",           43, False, False, "blonde hair"),
    ("exec-6", "man",   "Italian",                47, False, True,  ""),
    ("exec-7", "woman", "Middle Eastern",         44, False, False, ""),
    ("exec-8", "man",   "Japanese",               46, True,  False, ""),
    ("board-1", "woman","Dutch",                  61, False, False, "silver hair"),
    ("board-2", "woman","Chinese",                58, False, False, "greying hair"),
    ("board-3", "man",  "Irish",                  63, True,  False, "balding, grey hair"),
    ("board-4", "man",  "Turkish",                55, False, True,  "greying"),
    ("board-5", "woman","Irish",                  57, False, False, "grey hair"),
    ("reg-1",  "man",   "Irish",                  41, False, False, "auburn hair"),
    ("reg-2",  "woman", "Anglo-Australian",       44, False, False, ""),
    ("reg-3",  "man",   "Italian",                46, False, False, ""),
    ("reg-4",  "woman", "Ashkenazi Jewish",       42, False, False, "dark curly hair"),
    ("reg-5",  "man",   "Vietnamese",             39, False, False, ""),
    ("adv-1",  "man",   "Polish",                 49, False, False, "greying"),
    ("adv-2",  "man",   "Hispanic",               38, False, True,  ""),
    ("adv-3",  "man",   "Welsh",                  45, False, False, ""),
    ("adv-4",  "man",   "Eastern European",       36, False, True,  ""),
    ("adv-5",  "man",   "Eastern European",       52, True,  False, "greying"),
    ("adv-6",  "man",   "Dutch",                  57, True,  False, "bald, grey"),
]


def prompt_for(gender, heritage, age, glasses, beard, extra):
    bits = [f"a {age}-year-old {heritage} {gender}"]
    if extra:
        bits.append(extra)
    if glasses:
        bits.append("wearing glasses")
    if beard:
        bits.append("with a short, well-groomed beard")
    desc = ", ".join(bits)
    return (
        f"A hyperrealistic professional corporate headshot photograph of {desc}. "
        f"Tight head-and-shoulders crop of a single {gender}, the face clearly visible "
        "and filling most of the frame, looking directly into the camera. "
        "Wearing smart business attire, plain light grey studio background, "
        "soft even studio lighting, warm confident natural expression, "
        "natural realistic skin texture, shot on a DSLR with an 85mm lens, sharp focus. "
        "One real person, one face, one single uncropped photograph. "
        "Not full body, not a full-length shot, not from behind, not a fashion photo. "
        "Absolutely no text, no numbers, no letters, no words, no watermark, no logo, "
        "no caption, no border, no frame lines, not a collage, not a grid, "
        "not a contact sheet, not multiple images, not split panels."
    )


def generate(p):
    img, gender, heritage, age, glasses, beard, extra = p
    body = json.dumps({
        "instances": [{"prompt": prompt_for(gender, heritage, age, glasses, beard, extra)}],
        "parameters": {"sampleCount": 1, "aspectRatio": "3:4", "personGeneration": "allow_adult"},
    }).encode()
    req = urllib.request.Request(
        f"{ENDPOINT}?key={KEY}", data=body,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    preds = data.get("predictions") or []
    if not preds or "bytesBase64Encoded" not in preds[0]:
        raise RuntimeError(f"no image in response: {json.dumps(data)[:300]}")
    raw = base64.b64decode(preds[0]["bytesBase64Encoded"])
    ext = "png" if "png" in preds[0].get("mimeType", "image/png") else "jpg"
    out = os.path.join(ASSETS, f"{img}.{ext}")
    with open(out, "wb") as f:
        f.write(raw)
    return out


def main():
    if not KEY:
        sys.exit("Set GEMINI_API_KEY (or GOOGLE_API_KEY) first. See the header of this file.")
    # Optional: pass specific ids to regenerate only those, e.g.
    #   python3 build/photos.py exec-4 adv-5
    only = set(sys.argv[1:])
    people = [p for p in PEOPLE if not only or p[0] in only]
    ok = 0
    for p in people:
        name = p[0]
        done = False
        for attempt in range(1, 4):
            try:
                out = generate(p)
                ok += 1
                done = True
                print(f"  ✓ {name} -> {os.path.relpath(out, ROOT)}")
                break
            except Exception as e:
                msg = e.read()[:160].decode(errors="replace") if isinstance(e, urllib.error.HTTPError) else str(e)
                print(f"  … {name} attempt {attempt}: {msg[:120]}")
                time.sleep(3)
        if not done:
            print(f"  ✗ {name}: failed after retries")
        time.sleep(1.0)
    print(f"\nDone: {ok}/{len(people)} headshots written to assets/.")
    if ok:
        print("Next: re-run `python3 build/generate.py` to switch the site to the photos.")


if __name__ == "__main__":
    main()
