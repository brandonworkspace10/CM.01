export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { name, business, email, phone, type, volume, message } = req.body;

  if (!name || !business || !email || !phone) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer re_X8UNdiJn_2MYV7an1LeAp6wWfTtcDxNy8',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'Calling Matrix Contact <onboarding@resend.dev>',
      to: ['callingmatrix@gmail.com'],
      reply_to: email,
      subject: `New Lead: ${business} — ${type || 'Home Service'}`,
      html: `
        <div style="font-family:sans-serif;max-width:560px;margin:0 auto;color:#1a1a1a;">
          <h2 style="font-size:22px;margin-bottom:4px;">New Contact Form Submission</h2>
          <p style="color:#666;font-size:13px;margin-bottom:24px;">Submitted via callingmatrix.com</p>
          <table style="width:100%;border-collapse:collapse;font-size:15px;line-height:1.8;">
            <tr><td style="padding:8px 0;color:#666;width:160px;">Name</td><td style="padding:8px 0;font-weight:600;">${name}</td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Business</td><td style="padding:8px 12px;font-weight:600;">${business}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Email</td><td style="padding:8px 0;"><a href="mailto:${email}">${email}</a></td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Phone</td><td style="padding:8px 12px;"><a href="tel:${phone}">${phone}</a></td></tr>
            <tr><td style="padding:8px 0;color:#666;">Business Type</td><td style="padding:8px 0;">${type || '—'}</td></tr>
            <tr style="background:#f9f9f9"><td style="padding:8px 12px;color:#666;">Calls / Month</td><td style="padding:8px 12px;">${volume || '—'}</td></tr>
            <tr><td style="padding:8px 0;color:#666;vertical-align:top;">Message</td><td style="padding:8px 0;">${message || '—'}</td></tr>
          </table>
          <div style="margin-top:24px;padding:16px;background:#fff8f0;border-left:3px solid #C17B3F;font-size:13px;color:#666;">
            Reply directly to this email to reach ${name} at ${email}
          </div>
        </div>
      `,
    }),
  });

  if (r.ok) {
    res.status(200).json({ ok: true });
  } else {
    const err = await r.json().catch(() => ({}));
    console.error('Resend error:', err);
    res.status(500).json({ error: 'Failed to send' });
  }
}
