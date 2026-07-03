# Clear Sky Consulting — Website

A lightweight, multi-page marketing website for **Clear Sky Consulting** —
online business consulting by **Kenneth Jimmieson** for small business owners
and private clients.

Built as a static site (plain HTML, CSS and a little JavaScript), so it can be
hosted anywhere with no build step or server-side code.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Home — hero, services overview, about preview, calls to action |
| `about.html` | About Kenneth, approach and values |
| `services.html` | Full list of services + how it works |
| `apply.html` | Application form to work together |
| `contact.html` | Contact details + contact form |
| `payment.html` | Payment page (**Coming Soon**) |

## Your photo

The site looks for your headshot at **`assets/img/kenneth.jpg`**. Until that
file exists, a placeholder illustration is shown automatically.

To add your photo:

1. Save your headshot as `kenneth.jpg`.
2. Drop it into the `assets/img/` folder (replace nothing else).
3. Refresh the site — it will appear on the Home and About pages.

A square image (e.g. 600×600px or larger) works best.

## Making the forms live

Both the **Contact** and **Application** forms currently run in demo mode: they
show a success message but do not send anywhere. To receive real submissions,
use a no-code form backend such as [Formspree](https://formspree.io) or
[Netlify Forms](https://docs.netlify.com/forms/setup/):

1. In `contact.html` and `apply.html`, find the `<form ...>` tag.
2. Set `action` to your form endpoint URL and keep `method="post"`.
3. Remove the `data-demo-form` attribute so the browser submits normally.

## Contact / business details

- **Business:** Clear Sky Consulting
- **Consultant:** Kenneth Jimmieson
- **Phone:** +61 488 855 709
- **Website:** clear-sky-consulting.au
- **Email:** hello@clear-sky-consulting.au *(update to your real inbox)*

> Note: the email address above is a suggested placeholder. Replace
> `hello@clear-sky-consulting.au` throughout the site with your real address.

## Running locally

Just open `index.html` in your browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploying

Upload all files to any static host — Netlify, Cloudflare Pages, GitHub Pages,
Vercel, or traditional cPanel/FTP hosting for your `clear-sky-consulting.au`
domain. Keep the folder structure intact.
