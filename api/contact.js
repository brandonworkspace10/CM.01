// In-memory rate limit (best-effort; persists per warm instance)
const submissions = new Map();
const RATE_LIMIT = 3;
const RATE_WINDOW = 60 * 60 * 1000; // 1 hour

function checkRate(ip) {
  const now = Date.now();
  const recent = (submissions.get(ip) || []).filter(t => now - t < RATE_WINDOW);
  if (recent.length >= RATE_LIMIT) return false;
  recent.push(now);
  submissions.set(ip, recent);
  return true;
}

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  if (!process.env.RESEND_API_KEY) {
    console.error('RESEND_API_KEY env variable is missing');
    return res.status(500).json({ error: 'Email service not configured' });
  }

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (!checkRate(ip)) {
    return res.status(429).json({ error: 'Too many submissions. Try again later.' });
  }

  const { name, business, email, phone, type, volume, message, website } = req.body || {};

  // Honeypot — real users never fill this field (hidden via CSS)
  if (website) {
    console.warn('Honeypot tripped from IP:', ip);
    return res.status(200).json({ ok: true }); // silently succeed so bots don't retry
  }

  if (!name || !business || !email || !phone) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Basic email format check
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Invalid email address' });
  }

  // Cap field lengths to prevent abuse
  const capped = {
    name: String(name).slice(0, 120),
    business: String(business).slice(0, 160),
    email: String(email).slice(0, 160),
    phone: String(phone).slice(0, 40),
    type: String(type || '').slice(0, 60),
    volume: String(volume || '').slice(0, 40),
    message: String(message || '').slice(0, 2000),
  };

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'Calling Matrix <hello@callingmatrix.com>',
      to: ['callingmatrix@gmail.com'],
      reply_to: capped.email,
      subject: `New Lead: ${capped.business} — ${capped.type || 'Home Service'}`,
      html: `
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;color:#1a1a1a;">
          <h2 style="font-size:22px;margin-bottom:4px;">New Contact Form Submission</h2>
          <p style="color:#666;font-size:13px;margin-bottom:24px;">Submitted via callingmatrix.com</p>
          <table style="width:100%;border-collapse:collapse;font-size:15px;line-height:1.8;">
            <tr><td style="padding:8px 0;color:#666;width:160px;">Name</td><td style="padding:8px 0;font-weight:600;">${esc(capped.name)}</td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Business</td><td style="padding:8px 12px;font-weight:600;">${esc(capped.business)}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Email</td><td style="padding:8px 0;"><a href="mailto:${esc(capped.email)}">${esc(capped.email)}</a></td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Phone</td><td style="padding:8px 12px;"><a href="tel:${capped.phone.replace(/[^+\d\s\-().]/g, '')}">${esc(capped.phone)}</a></td></tr>
            <tr><td style="padding:8px 0;color:#666;">Business Type</td><td style="padding:8px 0;">${esc(capped.type) || '—'}</td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Calls / Month</td><td style="padding:8px 12px;">${esc(capped.volume) || '—'}</td></tr>
            <tr><td style="padding:8px 0;color:#666;vertical-align:top;">Message</td><td style="padding:8px 0;">${esc(capped.message) || '—'}</td></tr>
          </table>
          <div style="margin-top:24px;padding:16px;background:#fff8f0;border-left:3px solid #C17B3F;font-size:13px;color:#666;">
            Reply directly to this email to reach ${esc(capped.name)} at ${esc(capped.email)}
          </div>
        </div>
      `,
    }),
  });

  if (r.ok) {
    res.status(200).json({ ok: true });
  } else {
    const err = await r.json().catch(() => ({}));
    console.error('Resend error:', JSON.stringify(err));
    res.status(500).json({
      error: err.message || err.name || 'Failed to send',
    });
  }
}
