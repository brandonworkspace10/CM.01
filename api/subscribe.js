function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  if (!process.env.RESEND_API_KEY) {
    console.error('RESEND_API_KEY missing');
    return res.status(500).json({ error: 'Email service not configured' });
  }

  const { email } = req.body || {};

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email))) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  const safeEmail = String(email).slice(0, 254);

  try {
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Calling Matrix <hello@callingmatrix.com>',
        to: ['callingmatrix@gmail.com'],
        subject: `New newsletter subscriber: ${safeEmail}`,
        html: `<p>New subscriber via callingmatrix.com newsletter.</p><p><strong>${esc(safeEmail)}</strong></p>`,
      }),
    });

    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Calling Matrix <hello@callingmatrix.com>',
        to: [safeEmail],
        reply_to: 'callingmatrix@gmail.com',
        subject: "You're in — Calling Matrix playbooks start Tuesday",
        html: `
          <div style="font-family:sans-serif;max-width:560px;margin:0 auto;color:#1a1a1a;">
            <div style="background:#0E0D0B;padding:32px 40px;border-radius:12px 12px 0 0;">
              <table cellpadding="0" cellspacing="0" style="margin-bottom:20px;"><tr>
                <td style="vertical-align:middle;padding-right:12px;">
                  <svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="36">
                    <rect x="1" y="1" width="24" height="24" rx="6" stroke="rgba(255,255,255,0.3)" stroke-width="1"/>
                    <path d="M8 10 Q8 8 10 8 L12 8 L14 12 L12 14 Q14 17 16 18 L18 16 L22 18 L22 20 Q22 22 20 22 Q13 22 8 17 Q6 14 6 11 Z" fill="#C17B3F"/>
                    <circle cx="20" cy="6" r="2" fill="#C17B3F"/>
                  </svg>
                </td>
                <td style="vertical-align:middle;"><span style="color:#F6F2EB;font-size:17px;font-family:Georgia,serif;">Calling Matrix</span></td>
              </tr></table>
              <h1 style="color:#F6F2EB;font-size:26px;font-weight:400;margin:0;line-height:1.2;">You're subscribed.</h1>
            </div>
            <div style="padding:32px 40px;border:1px solid #e8e8e8;border-top:none;border-radius:0 0 12px 12px;">
              <p style="font-size:16px;line-height:1.7;color:#333;margin:0 0 16px;">Every Tuesday you'll get one short email — tactics, templates, and real call recordings from home service businesses that stopped missing jobs.</p>
              <p style="font-size:15px;line-height:1.7;color:#555;margin:0 0 28px;">In the meantime, see how Calling Matrix answers every call:</p>
              <a href="https://callingmatrix.com/#demo" style="display:inline-block;background:#C17B3F;color:#fff;text-decoration:none;padding:14px 28px;border-radius:999px;font-size:15px;font-weight:500;">Book a demo →</a>
              <p style="font-size:12px;color:#bbb;margin-top:32px;">To unsubscribe, reply to this email with "unsubscribe".</p>
            </div>
          </div>
        `,
      }),
    });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Subscribe error:', err);
    return res.status(500).json({ error: 'Failed to subscribe. Please try again.' });
  }
}
