#!/usr/bin/env python3
"""
Static site generator for the Clear Sky Consulting demo website.

Produces every HTML page from shared chrome (nav + mega-footer + utility bar)
plus generated placeholder portraits and decorative thumbnails, so the whole
site stays consistent. Run from anywhere:  python3 build/generate.py
All output is written to the repository root.
"""
import os
import re
import json
import html
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# ----------------------------------------------------------------------------
# Generated placeholder portraits (clearly illustrated, swap for real headshots)
# ----------------------------------------------------------------------------
PALETTES = [
    # bg1, bg2, skin, hair, coat, accent
    ("#EAF1F7", "#DCEBF6", "#F0CBA0", "#5A4632", "#134063", "#2F6F9F"),
    ("#F3E9D8", "#EAF1F7", "#EAB98E", "#3A2E22", "#2F6F9F", "#E2A24A"),
    ("#E7F0F8", "#D7E7F3", "#C68642", "#1C140E", "#1B4A6E", "#7FB2D6"),
    ("#F5EEE2", "#E9EFF6", "#F2D2B6", "#6B4A2A", "#2A5E86", "#E2A24A"),
    ("#E9F2F8", "#DBE9F4", "#8D5524", "#241A12", "#13405F", "#3A7CAD"),
    ("#F1E8DA", "#E6EFF7", "#FAD9BC", "#8B6A3E", "#274C6B", "#9FC3DE"),
    ("#EAF1F7", "#E0D6C4", "#E5B98C", "#2B2017", "#1E5277", "#E2A24A"),
    ("#E4EEF6", "#D2E3F0", "#D89B6A", "#0F0B08", "#173f5f", "#5FA0C8"),
]
HAIR = ("short", "long", "bald", "short", "long", "short", "long", "short")


