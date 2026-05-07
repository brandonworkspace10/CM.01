function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const WELCOME_HTML = `
<div style="font-family:sans-serif;max-width:560px;margin:0 auto;color:#1a1a1a;">
  <div style="background:#0E0D0B;padding:36px 40px 32px;border-radius:12px 12px 0 0;text-align:center;">
    <table cellpadding="0" cellspacing="0" style="margin:0 auto 20px;"><tr>
      <td style="vertical-align:middle;padding-right:10px;">
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" width="42" height="42">
          <rect width="32" height="32" rx="7" fill="#1A1310"/>
          <path d="M10 12 Q10 10 12 10 L14 10 L16.5 14.5 L14.5 16.5 Q16.5 19.5 19 21 L21 19 L25 21 L25 23 Q25 25 23 25 Q15 25 10 20 Q7 16.5 7 13 Z" fill="#E89B6C"/>
          <circle cx="23" cy="9" r="2.5" fill="#E89B6C"/>
        </svg>
      </td>
      <td style="vertical-align:middle;">
        <span style="color:#F6F2EB;font-size:20px;font-family:Georgia,'Times New Roman',serif;letter-spacing:-0.01em;">Calling Matrix</span>
      </td>
    </tr></table>
    <h1 style="color:#F6F2EB;font-size:28px;font-weight:400;margin:0 0 8px;line-height:1.2;font-family:Georgia,serif;">Welcome to the newsletter.</h1>
    <p style="color:#A09890;font-size:13px;margin:0;">You're now part of 12,400+ home service operators who stopped missing calls.</p>
  </div>

  <div style="padding:32px 40px;border:1px solid #e8e8e8;border-top:none;border-radius:0 0 12px 12px;">
    <p style="font-size:16px;line-height:1.7;color:#222;margin:0 0 16px;">
      <strong>Calling Matrix</strong> is a 24/7 AI receptionist built for home service businesses — HVAC, plumbing, electrical, roofing, and cleaning.
    </p>
    <p style="font-size:15px;line-height:1.7;color:#555;margin:0 0 24px;">
      While your competitors send calls to voicemail, Calling Matrix answers every call, qualifies the lead, and books the job automatically — so you wake up to a full calendar, not a missed-call list.
    </p>

    <div style="background:#faf9f7;border-left:3px solid #E89B6C;padding:16px 20px;border-radius:0 8px 8px 0;margin:0 0 28px;">
      <p style="font-size:12px;font-weight:700;color:#333;margin:0 0 10px;text-transform:uppercase;letter-spacing:0.1em;">What's in every Tuesday email</p>
      <ul style="margin:0;padding:0 0 0 18px;color:#555;font-size:14px;line-height:1.9;">
        <li>Real call recordings + what made them win (or lose) the job</li>
        <li>Dispatcher scripts and booking templates you can use immediately</li>
        <li>Tactics for peak season, storm surges, and after-hours calls</li>
        <li>Product updates straight from the Calling Matrix team</li>
      </ul>
    </div>

    <p style="font-size:15px;line-height:1.7;color:#555;margin:0 0 24px;">Want to see the AI receptionist in action? We'll show you a live demo built for your trade:</p>

    <a href="https://callingmatrix.com/#demo"
       style="display:inline-block;background:#E89B6C;color:#1a0e00;text-decoration:none;padding:14px 28px;border-radius:999px;font-size:15px;font-weight:600;letter-spacing:0.01em;">
      Book a free demo →
    </a>

    <hr style="border:none;border-top:1px solid #eee;margin:32px 0 20px;">
    <p style="font-size:12px;color:#aaa;margin:0;line-height:1.6;">
      You subscribed at <a href="https://callingmatrix.com" style="color:#aaa;">callingmatrix.com</a>.
      To unsubscribe, reply with "unsubscribe".
    </p>
  </div>
</div>`;

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

  const safeEmail = String(email).slice(0, 254).toLowerCase();

  try {
    // Dedup: add to Resend audience. created:true = first time, created:false = already subscribed.
    let isNew = true;
    if (process.env.RESEND_AUDIENCE_ID) {
      const cr = await fetch(`https://api.resend.com/audiences/${process.env.RESEND_AUDIENCE_ID}/contacts`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: safeEmail }),
      });
      if (cr.ok) {
        const data = await cr.json();
        isNew = data.created !== false;
      }
    }

    // Notify the business (always)
    fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Calling Matrix <hello@callingmatrix.com>',
        to: ['callingmatrix@gmail.com'],
        subject: isNew ? `New subscriber: ${safeEmail}` : `Re-subscribe (already on list): ${safeEmail}`,
        html: `<p>${isNew ? 'New subscriber' : 'Already-subscribed email re-submitted'} via callingmatrix.com.</p><p><strong>${esc(safeEmail)}</strong></p>`,
      }),
    }).catch(e => console.error('Notification email failed:', e));

    // Welcome email — first-time only
    if (isNew) {
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: 'Calling Matrix <hello@callingmatrix.com>',
          to: [safeEmail],
          reply_to: 'callingmatrix@gmail.com',
          subject: 'Welcome to the Calling Matrix newsletter',
          html: WELCOME_HTML,
        }),
      });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Subscribe error:', err);
    return res.status(500).json({ error: 'Failed to subscribe. Please try again.' });
  }
}
