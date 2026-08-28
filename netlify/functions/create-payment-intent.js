/**
 * create-payment-intent.js  —  Netlify serverless function
 *
 * Creates an Airwallex PaymentIntent server-side and returns the id +
 * client_secret to the browser, so the frontend never sees the secret API key.
 *
 * Required environment variables (Netlify > Site settings > Environment variables):
 *   AIRWALLEX_CLIENT_ID   Your Client ID   (Airwallex webapp > Account settings > Developer)
 *   AIRWALLEX_API_KEY     Your API key     (same place — keep secret)
 *   AIRWALLEX_ENV         "prod" (live charges, default) or "demo" (sandbox)
 *
 * Prices are fixed here on the server so the amount a client pays can't be
 * tampered with in the browser. "custom" lets a client pay an advisor-agreed
 * amount, bounded for sanity.
 */

const CURRENCY = 'AUD';
const COUNTRY = 'AU';

// Fixed catalogue (AUD, whole dollars). Mirrors pricing.html.
const SERVICES = {
  'decision-clarity': { label: 'Decision clarity session', amount: 2350 },
  'planning-strategy': { label: 'Planning & strategy',      amount: 3500 },
  'second-opinion':    { label: 'Second opinion review',    amount: 1650 },
  'ongoing-advisory':  { label: 'Ongoing advisory',         amount: 4750 },
  'custom':            { label: 'Custom invoice',           amount: null }, // amount supplied by client, bounded below
};
const CUSTOM_MIN = 1;
const CUSTOM_MAX = 50000;

function hosts() {
  const env = (process.env.AIRWALLEX_ENV || 'demo').toLowerCase();
  // Live by default. Only an explicit demo/sandbox value uses the sandbox hosts.
  const demo = env === 'demo' || env === 'sandbox' || env === 'test';
  return {
    env: demo ? 'demo' : 'prod',
    api: demo ? 'https://api-demo.airwallex.com' : 'https://api.airwallex.com',
    pci: demo ? 'https://pci-api-demo.airwallex.com' : 'https://pci-api.airwallex.com',
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

  // Billing details (used for AVS / risk assessment). Collected on the form.
  const b = (input.billing && typeof input.billing === 'object') ? input.billing : {};
  const addr = (b.address && typeof b.address === 'object') ? b.address : {};
  const trimmed = (v) => (typeof v === 'string' ? v.trim() : '');
  const billing = {
    first_name: trimmed(b.first_name) || trimmed(name).split(' ')[0] || trimmed(name),
    last_name: trimmed(b.last_name) || trimmed(name).split(' ').slice(1).join(' ') || trimmed(name),
    email: trimmed(email),
    phone_number: trimmed(b.phone_number) || undefined,
    address: {
      street: trimmed(addr.street),
      city: trimmed(addr.city),
      state: trimmed(addr.state),
      postcode: trimmed(addr.postcode),
      country_code: (trimmed(addr.country_code) || 'AU').toUpperCase().slice(0, 2),
    },
  };
  const a = billing.address;
  if (!a.street || !a.city || !a.state || !a.postcode || !a.country_code) {
    return json(400, { error: 'Please enter your full billing address (street, city, state and postcode).' });
  }

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
      return json(502, {
        error: 'Could not authenticate with the payment provider.',
        detail: `auth HTTP ${loginRes.status} — check the API key / Client ID match the ${env} environment. ${t.slice(0, 300)}`,
      });
    }
    const token = (await loginRes.json()).token;

    // STEP 2 — create the PaymentIntent.
    const newReqId = () => (globalThis.crypto?.randomUUID?.() || (String(Date.now()) + Math.random()));

    // Metadata for the merchant's dashboard (not read by the risk engine).
    const metadata = {
      service,
      service_label: svc.label,
      customer_name: `${billing.first_name} ${billing.last_name}`.trim(),
      customer_email: billing.email,
      customer_phone: billing.phone_number || '',
      billing_city: a.city,
      billing_state: a.state,
      billing_postcode: a.postcode,
      billing_country: a.country_code,
    };

    // Best-effort: create a Customer so the payment carries a customer_id (a
    // persistent profile the risk engine can use). Failure never blocks payment.
    let customerId;
    try {
      const custRes = await fetch(`${pci}/api/v1/pa/customers/create`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          request_id: newReqId(),
          merchant_customer_id: 'CSC-' + newReqId(),
          first_name: billing.first_name,
          last_name: billing.last_name,
          email: billing.email,
          phone_number: billing.phone_number,
          address: { city: a.city, country_code: a.country_code, postcode: a.postcode, state: a.state, street: a.street },
        }),
      });
      if (custRes.ok) {
        customerId = (await custRes.json()).id;
      } else {
        console.error('Airwallex customer create failed (continuing without customer_id)', custRes.status, (await custRes.text()).slice(0, 300));
      }
    } catch (e) {
      console.error('Airwallex customer create error (continuing)', e && e.message);
    }

    const createIntent = (body) => fetch(`${pci}/api/v1/pa/payment_intents/create`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const baseBody = { amount, currency: CURRENCY, merchant_order_id: orderId, descriptor: 'Clear Sky Consulting', metadata };
    // Enriched body: customer_id + order (line item + shipping address) for extra
    // risk signal. AVS billing is still applied at card confirmation (element `billing`).
    const enrichedBody = {
      ...baseBody,
      request_id: newReqId(),
      ...(customerId ? { customer_id: customerId } : {}),
      order: {
        products: [{
          name: svc.label,
          desc: svc.label + ' - Clear Sky Consulting',
          unit_price: amount,
          currency: CURRENCY,
          quantity: 1,
          url: 'https://www.clear-sky-consulting.au/payment.html',
        }],
        shipping: {
          first_name: billing.first_name,
          last_name: billing.last_name,
          phone_number: billing.phone_number,
          address: { city: a.city, country_code: a.country_code, postcode: a.postcode, state: a.state, street: a.street },
        },
      },
    };

    let intentRes = await createIntent(enrichedBody);
    let intent = await intentRes.json();
    if (!intentRes.ok) {
      // Never regress: if the enriched payload is rejected, retry with the minimal
      // known-good body (metadata only) so the payment still goes through.
      console.error('Airwallex enriched intent create failed, retrying minimal', intentRes.status, JSON.stringify(intent).slice(0, 300));
      intentRes = await createIntent({ ...baseBody, request_id: newReqId() });
      intent = await intentRes.json();
    }
    if (!intentRes.ok) {
      console.error('Airwallex intent create failed', intentRes.status, intent);
      const code = intent && (intent.code || intent.error || '');
      const message = intent && (intent.message || intent.detail || '');
      return json(502, {
        error: 'Could not start the payment.',
        detail: `create-intent HTTP ${intentRes.status}${code ? ' [' + code + ']' : ''}${message ? ' ' + message : ''}`.trim(),
      });
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
      billing,
      env,
    });
  } catch (err) {
    console.error('create-payment-intent error', err);
    return json(500, { error: 'Something went wrong starting your payment. Please try again.' });
  }
};
