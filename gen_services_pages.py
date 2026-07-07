#!/usr/bin/env python3
"""Generate the /services hub page and the four service pages.

Reuses shared.css classes and copies the footer + scripts + callback widget
verbatim from virtual-receptionist.html so everything stays consistent.
Run: python3 gen_services_pages.py
"""
import json, re

BASE = "https://callingmatrix.com"

# ---------------------------------------------------------------- shared tail
src = open("virtual-receptionist.html").read()
TAIL = src[src.index("<footer>"):]
# add Services to the footer Product column (skip if already present)
if '<h6>Product</h6><a href="/services">' not in TAIL:
    TAIL = TAIL.replace('<h6>Product</h6>', '<h6>Product</h6><a href="/services">Services</a>', 1)

LOGO = '<a href="/" class="logo"><span class="logo-mark"><svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="24" height="24" rx="6" stroke="currentColor" stroke-opacity="0.4"></rect><path d="M8 10 Q8 8 10 8 L12 8 L14 12 L12 14 Q14 17 16 18 L18 16 L22 18 L22 20 Q22 22 20 22 Q13 22 8 17 Q6 14 6 11 Z" fill="var(--accent)"></path><circle cx="20" cy="6" r="2" fill="var(--accent)"></circle></svg></span>Calling Matrix</a>'

ICONS = {
    "clock":  '<path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "cal":    '<rect x="3" y="4" width="14" height="13" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M7 2v4M13 2v4M3 9h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "bolt":   '<path d="M11 2l-7 10h7l-2 6 7-10h-7l2-6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "check":  '<path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "chat":   '<path d="M3 5a2 2 0 012-2h10a2 2 0 012 2v7a2 2 0 01-2 2H8l-4 3v-3H5a2 2 0 01-2-2V5z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "phone":  '<path d="M6 3h3l1.5 4-2 1.5a11 11 0 005 5L15 11.5 17 13v3a1.5 1.5 0 01-1.6 1.5C8.9 17 3 11.1 3 4.6A1.5 1.5 0 014.5 3H6z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "star":   '<path d="M10 2l2.4 5 5.6.7-4.1 3.8 1.1 5.5L10 14.3 5 17l1.1-5.5L2 7.7 7.6 7 10 2z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>',
    "repeat": '<path d="M3 7h11l-3-3M17 13H6l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "person": '<circle cx="10" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/><path d="M3 18c0-3 3-5 7-5s7 2 7 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
}

def icon(name):
    return f'<div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none">{ICONS[name]}</svg></div>'

ARROW = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10m0 0L9 4m4 4l-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# hover dropdown for the Services nav item (styles live in shared.css)
DD_ITEMS = [
    ("virtual-receptionist", "AI Receptionist", "24/7 inbound answering &amp; booking"),
    ("missed-call-text-back", "Missed Call Text Back", "Instant text saves every missed call"),
    ("ai-lead-follow-up", "AI Lead Follow-Up", "Every lead called &amp; texted in 60s"),
    ("ai-appointment-setter", "AI Appointment Setter", "Outbound booking &amp; reminders"),
    ("review-reputation-automation", "Review &amp; Reputation Automation", "Five-star reviews on autopilot"),
]

def services_dd(active=False):
    rows = "".join(f'<a href="/{s}"><span class="t">{l}</span><span class="d">{d}</span></a>' for s, l, d in DD_ITEMS)
    rows += '<a href="/services" class="all">All services →</a>'
    cls = ' class="active"' if active else ""
    return (f'<div class="nav-dd"><a href="/services"{cls}>Services<span class="dd-c"></span></a>'
            f'<div class="nav-dd-menu"><div class="nav-dd-box">{rows}</div></div></div>')

def link_li(href, label):
    return f'<li><a href="{href}" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color=\'var(--accent,#E89B6C)\'" onmouseout="this.style.color=\'var(--fg-dim,#B8B0A0)\'">{label} →</a></li>'

def head(p):
    faq_ld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]
    graph = [
        {"@type": "Organization", "name": "Calling Matrix", "url": BASE, "email": "hi@callingmatrix.com",
         "sameAs": ["https://twitter.com/callingmatrix", "https://linkedin.com/company/callingmatrix", "https://instagram.com/callingmatrix"]},
        {"@type": "WebPage", "name": f'{p["h1_plain"]} — Calling Matrix', "url": f'{BASE}/{p["slug"]}',
         "description": p["desc"], "inLanguage": "en-US"},
        {"@type": "Service", "name": p["service_name"], "serviceType": p["service_type"],
         "provider": {"@type": "Organization", "name": "Calling Matrix"},
         "description": p["service_desc"],
         "areaServed": {"@type": "Country", "name": "United States"}},
        {"@type": "FAQPage", "mainEntity": faq_ld},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services"},
        ] + ([] if p["slug"] == "services" else [{"@type": "ListItem", "position": 3, "name": p["service_name"], "item": f'{BASE}/{p["slug"]}'}])},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{BASE}/{p["slug"]}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Calling Matrix">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{BASE}/{p["slug"]}">
