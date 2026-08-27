# -*- coding: utf-8 -*-
"""Page content for the Clear Sky Consulting demo site. Called by generate.py."""
import re


def plain_attr(*parts):
    """Plain, quote-free, tag-free text safe to embed in an HTML attribute."""
    s = " ".join(parts).lower()
    s = re.sub(r"<[^>]+>", " ", s)               # drop any HTML tags
    s = s.replace("&amp;", " and ").replace("&middot;", " ").replace("&rarr;", " ")
    s = s.replace('"', " ").replace("'", " ")     # no quotes can break the attribute
    return re.sub(r"\s+", " ", s).strip()


def build(g):
    page = g["page"]
    cta_band = g["cta_band"]
    trust_strip = g["trust_strip"]
    page_hero = g["page_hero"]
    EXEC, BOARD, REGIONAL = g["EXEC"], g["BOARD"], g["REGIONAL"]
    ADVISORS = g["ADVISORS"]
    OFFICES, AUTHORS = g["OFFICES"], g["AUTHORS"]
    scene = g["scene"]
    # structured-data helpers (defined in generate.py)
    jsonld, plain = g["jsonld"], g["_plain"]
    to_iso, localbusiness_ld = g["_to_iso_date"], g["localbusiness_ld"]
    SITE_URL, ORG_ID = g["SITE_URL"], g["ORG_ID"]
    PAGE_IMAGES = g["PAGE_IMAGES"]

    mail = lambda e: f'<a href="mailto:{e}">{e}</a>'
    tel = lambda p: f'<a href="tel:{p.replace(" ", "")}">{p}</a>'
    slug = lambda n: re.sub(r"[^a-z0-9]+", "-", n.lower().replace("'", "")).strip("-")
    team_file = lambda p: f"team-{slug(p['name'])}.html"

    # ---- reusable fragments -------------------------------------------------
    def member_card(p, with_links=True):
        links = ""
        if with_links and p.get("email"):
            links = f'''<div class="links">
            <a href="mailto:{p['email']}"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg>{p['email']}</a>
            <a href="tel:{p['phone'].replace(' ', '')}"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg>{p['phone']}</a>
          </div>'''
        bio = f'<p class="bio">{p["bio"]}</p>' if p.get("bio") else ""
        href = team_file(p)
        return f'''<article class="member reveal">
        <a class="ph" href="{href}"><img src="assets/{p['img']}" alt="Portrait of {p['name']}" loading="lazy" width="400" height="400"></a>
        <div class="info">
          <h3><a href="{href}">{p['name']}</a></h3>
          <div class="role">{p['role']}</div>
          {bio}{links}
          <a class="member-more" href="{href}">View full profile &rarr;</a>
        </div>
      </article>'''

    def service_card(href, icon, title, tagline, text, best, meta):
        return f'''<a class="svc reveal" href="{href}">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{icon}</svg></div>
        <span class="svc-meta">{meta}</span>
        <h3>{title}</h3>
        <p class="svc-tag">{tagline}</p>
        <p>{text}</p>
        <div class="svc-best"><b>Best for</b> {best}</div>
        <span class="svc-more">Learn more &rarr;</span>
      </a>'''

    IC = dict(
        compass='<path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/>',
        chart='<path d="M4 19V5M4 19h16M8 15l3-4 3 3 4-6"/>',
        check='<path d="M21 12a9 9 0 11-9-9M21 4l-9 9-3-3"/>',
        clock='<path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/>',
        shield='<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/>',
        scale='<path d="M12 3v18M5 8l7-5 7 5"/>',
        pin='<path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        spark='<path d="M3 12h4l3 8 4-16 3 8h4"/>',
    )

    SERVICES = [
        ("service-decision-clarity.html", IC["scale"], "Decision clarity session",
         "Turn a tangle into a clear next step.",
         "A focused, one-off session to weigh a single big decision - the options, the risks, the trade-offs - so you leave knowing exactly what to do.",
         "One major decision you're stuck on",
         "90-minute session &middot; from $1,200"),
        ("service-planning-strategy.html", IC["chart"], "Planning &amp; strategy",
         "From a goal to a concrete plan.",
         "We turn a goal that matters into a clear, sequenced plan with milestones, so you always know the next move and the right time to make it.",
         "A goal with lots of moving parts",
         "Multi-session engagement &middot; from $3,500"),
        ("service-second-opinion.html", IC["check"], "Second opinion review",
         "An honest check before you sign.",
         "Already holding a proposal or quote? We review it independently and tell you plainly whether it stacks up - and what to question first.",
         "A proposal you're about to commit to",
         "Independent review &middot; from $900"),
        ("service-ongoing-advisory.html", IC["clock"], "Ongoing advisory",
         "A steady hand, year after year.",
         "A trusted advisor on call for the long run - regular sit-downs and an impartial person to think things through with whenever life calls for it.",
         "Decisions that keep coming up",
         "Annual retainer &middot; from $4,800"),
    ]

    # =========================================================================
    # HOME
    # =========================================================================
    TESTI = [
        ("RM", "I'd been going in circles for months. One session and I finally knew what to do - and why.", "Rebecca M.", "Subiaco, WA"),
        ("DP", "Honest, calm and completely on my side. Worth every cent of the fixed fee.", "Daniel &amp; Priya T.", "Norwood, SA"),
        ("GH", "They reviewed a proposal I was about to sign and saved me from a costly mistake.", "Geoffrey H.", "Hawthorn, VIC"),
        ("HV", "Everyone had an opinion. Clear Sky Consulting had no agenda - which is exactly what I needed.", "Helen V.", "Unley, SA"),
        ("OK", "Calm, fast and completely unbiased. We finally stopped second-guessing ourselves.", "The Okafor family", "Ipswich, QLD"),
        ("TB", "I had one day to decide. Their review gave me the confidence to push back - and it worked.", "Tom B.", "Spearwood, WA"),
    ]
    testi_html = "".join(f'''<figure class="tcard reveal">
        <div class="stars" aria-label="Rated 5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;{quote}&rdquo;</blockquote>
        <figcaption><span class="tavatar">{ini}</span><span class="twho"><b>{name}</b>{loc}</span></figcaption>
      </figure>''' for ini, quote, name, loc in TESTI)

    faces = "".join(f'''<a class="tt-face reveal" href="leadership.html">
        <img src="assets/{p['img']}" alt="Portrait of {p['name']}" loading="lazy" width="120" height="120">
        <b>{p['name']}</b><span>{p['role']}</span>
      </a>''' for p in EXEC[:5])

    logo_names = ["The Australian", "Financial Review", "ABC News", "Sydney Morning Herald", "Forbes AU", "Sky Business"]
    logo_track = "".join(f"<span>{n}</span>" for n in logo_names * 2)

    home = f'''
  <section class="hero hero-v2">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="hero-grid">
        <div class="hero-copy">
          <span class="eyebrow hero-anim">Independent personal advisory &middot; Five offices across Australia</span>
          <h1 class="hero-anim">Clear thinking for life's <em>bigger decisions.</em></h1>
          <p class="lead hero-anim">Clear Sky Consulting is one of Australia's largest independent personal advisory practices. When a decision feels too big to weigh up alone, we sit down with you in person and help you see it clearly.</p>
          <div class="hero-actions hero-anim">
            <a class="btn btn-primary" href="contact.html">Book a free meeting</a>
            <a class="btn btn-ghost" href="services.html">Explore what we do</a>
          </div>
          <div class="hero-rating hero-anim">
            <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span>Rated <b>4.9/5</b> by 25,000+ clients across Australia</span>
          </div>
        </div>
        <div class="hero-visual hero-anim" aria-hidden="true">
          <div class="hv-card">
            <svg class="hv-sky" viewBox="0 0 560 460" preserveAspectRatio="xMidYMid slice">
              <defs>
                <linearGradient id="hsky" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0" stop-color="#fdfdfe"/><stop offset=".5" stop-color="#dcebf6"/><stop offset="1" stop-color="#f5e6cf"/>
                </linearGradient>
                <radialGradient id="hsun" cx="50%" cy="50%" r="50%">
                  <stop offset="0" stop-color="#F7CD78"/><stop offset="1" stop-color="#E2A24A"/>
                </radialGradient>
              </defs>
              <rect width="560" height="460" fill="url(#hsky)"/>
              <circle cx="392" cy="150" r="82" fill="#E2A24A" opacity=".16"/>
              <circle class="hv-sun" cx="392" cy="150" r="54" fill="url(#hsun)"/>
              <g fill="#ffffff" opacity=".9">
                <ellipse cx="135" cy="135" rx="48" ry="16"/><ellipse cx="178" cy="125" rx="32" ry="13"/>
                <ellipse cx="455" cy="255" rx="38" ry="13"/>
              </g>
              <path d="M0 330 Q140 290 280 320 T560 320 V460 H0 Z" fill="#bcd6ea" opacity=".55"/>
              <path d="M0 372 Q160 330 320 360 T560 360 V460 H0 Z" fill="#9ec3df" opacity=".6"/>
              <path d="M0 408 Q180 376 360 402 T560 402 V460 H0 Z" fill="#7fb0d2" opacity=".7"/>
            </svg>
          </div>
          <div class="hv-chip hv-chip-1"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>Independent &amp; impartial</div>
          <div class="hv-chip hv-chip-2"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/></svg>Fixed fee, agreed upfront</div>
          <div class="hv-chip hv-chip-3"><span class="hv-score">+82</span><span class="hv-score-l">Net Promoter<br>Score</span></div>
        </div>
      </div>
    </div>
    <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
  </section>

  <div class="metrics-band">
    <div class="wrap">
      <div class="metrics-row reveal">
        <div class="mb"><div class="mb-n"><span class="count" data-to="25000" data-comma="1">0</span><span class="dawn">+</span></div><div class="mb-l">Clients advised since 2018</div></div>
        <div class="mb"><div class="mb-n">$<span class="count" data-to="48">0</span><span class="dawn">B+</span></div><div class="mb-l">In client decisions supported</div></div>
        <div class="mb"><div class="mb-n"><span class="count" data-to="98">0</span>%</div><div class="mb-l">Client satisfaction</div></div>
        <div class="mb"><div class="mb-n"><span class="count" data-to="4.9" data-dec="1">0</span><span class="dawn">/5</span></div><div class="mb-l">Average client rating</div></div>
      </div>
    </div>
  </div>

  {trust_strip()}

  <div class="logos logo-marquee">
    <div class="wrap"><p class="k">As featured in</p></div>
    <div class="logo-viewport"><div class="logo-track">{logo_track}</div></div>
  </div>

  <section class="block">
    <div class="wrap lead-2col reveal">
      <div>
        <span class="eyebrow">Our approach</span>
        <h2>Advice that works for you, not for anyone selling to you.</h2>
      </div>
      <div class="body">
        <p>Most people facing a major decision aren't short of information - they're short of clarity. There's too much of it, it conflicts, and everyone offering an opinion has something to gain.</p>
        <p>Clear Sky Consulting sits entirely on your side of the table. We take the time to understand your situation, lay out your real options in plain language, and help you choose the path that fits your life - not a one-size-fits-all answer.</p>
        <ul class="ticks">
          <li>Paid only by you - never a commission or a kickback</li>
          <li>Every meeting in person, never rushed</li>
          <li>A fixed fee, agreed before any work begins</li>
          <li>Plain English, with no hidden agenda</li>
        </ul>
        <p style="margin-top:.4rem"><a class="btn btn-ghost" href="approach.html">See how we work &rarr;</a></p>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">What we help with</span>
        <h2>Ways we work together</h2>
        <p>Whatever you're weighing up, every engagement is shaped around your situation - delivered in person, with a fixed fee agreed upfront. Here's how clients most often start.</p>
      </div>
      <div class="svc-grid">
        {''.join(service_card(*s) for s in SERVICES)}
      </div>
    </div>
  </section>

  <section class="stats-band block">
    <div class="wrap">
      <div class="section-head center reveal" style="color:#fff">
        <span class="eyebrow" style="color:#E2A24A">By the numbers</span>
        <h2 style="color:#fff">A practice built at national scale</h2>
      </div>
      <div class="stats-grid reveal">
        <div class="s"><div class="n"><span class="count" data-to="240">0</span><span class="dawn">+</span></div><div class="l">Advisors &amp; staff nationally</div></div>
        <div class="s"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Offices across Australia</div></div>
        <div class="s"><div class="n"><span class="count" data-to="25">0</span><span class="dawn">k+</span></div><div class="l">Clients advised</div></div>
        <div class="s"><div class="n"><span class="count" data-to="15">0</span><span class="dawn">+</span></div><div class="l">Industry awards won</div></div>
        <div class="s"><div class="n"><span class="count" data-to="100">0</span>%</div><div class="l">Commission-free advice</div></div>
      </div>
    </div>
  </section>

  <section class="block" id="how">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">How it works</span>
        <h2>A simple, four-step process</h2>
        <p>Clear from the first conversation. You'll always know where things stand and what happens next.</p>
      </div>
      <div class="steps process">
        <div class="step reveal"><h3>Free intro meeting</h3><p>A relaxed first meeting at your nearest office to hear what's on your mind and decide together whether we're the right fit. No cost, no obligation.</p></div>
        <div class="step reveal"><h3>Understand &amp; scope</h3><p>We dig into the detail of your situation and agree exactly what you want from the work - with a fixed fee quoted upfront.</p></div>
        <div class="step reveal"><h3>Clear recommendations</h3><p>You receive considered, plain-English advice that lays out your options and our honest view on the best way forward.</p></div>
        <div class="step reveal"><h3>Move forward</h3><p>We help you act on the plan and stay available for the questions that come up once you're underway.</p></div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">In their words</span>
        <h2>Trusted by thousands of Australians</h2>
        <p>A 4.9/5 average rating and an industry-leading Net Promoter Score of +82. Here's a little of why.</p>
      </div>
      <div class="tgrid">{testi_html}</div>
      <p style="text-align:center;margin-top:2.2rem"><a class="btn btn-ghost" href="case-studies.html">Read full client stories &rarr;</a></p>
    </div>
  </section>

  <section class="block team-teaser">
    <div class="wrap">
      <div class="tt-grid">
        <div class="tt-copy reveal">
          <span class="eyebrow">The people behind the advice</span>
          <h2>You'll work with a real advisor - start to finish.</h2>
          <p>We keep our practice deliberately personal. The advisor who understands your situation in the first meeting is the same one with you at the last - backed by an experienced national team and an independent board.</p>
          <a class="btn btn-ghost" href="leadership.html">Meet the team &rarr;</a>
        </div>
        <div class="tt-faces">{faces}</div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">Latest thinking</span>
        <h2>From our Insights desk</h2>
        <p>Plain-English perspective on making big decisions well.</p>
      </div>
      {insights_grid(g, limit=3)}
      <p style="margin-top:2rem"><a class="btn btn-ghost" href="insights.html">All insights &rarr;</a></p>
    </div>
  </section>

  {cta_band()}
'''
    page("index.html", "Independent Personal Advisory in Australia | Clear Sky Consulting",
         "Independent, commission-free personal advisory for individuals and families across Australia. Get clarity on life's bigger decisions, in person, for a fixed fee. Five offices nationwide.",
         None, home)

    # =========================================================================
    # ABOUT
    # =========================================================================
    founder_faces = "".join(f'''<a class="tt-face reveal" href="leadership.html">
        <img src="assets/{p['img']}" alt="Portrait of {p['name']}" loading="lazy" width="120" height="120">
        <b>{p['name']}</b><span>{p['role']}</span>
      </a>''' for p in EXEC[:2])
    about = f'''
  {page_hero("About us", "About Clear Sky Consulting", "The people in <em>your corner.</em>",
             "Clear Sky Consulting was founded by two advisors tired of watching good people make big decisions with conflicted advice. Today we're a national practice that has never wavered from that founding promise.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap split reveal">
      <div class="media"><img src="assets/{scene("scene-about","thumb-4.svg")}" alt="Clear Sky Consulting - independent personal advisory for Australian individuals and families" loading="lazy" width="640" height="360"></div>
      <div>
        <span class="eyebrow">Our mission</span>
        <h2>Clarity, for everyone facing a decision that matters.</h2>
        <p>Clear Sky Consulting Pty Ltd began in 2018 with a single conviction: everyone deserves advice that is genuinely, demonstrably in their corner - free of commissions, sales targets and hidden incentives.</p>
        <p>Our founders had spent two decades inside large institutions, and had seen how easily a client's best interest gets crowded out. So they left, and built something deliberately different.</p>
        <ul class="ticks">
          <li>Independent and impartial, by design</li>
          <li>One advisor, from your first meeting to your last</li>
          <li>Advice tailored to your life, not a product shelf</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n">2018</div><div class="l">Founded in Perth</div></div>
        <div class="s"><div class="n"><span class="count" data-to="240">0</span><span class="dawn">+</span></div><div class="l">People nationally</div></div>
        <div class="s"><div class="n"><span class="count" data-to="25">0</span><span class="dawn">k+</span></div><div class="l">Clients advised</div></div>
        <div class="s"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Offices</div></div>
        <div class="s"><div class="n"><span class="count" data-to="15">0</span><span class="dawn">+</span></div><div class="l">Industry awards won</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">The difference</span><h2>Advice without the tilt</h2><p>Most advice comes with an incentive quietly attached. Ours doesn't - and that changes everything.</p></div>
      <div class="compare reveal">
        <div class="cmp cmp-usual">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>The usual way</h3>
          <ul>
            <li>Paid by commissions and product sales</li>
            <li>Advice nudged toward what pays the adviser</li>
            <li>Hourly meters, or fees hidden inside products</li>
            <li>You get handed off between people</li>
            <li>Jargon that keeps you dependent</li>
          </ul>
        </div>
        <div class="cmp cmp-cs">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>The Clear Sky Consulting way</h3>
          <ul>
            <li>Paid only by you - no commissions, ever</li>
            <li>Advice pointed entirely at your interest</li>
            <li>A single fixed fee, agreed upfront</li>
            <li>One advisor, from start to finish</li>
            <li>Plain English you can act on</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Our journey</span><h2>From a single room to a national practice</h2></div>
      <div class="timeline reveal">
        <div class="tl"><div class="yr">2018</div><h3>Clear Sky Consulting opens in Perth</h3><p>Kenneth Jimmieson and Mei Lin Tan open the first office on Kings Park Road with one promise: advice with no hidden agenda.</p></div>
        <div class="tl"><div class="yr">2019</div><h3>Adelaide &amp; Brisbane</h3><p>Word of mouth carries the practice east. Two new offices open within fourteen months.</p></div>
        <div class="tl"><div class="yr">2021</div><h3>10,000th client</h3><p>The firm marks its ten-thousandth engagement and is named Independent Advisory Firm of the Year.</p></div>
        <div class="tl"><div class="yr">2022</div><h3>Sydney &amp; Bendigo</h3><p>A flagship Sydney office and a regional Victorian practice complete the national footprint.</p></div>
        <div class="tl"><div class="yr">2023</div><h3>Independence charter</h3><p>Clear Sky Consulting formalises its independence charter - no commissions, no products - overseen by a newly appointed independent board.</p></div>
        <div class="tl"><div class="yr">2026</div><h3>25,000 clients &amp; counting</h3><p>The practice supports more than $48 billion in client decisions while keeping every meeting face to face.</p></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">What we stand for</span><h2>The principles behind every engagement</h2><p>These aren't a poster on the wall. They're the rules we built the practice around.</p></div>
      <div class="values">
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['shield']}</svg></div><h3>Genuinely independent</h3><p>No commissions, no referral kickbacks, no products to push. The only party we answer to is you.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 2a5 5 0 015 5v3H7V7a5 5 0 015-5z"/><rect x="5" y="10" width="14" height="11" rx="2"/></svg></div><h3>Strictly confidential</h3><p>What you share with us stays between us. Discretion is the foundation of honest advice.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['scale']}</svg></div><h3>Fixed, upfront fees</h3><p>You'll know exactly what the work costs before it begins. No surprises, no meter running.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['spark']}</svg></div><h3>Plain English, always</h3><p>If we can't explain it simply, we haven't thought about it clearly enough. No jargon, ever.</p></div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Recognition</span><h2>Trusted, and recognised for it</h2></div>
      <div class="awards reveal">
        <div class="award"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M8 21h8M12 17v4M5 4h14v4a7 7 0 01-14 0z"/></svg><span><strong>Advisory Firm of the Year</strong>Independent Finance Awards, 2024</span></div>
        <div class="award"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M8 21h8M12 17v4M5 4h14v4a7 7 0 01-14 0z"/></svg><span><strong>Best Client Experience</strong>National Advisory Index, 2025</span></div>
        <div class="award"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M8 21h8M12 17v4M5 4h14v4a7 7 0 01-14 0z"/></svg><span><strong>Employer of Choice</strong>AU Workplace Awards, 2025</span></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="tt-grid">
        <div class="tt-copy reveal">
          <span class="eyebrow">Our founders</span>
          <h2>Meet the people who started it.</h2>
          <p>Clear Sky Consulting is still led, day to day, by the two advisors who founded it - alongside an experienced executive team and an independent board.</p>
          <a class="btn btn-ghost" href="leadership.html">Meet the full team &rarr;</a>
        </div>
        <div class="tt-faces">{founder_faces}</div>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page("about.html", "About Us - Independent Advisory Firm | Clear Sky Consulting",
         "Meet Clear Sky Consulting - one of Australia's largest independent personal advisory practices. Our mission, story, values and recognition.",
         "about.html", about)

    # =========================================================================
    # LEADERSHIP
    # =========================================================================
    leadership = f'''
  {page_hero("Leadership &amp; board", "Leadership &amp; board", "Accountable to <em>you.</em>",
             "An experienced executive team and an independent board keep Clear Sky Consulting true to its founding promise. Reach any of us - our doors, and our inboxes, are open.")}
  {trust_strip()}

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n"><span class="count" data-to="8">0</span></div><div class="l">On the executive team</div></div>
        <div class="s"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Independent directors</div></div>
        <div class="s"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Regional managing directors</div></div>
        <div class="s"><div class="n"><span class="count" data-to="240">0</span><span class="dawn">+</span></div><div class="l">People they lead</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Executive team</span><h2>The people who run Clear Sky Consulting</h2><p>Eight leaders responsible for advice quality, clients, people and performance - and reachable directly.</p></div>
      <div class="team-grid">
        {''.join(member_card(p) for p in EXEC)}
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Board of directors</span><h2>Independent oversight</h2><p>A majority-independent board safeguards the firm's independence and your interests.</p></div>
      <div class="team-grid">
        {''.join(member_card(p, with_links=False) for p in BOARD)}
      </div>
      <div class="callout reveal" style="max-width:820px;margin:2.4rem auto 0">
        <strong>Why an independent board matters.</strong> Most of our directors are independent and non-executive, which means the people guarding our no-commission promise don't answer to the people who run the business day to day. It's a deliberate check - independence you can hold us to, not just take our word for.
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Around the country</span><h2>Your regional managing directors</h2><p>The experienced advisor who leads your nearest office.</p></div>
      <div class="team-grid">
        {''.join(member_card(p) for p in REGIONAL)}
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Independent advisors</span><h2>Our independent advisors</h2><p>Experienced, independent advisors you can work with directly across the country.</p></div>
      <div class="team-grid">
        {''.join(member_card(p) for p in ADVISORS)}
      </div>
    </div>
  </section>

  {cta_band()}