def portrait(path, p, hair):
    bg1, bg2, skin, hair_c, coat, accent = p
    if hair == "bald":
        hair_shape = ""
    elif hair == "long":
        hair_shape = (
            f'<path d="M115 150c0-62 38-106 85-106s85 44 85 106c8 42 6 96-2 126'
            f'-10-22-12-74-12-74s-28 18-71 18-71-18-71-18 -2 52-12 74c-8-30-10-84-2-126z" '
            f'fill="{hair_c}"/>'
        )
    else:  # short
        hair_shape = (
            f'<path d="M120 122a80 80 0 0 1 160 0c0-11-6-21-6-21 5-23-13-46-74-46'
            f's-76 25-74 48c0 0-6 8-6 19z" fill="{hair_c}"/>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 460" role="img" aria-label="Generated portrait placeholder">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="coat" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{coat}"/><stop offset="1" stop-color="{coat}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="460" fill="url(#bg)"/>
  <circle cx="200" cy="130" r="80" fill="{skin}"/>
  {hair_shape}
  <path d="M152 188c-5 13-9 27-9 40 6 6 21 14 57 14s51-8 57-14c0-13-4-27-9-40-11 15-29 24-48 24s-37-9-48-24z" fill="{skin}" opacity=".88"/>
  <path d="M64 460c0-84 60-150 136-150s136 66 136 150z" fill="url(#coat)"/>
  <path d="M200 312c-19 0-36 4-52 11l52 60 52-60c-16-7-33-11-52-11z" fill="#F7FAFD"/>
  <path d="M200 323l-18 13 11 17 7-9 7 9 11-17z" fill="{accent}"/>
</svg>
'''
    with open(os.path.join(ASSETS, path), "w") as f:
        f.write(svg)


# ----------------------------------------------------------------------------
# Tailored illustrated corporate headshots (per-person: skin/hair/style/etc.)
# ----------------------------------------------------------------------------
SK = {"light": "#F0C9A0", "light2": "#EAD0AE", "olive": "#D7A268",
      "medium": "#C68642", "brown": "#A86B3D", "asian": "#ECC79A"}
HR = {"dark": "#241A12", "brown": "#5A4632", "blonde": "#C9A45A", "ginger": "#9A5A32",
      "grey": "#A7A199", "salt": "#6F665C", "darkgrey": "#4A443C"}
CO = {"c1": "#134063", "c2": "#1B4A6E", "c3": "#2A5E86", "c4": "#274C6B", "c5": "#1E5277"}


def portrait2(path, skin, hair, style, coat, accent="#E2A24A", beard=False, glasses=False):
    sk, hr, co = SK[skin], HR[hair], CO[coat]
    back = ""
    if style == "long":
        back = f'<path d="M116 150c-12 64-8 158 6 210h156c14-52 18-146 6-210-8-72-46-108-90-108s-78 36-84 108z" fill="{hr}"/>'
    elif style == "bun":
        back = f'<circle cx="200" cy="54" r="27" fill="{hr}"/>'
    head = (f'<rect x="180" y="196" width="40" height="126" rx="18" fill="{sk}"/>'
            f'<circle cx="120" cy="150" r="14" fill="{sk}"/><circle cx="280" cy="150" r="14" fill="{sk}"/>'
            f'<circle cx="200" cy="140" r="80" fill="{sk}"/>')
    if style == "short":
        front = f'<path d="M120 142c-4-66 36-102 80-102s84 36 80 102c-2-17-9-27-9-27 5-15-15-41-71-41s-76 26-71 41c0 0-7 10-9 27z" fill="{hr}"/>'
    elif style == "long":
        front = f'<path d="M118 152c-2-68 36-106 82-106s84 38 82 106c2-15-2-31-9-41-12 15-31 25-73 25s-61-10-73-25c-7 10-11 26-9 41z" fill="{hr}"/>'
    elif style == "bun":
        front = f'<path d="M122 140c-2-60 34-94 78-94s80 34 78 94c-2-13-3-27-9-35-12 12-29 20-69 20s-57-8-69-20c-6 8-7 22-9 35z" fill="{hr}"/>'
    else:  # bald / receding: thin greying sides only
        front = f'<path d="M124 150c-6-16-4-34 2-44 2 22 8 34 12 40zM276 150c6-16 4-34-2-44-2 22-8 34-12 40z" fill="{hr}" opacity="0.9"/>'
    beard_svg = (f'<path d="M126 150c0 52 30 96 74 96s74-44 74-96c-15 27-41 45-74 45s-59-18-74-45z" fill="{hr}"/>'
                 if beard else "")
    features = ('<g fill="#3a2c22" opacity="0.8"><ellipse cx="174" cy="139" rx="5" ry="6.5"/>'
                '<ellipse cx="226" cy="139" rx="5" ry="6.5"/></g>'
                '<g stroke="#5b4636" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.55">'
                '<path d="M165 127q9-6 18 0"/><path d="M217 127q9-6 18 0"/><path d="M197 147q3 7 6 0"/></g>'
                '<path d="M186 170q14 8 28 0" stroke="#a25c49" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.6"/>')
    glasses_svg = ('<g fill="none" stroke="#2a2f3a" stroke-width="3" opacity="0.85">'
                   '<rect x="159" y="129" width="31" height="22" rx="8"/>'
                   '<rect x="210" y="129" width="31" height="22" rx="8"/><path d="M190 139h20"/></g>'
                   if glasses else "")
    coat_svg = (f'<path d="M58 460c0-88 64-154 142-154s142 66 142 154z" fill="{co}"/>'
                f'<path d="M200 306c-21 0-39 4-56 12l56 66 56-66c-17-8-35-12-56-12z" fill="#F7FAFD"/>'
                f'<path d="M200 318l-18 13 11 18 7-10 7 10 11-18z" fill="{accent}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 460" role="img" aria-label="Illustrated corporate portrait placeholder">
  <defs><linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF4F9"/><stop offset="1" stop-color="#DBE7F1"/></linearGradient></defs>
  <rect width="400" height="460" fill="url(#pbg)"/>
  {back}{head}{front}{beard_svg}{features}{glasses_svg}{coat_svg}
</svg>
'''
    with open(os.path.join(ASSETS, path), "w") as f:
        f.write(svg)


# ----------------------------------------------------------------------------
# Decorative article / feature thumbnails (abstract "sky" gradients)
# ----------------------------------------------------------------------------
THUMB_SETS = [
    ("#cfe0ef", "#9bbcd8", "#E2A24A"),
    ("#dfe9d6", "#a9c6b0", "#2F6F9F"),
    ("#e7dbc6", "#d6b483", "#134063"),
    ("#d6e2ef", "#8fb0cf", "#E2A24A"),
    ("#ece3d3", "#c9b48d", "#3A7CAD"),
    ("#d2e4ec", "#8fc0cf", "#134063"),
]


def thumb(path, c, i):
    a, b, sun = c
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Decorative sky illustration">
  <defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fbfcfe"/><stop offset="0.55" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>
  </linearGradient></defs>
  <rect width="640" height="360" fill="url(#g{i})"/>
  <circle cx="470" cy="120" r="46" fill="{sun}" opacity="0.9"/>
  <circle cx="470" cy="120" r="66" fill="{sun}" opacity="0.18"/>
  <path d="M0 250 Q160 210 320 250 T640 250 V360 H0 Z" fill="#ffffff" opacity="0.25"/>
  <path d="M0 290 Q160 255 320 290 T640 290 V360 H0 Z" fill="#ffffff" opacity="0.35"/>
  <path d="M0 300 L640 300" stroke="{sun}" stroke-width="1" opacity="0.35"/>
</svg>
'''
    with open(os.path.join(ASSETS, path), "w") as f:
        f.write(svg)


# ----------------------------------------------------------------------------
# Branded mini-maps for the office location cards (stylised, not cartographic)
# ----------------------------------------------------------------------------
def citymap(path, label, water=None, greens=()):
    """A clean illustrated 'where to find us' minimap: street grid, an optional
    body of water and parkland, and a brand pin marking the office."""
    blocks = ""
    for gy in range(5):
        for gx in range(8):
            x, y = 12 + gx * 79, 12 + gy * 70
            blocks += f'<rect x="{x}" y="{y}" width="63" height="54" rx="7" fill="#d7e2ec"/>'
    green_svg = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#cfe3cf"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#b6d2b6" stroke-width="2"/>'
        for cx, cy, rx, ry in greens)
    water_svg = ""
    if water:
        side, wy = water
        if side == "top":
            water_svg = (f'<path d="M0 {wy} Q160 {wy + 34} 320 {wy} T640 {wy} V0 H0 Z" fill="#bcd6ea"/>'
                         f'<path d="M0 {wy + 14} Q160 {wy + 48} 320 {wy + 14} T640 {wy + 14} V0 H0 Z" fill="#cfe3f2" opacity="0.6"/>')
        else:
            water_svg = (f'<path d="M0 {wy} Q160 {wy - 34} 320 {wy} T640 {wy} V360 H0 Z" fill="#bcd6ea"/>'
                         f'<path d="M0 {wy + 12} Q160 {wy - 22} 320 {wy + 12} T640 {wy + 12} V360 H0 Z" fill="#a8c8e2" opacity="0.55"/>')
    chip_w = len(label) * 10 + 50
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Map showing the location of the {label} office">
  <rect width="640" height="360" fill="#eaf0f5"/>
  <g>{blocks}</g>
  <path d="M-20 320 L660 70" stroke="#ffffff" stroke-width="15"/>
  <path d="M-20 320 L660 70" stroke="#f0d9b4" stroke-width="3" stroke-dasharray="2 16"/>
  {green_svg}{water_svg}
  <ellipse cx="320" cy="246" rx="26" ry="7" fill="#13405f" opacity="0.18"/>
  <path d="M320 116c-28 0-50 22-50 50 0 33 50 76 50 76s50-43 50-76c0-28-22-50-50-50z" fill="#134063"/>
  <circle cx="320" cy="166" r="19" fill="#E2A24A"/>
  <circle cx="320" cy="166" r="7.5" fill="#ffffff" opacity="0.9"/>
  <g transform="translate(18,298)">
    <rect width="{chip_w}" height="38" rx="19" fill="#ffffff" opacity="0.95"/>
    <circle cx="23" cy="19" r="6" fill="#E2A24A"/>
    <text x="40" y="25" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="#16243A">{label}</text>
  </g>
</svg>
'''
    with open(os.path.join(ASSETS, path), "w") as f:
        f.write(svg)


# label, water (side, y) or None, green ellipses (cx, cy, rx, ry)
CITY_MAPS = {
    "perth":    ("West Perth WA",  ("bottom", 326), [(108, 78, 120, 66)]),
    "brisbane": ("Brisbane CBD",   ("bottom", 300), []),
    "adelaide": ("Adelaide CBD",   None,            [(320, 30, 380, 60), (320, 348, 380, 60)]),
    "sydney":   ("Sydney CBD",     ("top", 78),     []),
    "bendigo":  ("Bendigo VIC",    ("bottom", 338), [(560, 300, 110, 70)]),
}
# ----------------------------------------------------------------------------
EXEC = [
    dict(name="Kenneth Jimmieson", role="Co-Founder & Chief Executive Officer",
         email="kenneth.jimmieson@clear-sky-consulting.au", phone="+61 8 6555 0101", img="exec-1.svg",
         bio="Founded Clear Sky Consulting in 2018 after twelve years advising private clients inside two of Australia's largest institutions. Sets the firm's standard for independence."),
    dict(name="Mei Lin Tan", role="Co-Founder & Chief Advisory Officer",
         email="meilin.tan@clear-sky-consulting.au", phone="+61 8 8555 0102", img="exec-2.svg",
         bio="A lawyer turned advisor who oversees advice quality across every office. Known for reading the fine print no one else does."),
    dict(name="Ray Mitchel", role="Chief Financial Officer",
         email="ray.mitchel@clear-sky-consulting.au", phone="+61 2 8555 0103", img="exec-3.svg",
         bio="Leads finance, planning and the firm's commercial operations. Joined from a national professional-services group where he ran group finance."),
    dict(name="Priya Raman", role="Chief Operating Officer",
         email="priya.raman@clear-sky-consulting.au", phone="+61 7 3555 0104", img="exec-4.svg",
         bio="Runs the operating model that lets a small-feeling practice work at national scale without diluting the client experience."),
    dict(name="Sophie Lindgren", role="Chief Client Officer",
         email="sophie.lindgren@clear-sky-consulting.au", phone="+61 2 8555 0105", img="exec-5.svg",
         bio="Owns the end-to-end client journey and the firm's industry-leading satisfaction scores."),
    dict(name="Marcus Bellini", role="Chief People Officer",
         email="marcus.bellini@clear-sky-consulting.au", phone="+61 3 9555 0106", img="exec-6.svg",
         bio="Responsible for hiring, developing and keeping the advisors clients trust. Champions the firm's apprenticeship model."),
    dict(name="Aisha Mahmoud", role="General Counsel & Company Secretary",
         email="aisha.mahmoud@clear-sky-consulting.au", phone="+61 8 6555 0107", img="exec-7.svg",
         bio="Leads legal, risk and governance, and keeps the firm's independence promise enforceable in writing."),
    dict(name="Hiroshi Tanaka", role="Chief Technology Officer",
         email="hiroshi.tanaka@clear-sky-consulting.au", phone="+61 2 8555 0108", img="exec-8.svg",
         bio="Builds the secure, private tooling that supports advisors without ever turning advice into an algorithm."),
]

BOARD = [
    dict(name="Eleanor Voss", role="Independent Non-Executive Chair", img="board-1.svg",
         bio="Former CEO of a national wealth advisory group; chairs the Board and the Nominations Committee."),
    dict(name="Margaret Chen", role="Independent Non-Executive Director", img="board-2.svg",
         bio="Career economist and former central bank advisor; chairs the Audit & Risk Committee."),
    dict(name="Robert Fitzgerald", role="Independent Non-Executive Director", img="board-3.svg",
         bio="Consumer-advocacy leader who keeps the client's interest on every agenda."),
    dict(name="Yusuf Demir", role="Independent Non-Executive Director", img="board-4.svg",
         bio="Technology and cyber-security veteran; chairs the Technology Committee."),
    dict(name="Catherine O'Brien", role="Independent Non-Executive Director", img="board-5.svg",
         bio="Remuneration specialist and former HR director of a major Australian employer."),
]

REGIONAL = [
    dict(name="Liam Brennan", role="Managing Director - Perth", img="reg-1.svg",
         email="perth@clear-sky-consulting.au", phone="+61 8 6555 0140",
         bio="Leads the Perth office, where Clear Sky Consulting began. Liam has spent eighteen years advising West Australian families through major life and financial decisions."),
    dict(name="Grace Whitmore", role="Managing Director - Brisbane", img="reg-2.svg",
         email="brisbane@clear-sky-consulting.au", phone="+61 7 3555 0150",
         bio="Heads the Brisbane practice across South East Queensland. Grace is known for turning complicated, high-stakes decisions into a calm, clear set of options."),
    dict(name="Tom Ferraro", role="Managing Director - Adelaide", img="reg-3.svg",
         email="adelaide@clear-sky-consulting.au", phone="+61 8 8555 0160",
         bio="Runs the Adelaide office and has advised South Australian clients for over fifteen years, with a particular focus on planning toward long-term goals."),
    dict(name="Hannah Goldberg", role="Managing Director - Sydney", img="reg-4.svg",
         email="sydney@clear-sky-consulting.au", phone="+61 2 8555 0170",
         bio="Leads the flagship Sydney office. Hannah brings a sharp, independent eye to the proposals and decisions Greater Sydney clients bring to the table."),
    dict(name="Oliver Nguyen", role="Managing Director - Bendigo", img="reg-5.svg",
         email="bendigo@clear-sky-consulting.au", phone="+61 3 5555 0180",
         bio="Heads the Bendigo office, bringing the same independent advice to regional Victoria that the firm is known for in the capital cities."),
]

ADVISORS = [
    dict(name="Brian Kowalski", role="Independent Advisor", img="adv-1.svg",
         email="brian.kowalski@clear-sky-consulting.au", phone="+61 8 6555 0201",
         bio="Two decades guiding clients through major career and business decisions."),
    dict(name="Ben Garcia", role="Independent Advisor", img="adv-2.svg",
         email="ben.garcia@clear-sky-consulting.au", phone="+61 7 3555 0202",
         bio="A calm second opinion on the decisions that keep you up at night."),
    dict(name="Adrian Philips", role="Independent Advisor", img="adv-3.svg",
         email="adrian.philips@clear-sky-consulting.au", phone="+61 8 8555 0203",
         bio="Specialises in planning and sequencing toward long-term goals."),
    dict(name="Jacob Smok", role="Independent Advisor", img="adv-4.svg",
         email="jacob.smok@clear-sky-consulting.au", phone="+61 2 8555 0204",
         bio="Helps clients weigh big financial and life trade-offs with a clear head."),
    dict(name="Simon Kamensky", role="Independent Advisor", img="adv-5.svg",
         email="simon.kamensky@clear-sky-consulting.au", phone="+61 3 9555 0205",
         bio="Brings a lawyer's eye to proposals and the fine print others miss."),
    dict(name="Chester Vant", role="Independent Advisor", img="adv-6.svg",
         email="chester.vant@clear-sky-consulting.au", phone="+61 3 5555 0206",
         bio="A steady, long-term advisor for families navigating change."),
]

AUTHORS = {
    "Mei Lin Tan": "exec-2.svg",
    "Kenneth Jimmieson": "exec-1.svg",
    "Sophie Lindgren": "exec-5.svg",
    "Aisha Mahmoud": "exec-7.svg",
}

OFFICES = [
    dict(city="Perth", addr="44 Kings Park Road<br>West Perth WA 6005", lead="Liam Brennan",
         email="perth@clear-sky-consulting.au", phone="+61 8 6555 0140",
         q="44 Kings Park Road, West Perth WA"),
    dict(city="Brisbane", addr="1 William Street<br>Brisbane QLD 4000", lead="Grace Whitmore",
         email="brisbane@clear-sky-consulting.au", phone="+61 7 3555 0150",
         q="1 William Street, Brisbane QLD 4000"),
    dict(city="Adelaide", addr="128 Hindley Street<br>Adelaide SA 5000", lead="Tom Ferraro",
         email="adelaide@clear-sky-consulting.au", phone="+61 8 8555 0160",
         q="128 Hindley Street, Adelaide SA 5000"),
    dict(city="Sydney", addr="436 George Street<br>Sydney NSW 2000", lead="Hannah Goldberg",
         email="sydney@clear-sky-consulting.au", phone="+61 2 8555 0170",
         q="436 George Street, Sydney NSW 2000"),
    dict(city="Bendigo", addr="118 King Street<br>Bendigo VIC 3550", lead="Oliver Nguyen",
         email="bendigo@clear-sky-consulting.au", phone="+61 3 5555 0180",
         q="118 King Street, Bendigo VIC 3550"),
]

# Per-person headshot attributes (skin, hair, style, coat, accent, beard, glasses)
# Tuned to the cast's inferred gender / age (greying) / heritage (skin tone).
FACE = {
    "Kenneth Jimmieson":   ("light",  "salt",     "short", "c1", "#E2A24A", False, False),
    "Mei Lin Tan":      ("asian",  "dark",     "long",  "c2", "#2F6F9F", False, False),
    "Ray Mitchel":      ("light2", "darkgrey", "short", "c3", "#E2A24A", False, False),
    "Priya Raman":      ("brown",  "dark",     "long",  "c4", "#2F6F9F", False, False),
    "Sophie Lindgren":  ("light",  "blonde",   "long",  "c5", "#E2A24A", False, False),
    "Marcus Bellini":   ("olive",  "dark",     "short", "c1", "#2F6F9F", True,  False),
    "Aisha Mahmoud":    ("medium", "dark",     "long",  "c2", "#E2A24A", False, False),
    "Hiroshi Tanaka":   ("asian",  "dark",     "short", "c3", "#2F6F9F", False, True),
    "Eleanor Voss":     ("light",  "grey",     "bun",   "c4", "#E2A24A", False, False),
    "Margaret Chen":    ("asian",  "salt",     "long",  "c5", "#2F6F9F", False, False),
    "Robert Fitzgerald":("light",  "grey",     "bald",  "c1", "#E2A24A", False, True),
    "Yusuf Demir":      ("olive",  "salt",     "short", "c2", "#2F6F9F", True,  False),
    "Catherine O'Brien":("light2", "grey",     "long",  "c3", "#E2A24A", False, False),
    "Liam Brennan":     ("light",  "ginger",   "short", "c4", "#2F6F9F", False, False),
    "Grace Whitmore":   ("light2", "brown",    "long",  "c5", "#E2A24A", False, False),
    "Tom Ferraro":      ("olive",  "dark",     "short", "c1", "#2F6F9F", False, False),
    "Hannah Goldberg":  ("medium", "dark",     "long",  "c2", "#E2A24A", False, False),
    "Oliver Nguyen":    ("asian",  "dark",     "short", "c3", "#2F6F9F", False, False),
    "Brian Kowalski":   ("light",  "salt",     "short", "c4", "#E2A24A", False, False),
    "Ben Garcia":       ("medium", "dark",     "short", "c5", "#2F6F9F", True,  False),
    "Adrian Philips":   ("light",  "brown",    "short", "c1", "#E2A24A", False, False),
    "Jacob Smok":       ("light2", "dark",     "short", "c2", "#2F6F9F", True,  False),
    "Simon Kamensky":   ("light",  "salt",     "short", "c3", "#E2A24A", False, True),
    "Chester Vant":     ("light",  "grey",     "bald",  "c4", "#2F6F9F", False, True),
}

# Generate all portraits + thumbnails -----------------------------------------
all_people = EXEC + BOARD + REGIONAL + ADVISORS
for person in all_people:
    skin, hair, style, coat, accent, beard, glasses = FACE[person["name"]]
    portrait2(person["img"], skin, hair, style, coat, accent, beard, glasses)
# keep legacy founder images matching the two founders
portrait2("founder-1.svg", *FACE["Kenneth Jimmieson"])
portrait2("founder-2.svg", *FACE["Mei Lin Tan"])
for i, cset in enumerate(THUMB_SETS):
    thumb(f"thumb-{i+1}.svg", cset, i)
for _slug, (_label, _water, _greens) in CITY_MAPS.items():
    citymap(f"map-{_slug}.svg", _label, _water, _greens)

# favicon + social share image -------------------------------------------------
with open(os.path.join(ASSETS, "favicon.svg"), "w") as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="#134063"/>
  <circle cx="16" cy="14" r="6" fill="#E2A24A"/>
  <path d="M5 23h22M9 27h14" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round"/>
</svg>
''')

# Square brand logo for structured data (rasterised to logo.png by build/og.py).
with open(os.path.join(ASSETS, "logo.svg"), "w") as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="112" fill="#134063"/>
  <circle cx="256" cy="224" r="96" fill="#E2A24A"/>
  <path d="M80 368h352M144 432h224" stroke="#ffffff" stroke-width="35" stroke-linecap="round"/>
</svg>
''')

