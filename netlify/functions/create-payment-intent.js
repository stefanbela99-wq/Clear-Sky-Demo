/**
 * create-payment-intent.js  —  Netlify serverless function
 *
 * Creates an Airwallex PaymentIntent server-side and returns the id +
 * client_secret to the browser, so the frontend never sees the secret API key.
 *
 * Required environment variables (Netlify > Site settings > Environment variables):
 *   AIRWALLEX_CLIENT_ID   Your Client ID   (Airwallex webapp > Account settings > Developer)
 *   AIRWALLEX_API_KEY     Your API key     (same place — keep secret)
 *   AIRWALLEX_ENV         "demo" (sandbox, default) or "prod" (live charges)
 *
 * Prices are fixed here on the server so the amount a client pays can't be
 * tampered with in the browser. "custom" lets a client pay an advisor-agreed
 * amount, bounded for sanity.
 */

const CURRENCY = 'AUD';
const COUNTRY = 'AU';

// Fixed catalogue (AUD, whole dollars). Mirrors pricing.html.
const SERVICES = {
  'decision-clarity': { label: 'Decision clarity session', amount: 1200 },
  'planning-strategy': { label: 'Planning & strategy',      amount: 3500 },
  'second-opinion':    { label: 'Second opinion review',    amount: 900 },
  'ongoing-advisory':  { label: 'Ongoing advisory',         amount: 4800 },
  'custom':            { label: 'Custom invoice',           amount: null }, // amount supplied by client, bounded below
};
const CUSTOM_MIN = 1;
const CUSTOM_MAX = 50000;

function hosts() {
  const env = (process.env.AIRWALLEX_ENV || 'demo').toLowerCase();
  const prod = env === 'prod' || env === 'production';
  return {
    env: prod ? 'prod' : 'demo',
    api: prod ? 'https://api.airwallex.com' : 'https://api-demo.airwallex.com',
    pci: prod ? 'https://pci-api.airwallex.com' : 'https://pci-api-demo.airwallex.com',
  };
}

function json(statusCode, body) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify(body),
  };
}

const isEmail = (s) => typeof s === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s.trim());

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'Method not allowed' });
  }

  const clientId = process.env.AIRWALLEX_CLIENT_ID;
  const apiKey = process.env.AIRWALLEX_API_KEY;
  if (!clientId || !apiKey) {
    return json(500, { error: 'Payment is not configured yet. Please contact us to complete your payment.' });
  }

  let input;
  try {
    input = JSON.parse(event.body || '{}');
  } catch {
    return json(400, { error: 'Invalid request.' });
  }

  const { service, name, email } = input;
  const svc = SERVICES[service];
  if (!svc) return json(400, { error: 'Please choose a valid service.' });
  if (!isEmail(email)) return json(400, { error: 'Please enter a valid email address.' });
  if (!name || !String(name).trim()) return json(400, { error: 'Please enter your name.' });

  // Resolve amount: fixed from catalogue, or a bounded client-supplied amount for "custom".
  let amount;
  if (svc.amount != null) {
    amount = svc.amount;
  } else {
    amount = Number(input.amount);
    if (!Number.isFinite(amount) || amount < CUSTOM_MIN || amount > CUSTOM_MAX) {
      return json(400, { error: `Please enter an amount between $${CUSTOM_MIN} and $${CUSTOM_MAX.toLocaleString()}.` });
    }
    amount = Math.round(amount * 100) / 100; // allow cents, guard float noise
  }

  const { env, api, pci } = hosts();
  const orderId = 'CSC-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();

  try {
    // STEP 1 — authenticate to get a short-lived bearer token.
    const loginRes = await fetch(`${api}/api/v1/authentication/login`, {
      method: 'POST',
      headers: { 'x-client-id': clientId, 'x-api-key': apiKey, 'Content-Type': 'application/json' },
    });
    if (!loginRes.ok) {
      const t = await loginRes.text();
      console.error('Airwallex auth failed', loginRes.status, t);
      return json(502, { error: 'Could not reach the payment provider. Please try again shortly.' });
    }
    const token = (await loginRes.json()).token;

    // STEP 2 — create the PaymentIntent.
    const intentRes = await fetch(`${pci}/api/v1/pa/payment_intents/create`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        request_id: (globalThis.crypto?.randomUUID?.() || String(Date.now()) + Math.random()),
        amount,
        currency: CURRENCY,
        merchant_order_id: orderId,
        descriptor: 'Clear Sky Consulting',
        metadata: { service, service_label: svc.label, customer_name: String(name).trim(), customer_email: String(email).trim() },
      }),
    });

    const intent = await intentRes.json();
    if (!intentRes.ok) {
      console.error('Airwallex intent create failed', intentRes.status, intent);
      return json(502, { error: 'Could not start the payment. Please try again shortly.' });
    }

    // Only hand back what the browser needs. Never return the token or keys.
    return json(200, {
      id: intent.id,
      client_secret: intent.client_secret,
      currency: CURRENCY,
      country_code: COUNTRY,
      amount,
      service: svc.label,
      order_id: orderId,
      env,
    });
  } catch (err) {
    console.error('create-payment-intent error', err);
    return json(500, { error: 'Something went wrong starting your payment. Please try again.' });
  }
};
