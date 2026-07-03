#!/usr/bin/env python3
"""Generates hub + local landing pages for 4 new verticals:
garage door, pest control, restoration, appliance repair."""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

LOGO_SVG = '<svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1" y="1" width="24" height="24" rx="6" stroke="currentColor" stroke-opacity="0.4"></rect><path d="M8 10 Q8 8 10 8 L12 8 L14 12 L12 14 Q14 17 16 18 L18 16 L22 18 L22 20 Q22 22 20 22 Q13 22 8 17 Q6 14 6 11 Z" fill="var(--accent)"></path><circle cx="20" cy="6" r="2" fill="var(--accent)"></circle></svg>'
ARROW_SVG = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10m0 0L9 4m4 4l-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FONTS_URL = 'https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'
SCRIPTS = '''<script>
window.addEventListener('scroll',()=>{document.getElementById('nav').classList.toggle('scrolled',window.scrollY>20)});
const io=new IntersectionObserver(e=>{e.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')})},{threshold:.1});
document.querySelectorAll('.reveal:not(.in)').forEach(el=>io.observe(el));
document.querySelectorAll('.faq-item').forEach(i=>i.addEventListener('click',()=>i.classList.toggle('open')));
const CALENDLY_URL='https://calendly.com/callingmatrix/30min';
function openCalendly(){if(window.Calendly){Calendly.initPopupWidget({url:CALENDLY_URL});return;}if(!document.querySelector('link[href*="calendly"]')){const l=document.createElement('link');l.rel='stylesheet';l.href='https://assets.calendly.com/assets/external/widget.css';document.head.appendChild(l);}const s=document.createElement('script');s.src='https://assets.calendly.com/assets/external/widget.js';s.onload=()=>Calendly.initPopupWidget({url:CALENDLY_URL});document.head.appendChild(s);}
</script>'''

ICON_BOLT = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M11 2l-7 10h7l-2 6 7-10h-7l2-6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_CAL = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="3" y="4" width="14" height="13" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M7 2v4M13 2v4M3 9h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
ICON_LIST = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
ICON_CHECK = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_CLOCK = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'

# ---------------------------------------------------------------------------
# Cities (match existing site footprint)
# ---------------------------------------------------------------------------

CITIES = [
    ('Atlanta', 'GA', "Metro Atlanta's sprawl and severe-weather seasons keep home service phones ringing at all hours"),
    ('Austin', 'TX', "Austin's explosive growth means new households needing service every week — and they call in the evening"),
    ('Charlotte', 'NC', "Charlotte's fast-growing suburbs mix new construction with aging housing stock, driving steady service demand"),
    ('Columbus', 'OH', "Columbus's hot summers and freezing winters put homes through stress in both directions"),
    ('Dallas', 'TX', "DFW's size and storm activity generate huge call volume — after-hours callers book whoever answers first"),
    ('Denver', 'CO', "Denver's temperature swings and hail seasons are hard on homes, and emergencies don't wait for morning"),
    ('Houston', 'TX', "Houston's heat, humidity, and hurricane seasons make home emergencies a year-round, around-the-clock reality"),
    ('Indianapolis', 'IN', "Indianapolis winters and humid summers drive service emergencies in every season"),
    ('Las Vegas', 'NV', "Las Vegas runs 24/7 — extreme heat and a round-the-clock economy mean calls come in at every hour"),
    ('Los Angeles', 'CA', "LA's enormous market rewards the company that answers first — and punishes voicemail ruthlessly"),
    ('Miami', 'FL', "Miami's tropical climate and bilingual market mean high call volume — much of it Spanish-first"),
    ('Nashville', 'TN', "Nashville's booming population and severe storm seasons keep service businesses slammed"),
    ('Orlando', 'FL', "Orlando's heat, storms, and short-term rental boom generate constant service demand"),
    ('Phoenix', 'AZ', "Phoenix's extreme heat is brutal on homes and equipment — and callers with an emergency don't leave voicemails"),
    ('Portland', 'OR', "Portland's wet climate and older housing stock surface home issues year-round"),
    ('Sacramento', 'CA', "Sacramento Valley heat waves and an aging housing stock keep service calls coming around the clock"),
    ('San Antonio', 'TX', "San Antonio's growth and largely bilingual market reward companies that answer every call — in both languages"),
    ('Seattle', 'WA', "Seattle's rain, cold snaps, and construction boom drive steady year-round service demand"),
    ('Tampa', 'FL', "Tampa's storm seasons and coastal climate generate call surges that bury an unattended phone"),
]

# ---------------------------------------------------------------------------
# New industries
# ---------------------------------------------------------------------------