# Social share images: one shared template, per-section taglines/kickers.
def og_svg(name, tagline, kicker):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs><linearGradient id="og" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fdfdfe"/><stop offset="0.55" stop-color="#dcebf6"/><stop offset="1" stop-color="#f3e4cd"/>
  </linearGradient></defs>
  <rect width="1200" height="630" fill="url(#og)"/>
  <circle cx="950" cy="220" r="70" fill="#E2A24A" opacity="0.18"/>
  <circle cx="950" cy="220" r="48" fill="#E2A24A"/>
  <path d="M0 470 Q300 430 600 460 T1200 460 V630 H0 Z" fill="#9ec3df" opacity="0.55"/>
  <path d="M0 520 Q300 485 600 515 T1200 510 V630 H0 Z" fill="#7fb0d2" opacity="0.6"/>
  <g transform="translate(90,250)">
    <circle cx="22" cy="-6" r="18" fill="#E2A24A"/>
    <path d="M-2 22h60M8 34h44" stroke="#134063" stroke-width="5" stroke-linecap="round"/>
  </g>
  <text x="90" y="360" font-family="Georgia, 'Times New Roman', serif" font-size="86" font-weight="600" fill="#16243A">Clear Sky Consulting</text>
  <text x="92" y="420" font-family="Arial, Helvetica, sans-serif" font-size="34" fill="#45556C">{tagline}</text>
  <text x="92" y="470" font-family="Arial, Helvetica, sans-serif" font-size="23" fill="#2F6F9F" letter-spacing="1.5">{kicker}</text>