'''
    def _person_node(p):
        node = {"@type": "Person", "name": p["name"], "jobTitle": plain(p["role"]),
                "worksFor": {"@id": ORG_ID}, "image": f"{SITE_URL}/assets/{p['img']}"}
        if p.get("email"):
            node["email"] = p["email"]
        if p.get("bio"):
            node["description"] = plain(p["bio"])
        return node
    people_ld = jsonld({"@context": "https://schema.org",
                        "@graph": [_person_node(p) for p in EXEC + BOARD + REGIONAL + ADVISORS]})
    page("leadership.html", "Leadership &amp; Board | Clear Sky Consulting",
         "Meet the executive team, board of directors, regional managing directors and independent advisors of Clear Sky Consulting.",
         "about.html", leadership, extra_head=people_ld)

    # =========================================================================
    # INDIVIDUAL TEAM / PROFILE PAGES
    # =========================================================================
    all_people = EXEC + BOARD + REGIONAL + ADVISORS
    group_of = {id(p): g_ for g_, lst in
                (("Executive team", EXEC), ("Board of directors", BOARD),
                 ("Regional managing directors", REGIONAL), ("Independent advisors", ADVISORS))
                for p in lst}
    for p in all_people:
        first = p["name"].split()[0]
        group = group_of[id(p)]
        contact = ""
        if p.get("email"):
            contact = f'''<div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg><div><div class="k">Email</div><div class="v">{mail(p['email'])}</div></div></div>
        <div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg><div><div class="k">Phone</div><div class="v">{tel(p['phone'])}</div></div></div>'''
        bio = p.get("bio", f"{first} is part of the team at Clear Sky Consulting.")
        # a few colleagues from the same group for cross-linking
        peers = [q for q in all_people if group_of[id(q)] == group and q["name"] != p["name"]][:3]
        peer_cards = "".join(
            f'''<a class="tt-face reveal" href="{team_file(q)}">
          <img src="assets/{q['img']}" alt="Portrait of {q['name']}" loading="lazy" width="120" height="120">
          <b>{q['name']}</b><span>{q['role']}</span>
        </a>''' for q in peers)
        crumb = f'<a href="leadership.html">Leadership</a> &middot; {p["name"]}'
        body = f'''
  {page_hero(crumb, group, p["name"], p["role"])}
  {trust_strip()}

  <section class="block">
    <div class="wrap split reveal">
      <div class="media"><img src="assets/{p['img']}" alt="Portrait of {p['name']}, {plain(p['role'])} at Clear Sky Consulting" width="400" height="500" style="border-radius:18px"></div>
      <div>
        <span class="eyebrow">{group}</span>
        <h2>{p['name']}</h2>
        <p class="role" style="color:var(--sky-deep);font-weight:600;margin-bottom:1rem">{p['role']}</p>
        <p>{bio}</p>
        <p>Like everyone at Clear Sky Consulting, {first} is paid only by the clients they advise - never by commission - and stays with you from the first meeting through to the last.</p>
        {f'<div class="contact-details" style="margin:1.4rem 0">{contact}</div>' if contact else ''}
        <a class="btn btn-primary" href="contact.html">Book a meeting</a>
        <a class="btn btn-ghost" href="leadership.html">Back to the team</a>
      </div>
    </div>
  </section>
  {f"""
  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">{group}</span><h2>Others on the team</h2></div>
      <div class="tt-faces">{peer_cards}</div>
    </div>
  </section>""" if peer_cards else ""}

  {cta_band()}
'''
        person_ld = jsonld({
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "mainEntity": {
                "@type": "Person",
                "name": p["name"],
                "jobTitle": plain(p["role"]),
                "worksFor": {"@id": ORG_ID},
                "url": f"{SITE_URL}/{team_file(p)}",
                "image": f"{SITE_URL}/assets/{p['img']}",
                "description": plain(bio),
                **({"email": p["email"]} if p.get("email") else {}),
                **({"telephone": p["phone"]} if p.get("phone") else {}),
            },
        })
        page(team_file(p), f"{p['name']} - {plain(p['role'])} | Clear Sky Consulting",
             plain(bio), "about.html", body, extra_head=person_ld, og_type="profile")

    # =========================================================================
    # SERVICES OVERVIEW
    # =========================================================================
    services = f'''
  {page_hero("What we do", "What we do", "Four ways to think <em>more clearly.</em>",
             "Every engagement is shaped around your situation, delivered in person, and priced as a fixed fee agreed upfront. Here's how clients most often work with us.")}
  {trust_strip()}

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n"><span class="count" data-to="4">0</span></div><div class="l">Ways to work together</div></div>
        <div class="s"><div class="n"><span class="count" data-to="25">0</span><span class="dawn">k+</span></div><div class="l">Clients advised</div></div>
        <div class="s"><div class="n">100%</div><div class="l">Fixed-fee, commission-free</div></div>
        <div class="s"><div class="n"><span class="count" data-to="98">0</span>%</div><div class="l">Client satisfaction</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Our services</span><h2>Pick the shape that fits</h2><p>Each one is a fixed-fee engagement, delivered in person. Not sure which you need? <a href="find-your-service.html">Take our 60-second quiz</a> and we'll point you the right way.</p></div>
      <div class="svc-grid">
        {''.join(service_card(*s) for s in SERVICES)}
      </div>
      <p style="text-align:center;margin-top:2.2rem"><a class="btn btn-ghost" href="find-your-service.html">Not sure? Find your service &rarr;</a></p>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">The Clear Sky Consulting difference</span><h2>What you get, every single time</h2></div>
      <div class="values">
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['shield']}</svg></div><h3>A truly independent view</h3><p>We're paid only by you, so our only incentive is to get your decision right.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg></div><h3>Face-to-face advice</h3><p>We meet in person at one of five offices - never rushed, never by phone.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['scale']}</svg></div><h3>A fixed fee upfront</h3><p>You'll know the cost before any work begins. No meter, no surprises.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['spark']}</svg></div><h3>Plain-English clarity</h3><p>Considered recommendations you can actually act on, free of jargon.</p></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <figure class="svc-quote reveal">
        <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;I'd been going in circles for months. One session and I finally knew what to do - and why.&rdquo;</blockquote>
        <figcaption>Rebecca M., Subiaco WA</figcaption>
      </figure>
    </div>
  </section>

  {cta_band()}
'''
    page("services.html", "Independent Advisory Services in Australia | Clear Sky Consulting",
         "The four ways clients work with Clear Sky Consulting: decision clarity sessions, planning &amp; strategy, second-opinion reviews and ongoing advisory.",
         "services.html", services)

    # ---- individual service pages ------------------------------------------
    SVC_EXTRA = {
        "service-decision-clarity.html": dict(
            facts=[("90 min", "A focused session"), ("from $1,200", "One fixed fee"), ("2 days", "Written summary")],
            quote=("I'd been going in circles for months. One session and I finally knew what to do - and why.", "Rebecca M., Subiaco WA")),
        "service-planning-strategy.html": dict(
            facts=[("3-5", "Sessions over weeks"), ("from $3,500", "One fixed fee"), ("Milestones", "A clear staged plan")],
            quote=("They turned a vague dream into a month-by-month plan I actually trusted.", "Nadia K., Carlton VIC")),
        "service-second-opinion.html": dict(
            facts=[("2-3 days", "Typical turnaround"), ("from $900", "One fixed fee"), ("Written", "Verdict &amp; questions")],
            quote=("They reviewed a proposal I was about to sign and saved me from a costly mistake.", "Geoffrey H., Hawthorn VIC")),
        "service-ongoing-advisory.html": dict(
            facts=[("2-4 / yr", "In-person reviews"), ("from $4,800", "Per year, fixed"), ("On call", "Between meetings")],
            quote=("Knowing I could pick up the phone to someone genuinely on my side changed everything.", "Margaret S., New Farm QLD")),
    }

    def service_page(fn, crumb, eyebrow, h1, lead, intro, for_you, includes, faq_items):
        extra = SVC_EXTRA[fn]
        ticks = "".join(f"<li>{x}</li>" for x in for_you)
        inc = "".join(f'''<div class="step reveal"><h3>{t}</h3><p>{d}</p></div>''' for t, d in includes)
        facts_html = "".join(f'<div class="metric reveal"><div class="n">{v}</div><div class="l">{l}</div></div>' for v, l in extra["facts"])
        slug = fn.replace(".html", "")
        qas = ""
        for i, (q, a) in enumerate(faq_items):
            qid = f"{slug}-{i}"
            qas += f'''<div class="qa reveal">
            <button class="qa-q" aria-expanded="false" id="{qid}-q" aria-controls="{qid}-a"><span class="qa-q-txt">{q}</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button>
            <div class="qa-a" id="{qid}-a" role="region" aria-labelledby="{qid}-q"><div class="qa-a-inner"><p>{a}</p></div></div>
          </div>'''
        others = [s for s in SERVICES if s[0] != fn]
        rel = "".join(service_card(*s) for s in others)
        qtext, qwho = extra["quote"]
        svc_meta = next((s for s in SERVICES if s[0] == fn), None)
        svc_obj = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": plain(h1),
            "serviceType": plain(eyebrow),
            "description": plain(lead),
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "Country", "name": "Australia"},
            "url": f"{SITE_URL}/{fn}",
        }
        if svc_meta:
            m = re.search(r"\$([\d,]+)", svc_meta[6])
            if m:
                svc_obj["offers"] = {
                    "@type": "Offer",
                    "price": m.group(1).replace(",", ""),
                    "priceCurrency": "AUD",
                    "availability": "https://schema.org/InStock",
                    "url": f"{SITE_URL}/{fn}",
                }
        service_ld = jsonld(svc_obj)
        body = f'''
  {page_hero(crumb, eyebrow, h1, lead)}
  {trust_strip()}

  <section class="block" style="padding-bottom:0">
    <div class="wrap">
      <div class="metric-grid reveal" style="max-width:840px;margin-inline:auto">{facts_html}</div>
    </div>
  </section>

  <section class="block">
    <div class="wrap split reveal">
      <div class="media"><img src="assets/{scene('scene-' + slug.replace('service-', ''), f"thumb-{intro['thumb']}.svg")}" alt="{plain(eyebrow)} - independent, fixed-fee advice from Clear Sky Consulting" loading="lazy" width="640" height="360"></div>
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h2>{intro['h2']}</h2>
        <p>{intro['p1']}</p>
        <p>{intro['p2']}</p>
        <p class="ticks-label">Is this you?</p>
        <ul class="ticks">{ticks}</ul>
        <a class="btn btn-primary" href="contact.html">Book a free meeting</a>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">What's included</span><h2>How the engagement runs</h2></div>
      <div class="steps process">{inc}</div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <figure class="svc-quote reveal">
        <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;{qtext}&rdquo;</blockquote>
        <figcaption>{qwho}</figcaption>
      </figure>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Good to know</span><h2>Common questions</h2></div>
      <div class="qa-list" style="max-width:780px;margin-inline:auto">{qas}</div>
      <p style="text-align:center;margin-top:2rem"><a class="btn btn-ghost" href="pricing.html">See full pricing &rarr;</a></p>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Other ways we help</span><h2>Explore the rest</h2></div>
      <div class="svc-grid">{rel}</div>
    </div>
  </section>

  {cta_band()}