INDUSTRIES = [
    {
        'key': 'garage-door',
        'hub_slug': 'garage-door',
        'name': 'Garage Door',
        'lower': 'garage door',
        'slug_prefix': 'garage-door-answering-service',
        'hub_title': 'Garage Door Answering Service | 24/7 AI | Calling Matrix',
        'hub_meta': "24/7 answering for garage door companies — emergencies dispatched, repairs booked automatically. Live in 48 hours. Book a free demo.",
        'hub_h1': 'A door stuck open at 9 PM<br>is a security emergency. <span class="italic accent">Answer that call.</span>',
        'hub_sub': "Broken springs, dead openers, doors that won't close at night — garage door calls are urgent, high-intent, and gone in minutes if no one picks up. Calling Matrix answers every call <strong>24/7</strong>, dispatches emergencies, and books repairs straight into your calendar.",
        'city_angle': "When a garage door won't close at night, homeowners call until someone picks up — a security worry doesn't wait for business hours.",
        'stat1': ('64%', 'of garage door calls come outside office hours'),
        'stat2': ('$385', 'Average repair ticket per answered call'),
        'stat3': ('<2s', 'Answer time, every time'),
        'pain1': ('80%', "of callers book the first company that answers", "A homeowner with a door stuck open isn't leaving a voicemail. They call down the Google list and stop at the first live answer."),
        'pain2': ('$385', "Average garage door repair ticket", "Spring replacements, opener repairs, off-track doors — every missed call is real revenue handed to the next listing."),
        'pain3': ('2 min', "Before callers move to a competitor", "Garage door repair is a speed game. The company that answers instantly wins the job almost every time."),
        'features': [
            (ICON_BOLT, 'Security-urgent dispatch', "A door stuck open at night or a car trapped inside gets flagged as urgent and routed to your on-call tech by call or text — with name, address, and issue captured."),
            (ICON_LIST, 'Repair intake that preps your tech', "Captures door type, opener brand, and symptom (spring, cable, track, opener) during the call so your tech rolls up with the right parts on the truck."),
            (ICON_CAL, 'Same-day slot booking', "Books repairs directly into Housecall Pro, Jobber, ServiceTitan, or Google Calendar — customers see confirmation before they hang up."),
            (ICON_CHECK, 'New-door quote capture', "Replacement and new-install inquiries get full measurements, style preferences, and budget captured — then automatic follow-up until the estimate books."),
        ],
        'faqs': [
            ("Can it tell a security emergency from a routine repair?", "Yes. A door stuck open at night, a car trapped inside, or a door off its tracks gets flagged urgent and dispatched to your on-call tech immediately. A noisy opener books the next available slot instead."),
            ("Does it capture the details my techs need?", "Yes. It asks about the door type, opener brand, and specific symptom — broken spring, snapped cable, off-track, dead opener — so your tech arrives with the right parts."),
            ("Can it book same-day appointments?", "Yes. It reads your real availability from your scheduling software and books the first open slot, confirming with the customer on the call."),
            ("Does it handle new door sales inquiries too?", "Yes. Replacement and new-install leads get full intake — sizes, styles, timeline, budget — plus automatic follow-up at 24, 48, and 72 hours if they don't book immediately."),
            ("How fast can a garage door company go live?", "Most companies are live within 48 hours after a 30-minute onboarding call."),
        ],
        'final_h2': 'Every missed call is a<br><span class="italic">$385 repair lost.</span>',
        'final_p': "Garage door customers book the first company that answers. Calling Matrix makes sure that's always you — nights, weekends, and holidays included.",
    },
    {
        'key': 'pest-control',
        'hub_slug': 'pest-control',
        'name': 'Pest Control',
        'lower': 'pest control',
        'slug_prefix': 'pest-control-answering-service',
        'hub_title': 'Pest Control Answering Service | 24/7 AI | Calling Matrix',
        'hub_meta': "24/7 answering for pest control — every panic call answered, treatments booked, recurring plans pitched. Live in 48 hours. Book a free demo.",
        'hub_h1': 'They found termites an hour ago.<br><span class="italic accent">They\'ve already called three companies.</span>',
        'hub_sub': "Pest calls are panic calls — bed bugs, wasp nests, rodents in the kitchen. Callers dial down the list until someone answers. Calling Matrix picks up <strong>every call in under 2 seconds</strong>, books treatments, and turns one-time jobs into recurring quarterly plans.",
        'city_angle': "Pest sightings trigger immediate, emotional calls — and the caller books whichever exterminator picks up first.",
        'stat1': ('68%', 'of pest control calls come evenings & weekends'),
        'stat2': ('$720', 'Average annual value of a recurring plan'),
        'stat3': ('<2s', 'Answer time, every time'),
        'pain1': ('85%', "of panicked callers never call back", "Someone who just found roaches isn't waiting for a callback. If you don't answer, the next company on Google gets the job — and the recurring plan."),
        'pain2': ('$720', "Annual value of each recurring customer", "A single answered call becomes a quarterly plan worth hundreds a year. A single missed call is that revenue compounding for your competitor."),
        'pain3': ('10×', "Call spikes during swarm season", "Termite swarms and spring emergence bury your phone lines exactly when your techs are busiest in the field."),
        'features': [
            (ICON_BOLT, 'Urgency triage by pest type', "Bed bugs, wasps near kids, rodents in a restaurant — genuinely urgent calls route to same-day slots or your on-call tech; routine treatments book the next opening."),
            (ICON_CAL, 'Recurring plan setup', "Books the initial treatment and pitches your quarterly or monthly plan on the same call — capturing frequency, property size, and pest history automatically."),
            (ICON_CLOCK, 'Seasonal surge handling', "Termite swarm season, spring ant explosions, fall rodent rushes — every caller answered within 2 seconds no matter how hard your phone is ringing."),
            (ICON_CHECK, 'PestPac, FieldRoutes & CRM sync', "Bookings flow into your pest control software or calendar with full details — property type, target pest, and access notes included."),
        ],
        'faqs': [
            ("Can it book both one-time treatments and recurring plans?", "Yes. It books the initial visit and is trained to offer your recurring plan options — quarterly, bi-monthly, or monthly — converting one-time callers into contract revenue."),
            ("How does it handle panicked callers?", "It answers instantly, stays calm, gathers the pest type and severity, and gets a treatment on the calendar fast — which is exactly what a panicked caller needs to stop dialing competitors."),
            ("Does it screen for the pests we actually treat?", "Yes. During onboarding we load your service list — general pests, termites, bed bugs, wildlife — so it books what you do and refers out what you don't."),
            ("Can it handle commercial accounts differently from residential?", "Yes. Separate intake flows capture what commercial callers need — property type, compliance requirements, urgency — and route high-value accounts to you directly."),
            ("How fast can we go live?", "Most pest control companies are live within 48 hours after a 30-minute onboarding call."),
        ],
        'final_h2': 'Every missed call is a<br><span class="italic">recurring contract lost.</span>',
        'final_p': "Pest customers call in a panic and stay for years — if you answer. Calling Matrix picks up every call, books the job, and pitches the plan.",
    },
    {
        'key': 'restoration',
        'hub_slug': 'restoration',
        'name': 'Restoration',
        'lower': 'restoration',
        'slug_prefix': 'restoration-answering-service',
        'hub_title': 'Restoration Answering Service | 24/7 | Calling Matrix',
        'hub_meta': "24/7 answering for restoration companies — insurance details captured, crews dispatched instantly. Live in 48 hours. Book a free demo.",
        'hub_h1': 'Water is spreading through their house<br><span class="italic accent">while your phone rings.</span>',
        'hub_sub': "Restoration is the most time-critical trade there is. A flooded homeowner calls every company on Google in five minutes — and the $5,000+ mitigation job goes to whoever answers. Calling Matrix picks up <strong>every call in under 2 seconds</strong>, captures insurance details, and dispatches your crew instantly.",
        'city_angle': "Flood, fire, and mold emergencies are dispatched within minutes — the restoration company that answers first gets the mitigation job.",
        'stat1': ('100%', 'of restoration calls are emergencies'),
        'stat2': ('$5.2k', 'Average water mitigation job value'),
        'stat3': ('<2s', 'Answer time, every time'),
        'pain1': ('5 min', "From first call to a competitor dispatched", "A homeowner standing in water calls everyone. The first company to answer and confirm a crew wins — everyone else's phone just rang for nothing."),
        'pain2': ('$5.2k', "Average mitigation job that voicemail loses", "Water mitigation, fire cleanup, and mold remediation are four-figure jobs minimum. Missing one after-hours call erases a month of marketing spend."),
        'pain3': ('10×', "Call surges after storms and freezes", "Burst-pipe freezes and flood events bury your lines overnight. Every unanswered ring is a job your competitor is driving to."),
        'features': [
            (ICON_BOLT, 'Instant crew dispatch', "Active water, fire, or sewage emergencies trigger an immediate call or text to your on-call crew with address, source, and severity — while the caller is still on the line."),
            (ICON_LIST, 'Insurance & claim intake', "Captures carrier, policy details, cause of loss, and affected areas during the first call — so your estimator walks in ready and the claim starts clean."),
            (ICON_CLOCK, 'Storm & freeze surge coverage', "When a freeze bursts pipes across the metro, every panicked caller gets answered in under 2 seconds. No queue, no overflow service, no per-call surcharges."),
            (ICON_CHECK, 'Job sync to your platform', "Losses flow into your CRM or scheduling stack with full intake notes — DASH, Encircle, or plain calendar, configured during onboarding."),
        ],
        'faqs': [
            ("How fast does it dispatch an active water loss?", "Immediately. The AI confirms the emergency, captures address and severity, and notifies your on-call crew by call or text while the customer is still on the line."),
            ("Can it capture insurance information?", "Yes. It gathers carrier, claim status, cause of loss, and affected areas on the first call — so your team starts the claim with clean, complete intake."),
            ("What happens during a regional storm or freeze event?", "Calling Matrix answers unlimited simultaneous calls. When a freeze event triples your volume overnight, every caller still gets a sub-2-second answer and proper triage."),
            ("Does it qualify jobs before waking up my crew?", "Yes. Your emergency thresholds are configured during onboarding — active water dispatches now; a week-old stain books an inspection for tomorrow."),
            ("How fast can a restoration company go live?", "Most companies are live within 48 hours after a 30-minute onboarding call."),
        ],
        'final_h2': 'The next flooded homeowner<br><span class="italic">calls in five companies at once.</span>',
        'final_p': "Be the one that answers in 2 seconds, captures the claim, and dispatches a crew. That's the whole game in restoration — and it's live in 48 hours.",
    },
    {
        'key': 'appliance-repair',
        'hub_slug': 'appliance-repair',
        'name': 'Appliance Repair',
        'lower': 'appliance repair',
        'slug_prefix': 'appliance-repair-answering-service',
        'hub_title': 'Appliance Repair Answering Service | Calling Matrix',
        'hub_meta': "24/7 answering for appliance repair — brand, model & symptom captured, repairs booked automatically. Live in 48 hours. Book a free demo.",
        'hub_h1': 'Their fridge died with $400<br>of groceries inside. <span class="italic accent">They\'re calling right now.</span>',
        'hub_sub': "Dead refrigerators, flooding washers, ovens out the week of Thanksgiving — appliance calls are urgent and comparison-shopped hard. Calling Matrix answers <strong>every call in under 2 seconds</strong>, captures brand, model, and symptom, and books the repair before the caller can dial a competitor.",
        'city_angle': "A dead refrigerator or flooding washer gets fixed by whichever repair company answers the phone first.",
        'stat1': ('62%', 'of appliance calls come evenings & weekends'),
        'stat2': ('$285', 'Average repair ticket per answered call'),
        'stat3': ('<2s', 'Answer time, every time'),
        'pain1': ('75%', "of callers ring at least 3 repair companies", "Appliance repair is comparison-shopped harder than almost any trade. Instant answer plus instant booking ends the shopping spree at your company."),
        'pain2': ('$285', "Average ticket walking away per missed call", "Refrigerators, washers, dryers, ovens — every unanswered call is a booked job for the shop across town."),
        'pain3': ('50%', "of no-shows come from bad intake", "Wrong address, wrong appliance, no gate code, wrong parts on the truck. Sloppy phone intake burns tech hours every single week."),
        'features': [
            (ICON_LIST, 'Brand, model & symptom intake', "Captures appliance type, brand, model number, and symptom on the first call — so your tech arrives with the right parts instead of scheduling a second visit."),
            (ICON_BOLT, 'Urgency-aware booking', "A flooding washer or a dead fridge full of food books today's first opening; a noisy dryer books the next routine slot. Your rules, applied consistently."),
            (ICON_CAL, 'Real-time calendar booking', "Appointments land in your scheduling software or Google Calendar instantly, with time-window confirmations sent to the customer automatically."),
            (ICON_CHECK, 'Warranty & service-area screening', "Screens for the brands you service, your zip codes, and warranty status before booking — no more driving 40 minutes for a job you can't do."),
        ],
        'faqs': [
            ("Does it capture the model number during the call?", "Yes. It walks the caller through finding the brand and model, plus the symptom — so your tech shows up with the right parts and closes the job in one visit."),
            ("Can it prioritize genuine emergencies?", "Yes. A flooding washer or a dead refrigerator full of groceries books your first available slot; routine repairs queue behind them. Thresholds are configured to your rules."),
            ("Does it screen out brands or areas we don't service?", "Yes. Your service area and brand list load during onboarding — out-of-scope callers get politely referred out instead of wasting a booking slot."),
            ("Can it handle warranty and manufacturer-dispatch calls?", "Yes. It captures warranty status and claim details during intake, and can apply different flows for warranty work versus customer-pay repairs."),
            ("How fast can an appliance repair company go live?", "Most companies are live within 48 hours after a 30-minute onboarding call."),
        ],
        'final_h2': 'Every missed call books<br><span class="italic">the shop across town.</span>',
        'final_p': "Appliance customers comparison shop by phone — and stop at the first live answer. Calling Matrix makes sure that's you, 24/7.",
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc_json(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

def build_faq_ld(faqs):
    items = []
    for q, a in faqs:
        items.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (esc_json(q), esc_json(a))
        )
    return ','.join(items)

def feat_grid(features):
    cells = []
    for i, (icon, h3, p) in enumerate(features):
        d = '' if i == 0 else f' d{i}'
        cells.append(f'      <div class="feat reveal in{d}"><div class="feat-icon">{icon}</div><h3>{h3}</h3><p>{p}</p></div>')
    return '<div class="feat-grid">\n' + '\n'.join(cells) + '\n    </div>'

def faq_list(faqs):
    return '\n'.join(
        f'      <div class="faq-item"><div class="faq-q"><span>{q}</span><span class="faq-plus"></span></div>'
        f'<div class="faq-a">{a}</div></div>'
        for q, a in faqs
    )

HEAD_COMMON = f'''<script defer src="/_vercel/insights/script.js"></script>
<script src="https://analytics.ahrefs.com/analytics.js" data-key="94z1bOhN7RVx3o2W/eEUbQ" async></script>
<link rel="stylesheet" href="/shared.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="{FONTS_URL}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{FONTS_URL}"></noscript>'''

FOOTER = f'''<footer><div class="wrap">
  <div class="foot-inner">
    <div class="foot-brand"><a href="/" class="logo" style="font-family:var(--serif);font-size:20px;display:flex;align-items:center;gap:8px;"><span class="logo-mark">{LOGO_SVG}</span>Calling Matrix</a><p>24/7 AI receptionist for home service businesses. Answer every call. Book every job.</p></div>
    <div class="foot-col"><h6>Industries</h6><a href="/hvac">HVAC</a><a href="/plumbing">Plumbing</a><a href="/electrical">Electrical</a><a href="/roofing">Roofing</a><a href="/cleaning">Cleaning</a><a href="/garage-door">Garage Door</a><a href="/pest-control">Pest Control</a><a href="/restoration">Restoration</a><a href="/appliance-repair">Appliance Repair</a></div>
    <div class="foot-col"><h6>Product</h6><a href="/#features">Features</a><a href="/pricing">Pricing</a><a href="/faq">FAQ</a><a href="/roi-calculator">ROI Calculator</a><a href="/blog">Blog</a></div>
  </div>
  <div class="foot-bottom"><span>&copy; 2026 Calling Matrix. All rights reserved.</span><span>callingmatrix.com</span></div>
</div></footer>'''

INTEGRATIONS = '''<!-- Integration links for internal linking + SEO -->
<section style="background:var(--bg-2);border-top:1px solid var(--line);padding:48px 0;">
  <div class="wrap" style="text-align:center;">
    <p style="font-family:var(--mono);font-size:12px;letter-spacing:0.14em;text-transform:uppercase;color:var(--fg-mute);margin-bottom:20px;">Works with your software</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;">
      <a href="/housecall-pro" style="padding:10px 20px;border:1px solid var(--line);border-radius:999px;font-size:14px;color:var(--fg-dim);text-decoration:none;">Housecall Pro →</a>
      <a href="/servicetitan" style="padding:10px 20px;border:1px solid var(--line);border-radius:999px;font-size:14px;color:var(--fg-dim);text-decoration:none;">ServiceTitan →</a>
      <a href="/jobber" style="padding:10px 20px;border:1px solid var(--line);border-radius:999px;font-size:14px;color:var(--fg-dim);text-decoration:none;">Jobber →</a>
    </div>
  </div>
</section>'''

def nav_block():
    return f'''<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="/" class="logo"><span class="logo-mark">{LOGO_SVG}</span>Calling Matrix</a>
    <nav class="nav-links"><a href="#features">Features</a><a href="#faq">FAQ</a><a href="/pricing">Pricing</a><a href="/blog">Blog</a></nav>
    <a href="#" class="nav-cta" onclick="openCalendly();return false;">Book a consultation</a>
    <button class="mob-menu-btn" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</nav>'''

MOB_MENU_SCRIPT = '''<script>
(function(){
  var b=document.querySelector('.mob-menu-btn');
  var n=document.querySelector('.nav-links');
  if(!b||!n)return;
  b.addEventListener('click',function(){
    var o=n.classList.toggle('mob-open');
    b.classList.toggle('mob-open',o);
    b.setAttribute('aria-expanded',String(o));
    document.body.style.overflow=o?'hidden':'';
  });
  n.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click',function(){
      n.classList.remove('mob-open');
      b.classList.remove('mob-open');
      b.setAttribute('aria-expanded','false');
      document.body.style.overflow='';
    });
  });
})();
</script>'''

def head_meta(title, meta_desc, canonical, og_desc, og_industry):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="Calling Matrix">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Calling Matrix">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://callingmatrix.com/api/og?industry={og_industry}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@callingmatrix">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="https://callingmatrix.com/api/og?industry={og_industry}">'''

# ---------------------------------------------------------------------------
# Hub page
# ---------------------------------------------------------------------------

def build_hub(ind):
    canonical = f"https://callingmatrix.com/{ind['hub_slug']}"
    city_links = '\n'.join(
        f'''<li><a href="/{ind['slug_prefix']}-{c.lower().replace(' ', '-')}" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color='var(--accent,#E89B6C)'" onmouseout="this.style.color='var(--fg-dim,#B8B0A0)'">{ind['name']} Answering Service — {c}, {s} →</a></li>'''
        for c, s, _ in CITIES[:6]
    )
    schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"Organization","name":"Calling Matrix","url":"https://callingmatrix.com","email":"hi@callingmatrix.com"},'
        '{"@type":"WebPage","name":"' + esc_json(ind['name'] + ' AI Receptionist — Calling Matrix') + '",'
        '"url":"' + canonical + '","description":"' + esc_json(ind['hub_meta']) + '","inLanguage":"en-US"},'
        '{"@type":"Service","name":"' + esc_json(ind['name'] + ' Answering Service') + '",'
        '"serviceType":"' + esc_json(ind['name'] + ' Answering Service') + '",'
        '"provider":{"@type":"Organization","name":"Calling Matrix"},'
        '"description":"' + esc_json(ind['hub_meta']) + '",'
        '"areaServed":{"@type":"Country","name":"United States"},'
        '"offers":{"@type":"Offer","price":"497","priceCurrency":"USD"}},'
        '{"@type":"FAQPage","mainEntity":[' + build_faq_ld(ind['faqs']) + ']},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://callingmatrix.com"},'
        '{"@type":"ListItem","position":2,"name":"' + esc_json(ind['name'] + ' AI Receptionist') + '","item":"' + canonical + '"}]}]}'
    )
    return f'''<!DOCTYPE html><html lang="en"><head>
{head_meta(ind['hub_title'], ind['hub_meta'], canonical, ind['hub_meta'], ind['key'])}
<script type="application/ld+json">{schema}</script>
{HEAD_COMMON}
</head>
<body>
<a class="skip-nav" href="#main-content">Skip to content</a>
{nav_block()}

<header class="hero" id="main-content">
  <div class="hero-bg"></div><div class="hero-grid"></div>
  <div class="wrap">
    <span class="eyebrow reveal in"><span class="dot"></span><span>Built for {ind['lower']} companies</span></span>
    <h1 class="hero-title reveal in d1">{ind['hub_h1']}</h1>
    <p class="hero-sub reveal in d2">{ind['hub_sub']}</p>
    <div class="cta-row reveal in d3">
      <a href="#" class="btn btn-primary" onclick="openCalendly();return false;"><span>Book a free 15-min consultation</span> {ARROW_SVG}</a>
      <a href="#features" class="btn btn-ghost">See how it works →</a>
    </div>
    <div class="hero-stats reveal in d3">
      <div><div class="s-num">{ind['stat1'][0]}</div><div class="s-lbl">{ind['stat1'][1]}</div></div>
      <div><div class="s-num">{ind['stat2'][0]}</div><div class="s-lbl">{ind['stat2'][1]}</div></div>
      <div><div class="s-num">{ind['stat3'][0]}</div><div class="s-lbl">{ind['stat3'][1]}</div></div>
    </div>
  </div>
</header>

<section class="pain">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">The problem</div><h2 class="sec-title">Your customers call once.<br><span class="italic">Then they call someone else.</span></h2></div>
    <div class="pain-grid">
      <div class="pain-cell reveal in"><div class="big-num">{ind['pain1'][0]}</div><h3>{ind['pain1'][1]}</h3><p>{ind['pain1'][2]}</p></div>
      <div class="pain-cell reveal in d1"><div class="big-num">{ind['pain2'][0]}</div><h3>{ind['pain2'][1]}</h3><p>{ind['pain2'][2]}</p></div>
      <div class="pain-cell reveal in d2"><div class="big-num">{ind['pain3'][0]}</div><h3>{ind['pain3'][1]}</h3><p>{ind['pain3'][2]}</p></div>
    </div>
    <p style="margin-top:28px;font-family:var(--mono);font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--fg-mute);">Further reading &rarr; <a href="/blog/missed-call-value" style="color:var(--accent);text-decoration:none;transition:opacity .2s;" onmouseover="this.style.opacity='.7'" onmouseout="this.style.opacity='1'">What a missed call actually costs</a></p>
  </div>
</section>

<section class="features" id="features">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">Features</div><h2 class="sec-title">Built for how {ind['lower']}<br><span class="italic">businesses actually run.</span></h2><p class="sec-sub">Trained on your services, pricing, and territory during a 30-minute onboarding call — live within 48 hours.</p></div>
    {feat_grid(ind['features'])}
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">FAQ</div><h2 class="sec-title">Questions {ind['lower']} owners<br><span class="italic">ask us every day.</span></h2></div>
    <div class="faq-list">
{faq_list(ind['faqs'])}
    </div>
  </div>
</section>

<!-- INTERNAL LINKS -->
<section style="background:var(--bg-2,#141310);border-top:1px solid var(--line,rgba(180,120,60,.12));padding:56px 0;">
  <div style="max-width:1120px;margin:0 auto;padding:0 32px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;">
      <div>
        <p style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#E89B6C);margin-bottom:16px;">Cities we serve</p>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
          {city_links}
        </ul>
      </div>
      <div>
        <p style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#E89B6C);margin-bottom:16px;">Keep reading</p>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
          <li><a href="/virtual-receptionist" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color='var(--accent,#E89B6C)'" onmouseout="this.style.color='var(--fg-dim,#B8B0A0)'">Virtual Receptionist for Home Services →</a></li>
          <li><a href="/after-hours-answering-service" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color='var(--accent,#E89B6C)'" onmouseout="this.style.color='var(--fg-dim,#B8B0A0)'">After-Hours Answering Service →</a></li>
          <li><a href="/bilingual-answering-service" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color='var(--accent,#E89B6C)'" onmouseout="this.style.color='var(--fg-dim,#B8B0A0)'">Bilingual Answering Service →</a></li>
          <li><a href="/pricing" style="font-size:15px;color:var(--fg-dim,#B8B0A0);transition:color .2s;text-decoration:none;" onmouseover="this.style.color='var(--accent,#E89B6C)'" onmouseout="this.style.color='var(--fg-dim,#B8B0A0)'">Calling Matrix Pricing →</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="final"><div class="wrap inner">
  <h2 class="reveal in">{ind['final_h2']}</h2>
  <p class="reveal in d1">{ind['final_p']}</p>
  <a href="#" class="btn btn-primary reveal in d2" onclick="openCalendly();return false;"><span>Book a free 15-min consultation</span> {ARROW_SVG}</a>
</div></section>

{INTEGRATIONS}

{FOOTER}
{SCRIPTS}
{MOB_MENU_SCRIPT}
</body></html>'''