</svg>
'''
    with open(os.path.join(ASSETS, f"{name}.svg"), "w") as f:
        f.write(svg)


# variant -> (tagline, kicker). "og-image" is the default/home card.
OG_VARIANTS = {
    "og-image":    ("Clear thinking for life's bigger decisions.", "INDEPENDENT PERSONAL ADVISORY &#183; AUSTRALIA"),
    "og-insights": ("Plain-English thinking on big decisions.", "CLEAR SKY CONSULTING &#183; INSIGHTS"),
    "og-services": ("Independent, fixed-fee personal advisory.", "WHAT WE DO &#183; CLEAR SKY CONSULTING"),
    "og-offices":  ("Five offices, face to face, across Australia.", "PERTH &#183; BRISBANE &#183; ADELAIDE &#183; SYDNEY &#183; BENDIGO"),
}
for _name, (_tag, _kick) in OG_VARIANTS.items():
    og_svg(_name, _tag, _kick)

# PWA web app manifest (installable, themed)
with open(os.path.join(ROOT, "site.webmanifest"), "w") as f:
    f.write(json.dumps({
        "name": "Clear Sky Consulting",
        "short_name": "Clear Sky",
        "description": "Independent personal advisory across Australia.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#134063",
        "icons": [
            {"src": "assets/logo-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/logo.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }, indent=2))

# ----------------------------------------------------------------------------
# Shared chrome
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("services.html", "What we do", [
        ("service-decision-clarity.html", "Decision clarity session", "Untangle one big decision"),
        ("service-planning-strategy.html", "Planning &amp; strategy", "A structured plan toward a goal"),
        ("service-second-opinion.html", "Second opinion review", "Independent check before you commit"),
        ("service-ongoing-advisory.html", "Ongoing advisory", "A trusted advisor for the long run"),
        ("find-your-service.html", "Which service fits you?", "Take the 60-second quiz"),
        ("approach.html", "Our approach", "How we work, step by step"),
        ("pricing.html", "Pricing", "Fixed fees, agreed upfront"),
    ]),
    ("about.html", "Company", [
        ("about.html", "About Clear Sky Consulting", "Our story and mission"),
        ("leadership.html", "Leadership &amp; board", "The people accountable to you"),
        ("offices.html", "Offices", "Five locations across Australia"),
        ("careers.html", "Careers", "Build a practice worth trusting"),
        ("press.html", "Newsroom", "Announcements and media"),
        ("resources.html", "Free guides", "Downloadable checklists"),
    ]),
    ("insights.html", "Insights", None),
    ("case-studies.html", "Case studies", None),
    ("faq.html", "FAQ", None),
]


SITE_URL = "https://www.clear-sky-consulting.au"
# Google Analytics 4 measurement ID. Replace the placeholder with your real ID
# (e.g. "G-AB12CD34EF"); analytics only loads after the visitor accepts cookies,
# and stays off entirely while the ID is the placeholder.
ANALYTICS_ID = "G-XXXXXXXXXX"

# ----------------------------------------------------------------------------
# Structured data (JSON-LD) - helps search engines understand the site
# ----------------------------------------------------------------------------
ORG_ID = SITE_URL + "/#organization"
# filename -> [absolute image URLs] for the image sitemap; filled by pages.build
PAGE_IMAGES = {}
_OG_FILE = "og-image.png" if os.path.exists(os.path.join(ASSETS, "og-image.png")) \
    else "og-image.svg"
_OG_URL = SITE_URL + "/assets/" + _OG_FILE


def _og_variant(filename):
    """Pick the section-specific social card for a page."""
    f = filename or ""
    if f.startswith("insight-") or f == "insights.html":
        return "og-insights"
    if f.startswith("service-") or f in ("services.html", "pricing.html", "approach.html", "find-your-service.html"):
        return "og-services"
    if f.startswith("office-") or f in ("offices.html", "contact.html"):
        return "og-offices"
    return "og-image"


def _og_url(filename):
    """Absolute URL for a page's social card, preferring a rasterised PNG."""
    name = _og_variant(filename)
    for ext in ("png", "jpg"):
        if os.path.exists(os.path.join(ASSETS, f"{name}.{ext}")):
            return f"{SITE_URL}/assets/{name}.{ext}"
    return f"{SITE_URL}/assets/{name}.svg"
_LOGO_FILE = "logo.png" if os.path.exists(os.path.join(ASSETS, "logo.png")) \
    else "logo.svg"
_LOGO_URL = SITE_URL + "/assets/" + _LOGO_FILE
_DEFAULT_ROBOTS = ("index, follow, max-image-preview:large, "
                   "max-snippet:-1, max-video-preview:-1")
_MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}


def _plain(s):
    """Strip HTML tags and unescape entities -> clean text for JSON-LD values."""
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _to_iso_date(s):
    """'2 June 2026' -> '2026-06-02'. Returns the input unchanged if unparsable."""
    parts = s.split()
    if len(parts) == 3 and parts[1] in _MONTHS:
        day, mon, year = parts
        return f"{year}-{_MONTHS[mon]:02d}-{int(day):02d}"
    return s


def jsonld(obj):
    """Serialise a Python object to a <script type="application/ld+json"> tag."""
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            + "</script>\n")


# Organization + WebSite, emitted on every page.
SITEWIDE_LD = jsonld({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": ["Organization", "ProfessionalService"],
            "@id": ORG_ID,
            "name": "Clear Sky Consulting",
            "legalName": "Clear Sky Consulting Pty Ltd",
            "url": SITE_URL,
            "logo": {"@type": "ImageObject", "url": _LOGO_URL, "width": 512, "height": 512},
            "image": _OG_URL,
            "description": "Independent personal advisory for individuals and "
                           "families across Australia, since 2018.",
            "foundingDate": "2018",
            "slogan": "Clear thinking for life's bigger decisions.",
            "areaServed": "AU",
            "telephone": "+61 488 855 709",
            "email": "hello@clear-sky-consulting.au",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "44 Kings Park Road",
                "addressLocality": "West Perth",
                "addressRegion": "WA",
                "postalCode": "6005",
                "addressCountry": "AU",
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+61 488 855 709",
                "contactType": "customer service",
                "areaServed": "AU",
                "availableLanguage": "en",
            },
            "founder": [
                {"@type": "Person", "name": "Kenneth Jimmieson"},
                {"@type": "Person", "name": "Mei Lin Tan"},
            ],
        },
        {
            "@type": "WebSite",
            "@id": SITE_URL + "/#website",
            "url": SITE_URL,
            "name": "Clear Sky Consulting",
            "publisher": {"@id": ORG_ID},
            "inLanguage": "en-AU",
        },
    ],
})


def _parse_addr(addr):
    """'44 Kings Park Road<br>West Perth WA 6005' -> (street, locality, region, postcode)."""
    line1, line2 = addr.split("<br>")
    toks = line2.split()
    return line1.strip(), " ".join(toks[:-2]), toks[-2], toks[-1]


def localbusiness_ld(offices):
    """A ProfessionalService LocalBusiness node for each physical office."""
    items = []
    for o in offices:
        street, locality, region, postcode = _parse_addr(o["addr"])
        items.append({
            "@type": "ProfessionalService",
            "@id": f"{SITE_URL}/offices.html#{o['city'].lower()}",
            "name": f"Clear Sky Consulting - {o['city']}",
            "parentOrganization": {"@id": ORG_ID},
            "url": f"{SITE_URL}/offices.html",
            "image": _OG_URL,
            "telephone": o["phone"].replace(" ", ""),
            "email": o["email"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": street,
                "addressLocality": locality,
                "addressRegion": region,
                "postalCode": postcode,
                "addressCountry": "AU",
            },
            "areaServed": o["city"],
            "priceRange": "$$",
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "08:30",
                "closes": "17:30",
            },
        })
    return jsonld({"@context": "https://schema.org", "@graph": items})


def write_sitemap_and_robots():
    """Scan the built HTML pages and emit sitemap.xml + robots.txt at the root."""
    today = datetime.date.today().isoformat()
    pages = sorted(f for f in os.listdir(ROOT)
                   if f.endswith(".html") and f != "404.html")

    def meta(fn):
        if fn == "index.html":
            return "1.0", "weekly"
        if fn in ("privacy.html", "terms.html"):
            return "0.3", "yearly"
        if fn.startswith("insight-"):
            return "0.6", "monthly"
        if fn in ("insights.html", "case-studies.html", "press.html"):
            return "0.8", "weekly"
        return "0.8", "monthly"

    def _xml_escape(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    urls = []
    for fn in pages:
        loc = SITE_URL + "/" + ("" if fn == "index.html" else fn)
        prio, freq = meta(fn)
        imgs = "".join(
            f"\n    <image:image><image:loc>{_xml_escape(u)}</image:loc></image:image>"
            for u in PAGE_IMAGES.get(fn, []))
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>"
            f"{imgs}\n  </url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
               '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(sitemap)

    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              f"Sitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(robots)
    print(f"Wrote sitemap.xml ({len(pages)} URLs) and robots.txt.")


def _breadcrumb_ld(filename, title, page_url):
    """Auto BreadcrumbList: Home > [section] > current page. Empty for home."""
    if not filename or filename == "index.html":
        return ""
    trail = [("Home", SITE_URL + "/")]
    if filename.startswith("insight-"):
        trail.append(("Insights", SITE_URL + "/insights.html"))
    elif filename.startswith("service-"):
        trail.append(("What we do", SITE_URL + "/services.html"))
    elif filename.startswith("office-"):
        trail.append(("Offices", SITE_URL + "/offices.html"))
    elif filename.startswith("team-"):
        trail.append(("Leadership", SITE_URL + "/leadership.html"))
    name = _plain(title).split(" | ")[0].split(" - ")[0].strip()
    trail.append((name, page_url))
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
             for i, (n, u) in enumerate(trail)]
    return jsonld({"@context": "https://schema.org",
                   "@type": "BreadcrumbList", "itemListElement": items})


def head(title, desc, extra="", url="", robots=_DEFAULT_ROBOTS, og_type="website"):
    # index.html is served at the site root, so canonicalise it to "/"
    page_url = SITE_URL + "/" + ("" if url in ("", "index.html") else url)
    og_img = _og_url(url)
    og_alt = "Clear Sky Consulting - independent personal advisory, Australia"
    crumb_ld = _breadcrumb_ld(url, title, page_url)
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>(function(){{try{{var t=localStorage.getItem('csc-theme');if(t==='dark'||(!t&&window.matchMedia&&matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.setAttribute('data-theme','dark');}}catch(e){{}}}})();</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="en-au" href="{page_url}">
<link rel="alternate" hreflang="x-default" href="{page_url}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/logo.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#134063">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Clear Sky Consulting">
<meta property="og:locale" content="en_AU">
<meta property="og:url" content="{page_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<meta name="twitter:image:alt" content="{og_alt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{SITEWIDE_LD}{crumb_ld}{extra}</head>
<body>
<a class="skip-link" href="#top">Skip to content</a>'''