'''
        page(fn, f"{h1.replace('<em>','').replace('</em>','')} - Clear Sky Consulting", lead, "services.html", body, extra_head=service_ld)

    service_page(
        "service-decision-clarity.html", "Decision clarity session", "Decision clarity session",
        "Untangle one <em>big decision.</em>",
        "A focused session to weigh a single major decision - the options, the risks, the trade-offs - so you leave with a clear next step.",
        dict(thumb=1, h2="When one choice has taken over your thinking",
             p1="Some decisions are big enough that they sit with you for weeks. A clarity session gives that decision a few hours of undivided, expert attention - and gives you a way out of the loop.",
             p2="We map the real options, stress-test each one against what actually matters to you, and separate the noise from the things that truly move the needle."),
        ["You're weighing a single, significant decision",
         "You feel stuck, second-guessing, or going in circles",
         "You want an impartial sounding board with no stake in the outcome",
         "You'd value a clear, written summary you can act on"],
        [("Pre-session brief", "A short questionnaire so we arrive already understanding the shape of your decision."),
         ("The session", "A focused 90-minute sit-down at your nearest office, mapping options and trade-offs together."),
         ("Written summary", "A plain-English recap of the options, our view, and a recommended next step."),
         ("Follow-up", "A check-in to answer anything that surfaces once you've had time to sit with it.")],
        [("How long does it take?", "Most clarity sessions run to about 90 minutes, plus a written summary delivered within two business days."),
         ("Is it really one fixed fee?", "Yes. We quote a single fixed fee before the session, so you know the cost upfront."),
         ("What if I need more than one session?", "Some decisions warrant a follow-up. If so, we'll agree it with you - there's never any obligation.")])

    service_page(
        "service-planning-strategy.html", "Planning &amp; strategy", "Planning &amp; strategy",
        "A clear plan toward a <em>real goal.</em>",
        "A structured plan for a goal that matters - the steps, sequencing and timing - so you always know what to do and when.",
        dict(thumb=2, h2="From a goal to a sequence of clear steps",
             p1="Big goals stall when they stay abstract. We turn yours into a concrete, sequenced plan with milestones you can actually track.",
             p2="Then we pressure-test it: what has to be true, what could go wrong, and what the sensible order of operations really is."),
        ["You have a goal but no clear path to it",
         "Several moving parts need to be sequenced",
         "You want milestones and timing you can hold yourself to",
         "You'd like an advisor to revisit the plan as life changes"],
        [("Discovery", "We get to the bottom of the goal - and why it matters - before we plan a single step."),
         ("Options &amp; sequencing", "We lay out the routes, then agree the smartest order and timing."),
         ("The written plan", "A clear, staged plan with milestones, owners and dates."),
         ("Review cadence", "Optional regular check-ins to keep the plan honest as things change.")],
        [("How detailed is the plan?", "Detailed enough to act on tomorrow - concrete steps, sequence and timing, in plain English."),
         ("Can you work with my other advisors?", "Absolutely. We're happy to sit alongside your accountant, lawyer or other specialists."),
         ("Do you help me execute?", "We can stay involved through our ongoing advisory service, or simply hand you a plan you can run yourself.")])

    service_page(
        "service-second-opinion.html", "Second opinion review", "Second opinion review",
        "An honest check <em>before you sign.</em>",
        "Already have a proposal or quote in hand? We review it independently and tell you, plainly, whether it stacks up.",
        dict(thumb=3, h2="A fresh, impartial set of eyes",
             p1="A second opinion is cheap insurance against an expensive mistake. We read what's in front of you the way you wish you had the time to - line by line.",
             p2="You get a clear verdict: where it's fair, where it isn't, what to question, and whether to proceed."),
        ["You have a proposal, quote or recommendation to assess",
         "The stakes are high and the detail is dense",
         "You want an impartial party with nothing to gain either way",
         "You'd like specific questions to take back before you commit"],
        [("Send it over", "Share the proposal and any background ahead of our meeting."),
         ("Independent review", "We analyse it against your interests - not the seller's."),
         ("Plain verdict", "A clear written view: strengths, red flags, and questions to ask."),
         ("Decision support", "We talk it through so you're confident either way.")],
        [("What can you review?", "Most written proposals and recommendations where the decision is significant and you want an impartial read."),
         ("Will you tell me not to proceed?", "If that's our honest view, yes. We have no stake in your decision - that's the point."),
         ("How fast is it?", "Typically within a few business days, depending on the complexity of what you send.")])

    service_page(
        "service-ongoing-advisory.html", "Ongoing advisory", "Ongoing advisory",
        "A steady hand, <em>year after year.</em>",
        "A trusted advisor for the long run - regular sit-downs and someone to turn to whenever something important comes up.",
        dict(thumb=4, h2="The advisor you call before you decide",
             p1="Life doesn't hand you big decisions on a schedule. Ongoing advisory means you always have an impartial, informed person to think things through with.",
             p2="We hold the context year to year, so every conversation starts from understanding rather than scratch."),
        ["Important decisions come up for you regularly",
         "You value continuity and a relationship over one-off advice",
         "You want a sounding board you can reach between meetings",
         "You'd like an advisor who already knows your situation"],
        [("Onboarding", "We build a full picture of your situation and what matters to you."),
         ("Regular sit-downs", "Scheduled in-person reviews at a cadence that suits you."),
         ("On-call clarity", "Reach your advisor when something important lands."),
         ("Annual review", "A yearly step-back to make sure everything still fits.")],
        [("How often do we meet?", "Most ongoing clients meet two to four times a year, plus ad-hoc conversations as things arise."),
         ("Is there a lock-in?", "No. Ongoing advisory continues only while it's genuinely useful to you."),
         ("How is it priced?", "A simple fixed annual fee, agreed upfront - never a percentage of anything you own.")])

    # =========================================================================
    # FIND YOUR SERVICE (interactive quiz)
    # =========================================================================
    QUIZ = [
        ("What's prompting you to seek advice?", [
            ("clarity", "A single decision I keep going around on"),
            ("planning", "A goal I'd like turned into a real plan"),
            ("second", "A proposal or quote I need checked before I commit"),
            ("ongoing", "Lots of decisions, with no single trigger"),
        ]),
        ("What outcome would feel like success?", [
            ("clarity", "Knowing exactly what to do about one thing"),
            ("planning", "A clear, staged roadmap toward a goal"),
            ("second", "An honest, independent verdict before I sign"),
            ("ongoing", "A trusted advisor who knows my situation over time"),
        ]),
        ("What's your timeframe?", [
            ("second", "Right now - there's something in front of me to sign"),
            ("clarity", "Soon - I need to make one decision shortly"),
            ("planning", "The coming weeks or months"),
            ("ongoing", "Ongoing, with no real end date"),
        ]),
    ]
    steps_html = ""
    for si, (q, opts) in enumerate(QUIZ):
        opt_html = "".join(
            f'<button type="button" class="quiz-opt" data-svc="{svc}">{txt}'
            f'<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>'
            for svc, txt in opts)
        steps_html += f'''<fieldset class="quiz-step{' is-active' if si == 0 else ''}" data-step="{si}"{'' if si == 0 else ' hidden'}>
          <legend>{q}</legend>
          <div class="quiz-opts">{opt_html}</div>
        </fieldset>'''
    quiz = f'''
  {page_hero("Find your service", "Find your service", "Which service fits <em>you?</em>",
             "Answer three quick questions and we'll point you to the way of working that best matches your situation. It takes about a minute - and there's nothing to fill in.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap" style="max-width:760px">
      <div class="quiz" id="quiz">
        <div class="quiz-top">
          <p class="quiz-count" id="quizCount">Question 1 of {len(QUIZ)}</p>
          <div class="quiz-progress"><span class="quiz-bar" id="quizBar" style="width:{round(100/len(QUIZ))}%"></span></div>
        </div>
        {steps_html}
        <div class="quiz-result" id="quizResult" hidden></div>
        <button type="button" class="quiz-back" id="quizBack" hidden>&larr; Back</button>
        <noscript><p class="form-note">This quiz needs JavaScript. You can always <a href="services.html">see all four services</a> or <a href="contact.html">book a free meeting</a> and we'll point you the right way.</p></noscript>
      </div>
    </div>
  </section>

  {cta_band("Prefer to just talk it through?", "Your first meeting is complimentary, in person, and entirely without obligation - and we'll help you choose.")}
'''
    page("find-your-service.html", "Which Service Is Right for You? | Clear Sky Consulting",
         "Take our 60-second quiz to find the Clear Sky Consulting service that best fits your situation - a decision clarity session, planning, a second opinion or ongoing advisory.",
         "services.html", quiz)

    # =========================================================================
    # APPROACH
    # =========================================================================
    approach = f'''
  {page_hero("Our approach", "Our approach", "How we think, <em>step by step.</em>",
             "Independence isn't a slogan for us - it's a method. Here's exactly how an engagement runs, and the principles underneath it.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">The process</span><h2>A simple, four-step process</h2><p>Clear from the first conversation - you'll always know where things stand and what happens next.</p></div>
      <div class="steps process">
        <div class="step reveal"><h3>Free intro meeting</h3><p>A relaxed first meeting to hear what's on your mind and decide together whether we're the right fit. No cost, no obligation.</p></div>
        <div class="step reveal"><h3>Understand &amp; scope</h3><p>We dig into the detail and agree exactly what you want from the work - with a fixed fee quoted upfront.</p></div>
        <div class="step reveal"><h3>Clear recommendations</h3><p>You receive considered, plain-English advice that lays out your options and our honest view on the best way forward.</p></div>
        <div class="step reveal"><h3>Move forward</h3><p>We help you act on the plan and stay available for the questions that come up once you're underway.</p></div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap split reverse reveal">
      <div class="media"><img src="assets/{scene("scene-approach","thumb-5.svg")}" alt="Independent, fixed-fee advice with no commissions - the Clear Sky Consulting approach" loading="lazy" width="640" height="360"></div>
      <div>
        <span class="eyebrow">Why it works</span>
        <h2>Independence, by design</h2>
        <p>We take no commissions and sell no products, so there's never a reason to steer you anywhere but the right place. That independence is written into our constitution and overseen by an independent board.</p>
        <ul class="ticks">
          <li>Paid only by you - never by a third party</li>
          <li>No product shelf, no sales targets</li>
          <li>Fixed fees agreed before any work begins</li>
          <li>Every meeting in person, never rushed</li>
        </ul>
        <a class="btn btn-primary" href="contact.html">Book your intro meeting</a>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">The difference</span><h2>Advice without the tilt</h2><p>Most advice comes with an incentive quietly attached. Ours doesn't.</p></div>
      <div class="compare reveal">
        <div class="cmp cmp-usual">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>The usual way</h3>
          <ul>
            <li>Paid by commissions and product sales</li>
            <li>Advice nudged toward what pays the adviser</li>
            <li>Hourly meters, or fees hidden in products</li>
            <li>You get handed off between people</li>
          </ul>
        </div>
        <div class="cmp cmp-cs">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>The Clear Sky Consulting way</h3>
          <ul>
            <li>Paid only by you - no commissions, ever</li>
            <li>Advice pointed entirely at your interest</li>
            <li>A single fixed fee, agreed upfront</li>
            <li>One advisor, from start to finish</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Good to know</span><h2>How we work, answered</h2></div>
      <div class="qa-list" style="max-width:780px;margin-inline:auto">
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="ap-0-q" aria-controls="ap-0-a"><span class="qa-q-txt">Do I have to commit to anything at the first meeting?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="ap-0-a" role="region" aria-labelledby="ap-0-q"><div class="qa-a-inner"><p>Not at all. The first meeting is complimentary and without obligation. Nothing begins until we've agreed a clear scope and fixed fee in writing.</p></div></div></div>
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="ap-1-q" aria-controls="ap-1-a"><span class="qa-q-txt">How do you keep advice genuinely independent?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="ap-1-a" role="region" aria-labelledby="ap-1-q"><div class="qa-a-inner"><p>We accept no commissions, referral fees or product incentives - the only money on the table is the fee you pay us. It's written into our constitution and overseen by a majority-independent board.</p></div></div></div>
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="ap-2-q" aria-controls="ap-2-a"><span class="qa-q-txt">Will you work alongside my accountant or lawyer?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="ap-2-a" role="region" aria-labelledby="ap-2-q"><div class="qa-a-inner"><p>Gladly. Where a decision needs a licensed specialist we'll say so, and we're happy to sit alongside your existing advisers rather than replace them.</p></div></div></div>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page("approach.html", "Our Approach to Independent Advice | Clear Sky Consulting",
         "How Clear Sky Consulting works: a simple four-step process built on genuine independence, fixed fees and face-to-face advice.",
         "services.html", approach)

    # =========================================================================
    # PRICING
    # =========================================================================
    pricing = f'''
  {page_hero("Pricing", "Pricing", "Fixed fees, <em>agreed upfront.</em>",
             "No commissions. No percentages. No meter running. You'll know exactly what an engagement costs before any work begins. Indicative fees are shown below.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap">
      <div class="price-grid">
        <div class="plan reveal">
          <h3>Clarity session</h3>
          <div class="price">$1,200 <small>fixed</small></div>
          <p class="desc">A single big decision, untangled in one focused sitting.</p>
          <ul>
            <li>90-minute in-person session</li>
            <li>Pre-session brief</li>
            <li>Written summary &amp; next step</li>
            <li>One follow-up check-in</li>
          </ul>
          <a class="btn btn-ghost" href="service-decision-clarity.html">Learn more</a>
        </div>
        <div class="plan featured reveal">
          <h3>Planning &amp; strategy</h3>
          <div class="price">from $3,500 <small>fixed</small></div>
          <p class="desc">A structured, sequenced plan for a goal that matters.</p>
          <ul>
            <li>Discovery &amp; goal-setting</li>
            <li>Options &amp; sequencing</li>
            <li>Full written plan with milestones</li>
            <li>Two review sessions included</li>
          </ul>
          <a class="btn btn-primary" href="service-planning-strategy.html">Learn more</a>
        </div>
        <div class="plan reveal">
          <h3>Second opinion</h3>
          <div class="price">from $900 <small>fixed</small></div>
          <p class="desc">An independent read on a proposal before you commit.</p>
          <ul>
            <li>Independent document review</li>
            <li>Written verdict &amp; red flags</li>
            <li>Questions to take back</li>
            <li>Decision-support call</li>
          </ul>
          <a class="btn btn-ghost" href="service-second-opinion.html">Learn more</a>
        </div>
        <div class="plan reveal">
          <h3>Ongoing advisory</h3>
          <div class="price">from $4,800 <small>/year</small></div>
          <p class="desc">A trusted advisor on call, year after year.</p>
          <ul>
            <li>Full onboarding</li>
            <li>2-4 in-person reviews a year</li>
            <li>On-call clarity between meetings</li>
            <li>Annual step-back review</li>
          </ul>
          <a class="btn btn-ghost" href="service-ongoing-advisory.html">Learn more</a>
        </div>
      </div>
      <div class="callout reveal" style="margin-top:2rem">Every engagement begins with a <strong>complimentary intro meeting</strong>. Final fees are confirmed in writing before any paid work starts. Fees shown are indicative and exclude GST.</div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Included as standard</span><h2>What every fee buys you</h2></div>
      <div class="values">
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['shield']}</svg></div><h3>A truly independent view</h3><p>No commissions and no products - your fee is the only thing we're paid.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['scale']}</svg></div><h3>A fixed price, upfront</h3><p>Agreed and confirmed in writing before any work begins. The meter never runs.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg></div><h3>In-person time</h3><p>Real, unhurried meetings at your nearest office - never a rushed phone call.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['spark']}</svg></div><h3>Something to act on</h3><p>A clear written output in plain English, not a verbal summary you'll forget.</p></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Why fixed fees</span><h2>A fairer way to be paid</h2><p>The way an adviser is paid quietly shapes the advice you get. Here's how our model compares.</p></div>
      <div class="compare reveal">
        <div class="cmp cmp-usual">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>Hourly or commission</h3>
          <ul>
            <li>Hourly billing rewards taking longer</li>
            <li>Commission rewards selling you something</li>
            <li>The final cost is a surprise</li>
            <li>The meter runs while you think</li>
          </ul>
        </div>
        <div class="cmp cmp-cs">
          <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2"><path d="M20 6L9 17l-5-5"/></svg>Clear Sky Consulting fixed fees</h3>
          <ul>
            <li>One price, agreed before we start</li>
            <li>Paid only to get your decision right</li>
            <li>No commissions, no percentages of your assets</li>
            <li>Think for as long as you need</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Good to know</span><h2>Pricing questions</h2></div>
      <div class="qa-list" style="max-width:780px;margin-inline:auto">
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="pr-0-q" aria-controls="pr-0-a"><span class="qa-q-txt">Are these prices fixed, or just estimates?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="pr-0-a" role="region" aria-labelledby="pr-0-q"><div class="qa-a-inner"><p>The figures above are indicative starting points. Once we understand your situation in the free intro meeting, we confirm a single fixed fee in writing - and that's what you pay.</p></div></div></div>
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="pr-1-q" aria-controls="pr-1-a"><span class="qa-q-txt">Is the first meeting really free?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="pr-1-a" role="region" aria-labelledby="pr-1-q"><div class="qa-a-inner"><p>Yes - the introductory meeting is complimentary and carries no obligation. No fee applies until we've agreed a scope of work together.</p></div></div></div>
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="pr-2-q" aria-controls="pr-2-a"><span class="qa-q-txt">What if my needs change midway?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="pr-2-a" role="region" aria-labelledby="pr-2-q"><div class="qa-a-inner"><p>If the work genuinely needs to grow, we agree any change to scope and fee with you in advance - never after the fact.</p></div></div></div>
        <div class="qa reveal"><button class="qa-q" aria-expanded="false" id="pr-3-q" aria-controls="pr-3-a"><span class="qa-q-txt">Do you charge a percentage of my assets?</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button><div class="qa-a" id="pr-3-a" role="region" aria-labelledby="pr-3-q"><div class="qa-a-inner"><p>Never. We don't manage money or take a percentage of anything you own. You pay a flat fee for the advice itself, and nothing else.</p></div></div></div>
      </div>
    </div>
  </section>

  {cta_band("Not sure which is right for you?", "Start with a free intro meeting and we'll point you the right way - no obligation.")}
'''
    page("pricing.html", "Fixed-Fee Advisory Pricing | Clear Sky Consulting",
         "Clear Sky Consulting's fixed-fee pricing for clarity sessions, planning &amp; strategy, second-opinion reviews and ongoing advisory.",
         "services.html", pricing)

    # =========================================================================
    # INSIGHTS (listing) + articles
    # =========================================================================
    def ins_card(a):
        img = AUTHORS.get(a["author"], "exec-1.svg")
        thumb = scene("scene-" + a["fn"].replace(".html", ""), f"thumb-{a['thumb']}.svg")
        return f'''<article class="ins-card reveal" data-cat="{a['cat']}">
        <a class="ins-thumb" href="{a['fn']}"><img src="assets/{thumb}" alt="{plain_attr(a['title'])}" loading="lazy" width="640" height="360"><span class="ins-cat">{a['tag']}</span></a>
        <div class="ins-body">
          <h3><a href="{a['fn']}">{a['title']}</a></h3>
          <p>{a['dek']}</p>
          <div class="ins-by"><img src="assets/{img}" alt="" width="34" height="34"><span><b>{a['author']}</b>{a['date']} &middot; {a['read']}</span></div>
        </div>
      </article>'''

    feat = ARTICLES[0]
    rest = ARTICLES[1:]
    feat_img = AUTHORS.get(feat["author"], "exec-1.svg")
    cats_order = []
    for a in rest:
        if a["cat"] not in cats_order:
            cats_order.append(a["cat"])
    counts = {c: sum(1 for a in rest if a["cat"] == c) for c in cats_order}
    ins_chips = f'<button class="ins-chip active" data-filter="all" type="button">All topics <span class="ins-chip-n">{len(rest)}</span></button>'
    ins_chips += "".join(
        f'<button class="ins-chip" data-filter="{c}" type="button">{TOPIC_LABELS[c]} <span class="ins-chip-n">{counts[c]}</span></button>'
        for c in cats_order)
    ins_grid = "".join(ins_card(a) for a in rest)

    insights = f'''
  <section class="page-hero">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="inner reveal">
        <p class="breadcrumb"><a href="index.html">Home</a> &middot; Insights</p>
        <span class="eyebrow">Insights</span>
        <h1>Thinking <em>clearly,</em> in writing.</h1>
        <p class="lead">Plain-English perspective from our advisors on how to make big decisions well - and sidestep the traps that catch most people. No jargon, no selling.</p>
      </div>
    </div>
    <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal" style="margin-bottom:1.6rem"><span class="eyebrow">Latest</span><h2>Fresh from the advisory desk</h2></div>
      <article class="ins-featured reveal">
        <a class="ins-featured-media" href="{feat['fn']}">
          <img src="assets/{scene('scene-' + feat['fn'].replace('.html',''), f"thumb-{feat['thumb']}.svg")}" alt="{plain_attr(feat['title'])}" loading="lazy" width="640" height="360">
          <span class="ins-cat">{feat['tag']}</span>
        </a>
        <div class="ins-featured-body">
          <h3><a href="{feat['fn']}">{feat['title']}</a></h3>
          <p>{feat['dek']}</p>
          <div class="ins-by lg"><img src="assets/{feat_img}" alt="" width="44" height="44"><span><b>{feat['author']}</b>{feat['role']} &middot; {feat['date']} &middot; {feat['read']}</span></div>
          <a class="btn btn-primary" href="{feat['fn']}">Read the article</a>
        </div>
      </article>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Browse all</span><h2>Every article</h2><p>Filter by the topic you're thinking about.</p></div>
      <div class="ins-filter reveal">{ins_chips}</div>
      <div class="ins-grid" id="insGrid">{ins_grid}</div>
      <p class="cs-empty" id="insEmpty" hidden>No articles in this topic just yet.</p>
    </div>
  </section>

  <section class="block ins-news">
    <div class="wrap">
      <div class="news-card reveal">
        <div class="news-text">
          <span class="eyebrow" style="color:#E2A24A">The Clear Sky Consulting Letter</span>
          <h2>Clear thinking, once a month.</h2>
          <p>A short, practical note on making big decisions well - no spam, no selling, and you can unsubscribe any time.</p>
        </div>
        <form class="news-form" id="newsletter" novalidate>
          <div class="news-row">
            <label class="sr-only" for="newsEmail">Email address</label>
            <input id="newsEmail" type="email" placeholder="you@example.com" required autocomplete="email">
            <button class="btn btn-primary" type="submit">Subscribe</button>
          </div>
          <p class="news-done" id="newsDone" hidden>Thanks - you're on the list. (Demo only - nothing was sent.)</p>
        </form>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page("insights.html", "Insights on Making Big Decisions Well | Clear Sky Consulting",
         "Articles from Clear Sky Consulting advisors on making big personal decisions well - on independence, planning, money and life's bigger transitions.",
         "insights.html", insights)

    exec_by_name = {p["name"]: p for p in EXEC}
    for art in ARTICLES:
        author_img = AUTHORS.get(art["author"], "exec-1.svg")
        paras = "".join(f"<p>{p}</p>" if not p.startswith("##") else f"<h2>{p[2:].strip()}</h2>" for p in art["body"])
        others = [a for a in ARTICLES if a["fn"] != art["fn"]]
        rel = ([a for a in others if a["cat"] == art["cat"]] +
               [a for a in others if a["cat"] != art["cat"]])[:3]
        related = "".join(ins_card(a) for a in rel)
        ex = exec_by_name.get(art["author"])
        author_bio = ex["bio"] if ex else ""
        art_thumb = scene("scene-" + art["fn"].replace(".html", ""), f"thumb-{art['thumb']}.svg")
        PAGE_IMAGES[art["fn"]] = [f"{SITE_URL}/assets/{art_thumb}"]
        art_ld = jsonld({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": f"{SITE_URL}/{art['fn']}",
            "headline": plain(art["title"]),
            "description": plain(art["dek"]),
            "image": f"{SITE_URL}/assets/{art_thumb}",
            "datePublished": to_iso(art["date"]),
            "dateModified": to_iso(art["date"]),
            "articleSection": plain(art["tag"]),
            "wordCount": sum(len(p.split()) for p in art["body"]),
            "inLanguage": "en-AU",
            "author": {"@type": "Person", "name": art["author"], "jobTitle": plain(art["role"])},
            "publisher": {"@id": ORG_ID},
        })
        body = f'''
  <section class="page-hero article-hero">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="inner reveal">
        <p class="breadcrumb"><a href="index.html">Home</a> &middot; <a href="insights.html">Insights</a> &middot; {art['tag']}</p>
        <span class="tag">{art['tag']}</span>
        <h1>{art['title']}</h1>
        <p class="lead">{art['dek']}</p>
        <div class="byline">
          <img src="assets/{author_img}" alt="Portrait of {art['author']}">
          <div><div class="n">{art['author']}</div><div class="d">{art['role']} &middot; {art['date']} &middot; {art['read']}</div></div>
        </div>
      </div>
    </div>
  </section>
  <section class="block">
    <div class="wrap">
      <div class="prose reveal">
        {paras}
        <div class="callout">Thinking through a decision like this one? A Clear Sky Consulting clarity session gives it a few hours of undivided, impartial attention. <a href="contact.html">Book a meeting &rarr;</a></div>
      </div>
      <div class="author-card reveal">
        <img src="assets/{author_img}" alt="Portrait of {art['author']}">
        <div>
          <span class="eyebrow">Written by</span>
          <h3>{art['author']}</h3>
          <p class="role">{art['role']}</p>
          <p>{author_bio}</p>
        </div>
      </div>
    </div>
  </section>
  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Keep reading</span><h2>Related insights</h2></div>
      <div class="ins-grid">{related}</div>
      <p style="margin-top:2rem"><a class="btn btn-ghost" href="insights.html">&larr; All insights</a></p>
    </div>
  </section>
'''
        page(art["fn"], f"{art['title']} - Clear Sky Consulting Insights", art["dek"], "insights.html", body, extra_head=art_ld, og_type="article")

    # =========================================================================
    # CASE STUDIES
    # =========================================================================
    FEATURED = dict(
        service="Decision clarity", location="Subiaco, WA", thumb=1, result="Decided in one session",
        title="Two offers, one life - choosing without the fear",
        situation="Rebecca, an operations manager in her late thirties, had two offers on the table: a senior role interstate with a substantial pay rise, and a steadier promotion that kept her family close. Six weeks of pro-and-con lists had only deepened the fog.",
        action="In a single 90-minute session we set the spreadsheets aside and mapped what she was really choosing between - not two jobs, but two versions of the next five years. We pressure-tested each against what mattered most to her, and named the one regret she knew she couldn't live with.",
        outcome="Rebecca turned down the bigger salary and took the local promotion, leaving the session certain rather than anxious. Three months on, she told us it was the clearest decision she'd made in a decade.",
        quote="I'd been going in circles for months. One session and I finally knew what to do - and why.",
        who="Rebecca M., Subiaco WA")

    CASES = [
        ("second", "Second opinion", "A proposal that didn't add up", "~$38k saved",
         "Geoffrey was 48 hours from signing a major refurbishment contract. Our independent review flagged a payment schedule and a variation clause that quietly shifted the risk onto him - and gave him the questions to renegotiate.",
         "They reviewed a proposal I was about to sign and saved me from a costly mistake.", "Geoffrey H., Hawthorn VIC", 3),
        ("planning", "Planning &amp; strategy", "A five-year goal, turned into a plan", "Plan in 3 weeks",
         "Daniel and Priya knew where they wanted to be by their mid-forties, but had no path to get there. We built a staged plan with clear milestones, sequencing and review points - and replaced their anxiety with momentum.",
         "Honest, calm and completely on my side. Worth every cent of the fixed fee.", "Daniel &amp; Priya T., Norwood SA", 2),
        ("ongoing", "Ongoing advisory", "A steady hand through a hard year", "On call all year",
         "Through a separation and a career change in the same twelve months, Margaret had one impartial person who already understood her situation to think each step through with, whenever it mattered.",
         "Knowing I could pick up the phone to someone genuinely on my side changed everything.", "Margaret S., New Farm QLD", 5),
        ("clarity", "Decision clarity", "Sell the family home, or hold on?", "Clarity, no regret",
         "With their children moved out, Anne and Peter were torn between downsizing and keeping a home full of memories. We separated the emotional weight from the practical trade-offs so they could decide with a clear head.",
         "We finally talked about the thing under the decision, not just the numbers.", "Anne &amp; Peter L., Glenelg SA", 4),
        ("second", "Second opinion", "Is this franchise really worth it?", "Walked away",
         "Sam was ready to buy into a franchise on the strength of a glossy pitch. Our review tested the real numbers against three quieter assumptions the brochure skated over - and the maths didn't hold.",
         "I went in excited and left relieved. The questions they gave me ended the conversation fast.", "Sam R., Joondalup WA", 6),
        ("planning", "Planning &amp; strategy", "From a vague dream to a sabbatical that worked", "12-month runway",
         "Nadia wanted a year out to retrain without derailing her finances or her career. We mapped the sequencing - timing, savings runway and a clear re-entry plan - so she could leap with a net.",
         "They turned a vague dream into a month-by-month plan I actually trusted.", "Nadia K., Carlton VIC", 1),
        ("clarity", "Decision clarity", "Relocate the whole family, or not?", "Decided in one session",
         "A standout interstate role meant uprooting two children mid-school year. In a single session we weighed the career upside against what the move would cost the things the family valued most.",
         "Calm, fast and completely unbiased. We stopped second-guessing ourselves.", "The Okafor family, Ipswich QLD", 3),
        ("ongoing", "Ongoing advisory", "Navigating an unexpected inheritance", "No rushed moves",
         "A sudden inheritance brought a flood of advice from every direction. As her ongoing advisor, we gave Helen one steady, impartial place to think things through before she acted on any of it.",
         "Everyone had an opinion. Clear Sky Consulting had no agenda - that is exactly what I needed.", "Helen V., Unley SA", 2),
        ("second", "Second opinion", "A redundancy offer, reviewed in a day", "Better terms",
         "Handed a redundancy package and a 48-hour deadline, Tom needed to know if it was fair. We reviewed the terms independently and handed him the specific points worth negotiating.",
         "I had one day to decide. Their review gave me the confidence to push back - and it worked.", "Tom B., Spearwood WA", 4),
    ]

    FILTERS = [("all", "All stories"), ("clarity", "Decision clarity"),
               ("planning", "Planning &amp; strategy"), ("second", "Second opinion"),
               ("ongoing", "Ongoing advisory")]
    counts = {k: sum(1 for c in CASES if c[0] == k) for k, _ in FILTERS}
    counts["all"] = len(CASES)
    chips = "".join(
        f'<button class="cs-chip{" active" if k=="all" else ""}" data-filter="{k}" type="button">{label} <span class="cs-chip-n">{counts[k]}</span></button>'
        for k, label in FILTERS)

    cards = ""
    for i, (cat, service, title, result, summary, quote, who, t) in enumerate(CASES):
        cimg = scene(f"case-{i+1}", f"thumb-{t}.svg")
        cards += f'''<article class="cs-card reveal" data-cat="{cat}">
        <div class="cs-thumb"><img src="assets/{cimg}" alt="" loading="lazy" width="640" height="360"><span class="cs-badge">{result}</span></div>
        <div class="cs-body">
          <span class="tag">{service}</span>
          <h3>{title}</h3>
          <p>{summary}</p>
          <figure class="cs-quote"><blockquote>&ldquo;{quote}&rdquo;</blockquote><figcaption>{who}</figcaption></figure>
        </div>
      </article>'''

    casestudies = f'''
  <section class="page-hero">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="inner reveal">
        <p class="breadcrumb"><a href="index.html">Home</a> &middot; Case studies</p>
        <span class="eyebrow">Client stories</span>
        <h1>Real decisions, <em>made clearly.</em></h1>
        <p class="lead">Every name and detail below is illustrative and anonymised - but each story reflects the kind of work our advisors do every week. This is what clarity looks like in practice.</p>
      </div>
    </div>
    <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
  </section>

  {trust_strip()}

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n">25k<span class="dawn">+</span></div><div class="l">Clients advised</div></div>
        <div class="s"><div class="n">98%</div><div class="l">Client satisfaction</div></div>
        <div class="s"><div class="n">+82</div><div class="l">Net Promoter Score</div></div>
        <div class="s"><div class="n">4.9<span class="dawn">/5</span></div><div class="l">Average client rating</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Featured story</span><h2>When one decision takes over your thinking</h2></div>
      <article class="cs-featured reveal">
        <div class="cs-featured-media">
          <img src="assets/{scene('case-featured', f"thumb-{FEATURED['thumb']}.svg")}" alt="" loading="lazy" width="640" height="360">
          <span class="cs-badge lg">{FEATURED['result']}</span>
        </div>
        <div class="cs-featured-body">
          <span class="tag">{FEATURED['service']}</span>
          <h3>{FEATURED['title']}</h3>
          <p class="cs-loc"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>{FEATURED['location']}</p>
          <div class="cs-stage"><h4>The situation</h4><p>{FEATURED['situation']}</p></div>
          <div class="cs-stage"><h4>What we did</h4><p>{FEATURED['action']}</p></div>
          <div class="cs-stage"><h4>The outcome</h4><p>{FEATURED['outcome']}</p></div>
          <figure class="cs-pull"><blockquote>&ldquo;{FEATURED['quote']}&rdquo;</blockquote><figcaption>{FEATURED['who']}</figcaption></figure>
        </div>
      </article>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">More stories</span><h2>Clarity across every kind of decision</h2><p>Filter by the type of help people came to us for.</p></div>
      <div class="cs-filter reveal">{chips}</div>
      <div class="cs-grid" id="csGrid">{cards}</div>
      <p class="cs-empty" id="csEmpty" hidden>No stories in this category just yet.</p>
    </div>
  </section>

  {cta_band("Could your decision use a clear head?", "Bring us the thing you keep going around in circles on. The first conversation is complimentary.")}
'''
    page("case-studies.html", "Client Case Studies | Clear Sky Consulting",
         "Illustrative, anonymised client stories showing how Clear Sky Consulting helps people make big personal decisions with clarity and confidence.",
         None, casestudies)

    # =========================================================================
    # PRESS / NEWSROOM
    # =========================================================================
    press_items = [
        ("12 May 2026", "Company news", "Clear Sky Consulting surpasses 25,000 clients advised since founding", "company"),
        ("28 Mar 2026", "Milestone", "Clear Sky Consulting's national team passes 240 advisors, up 22% on last year", "company"),
        ("14 Feb 2026", "Awards", "Clear Sky Consulting named Best Client Experience at the National Advisory Index", "awards"),
        ("9 Dec 2025", "Company news", "Bendigo office marks two years and 1,000 regional clients", "company"),
        ("3 Oct 2025", "People", "Hiroshi Tanaka appointed Chief Technology Officer", "people"),
        ("18 Aug 2025", "ESG", "Clear Sky Consulting publishes its first Independence &amp; Trust report", "esg"),
        ("21 May 2025", "Recognition", "Client Net Promoter Score reaches an industry-leading +82", "awards"),
        ("7 Mar 2025", "Awards", "Recognised as an Employer of Choice in the AU Workplace Awards", "awards"),
    ]
    pfeat = press_items[0]
    prest = press_items[1:]
    PRESS_FILTERS = [("all", "All"), ("company", "Company"), ("awards", "Awards"), ("people", "People"), ("esg", "ESG")]
    pcounts = {k: sum(1 for it in prest if it[3] == k) for k, _ in PRESS_FILTERS}
    pchips = "".join(
        f'<button class="cs-chip{" active" if k=="all" else ""}" data-filter="{k}" type="button">{label} <span class="cs-chip-n">{len(prest) if k=="all" else pcounts[k]}</span></button>'
        for k, label in PRESS_FILTERS)
    rows = "".join(f'''<a class="press-item reveal" href="press.html" data-cat="{c}">
        <div class="date">{d}</div>
        <div><div class="src">{s}</div><h3>{t}</h3></div>
      </a>''' for d, s, t, c in prest)
    press = f'''
  {page_hero("Newsroom", "Newsroom", "News from <em>Clear Sky Consulting.</em>",
             "Company announcements, milestones and media coverage. For media enquiries, contact our communications team below.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap">
      <article class="press-featured reveal">
        <div class="pf-head"><span class="tag">Latest &middot; {pfeat[1]}</span><span class="pf-date">{pfeat[0]}</span></div>
        <h2>{pfeat[2]}</h2>
        <p>A milestone for the practice: more than 25,000 individuals and families have now sat down with a Clear Sky Consulting advisor since we opened our first office in 2018 - every one of them in person.</p>
        <a class="btn btn-primary" href="press.html">Read the announcement &rarr;</a>
      </article>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Announcements</span><h2>Newsroom archive</h2><p>Filter by category.</p></div>
      <div class="cs-filter reveal" data-target="pressGrid" data-empty="pressEmpty">{pchips}</div>
      <div class="press-list" id="pressGrid">{rows}</div>
      <p class="cs-empty" id="pressEmpty" hidden>No announcements in this category just yet.</p>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Media kit</span><h2>Clear Sky Consulting at a glance</h2><p>The quick facts most often asked for. For logos, imagery or interviews, contact our team below.</p></div>
      <div class="metric-grid reveal">
        <div class="metric"><div class="n">2018</div><div class="l">Founded, in Perth WA</div></div>
        <div class="metric"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Offices nationwide</div></div>
        <div class="metric"><div class="n"><span class="count" data-to="240">0</span><span class="dawn">+</span></div><div class="l">People nationally</div></div>
        <div class="metric"><div class="n"><span class="count" data-to="25">0</span><span class="dawn">k+</span></div><div class="l">Clients advised</div></div>
      </div>
    </div>
  </section>

  <div class="logos">
    <div class="wrap">
      <p class="k">Clear Sky Consulting in the media</p>
      <div class="logo-row">
        <span>The Australian</span><span>Financial Review</span><span>ABC News</span>
        <span>Sydney Morning Herald</span><span>Forbes AU</span><span>Sky Business</span>
      </div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="ways-grid">
        <div class="way-card reveal" style="cursor:default">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg></div>
          <h3>Media enquiries</h3>
          <p>Our communications team responds to journalists within the business day.</p>
          <span class="way-go">{mail("media@clear-sky-consulting.au")}</span>
        </div>
        <a class="way-card reveal" href="tel:+61285550190">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg></div>
          <h3>Call the press line</h3>
          <p>For time-sensitive enquiries during business hours, AEST.</p>
          <span class="way-go">+61 2 8555 0190 &rarr;</span>
        </a>
        <a class="way-card reveal" href="about.html">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/></svg></div>
          <h3>About the company</h3>
          <p>Background, history and leadership for your story.</p>
          <span class="way-go">Company profile &rarr;</span>
        </a>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page("press.html", "Newsroom & Media | Clear Sky Consulting",
         "Company announcements, milestones and media coverage from Clear Sky Consulting, plus media-kit facts and press contacts.",
         None, press)

    # =========================================================================
    # OFFICES
    # =========================================================================
    reg_by_name = {p["name"]: p for p in REGIONAL}
    cards = ""
    for o in OFFICES:
        q = o["q"].replace(" ", "%20").replace(",", "%2C")
        md = reg_by_name.get(o["lead"])
        md_img = md["img"] if md else "reg-1.svg"
        cards += f'''<div class="office-card reveal">
        <img class="office-map" src="assets/map-{o['city'].lower()}.svg" alt="Map of the Clear Sky Consulting {o['city']} office location" loading="lazy" width="640" height="360">
        <div class="office-head">
          <div>
            <div class="city"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg>{o['city']}</div>
            <div class="lead-name">Managing Director</div>
          </div>
          <img class="office-md" src="assets/{md_img}" alt="Portrait of {o['lead']}" loading="lazy" width="56" height="56" title="{o['lead']}">
        </div>
        <p class="office-mdname">{o['lead']}</p>
        <address>{o['addr']}</address>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg>{mail(o['email'])}</div>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg>{tel(o['phone'])}</div>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/></svg>Mon-Fri, 8:30am-5:30pm</div>
        <a class="dir" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">Get directions
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
        <a class="office-page-link" href="office-{o['city'].lower()}.html">Independent advice in {o['city']} &rarr;</a>
      </div>'''
    offices = f'''
  {page_hero("Offices", "Where we meet", "Five offices, <em>one standard.</em>",
             "We meet every client face to face - never by phone. Choose the office nearest you and we'll arrange a time to sit down together.")}
  {trust_strip()}

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n"><span class="count" data-to="5">0</span></div><div class="l">Offices nationwide</div></div>
        <div class="s"><div class="n"><span class="count" data-to="4">0</span></div><div class="l">States &amp; territories</div></div>
        <div class="s"><div class="n">100%</div><div class="l">Meetings in person</div></div>
        <div class="s"><div class="n">1</div><div class="l">Standard of advice</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Find your office</span><h2>Choose the one nearest you</h2><p>Each office is led by an experienced managing director, following the same firm-wide approach.</p></div>
      <div class="office-detail">{cards}</div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Your visit</span><h2>What to expect when you come in</h2></div>
      <div class="steps process">
        <div class="step reveal"><h3>A warm welcome</h3><p>Arrive a few minutes early and we'll have a quiet room and a coffee ready. No waiting around, no sales desk.</p></div>
        <div class="step reveal"><h3>An unhurried conversation</h3><p>We set aside real time to understand what's on your mind. The first meeting is complimentary and without obligation.</p></div>
        <div class="step reveal"><h3>A clear next step</h3><p>You'll leave knowing whether we can help and exactly what it would involve, with any fee agreed upfront.</p></div>
      </div>
    </div>
  </section>

  {cta_band()}
'''
    page("offices.html", "Offices in Perth, Brisbane, Adelaide, Sydney & Bendigo | Clear Sky Consulting",
         "Clear Sky Consulting's five offices across Australia: Perth, Brisbane, Adelaide, Sydney and Bendigo. Find your nearest and book a meeting.",
         "about.html", offices, extra_head=localbusiness_ld(OFFICES))

    # =========================================================================
    # CITY / LOCATION LANDING PAGES (local SEO)
    # =========================================================================
    CITY_INFO = {
        "Perth": dict(
            region="Greater Perth and the western suburbs",
            intro="Our founding office sits on Kings Park Road in West Perth, a short walk from Kings Park itself. From the CBD to the western suburbs and the coast, we help individuals and families across Perth weigh up the decisions that matter most.",
            transport="moments from the Esplanade Busport and the free CAT bus zone, with parking nearby on Kings Park Road",
            areas=["Subiaco", "Cottesloe", "Fremantle", "Nedlands", "Claremont", "Joondalup", "South Perth", "Scarborough"],
            quote="I'd been going in circles for months. One session and I finally knew what to do - and why.",
            quote_who="Rebecca M., Subiaco WA"),
        "Brisbane": dict(
            region="Brisbane and South East Queensland",
            intro="Our Brisbane office is on William Street in the heart of the CBD, beside the river. We sit down with people from right across South East Queensland - the inner city, the bayside, and the suburbs in between.",
            transport="a short walk from the Queen Street Mall and the city-cat ferry terminals",
            areas=["New Farm", "Paddington", "Bulimba", "Chermside", "Ipswich", "Toowong", "Springfield", "Redcliffe"],
            quote="Calm, fast and completely unbiased. We finally stopped second-guessing ourselves.",
            quote_who="The Okafor family, Ipswich QLD"),
        "Adelaide": dict(
            region="metropolitan Adelaide",
            intro="You'll find our Adelaide office on Hindley Street in the West End, an easy walk across the city. We advise people from across metropolitan Adelaide and the surrounding regions, in person and without the sales pitch.",
            transport="in the heart of the West End, close to the free City Connector bus and Adelaide Railway Station",
            areas=["Norwood", "Unley", "Glenelg", "Burnside", "Prospect", "North Adelaide", "Mawson Lakes", "Mitcham"],
            quote="Honest, calm and completely on my side. Worth every cent of the fixed fee.",
            quote_who="Daniel &amp; Priya T., Norwood SA"),
        "Sydney": dict(
            region="Greater Sydney",
            intro="Our Sydney office is on George Street in the CBD, minutes from Town Hall. We help individuals and families from across Greater Sydney think clearly about their bigger decisions - free of commissions and free of pressure.",
            transport="steps from Town Hall Station and the George Street light rail",
            areas=["North Sydney", "Parramatta", "Mosman", "Bondi", "Chatswood", "Manly", "Surry Hills", "Hornsby"],
            quote="They gave me room to think, and the questions I hadn't thought to ask. I left certain.",
            quote_who="James P., Mosman NSW"),
        "Bendigo": dict(
            region="Bendigo and the Loddon Mallee",
            intro="Our Bendigo office on King Street brings the same independent advice to regional Victoria. We work with people across the Loddon Mallee - Bendigo, the goldfields towns, and the surrounding shires.",
            transport="a short walk from the Bendigo Railway Station and the city centre",
            areas=["Kangaroo Flat", "Eaglehawk", "Castlemaine", "Strathfieldsaye", "Heathcote", "Maiden Gully", "Epsom", "Marong"],
            quote="They reviewed a proposal I was about to sign and saved me from a costly mistake.",
            quote_who="Geoffrey H., Bendigo VIC"),
    }

    city_files = {o["city"]: f"office-{o['city'].lower()}.html" for o in OFFICES}

    def city_business_ld(o, fn, info):
        street, rest = o["addr"].split("<br>")
        toks = rest.split()
        return jsonld({
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "@id": f"{SITE_URL}/{fn}#office",
            "name": f"Clear Sky Consulting - {o['city']}",
            "description": plain(info["intro"]),
            "parentOrganization": {"@id": ORG_ID},
            "url": f"{SITE_URL}/{fn}",
            "image": f"{SITE_URL}/assets/og-image.png",
            "telephone": o["phone"].replace(" ", ""),
            "email": o["email"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": street.strip(),
                "addressLocality": " ".join(toks[:-2]),
                "addressRegion": toks[-2],
                "postalCode": toks[-1],
                "addressCountry": "AU",
            },
            "areaServed": [{"@type": "City", "name": a} for a in [o["city"]] + info["areas"]],
            "priceRange": "$$",
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "08:30", "closes": "17:30",
            },
        })

    for o in OFFICES:
        city = o["city"]
        info = CITY_INFO[city]
        fn = city_files[city]
        slug = city.lower()
        street, locality_line = o["addr"].split("<br>")
        md = reg_by_name.get(o["lead"])
        md_img = md["img"] if md else "reg-1.svg"
        q = o["q"].replace(" ", "%20").replace(",", "%2C")
        areas_html = "".join(f"<li>{a}</li>" for a in info["areas"])
        svc_html = "".join(service_card(*s) for s in SERVICES)
        other_links = "".join(
            f'<a class="btn btn-ghost" href="{city_files[oo["city"]]}">{oo["city"]}</a>'
            for oo in OFFICES if oo["city"] != city)
        city_faqs = [
            (f"Where is your {city} office?",
             f"You'll find us at {street}, {locality_line} - {info['transport']}."),
            (f"Do you meet clients in person in {city}?",
             f"Yes. Every {city} engagement is face to face - we don't advise over the phone. The decisions clients bring us deserve an unhurried conversation across the table."),
            (f"Who will I meet with in {city}?",
             f"Your {city} office is led by {o['lead']}, Managing Director, with a local advisory team. The advisor who understands your situation in the first meeting is the same one with you at the last."),
        ]
        qa_html = ""
        for i, (qq, aa) in enumerate(city_faqs):
            qid = f"{slug}-faq-{i}"
            qa_html += f'''<div class="qa reveal">
            <button class="qa-q" aria-expanded="false" id="{qid}-q" aria-controls="{qid}-a"><span class="qa-q-txt">{qq}</span><span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span></button>
            <div class="qa-a" id="{qid}-a" role="region" aria-labelledby="{qid}-q"><div class="qa-a-inner"><p>{aa}</p></div></div>
          </div>'''
        crumb = f'<a href="offices.html">Offices</a> &middot; {city}'
        body = f'''
  {page_hero(crumb, f"{city} office", f"Independent personal advisory in <em>{city}.</em>", info["intro"])}
  {trust_strip()}

  <section class="block">
    <div class="wrap split reveal">
      <div class="office-card" style="margin:0">
        <img class="office-map" src="assets/map-{slug}.svg" alt="Map showing the Clear Sky Consulting {city} office location" loading="lazy" width="640" height="360">
        <div class="office-head">
          <div>
            <div class="city"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg>{city}</div>
            <div class="lead-name">Managing Director</div>
          </div>
          <img class="office-md" src="assets/{md_img}" alt="Portrait of {o['lead']}, Managing Director of the Clear Sky Consulting {city} office" loading="lazy" width="56" height="56" title="{o['lead']}">
        </div>
        <p class="office-mdname">{o['lead']}</p>
        <address>{o['addr']}</address>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg>{mail(o['email'])}</div>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg>{tel(o['phone'])}</div>
        <div class="row"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/></svg>Mon-Fri, 8:30am-5:30pm AEST</div>
        <a class="dir" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">Get directions
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      </div>
      <div>
        <span class="eyebrow">Visit us in {city}</span>
        <h2>Independent advice, in person in {city}</h2>
        <p>{info['intro']}</p>
        <p>Your first meeting is complimentary and entirely without obligation. We agree any work, and a fixed fee, in writing before we begin - so there are no surprises and nothing to sell you.</p>
        <ul class="ticks">
          <li>Commission-free advice, paid only by you</li>
          <li>One advisor, from first meeting to last</li>
          <li>Fixed fees, agreed upfront</li>
        </ul>
        <a class="btn btn-primary" href="contact.html">Book a meeting in {city}</a>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">How we help</span><h2>Ways we work with {city} clients</h2><p>Whatever you're weighing up, every engagement is shaped around your situation, delivered in person at our {city} office, with a fixed fee agreed upfront.</p></div>
      <div class="svc-grid">{svc_html}</div>
    </div>
  </section>

  <section class="block">
    <div class="wrap reveal">
      <div class="section-head"><span class="eyebrow">Local to you</span><h2>Advising clients across {info['region']}</h2><p>We meet clients from right across the region. A few of the areas we regularly work with:</p></div>
      <ul class="area-list">{areas_html}</ul>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <figure class="svc-quote reveal">
        <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;{info['quote']}&rdquo;</blockquote>
        <figcaption>{info['quote_who']}</figcaption>
      </figure>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">{city} questions</span><h2>Good to know</h2></div>
      <div class="qa-list" style="max-width:780px;margin-inline:auto">{qa_html}</div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Around the country</span><h2>Our other offices</h2><p>Not in {city}? We meet clients face to face in four other locations across Australia.</p></div>
      <div class="hero-actions" style="justify-content:center;flex-wrap:wrap">{other_links}</div>
    </div>
  </section>

  {cta_band(f"Ready to talk it through in {city}?", "Your first meeting is complimentary, in person, and entirely without obligation.")}
'''
        title = f"Independent Personal Advisory in {city} | Clear Sky Consulting"
        desc = (f"Independent, commission-free personal advisory in {city}. Meet our {city} "
                f"team in person at {street} for clear, fixed-fee advice on life's bigger decisions.")
        page(fn, title, desc, "about.html", body, extra_head=city_business_ld(o, fn, info))

    # =========================================================================
    # CAREERS
    # =========================================================================
    jobs = [
        ("Personal Advisor", "Sydney", "Full-time", "Advisory"),
        ("Personal Advisor", "Perth", "Full-time", "Advisory"),
        ("Senior Advisor - Planning &amp; Strategy", "Brisbane", "Full-time", "Advisory"),
        ("Client Experience Coordinator", "Adelaide", "Full-time", "Client"),
        ("Advisor Associate (Graduate)", "Bendigo", "Graduate", "Advisory"),
        ("Finance Business Partner", "Sydney", "Full-time", "Finance"),
        ("Product Designer", "Remote (AU)", "Full-time", "Technology"),
    ]
    joblist = "".join(f'''<a class="job reveal" href="careers.html">
        <div><h3>{t}</h3><div class="j-meta"><span>{loc}</span><span>·</span><span>{typ}</span><span>·</span><span>{team}</span></div></div>
        <span class="pill">View role →</span>
      </a>''' for t, loc, typ, team in jobs)
    STAFF = [
        ("Advisor, Sydney", "I left a big institution to actually help people, not hit a sales target. Here, the advice is the product - it's the most honest work I've done.", "Pri.", "exec-4.svg"),
        ("Senior Advisor, Brisbane", "The apprenticeship model is real. I learned more in my first year beside a senior advisor than in five years anywhere else.", "Marc.", "exec-6.svg"),
        ("Client Experience, Adelaide", "Everyone here genuinely cares that the client leaves clearer than they arrived. It's a calm, grown-up place to work.", "Soph.", "exec-5.svg"),
    ]
    staff_html = "".join(f'''<figure class="tcard reveal">
        <div class="stars" aria-label="Rated 5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;{q}&rdquo;</blockquote>
        <figcaption><img class="tphoto" src="assets/{img}" alt="" width="42" height="42"><span class="twho"><b>{who}</b>{role}</span></figcaption>
      </figure>''' for role, q, who, img in STAFF)
    careers = f'''
  {page_hero("Careers", "Careers", "Build a practice <em>worth trusting.</em>",
             "We hire people who'd rather be right than be selling. If that's you, Clear Sky Consulting is a place to do the best advisory work of your career.")}
  {trust_strip()}

  <section class="stats-band block">
    <div class="wrap">
      <div class="stats-grid reveal">
        <div class="s"><div class="n"><span class="count" data-to="4.7" data-dec="1">0</span><span class="dawn">/5</span></div><div class="l">Average team rating</div></div>
        <div class="s"><div class="n"><span class="count" data-to="93">0</span>%</div><div class="l">Would recommend us</div></div>
        <div class="s"><div class="n">100%</div><div class="l">Employee-owned</div></div>
        <div class="s"><div class="n"><span class="count" data-to="240">0</span><span class="dawn">+</span></div><div class="l">Colleagues nationwide</div></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap split reveal">
      <div class="media"><img src="assets/{scene("scene-careers","thumb-6.svg")}" alt="Careers at Clear Sky Consulting - independent advisory work across Australia" loading="lazy" width="640" height="360"></div>
      <div>
        <span class="eyebrow">Why Clear Sky Consulting</span>
        <h2>Independent work, done properly</h2>
        <p>No sales targets. No products to push. Just the craft of helping people think clearly - backed by a national practice that invests in your development.</p>
        <ul class="ticks">
          <li>Apprenticeship model - learn beside senior advisors</li>
          <li>Fixed-fee work, never commission-driven</li>
          <li>Profit share and genuine employee ownership</li>
          <li>Named Employer of Choice, 2025</li>
        </ul>
        <a class="btn btn-primary" href="#roles">See open roles</a>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Benefits</span><h2>How we look after our people</h2></div>
      <div class="values">
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['spark']}</svg></div><h3>Growth, funded</h3><p>Generous professional-development budget and study support for every advisor.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['shield']}</svg></div><h3>Ownership</h3><p>Employee share scheme so the people who do the work share in its success.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['clock']}</svg></div><h3>Balance</h3><p>Flexible arrangements and a genuine respect for life outside work.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg></div><h3>Five great offices</h3><p>Work from a city that suits you, with colleagues nationwide.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['shield']}</svg></div><h3>Wellbeing support</h3><p>Paid wellbeing days and confidential support, because clear heads need looking after.</p></div>
        <div class="value reveal"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['check']}</svg></div><h3>Work that matters</h3><p>Help real people make life's biggest decisions well. The impact is personal and immediate.</p></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Life at Clear Sky Consulting</span><h2>In our people's words</h2></div>
      <div class="tgrid">{staff_html}</div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Hiring process</span><h2>How we hire</h2><p>Considered and respectful - the same way we treat clients.</p></div>
      <div class="steps process">
        <div class="step reveal"><h3>Apply</h3><p>Send your CV and a short note on why independent advice appeals to you. No cover-letter gymnastics required.</p></div>
        <div class="step reveal"><h3>Intro call</h3><p>A relaxed conversation with our People &amp; Culture team to get to know each other.</p></div>
        <div class="step reveal"><h3>Meet the team</h3><p>An in-person interview and a real-world scenario, so we both see how you think.</p></div>
        <div class="step reveal"><h3>Offer</h3><p>A clear offer, a warm welcome, and a structured first ninety days.</p></div>
      </div>
    </div>
  </section>

  <section class="block" id="roles">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Open roles</span><h2>Where you could fit</h2><p>Don't see the perfect role? Introduce yourself anyway - we're always glad to meet good people.</p></div>
      <div class="jobs">{joblist}</div>
      <div class="callout reveal" style="margin-top:2rem"><strong>People &amp; Culture team</strong><br>{mail("careers@clear-sky-consulting.au")} &middot; {tel("+61 3 9555 0106")}</div>
    </div>
  </section>

  {cta_band("Want to talk to us about a career?", "Reach our People &amp; Culture team and we'll take it from there.")}
'''
    page("careers.html", "Careers in Independent Advisory | Clear Sky Consulting",
         "Join Clear Sky Consulting - independent advisory work with no sales targets, an apprenticeship model and employee ownership. See open roles.",
         "careers.html", careers)

    # =========================================================================
    # FAQ
    # =========================================================================
    LOCK = '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>'
    FAQ_CATS = [
        ("advice", "Advice &amp; independence", IC["shield"], [
            ("Are you really independent, or is that just marketing?",
             "It's structural, not a slogan. Clear Sky Consulting accepts no commissions, kickbacks or referral fees, and we don't sell any financial products - so there is never a hidden reason to steer you one way over another. The only money we ever receive is the fee you agree to pay us directly. That independence is written into the company's constitution and overseen by a majority-independent board, so it can't quietly erode over time."),
            ("What kinds of decisions do you actually help with?",
             "The big, infrequent ones, where the stakes are high and the right path isn't obvious - a career crossroads, a major commitment, a significant purchase or sale, a family or life transition, or simply a choice you keep going around in circles on. Planning toward a goal, or sense-checking a proposal someone has put in front of you, sit squarely in our wheelhouse too. If you're not sure whether we're the right fit, the first conversation is free and we'll tell you honestly."),
            ("Do you give financial, legal or tax advice?",
             "No - and we're deliberate about that line. Clear Sky Consulting provides independent decision-support and strategy; we do not provide licensed financial product advice, legal advice or tax advice unless we have expressly agreed to in writing. Where your decision genuinely needs a licensed specialist, we'll say so, and we're glad to work alongside your accountant, lawyer or other advisers rather than replace them."),
            ("How are you different from a financial adviser or a consultant?",
             "A financial adviser is usually licensed to recommend, and sometimes sell, financial products; a consultant typically works with businesses. We sit in a different seat entirely: a personal advisory practice for individuals and families, focused purely on helping you think clearly and decide well - with nothing to sell you at the end of it. You leave with clarity and a plan, not a pitch."),
        ]),
        ("process", "Meetings &amp; how it works", IC["clock"], [
            ("Do you meet over the phone or by video?",
             "No - we advise in person, every time. The decisions people bring us deserve an unhurried, face-to-face conversation, free of the distractions and shortcuts that creep into a call. You'll meet your advisor at whichever of our five offices - Perth, Brisbane, Adelaide, Sydney or Bendigo - is most convenient for you."),
            ("Is the first meeting really free?",
             "Yes, genuinely. Your introductory meeting is complimentary and carries no obligation whatsoever. Its only purpose is for us to understand what's on your mind, and for us both to decide whether we're the right fit. No advisory relationship - and no fee - begins until we've agreed a clear scope of work in writing."),
            ("How long does an engagement usually take?",
             "It depends on what you need. A decision clarity session is a single focused sitting of around 90 minutes, with a written summary to follow. A planning engagement runs over several meetings across a few weeks. A second-opinion review is typically turned around within a few business days. We'll give you a realistic timeframe upfront, alongside the fixed fee."),
            ("What should I bring to the first meeting?",
             "Just yourself and an honest sense of what you're weighing up - nothing formal is required. If your question relates to a specific document, proposal or quote, bringing it helps us be more useful, but it's never a prerequisite. The first meeting is about understanding your situation, not paperwork."),
            ("Which office should I choose?",
             "Whichever is easiest for you to reach - the standard of advice is identical across all five, each led by an experienced managing director following the same firm-wide approach. If you're unsure, choose 'not sure yet' when you enquire and we'll help you decide."),
        ]),
        ("fees", "Fees &amp; pricing", IC["scale"], [
            ("How much will it cost me?",
             "Every engagement is a single fixed fee, agreed and confirmed in writing before any paid work begins - so you're never surprised. As a guide, second-opinion reviews start from $900, clarity sessions from $1,200, and planning engagements from $3,500. You can see indicative pricing for each service on our <a href=\"pricing.html\">pricing page</a>."),
            ("Why fixed fees instead of hourly rates or commission?",
             "Because both of those quietly work against you. Hourly billing rewards taking longer; commission rewards selling you something. A fixed fee agreed upfront aligns us with the only thing that matters - getting your decision right, efficiently. You know the full cost before you commit, and the meter never runs while you think."),
            ("What's included in the fee?",
             "Everything we've scoped: the meeting or meetings, our preparation and analysis, and a clear written output you can act on - whether that's a summary, a plan, or a considered verdict. If your needs change midway and the work genuinely needs to grow, we agree any adjustment with you in advance, never after the fact."),
            ("Do you offer an ongoing arrangement?",
             "Yes. Many clients move from a one-off engagement to ongoing advisory - a simple fixed annual retainer that gives you regular sit-downs and an impartial person to call whenever something important comes up. It's never a percentage of your assets, and there's no lock-in: it continues only while it's genuinely useful to you."),
        ]),
        ("trust", "Trust, privacy &amp; getting started", LOCK, [
            ("How do you protect my privacy?",
             "Discretion is the foundation of honest advice, so we take it seriously. We collect only what we need, store it securely with restricted access, and handle everything in line with the Australian Privacy Principles. We never sell your information, and we receive no commissions that would give us any reason to share it. Full details are in our <a href=\"privacy.html\">privacy policy</a>."),
            ("Is everything I share with you confidential?",
             "Yes. What you tell us stays between you and your advisor. We disclose information only with your express consent, to trusted providers bound by confidentiality, or where the law requires it - and nowhere else."),
            ("Who will I actually be working with?",
             "A qualified advisor who stays with you from the first meeting to the last - not a call centre or a rotating cast. We keep the practice deliberately personal, so the person who understands your situation is the same person you deal with throughout. You can meet the people behind Clear Sky Consulting on our <a href=\"leadership.html\">leadership page</a>."),
            ("How do I get started?",
             "Book a complimentary introductory meeting through our <a href=\"contact.html\">contact page</a>, or call +61 488 855 709. Tell us a little about what you're weighing up and which office suits you, and we'll be in touch within one business day to arrange a time to sit down together."),
        ]),
    ]

    total_q = sum(len(items) for _, _, _, items in FAQ_CATS)

    chips = "".join(f'<a href="#{cid}">{title}</a>' for cid, title, _, items in FAQ_CATS)
    navlinks = "".join(
        f'<a href="#{cid}" data-spy="{cid}"><span>{title}</span><span class="cnt">{len(items)}</span></a>'
        for cid, title, _, items in FAQ_CATS)

    groups = ""
    for cid, title, icon, items in FAQ_CATS:
        qas = ""
        for i, (q, a) in enumerate(items):
            qid = f"{cid}-{i}"
            qas += f'''<div class="qa reveal" data-q="{plain_attr(q, a)}">
            <button class="qa-q" aria-expanded="false" id="{qid}-q" aria-controls="{qid}-a">
              <span class="qa-q-txt">{q}</span>
              <span class="qa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></span>
            </button>
            <div class="qa-a" id="{qid}-a" role="region" aria-labelledby="{qid}-q"><div class="qa-a-inner"><p>{a}</p></div></div>
          </div>'''
        groups += f'''<section class="faq-group reveal" id="{cid}">
        <div class="faq-group-head">
          <span class="faq-group-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{icon}</svg></span>
          <h2>{title}</h2>
        </div>
        <div class="qa-list">{qas}</div>
      </section>'''

    faq = f'''
  <section class="page-hero faq-hero">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="inner reveal">
        <p class="breadcrumb"><a href="index.html">Home</a> &middot; FAQ</p>
        <span class="eyebrow">Frequently asked questions</span>
        <h1>Answers, <em>before you ask.</em></h1>
        <p class="lead">Everything about how we work, what it costs, and what to expect - written as plainly as we'd explain it across the table. Search below, or jump to a topic.</p>
        <div class="faq-chips reveal">{chips}</div>
      </div>
    </div>
    <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
  </section>

  {trust_strip()}

  <section class="block">
    <div class="wrap faq-layout">
      <aside class="faq-side">
        <div class="faq-search">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
          <input id="faqSearch" type="search" placeholder="Search questions..." aria-label="Search questions" autocomplete="off">
        </div>
        <nav class="faq-nav" aria-label="FAQ categories">{navlinks}</nav>
        <div class="faq-help">
          <div class="faq-help-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 8v4l3 2M12 21a9 9 0 100-18 9 9 0 000 18z"/></svg></div>
          <h3>Still have a question?</h3>
          <p>Speak to a real advisor - your first meeting is complimentary.</p>
          <a class="btn btn-primary" href="contact.html">Book a meeting</a>
          <a class="faq-help-call" href="tel:+61488855709">or call +61 488 855 709</a>
        </div>
      </aside>

      <div class="faq-main">
        <div class="faq-tools">
          <p class="faq-count" id="faqCount">{total_q} questions</p>
          <button id="faqExpand" class="faq-expand" type="button">Expand all</button>
        </div>
        {groups}
        <p class="faq-noresults" id="faqNoResults" hidden>No questions match that search. <a href="contact.html">Ask us directly &rarr;</a></p>
      </div>
    </div>
  </section>

  <section class="block faq-ways">
    <div class="wrap">
      <div class="section-head center reveal">
        <span class="eyebrow">Prefer to talk?</span>
        <h2>Three easy ways to reach us</h2>
        <p>However you get in touch, a real person responds within one business day.</p>
      </div>
      <div class="ways-grid">
        <a class="way-card reveal" href="contact.html">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M8 2v4M16 2v4M3 9h18M5 5h14a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2z"/></svg></div>
          <h3>Book a meeting</h3>
          <p>Request a complimentary first sit-down at your nearest office.</p>
          <span class="way-go">Start here &rarr;</span>
        </a>
        <a class="way-card reveal" href="tel:+61488855709">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg></div>
          <h3>Call us</h3>
          <p>+61 488 855 709, Monday to Friday, 8:30am - 5:30pm AEST.</p>
          <span class="way-go">+61 488 855 709 &rarr;</span>
        </a>
        <a class="way-card reveal" href="mailto:hello@clear-sky-consulting.au">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg></div>
          <h3>Email us</h3>
          <p>Drop us a note and we'll point you in the right direction.</p>
          <span class="way-go">hello@clear-sky-consulting.au &rarr;</span>
        </a>
      </div>
    </div>
  </section>
'''
    faq_ld = jsonld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
            for _, _, _, items in FAQ_CATS for q, a in items
        ],
    })
    page("faq.html", "Frequently Asked Questions | Clear Sky Consulting",
         "Answers to common questions about Clear Sky Consulting's independent advice, fees, meetings, privacy and how to get started.",
         "faq.html", faq, extra_head=faq_ld)

    # =========================================================================
    # RESOURCES / FREE GUIDES (lead magnets)
    # =========================================================================
    GUIDES_LIST = [
        dict(file="guide-three-questions.pdf", title="The Clear-Head Checklist",
             desc="Three questions that cut through any big decision, with a one-page checklist you can keep by your desk.",
             article="insight-three-questions.html", icon=IC['scale']),
        dict(file="guide-second-opinion.pdf", title="Before You Sign",
             desc="A second-opinion checklist for any significant proposal - exactly what to check before you commit.",
             article="insight-second-opinion.html", icon=IC['check']),
    ]
    guide_cards = "".join(f'''<a class="guide-card reveal" href="assets/{gd['file']}" download>
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{gd['icon']}</svg></div>
        <span class="guide-meta">Free PDF &middot; 2 pages</span>
        <h3>{gd['title']}</h3>
        <p>{gd['desc']}</p>
        <span class="guide-dl"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"><path d="M12 3v12M7 11l5 5 5-5M5 21h14"/></svg>Download the PDF</span>
      </a>''' for gd in GUIDES_LIST)
    resources = f'''
  {page_hero("Resources", "Free guides", "Tools for a <em>clearer head.</em>",
             "Practical, plain-English guides drawn from thousands of advisory conversations. Free to download, nothing to fill in - keep them, share them, use them.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Download</span><h2>Free guides &amp; checklists</h2><p>Short, useful, and free. Each is a two-page PDF you can keep.</p></div>
      <div class="guide-grid">{guide_cards}</div>
    </div>
  </section>

  <section class="block ins-news">
    <div class="wrap">
      <div class="news-card reveal">
        <div class="news-text">
          <span class="eyebrow" style="color:#E2A24A">The Clear Sky Consulting Letter</span>
          <h2>New guides, straight to your inbox.</h2>
          <p>A short, practical note once a month on making big decisions well - and the first to hear when we publish a new guide. No spam, unsubscribe any time.</p>
        </div>
        <form class="news-form" id="newsletter" novalidate>
          <div class="news-row">
            <label class="sr-only" for="newsEmail">Email address</label>
            <input id="newsEmail" type="email" placeholder="you@example.com" required autocomplete="email">
            <button class="btn btn-primary" type="submit">Subscribe</button>
          </div>
          <p class="news-done" id="newsDone" hidden>Thanks - you're on the list. (Demo only - nothing was sent.)</p>
        </form>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Plain English</span><h2>Looking for a term?</h2><p>Our glossary explains the words that get used around advice - without the jargon.</p></div>
      <p style="text-align:center"><a class="btn btn-ghost" href="glossary.html">Open the glossary &rarr;</a></p>
    </div>
  </section>

  {cta_band()}
'''
    page("resources.html", "Free Guides &amp; Resources | Clear Sky Consulting",
         "Free, plain-English guides and checklists from Clear Sky Consulting to help you make big decisions well - download the PDFs, no sign-up required.",
         "resources.html", resources)

    # =========================================================================
    # GLOSSARY
    # =========================================================================
    GLOSSARY = [
        ("Best-interest duty", "An obligation to put your interests ahead of the adviser's own. We hold ourselves to this in practice by refusing commissions and product sales."),
        ("Commission", "A payment an adviser receives from a third party (like a product provider) when you buy something. It creates an incentive to recommend that product. We accept none."),
        ("Conflict of interest", "Any situation where what's best for the adviser and what's best for you can pull in different directions. Independence is about removing these, not just disclosing them."),
        ("Decision fatigue", "The decline in the quality of decisions after a long session of decision-making. Big choices made on a tired mind tend to be worse ones."),
        ("Due diligence", "The careful, independent checking of the facts behind a decision or proposal before you commit to it."),
        ("Fixed fee", "A single price for a defined piece of work, agreed in writing before it begins - so you know the full cost upfront, with no hourly meter."),
        ("Independent advice", "Guidance from someone with no financial stake in the outcome - paid only by you, with nothing to sell. It's the core of how we work."),
        ("Opportunity cost", "The value of the next-best option you give up when you choose one path over another. Often the real cost of a decision."),
        ("Reversible decision", "A choice you can undo at modest cost. These deserve speed; irreversible ones deserve far more care."),
        ("Risk tolerance", "How much uncertainty or potential loss you're genuinely comfortable carrying - which is personal, and rarely just about money."),
        ("Scope of work", "A clear, written description of what an engagement will and won't cover, agreed before any paid work starts."),
        ("Second opinion", "An independent review of a proposal, quote or recommendation before you commit - cheap insurance against an expensive mistake."),
        ("Sunk cost", "Money or effort already spent that you can't get back. It shouldn't drive a forward-looking decision, though it often does."),
        ("Statement of advice", "A formal document a licensed financial adviser must give when providing personal financial product advice. We provide decision-support, not product advice, so we don't issue one."),
    ]
    terms_html = "".join(
        f'''<div class="term reveal" id="{re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")}">
        <dt>{t}</dt><dd>{d}</dd></div>''' for t, d in GLOSSARY)
    glossary_ld = jsonld({
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Clear Sky Consulting glossary",
        "url": f"{SITE_URL}/glossary.html",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": t, "description": plain(d)} for t, d in GLOSSARY
        ],
    })
    glossary = f'''
  {page_hero("Glossary", "Plain English", "The words around <em>advice,</em> explained.",
             "Advice comes wrapped in jargon. Here's what the common terms actually mean - in plain English, with no agenda.")}
  {trust_strip()}

  <section class="block">
    <div class="wrap" style="max-width:820px">
      <dl class="glossary">{terms_html}</dl>
    </div>
  </section>

  {cta_band("Still not sure what something means?", "Ask us - plain answers, no jargon, and your first meeting is on us.")}
'''
    page("glossary.html", "Glossary of Advice Terms | Clear Sky Consulting",
         "A plain-English glossary of personal-advisory and decision-making terms - independence, commissions, fixed fees, second opinions and more.",
         "resources.html", glossary, extra_head=glossary_ld)

    # =========================================================================
    # CONTACT
    # =========================================================================
    office_opts = "".join(f"<option>{o['city']} - {o['addr'].split('<br>')[0]}</option>" for o in OFFICES)
    contact = f'''
  {page_hero("Contact", "Get in touch", "Let's book a <em>meeting.</em>",
             "Tell us a little about what you're weighing up and which office suits you. A real advisor will be in touch within one business day to arrange a time to sit down together - your first meeting is complimentary.")}
  {trust_strip()}

  <section class="block contact">
    <div class="wrap contact-grid">
      <div class="reveal">
        <span class="eyebrow">Talk to us</span>
        <h2>We'd love to help</h2>
        <p class="intro">Fill in the form, or reach us directly - whichever you prefer. Either way, a person responds, not an auto-reply.</p>
        <div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg><div><div class="k">Phone</div><div class="v">{tel("+61 488 855 709")}</div></div></div>
        <div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg><div><div class="k">Email</div><div class="v">{mail("hello@clear-sky-consulting.au")}</div></div></div>
        <div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg><div><div class="k">Offices</div><div class="v">Perth &middot; Brisbane &middot; Adelaide &middot; Sydney &middot; Bendigo</div></div></div>
        <div class="detail"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['clock']}</svg><div><div class="k">Hours</div><div class="v">Mon-Fri, 8:30am-5:30pm AEST</div></div></div>
        <ul class="ticks contact-promise">
          <li>Your first meeting is complimentary</li>
          <li>A real reply within one business day</li>
          <li>No obligation, and no sales pitch</li>
        </ul>
        <p style="margin-top:1.2rem"><a class="btn btn-ghost" href="offices.html">See all office details &rarr;</a></p>
      </div>
      <form id="enquiry" name="enquiry" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="enquiry">
        <p class="hp-field" hidden aria-hidden="true"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <p class="form-title">Request your free meeting</p>
        <div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="phone">Phone (optional)</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="topic">What's this about?</label>
          <select id="topic" name="topic">
            <option>A decision I need help weighing up</option>
            <option>Planning towards a goal</option>
            <option>A second opinion on a proposal</option>
            <option>Ongoing advice</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field"><label for="office">Preferred office</label>
          <select id="office" name="office">{office_opts}<option>Not sure yet</option></select>
        </div>
        <div class="field"><label for="message">A little more detail</label>
          <textarea id="message" name="message" placeholder="No need for everything - just enough to point us in the right direction."></textarea>
        </div>
        <button class="btn btn-primary" type="submit">Send enquiry</button>
        <p class="form-note">A real advisor replies within one business day. We handle your details per our <a href="privacy.html">privacy policy</a>.</p>
        <div class="form-done" id="enquiryDone" hidden role="status">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>
          <h3>Thank you - your enquiry is on its way.</h3>
          <p>A Clear Sky Consulting advisor will be in touch within one business day. If it's urgent, call us on <a href="tel:+61488855709">+61 488 855 709</a>.</p>
        </div>
      </form>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">What happens next</span><h2>From enquiry to sitting down together</h2></div>
      <div class="steps process">
        <div class="step reveal"><h3>You send your note</h3><p>Tell us what's on your mind and which office is easiest for you. A sentence or two is plenty to start.</p></div>
        <div class="step reveal"><h3>We reply within a day</h3><p>A real advisor gets back to you within one business day to find a time that suits - by email or a quick call.</p></div>
        <div class="step reveal"><h3>We meet, on us</h3><p>A relaxed, complimentary first meeting at your nearest office. No obligation to go any further.</p></div>
      </div>
    </div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Other ways to reach us</span><h2>However suits you best</h2></div>
      <div class="ways-grid">
        <a class="way-card reveal" href="tel:+61488855709">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h5l2 5-3 2a12 12 0 005 5l2-3 5 2v5a2 2 0 01-2 2A17 17 0 014 6a2 2 0 012-2z"/></svg></div>
          <h3>Call us</h3>
          <p>+61 488 855 709, Monday to Friday, 8:30am - 5:30pm AEST.</p>
          <span class="way-go">+61 488 855 709 &rarr;</span>
        </a>
        <a class="way-card reveal" href="mailto:hello@clear-sky-consulting.au">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M4 4h16v16H4zM4 7l8 6 8-6"/></svg></div>
          <h3>Email us</h3>
          <p>Drop us a note any time and we'll point you in the right direction.</p>
          <span class="way-go">hello@clear-sky-consulting.au &rarr;</span>
        </a>
        <a class="way-card reveal" href="offices.html">
          <div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7">{IC['pin']}</svg></div>
          <h3>Visit an office</h3>
          <p>Find your nearest of our five offices and the managing director who leads it.</p>
          <span class="way-go">Find an office &rarr;</span>
        </a>
      </div>
    </div>
  </section>
'''
    page("contact.html", "Contact Us & Book a Free Meeting | Clear Sky Consulting",
         "Book a complimentary meeting with Clear Sky Consulting, or reach us by phone or email. Offices in Perth, Brisbane, Adelaide, Sydney and Bendigo.",
         None, contact)

    # =========================================================================
    # 404
    # =========================================================================
    notfound = '''
  <section class="page-hero">
    <div class="sky-field" aria-hidden="true"></div>
    <div class="wrap">
      <div class="notfound reveal">
        <div class="big">404</div>
        <h1>This page drifted off the map.</h1>
        <p>The page you're after may have moved, or perhaps never existed. Let's get you back to clear skies.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="index.html">Back to home</a>
          <a class="btn btn-ghost" href="contact.html">Book a meeting</a>
        </div>
      </div>
    </div>
    <div class="horizon"><span class="sun" aria-hidden="true"></span></div>
  </section>

  <section class="block services">
    <div class="wrap">
      <div class="section-head center reveal"><span class="eyebrow">Popular pages</span><h2>Maybe you were looking for</h2></div>
      <div class="ways-grid">
        <a class="way-card reveal" href="services.html"><div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 3v18M5 8l7-5 7 5"/></svg></div><h3>What we do</h3><p>The four ways clients work with us.</p><span class="way-go">Explore services &rarr;</span></a>
        <a class="way-card reveal" href="pricing.html"><div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 3v18M5 8l7-5 7 5"/></svg></div><h3>Pricing</h3><p>Fixed fees, agreed upfront.</p><span class="way-go">See pricing &rarr;</span></a>
        <a class="way-card reveal" href="offices.html"><div class="way-ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.7"><path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><h3>Offices</h3><p>Find your nearest of our five offices.</p><span class="way-go">Find an office &rarr;</span></a>
      </div>
    </div>
  </section>
'''
    page("404.html", "Page not found - Clear Sky Consulting Pty Ltd",
         "Sorry, we couldn't find that page. Head back to the Clear Sky Consulting home page or get in touch.",
         None, notfound, robots="noindex, follow")

    # =========================================================================
    # PRIVACY + TERMS (regenerated into shared chrome)
    # =========================================================================
    page("privacy.html", "Privacy policy - Clear Sky Consulting Pty Ltd",
         "How Clear Sky Consulting collects, uses, stores and protects your personal information, in line with the Australian Privacy Principles.",
         None, PRIVACY(page_hero))
    page("terms.html", "Terms of engagement - Clear Sky Consulting Pty Ltd",
         "The terms on which Clear Sky Consulting provides its independent personal advisory services across Australia.",
         None, TERMS(page_hero))


# ---------------------------------------------------------------------------
# Articles + insights grid + legal bodies (module-level helpers)
# ---------------------------------------------------------------------------
ARTICLES = [
    dict(fn="insight-three-questions.html", tag="Decision-making", cat="decision-making", thumb=1,
         title="The three questions that cut through any big decision",
         dek="When a choice feels impossibly tangled, these three questions reliably reveal what actually matters.",
         author="Mei Lin Tan", role="Chief Advisory Officer", date="2 June 2026", read="6 min read",
         body=[
             "Most people facing a major decision aren't short of information. They're drowning in it. Every option has a spreadsheet, an opinion, and a friend-of-a-friend who did the opposite and swears by it.",
             "After thousands of clarity sessions, we've found that almost any tangled decision yields to three questions. They won't make the choice for you - but they'll show you what you're really deciding.",
             "## 1. What are you actually choosing between?",
             "It sounds obvious, but most stuck decisions are stuck because the options are blurry. People agonise over a false binary while a third, better option sits unnamed. Write the real options down, plainly. Often the act of naming them resolves half the difficulty.",
             "## 2. What has to be true for each option to be the right one?",
             "Instead of asking which option is best, ask what would have to be true for each to be best. This flips anxiety into investigation. Now you have something concrete to check, rather than a feeling to wrestle.",
             "## 3. Which regret could you not live with?",
             "When options are genuinely close, stop optimising and look at the downside. You can live with most disappointments. The decision usually comes down to the one regret you couldn't make peace with - and that's worth listening to.",
             "None of this requires an advisor. But a good one makes the questions sharper and keeps you honest in answering them. That's most of what a clarity session is.",
         ]),
    dict(fn="insight-second-opinion.html", tag="Independence", cat="independence", thumb=3,
         title="Why a second opinion is the cheapest insurance you'll ever buy",
         dek="Before you sign anything significant, an independent read pays for itself many times over.",
         author="Kenneth Jimmieson", role="Chief Executive Officer", date="19 May 2026", read="5 min read",
         body=[
             "Here's a pattern we see constantly: someone smart, careful and busy is handed a polished proposal. It looks thorough. The person presenting it seems credible. The pressure to proceed is gentle but real. And almost nobody reads it the way they'd read it if they had a free week.",
             "That gap - between how carefully you'd assess something and how carefully you actually can - is where expensive mistakes live.",
             "## The problem isn't the document. It's incentives.",
             "Most proposals are written by someone who benefits if you say yes. That doesn't make them dishonest. It makes them not neutral. A second opinion's entire value is that it has no stake in your answer.",
             "## What an independent review actually finds",
             "Usually not a smoking gun. More often: a clause that quietly shifts risk onto you, an assumption that doesn't hold, a comparison that was never made, or a question you'd want answered before committing. Small things, with large consequences.",
             "## The maths is lopsided",
             "A review costs a fraction of most decisions worth reviewing. If it changes nothing, you proceed with confidence. If it changes one term, it can pay for itself many times over. That asymmetry is why we think second opinions are the cheapest insurance most people never buy.",
         ]),
    dict(fn="insight-decision-fatigue.html", tag="Wellbeing", cat="wellbeing", thumb=2,
         title="Decision fatigue is real - here's how to stop it sabotaging you",
         dek="Big decisions made on a tired, overloaded mind tend to be bad ones. A few simple habits help.",
         author="Sophie Lindgren", role="Chief Client Officer", date="28 April 2026", read="4 min read",
         body=[
             "By the time most people sit down to weigh a major decision, they've already made a few hundred small ones that day. Willpower and judgement are finite, and they run down. Psychologists call it decision fatigue, and it quietly degrades exactly the choices you most want to get right.",
             "## Don't decide when you're depleted",
             "The simplest fix is timing. Reserve big decisions for when you're fresh - for most people, earlier in the day. A decision that feels impossible at 9pm often looks obvious after sleep.",
             "## Shrink the field first",
             "Fatigue comes from holding too many options at once. Eliminate the clearly-worse choices early so your best energy goes to the genuinely close ones. A shorter list is a kinder list.",
             "## Borrow a calm outside head",
             "When you're in it, you can't always see it. Talking a decision through with someone impartial - who isn't tired in the same way you are, and has nothing to gain - restores perspective fast. That's a large part of what we do.",
             "Clear decisions aren't only a matter of intelligence. They're a matter of conditions. Set the conditions, and the thinking gets easier.",
         ]),
    dict(fn="insight-reversible-decisions.html", tag="Decision-making", cat="decision-making", thumb=4,
         title="Reversible or not? A simple test for any big choice",
         dek="The choices you can undo deserve a completely different approach from the ones you can't.",
         author="Kenneth Jimmieson", role="Chief Executive Officer", date="14 April 2026", read="5 min read",
         body=[
             "Not all decisions deserve the same amount of agony. One of the most useful habits you can build is sorting a choice into one of two buckets before you spend a single hour on it: can I undo this, or not?",
             "## Two doors, two speeds",
             "Some decisions are a door you can walk back out of - try the role, the suburb, the subscription, and reverse it at modest cost if it's wrong. Others are one-way doors: selling a family business, a choice with a long legal tail, a bridge you can't un-burn. The common mistake is treating both the same, which means agonising over the reversible ones and rushing the irreversible ones.",
             "## Spend your worry where it counts",
             "For reversible decisions, bias toward action. The cost of deliberating usually exceeds the cost of being briefly wrong, and you learn more from trying than from another week of thinking. For irreversible ones, slow down on purpose: widen your options, seek an outside view, and sit with the downside before you commit.",
             "## The trap: fake irreversibility",
             "Plenty of decisions feel permanent but aren't, and a few feel casual but aren't. Part of thinking clearly is checking the label. Ask: if this turns out wrong in a year, what would it actually take to reverse, and what would that cost? The honest answer often changes how hard the decision really is.",
             "When clients bring us a choice that's been keeping them up at night, the first thing we often do is work out which door they're standing in front of. Surprisingly often, the agony eases the moment they realise the door swings both ways.",
         ]),
    dict(fn="insight-free-advice.html", tag="Independence", cat="independence", thumb=5,
         title="The hidden cost of 'free' advice",
         dek="If you're not paying for the advice, it's worth looking closely at who is - and why.",
         author="Mei Lin Tan", role="Chief Advisory Officer", date="31 March 2026", read="5 min read",
         body=[
             "Advice is never really free. If you aren't paying for it directly, the cost is simply somewhere you can't see - and the most common hiding place is whose interest the advice actually serves.",
             "## Follow the incentive",
             "When someone offers guidance at no charge, ask a plain question: how do they get paid? Often the answer is a commission, a product sale, or a referral fee triggered by you saying yes. None of that makes them villains. It makes their advice a sales conversation wearing the clothes of a neutral one.",
             "## The tilt you can't feel",
             "The danger isn't outright dishonesty - it's the gentle tilt. A recommendation nudged toward the option that pays better. A risk mentioned a little too lightly. An alternative that never comes up because no one earns anything from it. You rarely notice the tilt, because the advice still sounds reasonable. It just isn't pointed entirely at you.",
             "## What 'paid only by you' buys",
             "When the only money on the table is the fee you agree to pay, the incentive collapses to one thing: getting your decision right, so you come back and tell a friend. That's the whole reason we take no commissions and sell no products. It costs us some revenue. It buys you advice you can actually trust.",
             "Free advice has its place - from friends who love you, with no agenda. For decisions that matter, though, it's worth knowing exactly who your adviser is working for. Ideally, it's only you.",
         ]),
    dict(fn="insight-good-second-opinion.html", tag="Money &amp; value", cat="money", thumb=6,
         title="What a good second opinion actually checks",
         dek="A useful review is more than a gut feel. Here's the checklist we run before you sign.",
         author="Aisha Mahmoud", role="General Counsel", date="17 March 2026", read="6 min read",
         body=[
             "When clients ask us to review a proposal before they sign, they often expect a simple yes or no. What they get is more useful: a structured read of the things that are easy to miss when the document is in front of you and the clock is ticking.",
             "## 1. Who carries the risk?",
             "The first thing we trace is where the risk sits. Proposals are often written so that costs, delays or things going wrong land on you rather than the other side. A single clause about variations, liability or termination can quietly rewrite the deal. We map who's holding what if things don't go to plan.",
             "## 2. What's assumed, not stated?",
             "Every proposal rests on assumptions - about timing, scope, conditions and what's included. The expensive ones are the assumptions that were never written down. We surface them and ask whether they actually hold for your situation.",
             "## 3. What isn't being compared?",
             "A proposal naturally frames itself as the obvious choice. Part of a good review is reintroducing the alternatives it conveniently leaves out - including the option of doing nothing, or simply waiting.",
             "## 4. What would you ask if you had a month?",
             "Finally, we write down the questions you'd reach if you had unlimited time, so you can take the three or four that matter most back to the table. More often than not, those questions - not a flat refusal - are what improve the deal.",
             "A good second opinion rarely ends in drama. It ends in a clearer head, a shorter list of real concerns, and the confidence to proceed or to walk away. That is the entire point.",
         ]),
    dict(fn="insight-planning-backwards.html", tag="Planning", cat="planning", thumb=1,
         title="Plan backwards: start from the outcome, not the next step",
         dek="The most reliable plans are built in reverse, from the finish line back to this week.",
         author="Sophie Lindgren", role="Chief Client Officer", date="3 March 2026", read="5 min read",
         body=[
             "Most plans fail in the same way: they start from where you are and ask 'what's the next step?' It feels productive, but it tends to produce a plan shaped by today's constraints rather than tomorrow's goal. The fix is to build the plan in reverse.",
             "## Start at the finish line",
             "Picture the outcome you actually want - concretely, and dated. Not 'be more secure' but a specific picture at a specific time. Then ask what has to be true the step before that, and the step before that, working backwards until you arrive at something you can do this week.",
             "## Backwards planning exposes the real bottleneck",
             "Planning forwards, you tend to schedule the easy things first. Planning backwards, the genuine constraint shows up early - the one thing everything else depends on. That's where your attention belongs, and it's usually not where you'd have started.",
             "## Leave room for the plan to be wrong",
             "A good backwards plan isn't a rigid script; it's a sequence with checkpoints. At each milestone you gain new information and adjust. The point isn't to predict the future perfectly - it's to always know the next move, and why it's next.",
             "When we build plans with clients, we spend the first session almost entirely on the destination, because a clear finish line does most of the work. Get that right, and the steps tend to arrange themselves.",
         ]),
    dict(fn="insight-money-decisions.html", tag="Money &amp; value", cat="money", thumb=2,
         title="Money decisions are rarely about money",
         dek="The numbers matter - but they're almost never what the decision is really about.",
         author="Mei Lin Tan", role="Chief Advisory Officer", date="17 February 2026", read="6 min read",
         body=[
             "People come to us with what look like financial decisions - whether to sell, to commit, to spend, to wait. We take the numbers seriously. But after enough of these conversations, a pattern is hard to ignore: the money is rarely the real question.",
             "## The number is a proxy",
             "Underneath a money decision there's almost always something else: security, freedom, status, family, fear, a sense of fairness, a story about who you are. The dollar figure is just the visible handle on a much more personal lever. Decide only on the number and you often solve the wrong problem.",
             "## Why this matters for the decision",
             "Two people facing identical figures will rightly choose differently, because the figures mean different things to them. That's not irrationality - it's the part of the decision a spreadsheet can't hold. Good advice makes room for it instead of pretending it away.",
             "## Naming it changes the maths",
             "Once you name what the money actually represents for you, the trade-offs get clearer, not murkier. The option that looked worse on paper sometimes turns out to be obviously right - and you can choose it without guilt, because you understand why.",
             "This is why our first questions are rarely financial. Tell us what the decision would change about your life, and the numbers tend to fall into place around the answer.",
         ]),
    dict(fn="insight-life-transitions.html", tag="Life transitions", cat="transitions", thumb=3,
         title="Deciding well when everything is changing at once",
         dek="Big transitions scramble judgement. A few simple anchors keep you steady.",
         author="Sophie Lindgren", role="Chief Client Officer", date="3 February 2026", read="6 min read",
         body=[
             "A new job, a move, a relationship beginning or ending, a loss, a windfall - big transitions tend to arrive with a pile of decisions attached. And they're the worst possible time to make them, because the ground you'd normally stand on to decide is the very thing that's shifting.",
             "## Why transitions scramble judgement",
             "During a transition, your routines, your sense of identity and your usual reference points are all in flux at once. Everything feels urgent, and it's genuinely hard to tell which decisions truly are. That combination pushes people into choices they later wish they'd slept on.",
             "## Anchor 1: separate the urgent from the merely loud",
             "Very few decisions in a transition actually have to be made today. Write them all down, then mark only the ones with real deadlines. Most of the noise can wait - and waiting is often the most powerful move available to you.",
             "## Anchor 2: borrow stability from outside",
             "When your own footing is unsteady, an impartial person who already understands your situation becomes disproportionately valuable - not to decide for you, but to hold the context steady while you think. It's one of the main reasons clients keep an ongoing advisor through life's bigger turns.",
             "## Anchor 3: decide in pencil",
             "Where you can, make reversible moves and revisit them once the dust settles. Treat early decisions as drafts, not verdicts. Clarity returns - it always does - and you want to have kept your options open until it does.",
             "Transitions end. The decisions you make during them can outlast the turbulence by years, so the kindest thing you can do for your future self is to decide slowly, lean on steady help, and keep as many doors open as you reasonably can.",
         ]),
]

TOPIC_LABELS = {
    "decision-making": "Decision-making",
    "independence": "Independence",
    "planning": "Planning",
    "money": "Money &amp; value",
    "wellbeing": "Wellbeing",
    "transitions": "Life transitions",
}


def insights_grid(g, limit=None):
    AUTHORS = g["AUTHORS"]
    scene = g["scene"]
    arts = ARTICLES[:limit] if limit else ARTICLES
    cards = ""
    for a in arts:
        img = AUTHORS.get(a["author"], "exec-1.svg")
        thumb = scene("scene-" + a["fn"].replace(".html", ""), f"thumb-{a['thumb']}.svg")
        cards += f'''<article class="ins-card reveal" data-cat="{a['cat']}">
        <a class="ins-thumb" href="{a['fn']}"><img src="assets/{thumb}" alt="{plain_attr(a['title'])}" loading="lazy" width="640" height="360"><span class="ins-cat">{a['tag']}</span></a>
        <div class="ins-body">
          <h3><a href="{a['fn']}">{a['title']}</a></h3>
          <p>{a['dek']}</p>
          <div class="ins-by"><img src="assets/{img}" alt="" width="34" height="34"><span><b>{a['author']}</b>{a['date']} &middot; {a['read']}</span></div>
        </div>
      </article>'''
    return f'<div class="ins-grid">{cards}</div>'


def PRIVACY(page_hero):
    return f'''
  {page_hero("Privacy policy", "Legal", "Privacy policy",
             "Confidentiality is the foundation of honest advice. This policy explains how we handle the personal information you trust us with.")}
  <section class="block">
    <div class="wrap"><div class="prose reveal">
      <p class="updated">Last updated: 22 June 2026</p>
      <p>Clear Sky Consulting Pty Ltd (<strong>“Clear Sky Consulting”</strong>, <strong>“we”</strong>, <strong>“us”</strong>) is committed to protecting your privacy. This policy describes how we collect, use, disclose and safeguard your personal information, in line with the <em>Privacy Act 1988</em> (Cth) and the Australian Privacy Principles (APPs).</p>
      <h2>1. The information we collect</h2>
      <p>We only collect personal information reasonably necessary to provide our advisory services, including your contact details, the details of your enquiry, information about your circumstances and goals, and limited website-usage data.</p>
      <h2>2. How we collect it</h2>
      <p>We collect information directly from you - through our enquiry form, by email, over correspondence, and in person - wherever it is reasonable and practical to do so.</p>
      <h2>3. How we use your information</h2>
      <p>We use your information to respond to your enquiry, deliver and tailor our services, communicate with you, and meet our legal obligations. We do <strong>not</strong> sell your information, and we receive no commissions that would create an incentive to share it.</p>
      <h2>4. Disclosure to others</h2>
      <p>We treat your information as strictly confidential and disclose it only with your consent, to trusted service providers bound by confidentiality, or where required by law.</p>
      <h2>5. How we store and protect it</h2>
      <p>We take reasonable steps to protect your information from misuse, loss and unauthorised access through secure storage, restricted access and confidentiality obligations, and we securely destroy or de-identify it when no longer needed.</p>
      <h2>6. Accessing and correcting your information</h2>
      <p>You may request access to the information we hold about you and ask us to correct it. We will respond within a reasonable period.</p>
      <h2>7. Cookies and analytics</h2>
      <p>We set cookies only after you accept them. With your consent, we use privacy-respecting analytics (with IP addresses anonymised) to understand, in aggregate, how our website is used; if you decline, none are set. You can change your choice at any time via &ldquo;Cookie preferences&rdquo; in the footer. Our enquiry form transmits only the details you choose to provide.</p>
      <h2>8. Changes to this policy</h2>
      <p>We may update this policy from time to time. The current version will always be available on this page.</p>
      <h2>9. How to contact us</h2>
      <p>For any privacy question or complaint, contact <a href="mailto:privacy@clear-sky-consulting.au">privacy@clear-sky-consulting.au</a>. If you are not satisfied with our response, you may contact the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener">oaic.gov.au</a>.</p>
      <p style="margin-top:2rem"><a class="btn btn-ghost" href="index.html">← Back to home</a></p>
    </div></div>
  </section>
'''


def TERMS(page_hero):
    return f'''
  {page_hero("Terms of engagement", "Legal", "Terms of engagement",
             "Clear from the first conversation - including the terms on which we work together. Here's what you can expect from us, and what we ask of you.")}
  <section class="block">
    <div class="wrap"><div class="prose reveal">
      <p class="updated">Last updated: 22 June 2026</p>
      <p>These terms set out the general basis on which Clear Sky Consulting Pty Ltd provides its advisory services. They are supplemented by the specific scope and fee we agree with you in writing before any work begins; where the two differ, the written engagement prevails.</p>
      <h2>1. Our services</h2>
      <p>Clear Sky Consulting provides independent advisory and decision-support services to individuals and families. We provide considered opinions and recommendations; the final decision, and responsibility for acting on it, always remains yours.</p>
      <h2>2. Independence</h2>
      <p>We are genuinely independent. We do not receive commissions, referral fees or third-party incentives. Our only compensation is the fee you agree to pay us directly.</p>
      <h2>3. A complimentary first meeting</h2>
      <p>Your initial introductory meeting is free and without obligation. No advisory relationship is formed until we agree a scope of work in writing.</p>
      <h2>4. Scope of work</h2>
      <p>Before any paid work begins, we agree a clear scope describing what we will do and deliver. If your needs change, we agree any change (and related fee) with you before continuing.</p>
      <h2>5. Fees</h2>
      <p>We work on <strong>fixed fees agreed upfront</strong>. You will know the cost before work starts, with no hourly meter. Fees are quoted in Australian dollars and exclude GST unless stated otherwise.</p>
      <h2>6. Your responsibilities</h2>
      <p>So we can advise you well, you agree to give us accurate, complete and timely information, to tell us promptly if your situation changes, and to understand that our advice is based on the information you provide at the time.</p>
      <h2>7. Nature of our advice</h2>
      <p>Our advice is tailored to your situation as you describe it and is current as at the date given. It does not constitute legal, tax, accounting or licensed financial product advice unless we expressly say so in writing.</p>
      <h2>8. Confidentiality</h2>
      <p>Everything you share is treated as strictly confidential and handled per our <a href="privacy.html">Privacy policy</a>.</p>
      <h2>9. How we meet</h2>
      <p>We advise in person, at one of our offices in Perth, Brisbane, Adelaide, Sydney or Bendigo. We do not provide advice over the phone.</p>
      <h2>10. Limitation of liability</h2>
      <p>To the extent permitted by law, our liability arising from an engagement is limited to the fees paid for that engagement. Nothing excludes rights you have under the <em>Australian Consumer Law</em> that cannot lawfully be excluded.</p>
      <h2>11. Ending an engagement</h2>
      <p>You may end an engagement at any time in writing. If it ends early, you remain responsible for fees fairly attributable to the work completed.</p>
      <h2>12. Governing law</h2>
      <p>These terms are governed by the laws of the State or Territory in which your engaging Clear Sky Consulting office is located.</p>
      <h2>13. Questions</h2>
      <p>If anything here is unclear, please ask. Contact us at <a href="mailto:hello@clear-sky-consulting.au">hello@clear-sky-consulting.au</a>.</p>
      <p style="margin-top:2rem"><a class="btn btn-ghost" href="index.html">← Back to home</a></p>
    </div></div>
  </section>
'''