# ---------------------------------------------------------------------------
# City page
# ---------------------------------------------------------------------------

def build_city(ind, city, state, fact):
    slug = f"{ind['slug_prefix']}-{city.lower().replace(' ', '-')}"
    canonical = f'https://callingmatrix.com/{slug}'
    base_title = f"{ind['name']} Answering Service in {city}, {state}"
    title = base_title + ' | Calling Matrix' if len(base_title) <= 43 else base_title
    meta_desc = f"Never miss a {ind['lower']} call in {city}. 24/7 AI answering — emergencies routed, jobs booked automatically. Live in 48 hours. Book a free demo."
    og_desc = f"24/7 AI answering service for {ind['lower']} companies in {city}, {state}. Every call answered, every job booked."
    local_desc = f"24/7 AI answering service for {ind['lower']} companies in {city}, {state}. Answers every call, routes emergencies, and books jobs automatically."
    hero_sub = f"{fact}. {ind['city_angle']} Calling Matrix answers every call <strong>24/7</strong> — emergencies routed instantly, every job booked automatically. Live in 48 hours."

    faq_ld = ind['faqs'][:3]
    schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"Organization","name":"Calling Matrix","url":"https://callingmatrix.com"},'
        '{"@type":"LocalBusiness","name":"Calling Matrix",'
        '"url":"' + canonical + '",'
        '"description":"' + esc_json(local_desc) + '",'
        '"areaServed":{"@type":"City","name":"' + city + '","addressRegion":"' + state + '"}},'
        '{"@type":"Service","name":"' + esc_json(ind['name'] + ' Answering Service ' + city + ' ' + state) + '",'
        '"serviceType":"' + esc_json(ind['name'] + ' Answering Service') + '",'
        '"provider":{"@type":"Organization","name":"Calling Matrix"},'
        '"description":"' + esc_json(local_desc) + '",'
        '"areaServed":{"@type":"City","name":"' + city + '","addressRegion":"' + state + '"},'
        '"offers":{"@type":"Offer","price":"497","priceCurrency":"USD"}},'
        '{"@type":"FAQPage","mainEntity":[' + build_faq_ld(faq_ld) + ']},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://callingmatrix.com"},'
        '{"@type":"ListItem","position":2,"name":"' + esc_json(ind['name'] + ' AI Receptionist') + '","item":"https://callingmatrix.com/' + ind['hub_slug'] + '"},'
        '{"@type":"ListItem","position":3,"name":"' + esc_json(city + ' ' + ind['name']) + '","item":"' + canonical + '"}]}]}'
    )

    return slug, f'''<!DOCTYPE html><html lang="en"><head>
{head_meta(title, meta_desc, canonical, og_desc, ind['key'])}
<script type="application/ld+json">{schema}</script>
{HEAD_COMMON}
</head>
<body>
<a class="skip-nav" href="#main-content">Skip to content</a>
{nav_block()}

<header class="hero" id="main-content">
  <div class="hero-bg"></div><div class="hero-grid"></div>
  <div class="wrap">
    <span class="eyebrow reveal in"><span class="dot"></span><span>Built for {city} {ind['lower']} companies</span></span>
    <h1 class="hero-title reveal in d1">{city} {ind['lower']} calls answered.<br>Day, night, <span class="italic accent">24/7.</span></h1>
    <p class="hero-sub reveal in d2">{hero_sub}</p>
    <div class="cta-row reveal in d3">
      <a href="#" class="btn btn-primary" onclick="openCalendly();return false;"><span>Book a free 15-min consultation</span> {ARROW_SVG}</a>
      <a href="#features" class="btn btn-ghost">See how it works &rarr;</a>
    </div>
    <div class="hero-stats reveal in d3">
      <div><div class="s-num">{ind['stat1'][0]}</div><div class="s-lbl">{ind['stat1'][1]}</div></div>
      <div><div class="s-num">{ind['stat2'][0]}</div><div class="s-lbl">{ind['stat2'][1]}</div></div>
      <div><div class="s-num">{ind['stat3'][0]}</div><div class="s-lbl">{ind['stat3'][1]}</div></div>
    </div>
  </div>
</header>

<section class="pain">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">The problem</div><h2 class="sec-title">{city} competitors are answering.<br><span class="italic">You're going to voicemail.</span></h2></div>
    <div class="pain-grid">
      <div class="pain-cell reveal in"><div class="big-num">{ind['pain1'][0]}</div><h3>{ind['pain1'][1]}</h3><p>{city} homeowners and businesses don't leave voicemails — they book whoever picks up first.</p></div>
      <div class="pain-cell reveal in d1"><div class="big-num">{ind['pain2'][0]}</div><h3>{ind['pain2'][1]}</h3><p>Every missed {ind['lower']} call in {city} is revenue going straight to your competitor.</p></div>
      <div class="pain-cell reveal in d2"><div class="big-num">{ind['pain3'][0]}</div><h3>{ind['pain3'][1]}</h3><p>Calling Matrix answers in under 2 seconds. Every caller, every time.</p></div>
    </div>
    <p style="margin-top:28px;font-family:var(--mono);font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--fg-mute);">Further reading &rarr; <a href="/blog/missed-call-value" style="color:var(--accent);text-decoration:none;transition:opacity .2s;" onmouseover="this.style.opacity='.7'" onmouseout="this.style.opacity='1'">What a missed call actually costs</a></p>
  </div>
</section>

<section class="features" id="features">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">Features</div><h2 class="sec-title">Built for how {city} {ind['lower']}<br><span class="italic">businesses actually work.</span></h2><p class="sec-sub">Trained on your services, pricing, and {city} territory. Handles emergencies, surges, and routine bookings without missing a beat.</p></div>
    {feat_grid(ind['features'])}
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
    <div class="sec-head reveal in"><div class="sec-label">FAQ</div><h2 class="sec-title">Questions {city} {ind['lower']} owners<br><span class="italic">ask us every day.</span></h2></div>
    <div class="faq-list">
{faq_list(ind['faqs'])}
    </div>
  </div>
</section>

<section class="final"><div class="wrap inner">
  <h2 class="reveal in">Stop losing {city} jobs to<br><span class="italic">voicemail.</span></h2>
  <p class="reveal in d1">See how {city} {ind['lower']} companies are booking more jobs with an AI receptionist that never takes a day off.</p>
  <a href="#" class="btn btn-primary reveal in d2" onclick="openCalendly();return false;"><span>Book a free 15-min consultation</span> {ARROW_SVG}</a>
</div></section>

<!-- INTERNAL LINKS -->
<section style="background:var(--bg-2,#141310);border-top:1px solid var(--line,rgba(180,120,60,.12));padding:48px 0;">
  <div style="max-width:1120px;margin:0 auto;padding:0 32px;text-align:center;">
    <p style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#E89B6C);margin-bottom:16px;">Learn more</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;">
      <a href="/{ind['hub_slug']}" style="padding:10px 20px;border:1px solid var(--line,#2A2620);border-radius:999px;font-size:14px;color:var(--fg-dim,#B8B0A0);text-decoration:none;">{ind['name']} AI Receptionist →</a>
      <a href="/after-hours-answering-service" style="padding:10px 20px;border:1px solid var(--line,#2A2620);border-radius:999px;font-size:14px;color:var(--fg-dim,#B8B0A0);text-decoration:none;">After-Hours Answering →</a>
      <a href="/pricing" style="padding:10px 20px;border:1px solid var(--line,#2A2620);border-radius:999px;font-size:14px;color:var(--fg-dim,#B8B0A0);text-decoration:none;">Pricing →</a>
    </div>
  </div>
</section>

{FOOTER}
{SCRIPTS}
{MOB_MENU_SCRIPT}
</body></html>'''

# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    count = 0
    slugs = []
    for ind in INDUSTRIES:
        html = build_hub(ind)
        with open(os.path.join(OUT, ind['hub_slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        slugs.append(ind['hub_slug'])
        count += 1
        for city, state, fact in CITIES:
            slug, html = build_city(ind, city, state, fact)
            with open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            slugs.append(slug)
            count += 1
    print(f"Done. {count} pages written.")
    with open(os.path.join(OUT, 'new_trade_slugs.txt'), 'w') as f:
        f.write('\n'.join(slugs))
