/**
 * payment-config.js  —  read-only status check (no secrets exposed)
 *
 * Open /.netlify/functions/payment-config in a browser to see what the LIVE
 * deployed function actually resolves to. It reports the mode and whether each
 * credential is present, but never the credential values themselves.
 *
 * Safe to leave in place, or delete once payments are confirmed working.
 */
exports.handler = async () => {
  const raw = process.env.AIRWALLEX_ENV;
  const env = (raw || 'prod').toLowerCase();
  const demo = env === 'demo' || env === 'sandbox' || env === 'test';
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    body: JSON.stringify({
      resolved_mode: demo ? 'demo (SANDBOX — no real charges)' : 'prod (LIVE — real charges)',
      AIRWALLEX_ENV_raw: raw || '(not set — defaults to prod)',
      hasClientId: !!process.env.AIRWALLEX_CLIENT_ID,
      hasApiKey: !!process.env.AIRWALLEX_API_KEY,
      hosts: demo
        ? { api: 'https://api-demo.airwallex.com', pci: 'https://pci-api-demo.airwallex.com' }
        : { api: 'https://api.airwallex.com', pci: 'https://pci-api.airwallex.com' },
      note: 'If resolved_mode is not prod/LIVE, set AIRWALLEX_ENV=prod in Netlify and redeploy.',
    }, null, 2),
  };
};
