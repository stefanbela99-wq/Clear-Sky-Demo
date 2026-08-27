# Clear Sky Consulting Pty Ltd — website (demo)

A full marketing + corporate website for **Clear Sky Consulting**, a fictional
**private** Australian independent personal advisory firm. Static site, no build
step required to view — open `index.html` or serve the folder with any static
host.

> ⚠️ **This is a demo.** All people, photos, emails, phone numbers, awards and
> testimonials are **fictional / AI-generated** placeholders. Replace them with
> real content before going anywhere near production.

## Pages (22)

**Core**
- `index.html` — home (hero, metrics, services, stats, process, insights)
- `about.html` — company story, mission, timeline, values, awards
- `leadership.html` — executive team, board of directors, regional MDs
- `offices.html` — five office locations with contacts & directions
- `careers.html` — why Clear Sky Consulting, benefits, open roles
- `press.html` — newsroom / announcements
- `contact.html` — booking form + contact details
- `faq.html` — frequently asked questions

**What we do**
- `services.html` — overview
- `service-decision-clarity.html`
- `service-planning-strategy.html`
- `service-second-opinion.html`
- `service-ongoing-advisory.html`
- `approach.html` — how we work
- `pricing.html` — fixed-fee plans

**Resources**
- `insights.html` — article listing
- `insight-three-questions.html`
- `insight-second-opinion.html`
- `insight-decision-fatigue.html`
- `case-studies.html` — illustrative client stories

**Legal**
- `privacy.html`, `terms.html`

**Utility**
- `404.html` — styled not-found page (point your host's 404 handler at it)

## Structure

- `styles.css` — all styles (single shared stylesheet)
- `main.js` — nav toggle, mobile dropdowns, scroll reveal, count-up stats,
  accordions, category filters, newsletter + contact-form → mailto
- `assets/` — generated placeholder portraits (`exec-*`, `board-*`, `reg-*`,
  `founder-*`), decorative thumbnails (`thumb-*`), `favicon.svg`, `og-image.svg`
- `build/` — the generator that produces every HTML page from shared chrome

## SEO / social

Every page includes a favicon, Open Graph and Twitter card meta tags. Two
caveats before going live:
- **`og-image.svg` is an SVG** (no PNG converter was available here). Most social
  platforms want a **1200×630 PNG/JPG** — export one and update the `og:image` /
  `twitter:image` paths in `build/generate.py`.
- Social scrapers need **absolute URLs**. Once you have a domain, prefix the
  image paths (e.g. `https://yourdomain/assets/og-image.svg`).

## Regenerating the site

Every page is produced from one source of truth so the nav, footer and styling
stay identical across all 23 pages:

```bash
python3 build/generate.py
```

Edit content/people in `build/pages.py` and `build/generate.py`, then re-run.

## Replace before going live

- **People** — names, roles, bios in `build/generate.py` (`EXEC`, `BOARD`,
  `REGIONAL`) and the portrait SVGs in `assets/` (swap for real headshots).
- **Contact details** — `hello@clear-sky-consulting.au`, `1300 CLEAR SKY`, all
  `+61 …` numbers, and per-office emails/phones.
- **ABN** — placeholder in the footer.
- **Testimonials / case studies / awards / press** — all illustrative.
- **Contact form** — currently opens the visitor's email app via `mailto`;
  swap for a real backend in `main.js` when ready.