<meta property="og:image" content="{BASE}/api/og">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Calling Matrix — {p["service_name"]} for Home Service Businesses">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@callingmatrix">
<meta name="twitter:title" content="{p["title"]}">
<meta name="twitter:description" content="{p["desc"]}">
<meta name="twitter:image" content="{BASE}/api/og">
<script type="application/ld+json">
{ld}
</script>
<script defer src="/_vercel/insights/script.js"></script>
<script src="https://analytics.ahrefs.com/analytics.js" data-key="94z1bOhN7RVx3o2W/eEUbQ" async></script>
<link rel="stylesheet" href="/shared.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"></noscript>
</head>
<body>
<a class="skip-nav" href="#main-content">Skip to content</a>
<nav class="nav" id="nav">
  <div class="nav-inner">
    {LOGO}
    <nav class="nav-links">{services_dd(active=p["slug"] == "services")}<a href="#features">Features</a><a href="#faq">FAQ</a><a href="/pricing">Pricing</a><a href="/blog">Blog</a></nav>
    <a href="#" class="nav-cta" onclick="openCalendly();return false;">Book a consultation</a>
    <button class="mob-menu-btn" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</nav>
'''

def hero(p):
    stats = "".join(f'<div><div class="s-num">{n}</div><div class="s-lbl">{l}</div></div>' for n, l in p["stats"])
    return f'''
<header class="hero" id="main-content">
  <div class="hero-bg"></div><div class="hero-grid"></div>
  <div class="wrap">
    <span class="eyebrow reveal in"><span class="dot"></span><span>{p["eyebrow"]}</span></span>
    <h1 class="hero-title reveal in d1">{p["h1"]}</h1>
    <p class="hero-sub reveal in d2">{p["sub"]}</p>
    <div class="cta-row reveal in d3">
      <a href="#" class="btn btn-primary" onclick="openCalendly();return false;"><span>{p["cta"]}</span> {ARROW}</a>
      <a href="{p["cta2_href"]}" class="btn btn-ghost">{p["cta2"]} →</a>
    </div>
    <div class="hero-stats reveal in d3">{stats}</div>
  </div>
</header>
'''

def pain(p):
    cells = "".join(
        f'<div class="pain-cell reveal in{" d" + str(i) if i else ""}"><div class="big-num">{n}</div><h3>{h}</h3><p>{b}</p></div>'
        for i, (n, h, b) in enumerate(p["pains"]))
    return f'''
<section class="pain">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">The problem</div><h2 class="sec-title">{p["pain_title"]}</h2></div>
    <div class="pain-grid">{cells}</div>
  </div>
</section>
'''

def features(p):
    feats = "".join(
        f'<div class="feat reveal in{" d" + str(i) if i else ""}">{icon(ic)}<h3>{h}</h3><p>{b}</p></div>'
        for i, (ic, h, b) in enumerate(p["feats"]))
    return f'''
<section class="features" id="features">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">{p["feat_label"]}</div><h2 class="sec-title">{p["feat_title"]}</h2><p class="sec-sub">{p["feat_sub"]}</p></div>
    <div class="feat-grid">{feats}</div>
  </div>
</section>
'''

def faq(p):
    items = "".join(
        f'<div class="faq-item"><div class="faq-q"><span>{q}</span><span class="faq-plus"></span></div><div class="faq-a">{a}</div></div>'
        for q, a in p["faqs"])
    return f'''
<section class="faq" id="faq">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">FAQ</div><h2 class="sec-title">{p["faq_title"]}</h2></div>
    <div class="faq-list">{items}</div>
  </div>
</section>
'''

def internal_links(p):
    col1 = "".join(link_li(h, l) for h, l in p["links1"])
    col2 = "".join(link_li(h, l) for h, l in p["links2"])
    return f'''
<!-- INTERNAL LINKS -->
<section style="background:var(--bg-2,#141310);border-top:1px solid var(--line,rgba(180,120,60,.12));padding:56px 0;">
  <div style="max-width:1120px;margin:0 auto;padding:0 32px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;">
      <div>
        <p style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#E89B6C);margin-bottom:16px;">{p["links1_label"]}</p>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">{col1}</ul>
      </div>
      <div>
        <p style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#E89B6C);margin-bottom:16px;">{p["links2_label"]}</p>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">{col2}</ul>
      </div>
    </div>
  </div>
</section>
'''

def final(p):
    return f'''
