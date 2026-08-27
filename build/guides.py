#!/usr/bin/env python3
"""
Render branded PDF guides (lead magnets) from HTML via headless Chromium.
Saves assets/guide-*.pdf.  Run:  python3 build/guides.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """
@page { size: A4; margin: 22mm 20mm; }
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; color: #16243A; line-height: 1.6; margin: 0; }
.cover { page-break-after: always; padding-top: 60mm; }
.brand { font-family: Arial, sans-serif; font-weight: 700; color: #134063; font-size: 13pt; letter-spacing: .5px; }
.mark { display:inline-block; width:14px; height:14px; border-radius:50%; background:#E2A24A; vertical-align:middle; margin-right:8px; }
.cover h1 { font-size: 30pt; line-height: 1.15; margin: 14mm 0 6mm; }
.cover .sub { font-family: Arial, sans-serif; font-size: 13pt; color: #45556C; }
.cover .kicker { font-family: Arial, sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 9pt; color: #2F6F9F; margin-top: 30mm; }
h2 { font-size: 15pt; color: #134063; margin: 9mm 0 3mm; }
p { font-size: 11.5pt; margin: 0 0 4mm; }
.lead { font-size: 12.5pt; color: #34465c; }
ol, ul { font-size: 11.5pt; padding-left: 6mm; }
li { margin-bottom: 2.5mm; }
.check li { list-style: none; position: relative; padding-left: 7mm; }
.check li::before { content: "\\2713"; position: absolute; left: 0; color: #2F6F9F; font-weight: bold; }
.foot { font-family: Arial, sans-serif; font-size: 8.5pt; color: #73869c; border-top: 1px solid #dbe7f1; margin-top: 12mm; padding-top: 4mm; }
a { color: #134063; }
"""

GUIDES = {
    "guide-three-questions": dict(
        title="The Clear-Head Checklist",
        sub="Three questions that cut through any big decision.",
        kicker="A Clear Sky Consulting guide",
        lead="When a decision feels impossibly tangled, you're rarely short of information - "
             "you're short of clarity. These three questions, drawn from thousands of advisory "
             "sessions, reliably reveal what you're actually deciding.",
        sections=[
            ("1. What are you actually choosing between?",
             ["Most stuck decisions are stuck because the options are blurry. People agonise over a "
              "false binary while a third, better option sits unnamed.",
              "Write the real options down, plainly. Often the act of naming them resolves half the difficulty."]),
            ("2. What would have to be true for each option to be the right one?",
             ["Instead of asking which option is best, ask what would have to be true for each to be best. "
              "This turns anxiety into investigation - now you have something concrete to check, rather than "
              "a feeling to wrestle with."]),
            ("3. Which regret could you not live with?",
             ["When options are genuinely close, stop optimising and look at the downside. You can live with "
              "most disappointments. The decision usually comes down to the one regret you couldn't make peace "
              "with - and that's worth listening to."]),
            ("Your one-page checklist",
             ["<ul class='check'><li>I've written down the real options - including any I'd been ignoring.</li>"
              "<li>For each, I know what would have to be true for it to be right.</li>"
              "<li>I've named the downside I genuinely couldn't live with.</li>"
              "<li>I've separated what truly matters from the noise.</li>"
              "<li>I know my next concrete step.</li></ul>"]),
        ]),
    "guide-second-opinion": dict(
        title="Before You Sign",
        sub="A second-opinion checklist for any significant proposal.",
        kicker="A Clear Sky Consulting guide",
        lead="A second opinion is cheap insurance against an expensive mistake. Before you commit to any "
             "significant proposal, quote or recommendation, run it through this checklist - the things that "
             "are easiest to miss when the document is in front of you and the clock is ticking.",
        sections=[
            ("1. Who carries the risk?",
             ["Proposals are often written so that costs, delays or things going wrong land on you rather than "
              "the other side. Trace where the risk sits if things don't go to plan - a single clause on "
              "variations, liability or termination can quietly rewrite the deal."]),
            ("2. What's assumed, but not stated?",
             ["Every proposal rests on assumptions about timing, scope and what's included. The expensive ones "
              "are the assumptions never written down. Surface them, and ask whether they actually hold for you."]),
            ("3. What isn't being compared?",
             ["A proposal frames itself as the obvious choice. Reintroduce the alternatives it leaves out - "
              "including doing nothing, or simply waiting."]),
            ("4. What would you ask if you had a month?",
             ["Write down the questions you'd reach with unlimited time, then take the three or four that matter "
              "most back to the table. More often than not, those questions - not a flat refusal - improve the deal."]),
            ("Your pre-signature checklist",
             ["<ul class='check'><li>I know exactly who carries the risk if things go wrong.</li>"
              "<li>I've listed the unstated assumptions and checked they hold.</li>"
              "<li>I've compared this against the real alternatives, including waiting.</li>"
              "<li>I have my three or four questions to ask before committing.</li>"
              "<li>I'm proceeding because it's right - not because of time pressure.</li></ul>"]),
        ]),
}


def render(name, g):
    secs = "".join(
        f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" if not p.startswith("<ul") else p for p in ps)
        for h, ps in g["sections"])
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
      <section class="cover">
        <div class="brand"><span class="mark"></span>Clear Sky Consulting</div>
        <h1>{g['title']}</h1>
        <p class="sub">{g['sub']}</p>
        <p class="kicker">{g['kicker']} &middot; clear-sky-consulting.au</p>
      </section>
      <p class="lead">{g['lead']}</p>
      {secs}
      <div class="foot">Clear Sky Consulting Pty Ltd - independent personal advisory across Australia.
      This guide is general information, not personal advice. For a complimentary conversation about your
      situation, visit clear-sky-consulting.au or call +61 488 855 709.</div>
    </body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ASSETS) as tf:
        tf.write(html)
        tmp = tf.name
    out = os.path.join(ASSETS, f"{name}.pdf")
    try:
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", "file://" + tmp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.remove(tmp)
    print(f"  {name}.pdf ({os.path.getsize(out)//1024}KB)")


if __name__ == "__main__":
    for name, g in GUIDES.items():
        render(name, g)