def utility_bar():
    return f'''<div class="utility">
  <div class="wrap">
    <div class="u-left">
      <span>Independent &amp; impartial advice</span>
      <span>Five offices across Australia</span>
      <span>Mon-Fri, 8:30am-5:30pm AEST</span>
    </div>
    <div class="u-right">
      <a href="tel:+61488855709">+61 488 855 709</a>
      <a href="offices.html">Offices</a>
      <a href="contact.html">Contact</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle dark mode" title="Toggle dark mode">
        <svg class="t-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg>
        <svg class="t-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</div>'''


def header(active):
    links = []
    for href, label, sub in NAV_ITEMS:
        cls = ' class="active"' if active == href else ""
        if sub:
            items = "".join(
                f'<a href="{h}">{t}<small>{d}</small></a>' for h, t, d in sub)
            links.append(
                f'<div class="has-menu"><a href="{href}"{cls}>{label}</a>'
                f'<div class="dropdown">{items}</div></div>')
        else:
            links.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "\n      ".join(links)
    return f'''<header>
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Clear Sky Consulting home">
      <svg class="mark" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle cx="12" cy="9" r="4.5" fill="#E2A24A"/>
        <path d="M2 18h20M6 21h12" stroke="#134063" stroke-width="1.6" stroke-linecap="round"/>
      </svg>
      Clear&nbsp;Sky&nbsp;Consulting
    </a>
    <nav class="nav-links" id="menu">
      {nav}
      <a class="btn btn-primary" href="contact.html">Book a meeting</a>
    </nav>
    <button class="nav-toggle" id="toggle" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="foot-mega">
      <div>
        <div class="foot-brand">
          <svg viewBox="0 0 24 24" fill="none" width="20" height="20" aria-hidden="true">
            <circle cx="12" cy="9" r="4.5" fill="#E2A24A"/>
            <path d="M2 18h20M6 21h12" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
          Clear Sky Consulting
        </div>
        <p style="max-width:280px;margin-top:.8rem;color:#73869c">Independent personal advisory for individuals and families across Australia, since 2018.</p>
        <a href="https://www.clear-sky-consulting.au" style="display:inline-block;margin-top:.7rem;color:#aebfd3;font-weight:600;font-size:.88rem">www.clear-sky-consulting.au</a>
      </div>
      <div>
        <div class="h">What we do</div>
        <a href="service-decision-clarity.html">Decision clarity</a>
        <a href="service-planning-strategy.html">Planning &amp; strategy</a>
        <a href="service-second-opinion.html">Second opinion</a>
        <a href="service-ongoing-advisory.html">Ongoing advisory</a>
        <a href="approach.html">Our approach</a>
        <a href="pricing.html">Pricing</a>
      </div>
      <div>
        <div class="h">Company</div>
        <a href="about.html">About us</a>
        <a href="leadership.html">Leadership &amp; board</a>
        <a href="careers.html">Careers</a>
        <a href="offices.html">Offices</a>
        <a href="press.html">Newsroom</a>
        <a href="contact.html">Contact</a>
      </div>
      <div>
        <div class="h">Resources</div>
        <a href="insights.html">Insights</a>
        <a href="resources.html">Free guides</a>
        <a href="glossary.html">Glossary</a>
        <a href="case-studies.html">Case studies</a>
        <a href="faq.html">FAQ</a>
      </div>
      <div>
        <div class="h">Get in touch</div>
        <a href="contact.html">Book a meeting</a>
        <a href="offices.html">Find an office</a>
        <a href="press.html">Newsroom</a>
        <a href="privacy.html">Privacy policy</a>
        <a href="terms.html">Terms of engagement</a>
        <a href="#" data-cookie-prefs>Cookie preferences</a>
      </div>
    </div>
    <div class="foot-offices">
      <span>Our offices</span>
      <a href="office-perth.html">Perth</a>
      <a href="office-brisbane.html">Brisbane</a>
      <a href="office-adelaide.html">Adelaide</a>
      <a href="office-sydney.html">Sydney</a>
      <a href="office-bendigo.html">Bendigo</a>
    </div>
    <div class="foot-bottom">
      <div>© <span id="year"></span> Clear Sky Consulting Pty Ltd · ABN 47 615 920 188</div>
      <div>Made with a clear head in Australia 🇦🇺</div>
    </div>
  </div>
</footer>
<a class="to-top" id="toTop" href="#top" aria-label="Back to top" hidden>
  <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>
</a>
<div class="mobile-cta" aria-label="Quick actions">
  <a class="btn btn-ghost" href="tel:+61488855709">Call us</a>
  <a class="btn btn-primary" href="contact.html">Book a meeting</a>
</div>
<div class="consent" id="consent" hidden role="dialog" aria-live="polite" aria-label="Cookie notice">
  <div class="consent-inner">
    <p>We use a couple of privacy-friendly cookies to understand how the site is used - nothing is loaded until you choose. See our <a href="privacy.html">privacy policy</a>.</p>
    <div class="consent-actions">
      <button class="btn btn-ghost" id="consentDecline" type="button">Decline</button>
      <button class="btn btn-primary" id="consentAccept" type="button">Accept</button>
    </div>
  </div>
</div>
<script>window.CSC_GA_ID="{ANALYTICS_ID}";</script>
<script src="main.js"></script>
</body>
</html>'''