<section class="final"><div class="wrap inner">
  <h2 class="reveal in">{p["final_title"]}</h2>
  <p class="reveal in d1">{p["final_sub"]}</p>
  <a href="#" class="btn btn-primary reveal in d2" onclick="openCalendly();return false;"><span>Book a free 15-min consultation</span> {ARROW}</a>
</div></section>
'''

# ------------------------------------------------------------- service pages
SERVICE_CARDS = [
    ("phone", "AI Receptionist", "Our flagship. Answers every inbound call in under 2 seconds, 24/7 — qualifies the caller, books the job into your software, and routes real emergencies to your on-call tech.", "/virtual-receptionist", "The flagship"),
    ("chat", "Missed Call Text Back", "Can't answer? Every missed caller gets a text within seconds — then our AI texts with them to qualify the job and get it booked before they dial a competitor.", "/missed-call-text-back", "The safety net"),
    ("bolt", "AI Lead Follow-Up", "Every web form, Angi, and Thumbtack lead gets a call and text in under 60 seconds — then a persistent multi-touch sequence until they book or say no. Unsold estimates included.", "/ai-lead-follow-up", "Speed to lead"),
    ("cal", "AI Appointment Setter", "Outbound booking. We call and text your lead lists, quote requests, and past customers, and put confirmed appointments — with reminders — straight on your calendar.", "/ai-appointment-setter", "Outbound booking"),
    ("star", "Review & Reputation Automation", "Every completed job triggers a review request by text. More five-star Google reviews, an alert before an unhappy customer posts, and responses handled for you.", "/review-reputation-automation", "Close the loop"),
]

PAGES = {}

PAGES["services"] = dict(
    slug="services",
    title="AI Services for Home Service Businesses | Calling Matrix",
    desc="One platform, five services: 24/7 AI receptionist, missed call text back, AI lead follow-up, AI appointment setter, and review automation — flat monthly pricing, live in 48 hours.",
    h1_plain="Services",
    service_name="AI Front Office for Home Services",
    service_type="AI Answering, Lead Follow-Up, Appointment Setting, and Review Automation",
    service_desc="A complete AI front office for home service businesses: 24/7 call answering, missed call text back, instant lead follow-up, outbound appointment setting, and review & reputation automation. Flat monthly pricing.",
    eyebrow="Everything we do",
    h1='Every call answered. Every lead worked.<br><span class="italic accent">Every review captured.</span>',
    sub='Calling Matrix started as a 24/7 AI receptionist. It grew into a complete <strong>AI front office for home service businesses</strong> — five services that catch every job from first ring to five-star review, at one flat monthly price.',
    cta="Book a free consultation",
    cta2="See pricing", cta2_href="/pricing",
    stats=[("5", "Services, one platform, one flat bill"), ("&lt;2s", "Inbound answer time, 24/7/365"), ("48h", "From signup to fully live")],
    pain_title='Jobs don\'t just leak at the phone.<br><span class="italic">They leak everywhere.</span>',
    pains=[
        ("85%", "of missed callers never call back", "The phone is the front door, and it's where most revenue walks away. But answering every call is only step one."),
        ("78%", "of customers hire whoever responds first", "Web leads, Angi leads, quote requests — the company that follows up in the first minutes wins the job. Most contractors take hours, or never follow up at all."),
        ("88%", "of homeowners read reviews before calling", "You can answer every call and still lose — if your Google profile shows 12 reviews while the competitor shows 300, you were eliminated before the phone rang."),
    ],
    feat_label="The services",
    feat_title='Five services. One system.<br><span class="italic">Zero jobs slipping through.</span>',
    feat_sub="Start with the AI receptionist, or start small with missed call text back. Every service works standalone — together they cover the entire customer lifecycle.",
    feats=[(ic, f'{h} <span style="display:block;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-top:4px;">{tag}</span>',
            f'{b} <a href="{href}" style="color:var(--accent);text-decoration:none;">Learn more →</a>') for ic, h, b, href, tag in SERVICE_CARDS],
    faq_title='Questions about the platform,<br><span class="italic">answered straight.</span>',
    faqs=[
        ("Do I need all five services?", "No. Every service works standalone. Most companies start with the 24/7 AI receptionist and add lead follow-up or review automation once they see the booked-job numbers. Missed call text back is the most common entry point for businesses that aren't ready to hand over the phones yet."),
        ("How do the services work together?", "They cover the customer lifecycle: the AI receptionist answers and books inbound calls; missed call text back catches anything that slips; lead follow-up chases web and marketplace leads in under 60 seconds; the appointment setter works your lists and unsold estimates outbound; and review automation turns completed jobs into Google reviews that bring the next customer in."),
        ("Does this work with my scheduling software?", "Yes. Every service books into and reads from ServiceTitan, Housecall Pro, Jobber, and Google Calendar — jobs, appointments, and customer records sync in real time with no double entry."),
        ("How is it priced?", "Flat monthly pricing, no per-minute or per-lead charges. Answering plans start at $297/month for after-hours coverage and $497/month for full 24/7 answering — see the <a href='/pricing' style='color:var(--accent);'>pricing page</a>. The other services are scoped to your business on the free consultation call, since the right setup depends on your lead volume, lists, and software — always a flat monthly rate."),
        ("How fast can I go live?", "48 hours for most businesses. One 30-minute onboarding call covers your services, pricing, service area, and routing rules — we build and train everything for you."),
    ],
    links1_label="The services",
    links1=[("/virtual-receptionist", "AI Receptionist"), ("/missed-call-text-back", "Missed Call Text Back"), ("/ai-lead-follow-up", "AI Lead Follow-Up"), ("/ai-appointment-setter", "AI Appointment Setter"), ("/review-reputation-automation", "Review & Reputation Automation")],
    links2_label="Built for your industry",
    links2=[("/hvac", "HVAC"), ("/plumbing", "Plumbing"), ("/electrical", "Electrical"), ("/roofing", "Roofing"), ("/cleaning", "Cleaning")],
    final_title='One consultation.<br><span class="italic">Every leak plugged.</span>',
    final_sub="Tell us where jobs are slipping — missed calls, slow follow-up, no-shows, or a thin Google profile — and we'll show you exactly which services fix it. Live in 48 hours.",
)

PAGES["ai-lead-follow-up"] = dict(
    slug="ai-lead-follow-up",
    title="AI Lead Follow-Up for Home Services | Calling Matrix",
    desc="Every web, Angi, and Thumbtack lead called and texted in under 60 seconds — then followed up until they book or say no. Unsold estimates chased automatically. Flat monthly rate.",
    h1_plain="AI Lead Follow-Up",
    service_name="AI Lead Follow-Up",
    service_type="Lead Follow-Up and Speed-to-Lead Automation",
    service_desc="Automated AI lead follow-up for home service businesses: instant call-and-text response to every web form and marketplace lead in under 60 seconds, persistent multi-touch sequences, unsold estimate follow-up, and database reactivation campaigns.",
    eyebrow="Speed to lead, automated",
    h1='Every lead gets a call in 60 seconds.<br><span class="italic accent">Even the ones from 2 AM.</span>',
    sub='The company that responds first wins the job — and most contractors respond in hours, not seconds. Calling Matrix <strong>calls and texts every new lead within 60 seconds</strong>, qualifies them, books them, and keeps following up until they schedule or say no.',
    cta="See it chase a lead",
    cta2="How it works", cta2_href="#features",
    stats=[("78%", "of customers hire the first company to respond"), ("21x", "more likely to qualify a lead in 5 min vs. 30"), ("&lt;60s", "Our response time to every new lead")],
    pain_title='Your marketing buys the lead.<br><span class="italic">Your follow-up loses it.</span>',
    pains=[
        ("$50+", "is what you pay for a single lead", "Google Ads, Angi, Thumbtack, SEO — leads aren't cheap. Letting one sit in your inbox overnight is the same as setting the money on fire."),
        ("47%", "of leads never get a follow-up call at all", "Techs are on roofs and under sinks. Nobody's job is 'call the web leads back' — so on busy weeks, nobody does."),
        ("60%", "of unsold estimates are never followed up", "You drove out, quoted the job, and never called again. The contractor who follows up twice more wins that job — it should be you."),
    ],
    feat_label="What it does",
    feat_title='Relentless follow-up.<br><span class="italic">Without hiring anyone.</span>',
    feat_sub="Connect your lead sources once — web forms, Angi, Thumbtack, Facebook ads — and every lead gets worked the same way, every time.",
    feats=[
        ("bolt", "Instant speed-to-lead response", "The moment a lead comes in, they get a call and a text — in under 60 seconds, at any hour. While competitors are still checking email, you're already on the phone with the customer."),
        ("repeat", "Multi-touch sequences that don't give up", "No answer? The AI follows up with calls and texts over the following days — politely persistent until the lead books, replies, or asks to stop. No lead marked 'contacted once' and forgotten."),
        ("check", "Unsold estimate follow-up", "Every open quote gets chased automatically: a check-in text the next day, a call later that week, a nudge before the quote expires. The highest-margin jobs you'll ever win are the ones you already quoted."),
        ("person", "Database reactivation", "Your old customer list is an asset. We run seasonal campaigns — tune-up reminders, maintenance offers, 'it's been a year' check-ins — that wake up past customers and fill slow weeks."),
    ],
    faq_title='Lead follow-up questions,<br><span class="italic">answered straight.</span>',
    faqs=[
        ("What lead sources can it follow up with?", "Any source that can send a webhook, email, or integration: website forms, Angi, Thumbtack, HomeAdvisor, Facebook and Google lead ads, and leads already sitting in ServiceTitan, Housecall Pro, or Jobber. If a lead lands anywhere digital, we can chase it."),
        ("How fast does it actually respond?", "Under 60 seconds from the moment the lead arrives — a phone call plus a text message, 24/7 including nights and weekends. Research from InsideSales/MIT shows you're 21x more likely to qualify a lead responding within 5 minutes versus 30; we don't leave that to chance."),
        ("What happens when a lead answers?", "The AI qualifies them — job type, location, urgency, timeline — answers questions about your services and pricing, and books them directly into your scheduling software. Hot leads can be transferred live to your team."),
        ("Can it follow up on estimates I've already sent?", "Yes. Unsold quote follow-up is built in: the AI checks in after you send the estimate, handles common objections, answers questions, and books the job when the customer is ready. Most companies see this feature alone pay for the service."),
        ("Will it annoy my leads?", "No. Sequences are politely persistent, spaced over days, and stop instantly when someone books, declines, or replies 'stop.' Every message is customized to your company voice during onboarding."),
        ("How is this different from the AI receptionist?", "The <a href='/virtual-receptionist' style='color:var(--accent);'>AI receptionist</a> handles inbound — people calling you. Lead follow-up is outbound — reaching out to people who filled out a form or got a quote but haven't booked. Most companies run both, so nothing leaks in either direction."),
    ],
    links1_label="More services",
    links1=[("/services", "All services"), ("/virtual-receptionist", "AI Receptionist"), ("/ai-appointment-setter", "AI Appointment Setter"), ("/missed-call-text-back", "Missed Call Text Back"), ("/review-reputation-automation", "Review & Reputation Automation")],
    links2_label="Keep reading",
    links2=[("/roi-calculator", "ROI Calculator — what missed leads cost"), ("/pricing", "Calling Matrix Pricing"), ("/hvac", "AI for HVAC Companies"), ("/plumbing", "AI for Plumbers"), ("/blog", "The Calling Matrix Blog")],
    final_title='Your leads are going cold<br><span class="italic">right now.</span>',
    final_sub="Every hour a lead sits unworked, someone else is calling them back. Put an AI on it — every lead, every estimate, every time. Live in 48 hours.",
)

PAGES["ai-appointment-setter"] = dict(
    slug="ai-appointment-setter",
    title="AI Appointment Setter for Home Services | Calling Matrix",
    desc="An AI appointment setter that makes outbound calls and texts, books confirmed jobs into ServiceTitan, Housecall Pro, Jobber, or Google Calendar, and cuts no-shows with automatic reminders.",
    h1_plain="AI Appointment Setter",
    service_name="AI Appointment Setter",
    service_type="Outbound Appointment Setting and Scheduling Automation",
    service_desc="AI-powered outbound appointment setting for home service businesses: calls and texts leads and past customers, books confirmed appointments directly into scheduling software, and sends reminders that cut no-shows.",
    eyebrow="Outbound booking, handled",
    h1='An appointment setter that dials all day.<br><span class="italic accent">And never asks for commission.</span>',
    sub='Your calendar doesn\'t fill itself. Calling Matrix works your leads, quote requests, and customer lists <strong>outbound — by call and text</strong> — and puts confirmed, reminded, show-up-ready appointments straight into your scheduling software.',
    cta="Hear it book an appointment",
    cta2="How it works", cta2_href="#features",
    stats=[("24/7", "Booking window — not 9 to 5"), ("100%", "of appointments land in your software"), ("38%", "fewer no-shows with automatic reminders")],
    pain_title='Booking jobs by phone tag<br><span class="italic">is costing you the job.</span>',
    pains=[
        ("6+", "calls to reach one lead by phone tag", "You call, they miss it. They call back, you're under a sink. By round three they've booked whoever answered — appointment setting is a full-time job nobody at your company has time for."),
        ("30%", "of appointments no-show without reminders", "An empty 2-hour window with a tech on the clock is pure loss. Most no-shows aren't rude customers — they're customers nobody reminded."),
        ("$0", "is what your customer list earns sitting idle", "Hundreds of past customers who already trust you, and nobody calls them for seasonal tune-ups, maintenance plans, or the repair they postponed last year."),
    ],
    feat_label="What it does",
    feat_title='From lead list to booked calendar.<br><span class="italic">Automatically.</span>',
    feat_sub="Point it at your leads, quote requests, and customer list — it dials, texts, books, confirms, and reminds. You just show up to the job.",
    feats=[
        ("phone", "Outbound calls and texts that book", "The AI calls your leads and lists, has a natural conversation, offers real openings from your calendar, and locks in the appointment on the spot — then texts a confirmation."),
        ("cal", "Direct scheduling-software booking", "Every appointment lands in ServiceTitan, Housecall Pro, Jobber, or Google Calendar in real time — customer details, job type, and notes included. No double entry, no sticky notes."),
        ("clock", "Reminders that kill no-shows", "Automatic confirmation and reminder texts before every appointment — with one-tap confirm or reschedule. Cancellations get backfilled from your waitlist instead of leaving a hole in the day."),
        ("repeat", "Rescheduling handled end to end", "Customer needs to move the appointment? The AI handles the back-and-forth, finds the next slot that works, and updates your calendar — without your office touching it."),
    ],
    faq_title='Appointment setter questions,<br><span class="italic">answered straight.</span>',
    faqs=[
        ("How is this different from the AI receptionist?", "Direction. The <a href='/virtual-receptionist' style='color:var(--accent);'>AI receptionist</a> answers calls coming in; the appointment setter makes calls going out — to new leads, unsold quotes, and past customers — and books them. Together they fill your calendar from both ends."),
        ("Who does it call?", "Whoever you point it at: new leads from your website or ad campaigns, quote requests that haven't booked, maintenance-plan customers due for service, and past customers for seasonal campaigns. You control the lists and the rules."),
        ("Does it book into my scheduling software?", "Yes — ServiceTitan, Housecall Pro, Jobber, and Google Calendar, in real time. It only offers slots that are actually open, respects your service-area and job-type rules, and writes complete customer details into every booking."),
        ("What about no-shows?", "Every appointment gets automatic confirmation and reminder texts with one-tap confirm or reschedule. Industry data consistently shows reminder texts cut no-shows by roughly a third or more — and cancellations get backfilled instead of wasted."),
        ("Will customers know it's an AI?", "Customers get a fast, natural conversation and a confirmed appointment without phone tag. What they remember is that booking with your company was easy — listen to our <a href='/demo-transcript' style='color:var(--accent);'>real call demos</a> and judge for yourself."),
        ("Is outbound calling compliant?", "Yes — we only contact your own leads and customers (people who gave you their number), honor opt-outs instantly, and register your texting numbers properly. No cold-call spam, ever."),
    ],
    links1_label="More services",
    links1=[("/services", "All services"), ("/virtual-receptionist", "AI Receptionist"), ("/ai-lead-follow-up", "AI Lead Follow-Up"), ("/missed-call-text-back", "Missed Call Text Back"), ("/review-reputation-automation", "Review & Reputation Automation")],
    links2_label="Keep reading",
    links2=[("/servicetitan", "Works with ServiceTitan"), ("/housecall-pro", "Works with Housecall Pro"), ("/jobber", "Works with Jobber"), ("/pricing", "Calling Matrix Pricing"), ("/roi-calculator", "ROI Calculator")],
    final_title='An empty calendar slot<br><span class="italic">never pays for itself.</span>',
    final_sub="Put an AI appointment setter on your leads and lists — booked, confirmed, reminded appointments in your software without a single game of phone tag. Live in 48 hours.",
)

PAGES["missed-call-text-back"] = dict(
    slug="missed-call-text-back",
    title="Missed Call Text Back for Home Services | Calling Matrix",
    desc="Every missed call gets an instant text back — then AI texting qualifies the customer and books the job before they call a competitor. The simplest way to stop losing jobs to voicemail.",
    h1_plain="Missed Call Text Back",
    service_name="Missed Call Text Back",
    service_type="Missed Call Text Back and SMS Lead Capture",
    service_desc="Automatic missed call text back for home service businesses: every missed caller receives an instant text within seconds, then AI two-way texting qualifies the job and books the appointment. Works standalone or as a safety net behind the AI receptionist.",
    eyebrow="The 10-second save",
    h1='Miss the call.<br><span class="italic accent">Keep the customer.</span>',
    sub='When you can\'t pick up, 85% of callers won\'t leave a voicemail — they call the next company on Google. Calling Matrix <strong>texts every missed caller within seconds</strong>, then holds the conversation, qualifies the job, and books it. The customer never gets far enough to dial a competitor.',
    cta="See a missed call get saved",
    cta2="How it works", cta2_href="#features",
    stats=[("&lt;10s", "From missed call to text in their hand"), ("98%", "of texts get read — most within minutes"), ("85%", "of missed callers never call back — until now")],
    pain_title='Voicemail isn\'t a backup.<br><span class="italic">It\'s a goodbye.</span>',
    pains=[
        ("85%", "of callers who hit voicemail never call back", "They don't leave a message. They don't try again later. They hit the back button and tap the next plumber on Google — your missed call is their booked job."),
        ("62%", "of calls to small businesses go unanswered", "You're on a roof, under a house, or driving between jobs. The phone rings when you physically cannot answer it — that's not a discipline problem, it's a coverage problem."),
        ("$300+", "average value of a single missed job", "One missed call a day at average ticket prices is six figures a year in walked-away revenue. The fix costs less than one saved job a month."),
    ],
    feat_label="What it does",
    feat_title='The instant save.<br><span class="italic">Then the booked job.</span>',
    feat_sub="Most missed-call-text-back tools send one canned text and stop. Ours starts a conversation that ends with an appointment on your calendar.",
    feats=[
        ("chat", "Instant text back, every missed call", "Within seconds of a missed ring, the caller gets a text: 'Sorry we missed you — what can we help with?' They've barely left your call screen, and you've already responded."),
        ("bolt", "AI texting that qualifies and books", "This isn't an autoresponder. The AI holds a real text conversation — job type, address, urgency, photos if useful — and books the appointment straight into your scheduling software."),
        ("clock", "After-hours and overflow coverage", "Nights, weekends, holidays, and the lunch rush all covered. Emergencies get flagged and routed to your on-call tech by your rules; everything else books for the next opening."),
        ("check", "The natural first step", "Not ready to hand your phones to an AI? Start here. Keep answering the calls you can, let text-back save the ones you can't — and upgrade to the full <a href='/virtual-receptionist' style='color:var(--accent);'>AI receptionist</a> whenever you're ready."),
    ],
    faq_title='Missed call text back questions,<br><span class="italic">answered straight.</span>',
    faqs=[
        ("What is missed call text back?", "A system that automatically sends a text message to anyone whose call you miss, within seconds. Instead of hitting voicemail and calling your competitor, the customer gets an instant response and a way to book. Calling Matrix goes further than basic tools: our AI continues the text conversation, qualifies the job, and books the appointment."),
        ("How fast is the text back?", "Under 10 seconds from the missed call. Speed is the whole point — the customer is still holding their phone, still thinking about their problem, and hasn't searched for anyone else yet."),
        ("Can it actually book jobs, or just reply?", "It books. The AI asks the right questions — job type, location, urgency — answers questions about your services, and schedules directly into ServiceTitan, Housecall Pro, Jobber, or Google Calendar."),
        ("What happens with emergencies?", "Texts that indicate a true emergency — burst pipe, no heat, sparking panel — get flagged and routed to your on-call tech immediately by call or text, following the rules you set at onboarding."),
        ("How is this different from the AI receptionist?", "The <a href='/virtual-receptionist' style='color:var(--accent);'>AI receptionist</a> answers the call itself, so it never gets missed. Missed call text back is the lighter option: your phones keep working exactly as they do now, and the AI only steps in when a call slips through. Many customers start here and upgrade."),
        ("Is the texting compliant?", "Yes. We register your number for A2P 10DLC (the carrier requirement for business texting), only text people who called you first, and honor opt-outs instantly."),
    ],
    links1_label="More services",
    links1=[("/services", "All services"), ("/virtual-receptionist", "AI Receptionist"), ("/ai-lead-follow-up", "AI Lead Follow-Up"), ("/ai-appointment-setter", "AI Appointment Setter"), ("/review-reputation-automation", "Review & Reputation Automation")],
    links2_label="Keep reading",
    links2=[("/after-hours-answering-service", "After-Hours Answering Service"), ("/roi-calculator", "ROI Calculator — what missed calls cost"), ("/pricing", "Calling Matrix Pricing"), ("/hvac", "AI for HVAC Companies"), ("/plumbing", "AI for Plumbers")],
    final_title='The next missed call<br><span class="italic">doesn\'t have to be a lost job.</span>',
    final_sub="Set it up once and every missed caller gets an instant text, a real conversation, and a booked appointment. The simplest, cheapest leak to plug in your business — live in 48 hours.",
)

PAGES["review-reputation-automation"] = dict(
    slug="review-reputation-automation",
    title="Review & Reputation Automation for Home Services | Calling Matrix",
    desc="Turn completed jobs into five-star Google reviews automatically. Review requests by text, alerts before unhappy customers post, and AI-drafted responses — reputation on autopilot.",
    h1_plain="Review & Reputation Automation",
    service_name="Review & Reputation Automation",
    service_type="Review Generation and Reputation Management Automation",
    service_desc="Automated review and reputation management for home service businesses: post-job review requests by text, unhappy-customer alerts, AI-drafted review responses, and reputation monitoring across Google and major platforms.",
    eyebrow="Reputation on autopilot",
    h1='Finished jobs become five-star reviews.<br><span class="italic accent">Automatically.</span>',
    sub='Homeowners pick the company with more and better Google reviews — before they ever call. Calling Matrix <strong>asks every customer for a review the moment the job closes</strong>, catches unhappy ones before they post, and answers every review for you.',
    cta="See how review requests work",
    cta2="How it works", cta2_href="#features",
    stats=[("88%", "of consumers trust reviews like personal referrals"), ("2-3x", "more reviews when you ask by text, every job"), ("100%", "of your reviews answered — good and bad")],
    pain_title='Great work nobody can see<br><span class="italic">loses to average work everybody can.</span>',
    pains=[
        ("0", "reviews is what most happy customers leave", "Customers love the work, say thanks at the door, and never think about it again. Not because they wouldn't leave a review — because nobody asked while it was fresh."),
        ("57%", "of consumers only consider 4+ star businesses", "Your Google rating is a filter you pass or fail before the phone ever rings. A thin profile with a few old reviews fails it — no matter how good your techs are."),
        ("1", "angry review can undo twenty happy customers", "The customer with a complaint is the one most motivated to post. Without a system that catches problems early and buries outliers in five-star volume, one bad week lives on your profile for years."),
    ],
    feat_label="What it does",
    feat_title='Ask every time. Catch problems early.<br><span class="italic">Respond to everything.</span>',
    feat_sub="Connected to your scheduling software, so the moment a job is marked complete, the reputation machine starts turning.",
    feats=[
        ("star", "Automatic post-job review requests", "The moment a job closes in ServiceTitan, Housecall Pro, or Jobber, the customer gets a text with a direct link to your Google profile — while the good experience is minutes old, not weeks."),
        ("bolt", "Unhappy-customer early warning", "Every customer gets asked how the job went. Signals of an unhappy one trigger an instant alert to you — so you can call and make it right before it becomes a public one-star."),
        ("chat", "AI-drafted responses to every review", "Every review gets a thoughtful, personalized response in your company's voice — thank-yous on the five-stars, professional and calm on the critical ones. Google rewards active profiles."),
        ("repeat", "The loop back to more calls", "More reviews mean higher Google Maps ranking, which means more calls — which your <a href='/virtual-receptionist' style='color:var(--accent);'>AI receptionist</a> answers and books. This is the service that feeds all the others."),
    ],
    faq_title='Review automation questions,<br><span class="italic">answered straight.</span>',
    faqs=[
        ("How does it get more reviews?", "By asking every single customer, by text, at the exact right moment — right after the job closes. Most companies ask sporadically or not at all; asking consistently at the peak-happiness moment typically multiplies review volume 2–3x. The text contains a direct link, so leaving a review takes under a minute."),
        ("Is this review gating? Is it allowed?", "No gating. Every customer gets the same review invitation — that's Google-policy compliant. What we add is an early-warning layer: when a customer signals they're unhappy, you get an alert so you can fix the problem like a great business does. Solved problems often become five-star reviews on their own."),
        ("What platforms does it cover?", "Google Business Profile is the priority — it drives local search and the map pack. We also monitor and route to Facebook, Yelp, and industry platforms like Angi where it matters for your trade."),
        ("Who writes the responses to reviews?", "The AI drafts a personalized response to every review in your company voice; you can auto-publish or approve with one tap. Responding to every review — especially critical ones — measurably improves how prospects perceive you and keeps your profile active in Google's eyes."),
        ("Does it work with my scheduling software?", "Yes. It watches for completed jobs in ServiceTitan, Housecall Pro, Jobber, or Google Calendar and triggers the review request automatically — no one on your team has to remember anything."),
        ("Why does this matter for getting more calls?", "Reviews are among the strongest local ranking factors on Google. More recent reviews, a higher average, and owner responses push you up the map pack — and the map pack is where homeowners choose who to call. It's the flywheel: reviews bring calls, our receptionist books them, finished jobs bring reviews."),
    ],
    links1_label="More services",
    links1=[("/services", "All services"), ("/virtual-receptionist", "AI Receptionist"), ("/missed-call-text-back", "Missed Call Text Back"), ("/ai-lead-follow-up", "AI Lead Follow-Up"), ("/ai-appointment-setter", "AI Appointment Setter")],
    links2_label="Keep reading",
    links2=[("/case-studies", "Customer Stories"), ("/pricing", "Calling Matrix Pricing"), ("/hvac", "AI for HVAC Companies"), ("/roofing", "AI for Roofers"), ("/blog", "The Calling Matrix Blog")],
    final_title='Your next 100 customers<br><span class="italic">are reading your reviews tonight.</span>',
    final_sub="Put review collection on autopilot — every job asked, every review answered, every problem caught early. Live in 48 hours.",
)

# ------------------------------------------------------------------ generate
for slug, p in PAGES.items():
    html = head(p) + hero(p) + pain(p) + features(p) + faq(p) + internal_links(p) + final(p) + "\n" + TAIL
    open(f"{slug}.html", "w").write(html)
    print(f"wrote {slug}.html ({len(html)//1024}KB)")
