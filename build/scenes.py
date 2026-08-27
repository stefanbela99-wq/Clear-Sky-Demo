#!/usr/bin/env python3
"""
Generate bespoke editorial/scene photographs (landscape) for article cards,
service panels and case studies, via Google Imagen 4. Saves to assets/.

Run:  GEMINI_API_KEY=... python3 build/scenes.py            (all)
      GEMINI_API_KEY=... python3 build/scenes.py scene-about case-3   (subset)
"""
import os, sys, json, base64, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
MODEL = os.environ.get("IMAGEN_MODEL", "imagen-4.0-generate-001")
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predict"

NEG = ("One single photograph, photorealistic, candid editorial style, natural soft "
       "lighting, shallow depth of field, muted calm colour palette. "
       "Absolutely no text, no numbers, no letters, no words, no watermark, no logo, "
       "no caption, no signage, no border, not a collage, not a grid, not split panels, "
       "not multiple images.")

# name -> scene description (landscape 16:9)
SCENES = {
    # ---- insight article images (one per article) ----
    "scene-insight-three-questions": "A person sitting thoughtfully at a wooden desk beside a large window, considering a decision, chin resting on hand, warm daylight",
    "scene-insight-second-opinion": "Two colleagues seated at a desk reviewing a printed report together, one pointing to a detail on the page, calm modern office, soft natural light",
    "scene-insight-decision-fatigue": "A tired professional resting their forehead on their hand at a desk in the late afternoon, soft moody light, papers around",
    "scene-insight-reversible-decisions": "A person pausing thoughtfully in a bright modern office corridor that branches in two directions, contemplative",
    "scene-insight-free-advice": "A person carefully reading the fine print of a contract at a desk, focused and a little wary, soft light",
    "scene-insight-good-second-opinion": "Close-up of hands annotating a printed business proposal with a pen on a wooden desk, considered and precise",
    "scene-insight-planning-backwards": "A person mapping out a plan with sticky notes and arrows on a glass wall in a bright office, organised",
    "scene-insight-money-decisions": "A couple talking seriously at a kitchen table with paperwork between them, warm domestic evening light",
    "scene-insight-life-transitions": "A person gazing out of a large window in quiet contemplation during a moment of change, soft hopeful light",
    # ---- service / section 'media' panels ----
    "scene-about": "Two warm professional advisors in conversation with a client across a table in a calm modern Australian office, candid and trusting",
    "scene-approach": "An unhurried advisory meeting in progress, an advisor calmly explaining something to a client, daylight office, genuine",
    "scene-careers": "A diverse, friendly team of professionals collaborating around a table in a bright modern Australian office, candid",
    "scene-decision-clarity": "An advisor and a client in a focused one-on-one conversation across a small table in a calm modern office, attentive and clear, soft daylight",
    "scene-planning-strategy": "An advisor and a client reviewing a printed plan with milestones laid out on a desk, collaborative",
    "scene-second-opinion": "An advisor independently and carefully reviewing a printed proposal for a client, reading glasses on, considered",
    "scene-ongoing-advisory": "A relaxed, friendly ongoing advisory chat between an advisor and a long-term client in a warm office, trust and ease",
    # ---- case studies (themed to each story) ----
    "case-featured": "A professional woman at her desk thoughtfully weighing two printed job offer letters, one in each consideration, contemplative",
    "case-1": "Close-up of hands reviewing a detailed building refurbishment proposal and contract on a desk, scrutinising",
    "case-2": "A couple in their forties planning their future together at a table with notes and a laptop, optimistic",
    "case-3": "A woman in calm conversation with her trusted advisor across a table in a quiet office",
    "case-4": "An older couple discussing thoughtfully in the living room of their family home, warm light, a little nostalgic",
    "case-5": "A man at a cafe table sceptically reviewing a glossy franchise brochure, weighing it up",
    "case-6": "A woman planning a year-long career break with a calendar, notebook and coffee, hopeful and focused",
    "case-7": "A couple in their thirties considering a big interstate move, cardboard moving boxes and a map spread on a table in a sunlit home, contemplative",
    "case-8": "A woman receiving calm guidance about paperwork from an advisor across a table, reassured",
    "case-9": "A man at a desk seriously reviewing a printed document, pen in hand, considering his options, soft natural office light",
}


def generate(name, prompt):
    body = json.dumps({
        "instances": [{"prompt": f"{prompt}. {NEG}"}],
        "parameters": {"sampleCount": 1, "aspectRatio": "16:9", "personGeneration": "allow_adult"},
    }).encode()
    req = urllib.request.Request(f"{ENDPOINT}?key={KEY}", data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    preds = data.get("predictions") or []
    if not preds or "bytesBase64Encoded" not in preds[0]:
        raise RuntimeError(f"no image: {json.dumps(data)[:200]}")
    raw = base64.b64decode(preds[0]["bytesBase64Encoded"])
    ext = "png" if "png" in preds[0].get("mimeType", "image/png") else "jpg"
    out = os.path.join(ASSETS, f"{name}.{ext}")
    with open(out, "wb") as f:
        f.write(raw)
    return out


def main():
    if not KEY:
        sys.exit("Set GEMINI_API_KEY first.")
    only = set(sys.argv[1:])
    items = [(n, p) for n, p in SCENES.items() if not only or n in only]
    ok = 0
    for name, prompt in items:
        for attempt in range(1, 4):
            try:
                out = generate(name, prompt)
                ok += 1
                print(f"  ✓ {name} -> {os.path.relpath(out, ROOT)}")
                break
            except Exception as e:
                msg = e.read()[:140].decode(errors="replace") if isinstance(e, urllib.error.HTTPError) else str(e)
                print(f"  … {name} attempt {attempt}: {msg[:110]}")
                time.sleep(3)
        time.sleep(1.0)
    print(f"\nDone: {ok}/{len(items)} scene images written to assets/.")


if __name__ == "__main__":
    main()