def page(filename, title, desc, active, body, extra_head="", robots=_DEFAULT_ROBOTS, og_type="website"):
    htmldoc = "\n".join([
        head(title, desc, extra_head, url=filename, robots=robots, og_type=og_type),
        "",
        utility_bar(),
        header(active),
        "",
        '<main id="top">',
        body,
        "</main>",
        "",
        footer(),
    ])
    with open(os.path.join(ROOT, filename), "w") as f:
        f.write(htmldoc + "\n")


def trust_strip():
    return '''<div class="trust">
  <div class="wrap">
    <span>Independent &amp; impartial</span>
    <span>Strictly confidential</span>
    <span>Fixed, upfront fees</span>
    <span>In-person meetings only</span>
  </div>
</div>'''


def cta_band(title="Ready to talk it through with someone on your side?",
             text="Your first meeting is complimentary, in person, and entirely without obligation."):
    return f'''<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="contact.html">Book a meeting</a>
      <a class="btn btn-ghost" href="offices.html">Find your nearest office</a>
    </div>
  </div>
</section>'''


def page_hero(crumb, eyebrow, h1, lead):
    return f'''<section class="page-hero">
  <div class="sky-field" aria-hidden="true"></div>
  <div class="wrap">
    <div class="inner reveal">
      <p class="breadcrumb"><a href="index.html">Home</a> · {crumb}</p>
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
  </div>
  <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
</section>'''


# Prefer real photos (assets/<name>.jpg, e.g. from build/photos.py) over the
# illustrated .svg placeholders whenever they're present.
def _prefer_photo(v):
    base = v.rsplit(".", 1)[0]
    for ext in ("webp", "jpg", "png"):
        if os.path.exists(os.path.join(ASSETS, f"{base}.{ext}")):
            return f"{base}.{ext}"
    return v


def scene(base, fallback):
    """Return <base>.webp/.jpg/.png if a generated scene image exists, else the fallback."""
    for ext in ("webp", "jpg", "png"):
        if os.path.exists(os.path.join(ASSETS, f"{base}.{ext}")):
            return f"{base}.{ext}"
    return fallback


for _p in all_people:
    _p["img"] = _prefer_photo(_p["img"])
for _k in list(AUTHORS):
    AUTHORS[_k] = _prefer_photo(AUTHORS[_k])


# build pages in a separate module to keep this readable
import pages
pages.build(globals())

# search-engine foundation: sitemap + robots (after all pages exist)
write_sitemap_and_robots()
print("Site generated.")
