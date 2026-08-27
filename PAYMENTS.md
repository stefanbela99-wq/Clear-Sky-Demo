# Online payments (Airwallex)

Clients can pay for a service by card from **`/payment.html`**: they pick a service
(or enter a custom, advisor-agreed amount), review the invoice summary, and pay with
a card field embedded on the page (Airwallex Drop-in). Card details go straight to
Airwallex — they never touch our server. On success they land on `/payment-success.html`.

## How it works

1. **`payment.html`** (frontend) collects the service, name and email, then calls the
   serverless function to create a payment intent, and mounts the Airwallex Drop-in
   element with the returned `client_secret`.
2. **`netlify/functions/create-payment-intent.js`** (backend) authenticates to Airwallex
   with the secret API key, creates a PaymentIntent for a **server-fixed price**, and
   returns only `{ id, client_secret, amount, ... }` to the browser.

Prices live in the function (`SERVICES`) so they can't be tampered with in the browser.
The `custom` option lets a client pay an advisor-agreed amount, bounded $1–$50,000.

## Going live — what you need to do

1. **Airwallex account** with Online Payments activated (requires business KYC).
2. In **Netlify → Site settings → Environment variables**, add:
   - `AIRWALLEX_CLIENT_ID`
   - `AIRWALLEX_API_KEY`
   - `AIRWALLEX_ENV` = `demo` while testing, `prod` for real charges
   (Find the Client ID / API key in Airwallex → Account settings → Developer.)
3. Redeploy. That's it — the function picks up the keys at runtime.

## Testing (sandbox)

With `AIRWALLEX_ENV=demo` and demo keys, a yellow "Test mode" banner shows and no real
money moves. Use Airwallex's test card **4035 5010 0000 0008**, any future expiry, any CVC.
Run locally with `netlify dev` (copy `.env.example` to `.env` first).

## Notes / possible next steps

- **Receipts/invoices:** Airwallex emails a payment confirmation. For formal branded
  invoices (line items, PDF), consider Airwallex's invoicing product or a generated
  receipt — not included here.
- **GST:** prices mirror `pricing.html` and exclude GST; adjust the `SERVICES` amounts
  if you want tax-inclusive charging.
- **Discoverability:** the payment page is linked from the footer and `pricing.html`.
  It's set to `noindex` so it stays out of search results.
