#!/usr/bin/env python3
"""Generates 8 local landing pages for HVAC + Plumbing x 4 cities."""

import os, json

OUT = '/Users/bren/CM.01'

# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Page data
# ---------------------------------------------------------------------------

HVAC_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Emergency call routing</h3><p>Identifies urgent calls — no AC, no heat, system not responding — and immediately notifies your on-call technician via text or call forwarding. No emergencies slip through.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Seasonal surge handling</h3><p>Handles 10x normal call volume during heat waves and cold snaps without adding staff. Every caller gets a live answer within 2 seconds.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 10h14M3 5h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Service agreement upsells</h3><p>Trained to mention your maintenance plan and capture service agreement signups during every booking call — turning one-time customers into recurring revenue.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Housecall Pro &amp; ServiceTitan sync</h3><p>Jobs book directly into your existing software. No double entry, no missed slots — your technicians see new jobs the moment they are booked.</p></div>
    </div>'''

PLUMBING_FEATURES = '''<div class="feat-grid">
      <div class="feat reveal in"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Emergency leak routing</h3><p>Identifies burst pipe, flooding, and sewage backup calls and immediately dispatches your on-call plumber with customer name, address, and issue description sent by text.</p></div>
      <div class="feat reveal in d1"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/><path d="M7 10h6M10 7v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Service area screening</h3><p>Asks callers for their zip code before booking — ensures you only take calls within your service territory and never dispatch a tech to an out-of-range address.</p></div>
      <div class="feat reveal in d2"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div><h3>Job type intake</h3><p>Collects the issue, location, and urgency before confirming the booking so your tech shows up prepared with the right parts, not guessing from a vague work order.</p></div>
      <div class="feat reveal in d3"><div class="feat-icon"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 10l4 4 6-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>ServiceTitan &amp; Jobber sync</h3><p>Every booking flows directly into your scheduling software. Zero manual entry, zero missed slots — jobs appear on your techs schedules the moment they are confirmed.</p></div>
    </div>'''

PAGES = [
  # ── HVAC ──────────────────────────────────────────────────────────────────
  {
    'slug': 'hvac-answering-service-austin',
    'industry': 'hvac',
    'city': 'Austin',
    'state': 'TX',
    'title': 'HVAC Answering Service in Austin, TX | Calling Matrix',
    'meta_desc': "Austin's AC season runs 9 months. Calling Matrix answers every HVAC call 24/7 — routes emergencies to your tech, books tune-ups automatically. Live in 48 hours.",
    'og_desc': "Austin's AC season runs 9 months. 24/7 AI answering service for Austin HVAC companies — routes emergencies, books tune-ups, handles heat wave surge.",
    'parent_name': 'HVAC AI Receptionist',
    'parent_url': 'https://callingmatrix.com/hvac',
    'local_service_desc': '24/7 AI answering service for HVAC companies in Austin, TX. Answers every AC emergency call, routes to on-call techs, and books tune-ups automatically.',
    'eyebrow': 'Built for Austin HVAC companies',
    'h1': 'Austin AC calls answered.<br>Day, night, <span class="italic accent">heat wave.</span>',
    'hero_sub': "Austin summers routinely push past 105°F. When a homeowner's AC fails at midnight, they call every HVAC company on Google and book the first one that picks up. Calling Matrix answers every call <strong>24/7</strong> — emergencies routed to your on-call tech, tune-ups booked automatically.",
    'stat1_num': '67%',
    'stat1_lbl': 'of HVAC calls happen after 6 PM',
    'stat2_num': '$380',
    'stat2_lbl': 'Average job value per missed call',
    'stat3_num': '<2s',
    'stat3_lbl': 'Answer time, every time',
    'pain_label': 'The problem',
    'pain_title': 'Austin competitors are answering.<br><span class="italic">You\'re going to voicemail.</span>',
    'pain1_num': '63%',
    'pain1_h3': 'of after-hours calls go straight to voicemail',
    'pain1_p': "Austin homeowners with broken AC don't wait until morning. They call three companies and book the first one that answers.",
    'pain2_num': '$4.2k',
    'pain2_h3': 'Lost per week in Austin peak season',
    'pain2_p': "Missing just 3 calls a day during summer adds up fast. One month of Calling Matrix costs less than a single missed Austin job.",
    'pain3_num': '2 min',
    'pain3_h3': 'Before callers move to your Austin competitor',
    'pain3_p': "68% of callers move on to the next HVAC company on Google if no one answers within 2 minutes.",
    'pain_link_href': 'https://callingmatrix.blog/hvac-answering-service-cost',
    'pain_link_text': 'How much does an HVAC answering service cost?',
    'feat_label': 'Features',
    'feat_title': 'Built for how Austin HVAC<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, pricing, and Austin territory. Handles emergencies, seasonal surges, and routine bookings without missing a beat.',
    'feat_html': HVAC_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Austin HVAC owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ('Does it handle Austin heat wave surge?', "Yes. Calling Matrix handles 10x normal call volume during Austin's summer heat waves without any staffing changes. Every caller gets a live answer within 2 seconds, whether it's your 10th call or your 200th."),
      ('Can it serve Greater Austin including Round Rock, Cedar Park, and Pflugerville?', "Yes. During onboarding we load your full service territory — zip codes, cities, and suburbs — so the AI books calls inside your area and declines calls outside it."),
      ('Will it know Austin-specific HVAC brands like Lennox and Carrier?', "Yes. We train the AI on the brands your company services so it can field questions about specific systems, capture equipment details, and route accordingly."),
      ('Does it handle both residential and commercial HVAC calls?', "Yes. We configure intake workflows for both residential and commercial — different questions, urgency levels, and routing for each call type."),
      ('How fast can an Austin HVAC company go live?', "Most Austin companies are live in 48 hours. We start with a 30-minute onboarding call, then build and deploy your AI receptionist. Same-week go-live is standard."),
    ],
    'final_h2': 'Stop losing Austin jobs to<br><span class="italic">voicemail.</span>',
    'final_p': "See how Austin HVAC companies are booking 37% more jobs with an AI receptionist that never takes a day off — not during heat waves, not at 2 AM, not on holidays.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ('Does it handle Austin heat wave surge?', "Yes. Calling Matrix handles 10x normal call volume during Austin's summer heat waves without any staffing changes. Every caller gets a live answer within 2 seconds, whether it's your 10th call or your 200th."),
      ('Can it serve Greater Austin including Round Rock, Cedar Park, and Pflugerville?', "Yes. During onboarding we load your full service territory -- zip codes, cities, and suburbs -- so the AI books calls inside your area and declines calls outside it."),
      ('How fast can an Austin HVAC company go live?', "Most Austin companies are live in 48 hours after a 30-minute onboarding call. Same-week go-live is standard."),
    ],
  },
  {
    'slug': 'hvac-answering-service-sacramento',
    'industry': 'hvac',
    'city': 'Sacramento',
    'state': 'CA',
    'title': 'HVAC Answering Service in Sacramento, CA | Calling Matrix',
    'meta_desc': "Sacramento summers hit 110°F. Calling Matrix answers every AC emergency call 24/7 — routes to your on-call tech, books tune-ups, handles heat dome surge. Live in 48 hours.",
    'og_desc': "Sacramento Valley heat tops 110°F. 24/7 AI answering service for Sacramento HVAC companies — routes emergencies, books tune-ups, no voicemail.",
    'parent_name': 'HVAC AI Receptionist',
    'parent_url': 'https://callingmatrix.com/hvac',
    'local_service_desc': '24/7 AI answering service for HVAC companies in Sacramento, CA. Answers every AC emergency call, routes to on-call techs, and books tune-ups automatically.',
    'eyebrow': 'Built for Sacramento HVAC companies',
    'h1': 'Sacramento summers are relentless.<br>Your calls <span class="italic accent">shouldn\'t suffer.</span>',
    'hero_sub': "Sacramento Valley heat regularly tops 110°F. When AC fails mid-afternoon in July, homeowners don't leave voicemails — they call until someone picks up. Calling Matrix answers every call <strong>24/7</strong> and routes emergencies to your on-call tech instantly.",
    'stat1_num': '67%',
    'stat1_lbl': 'of HVAC calls happen after 6 PM',
    'stat2_num': '$380',
    'stat2_lbl': 'Average job value per missed call',
    'stat3_num': '<2s',
    'stat3_lbl': 'Answer time, every time',
    'pain_label': 'The problem',
    'pain_title': 'Sacramento competitors are answering.<br><span class="italic">You\'re missing the peak-season surge.</span>',
    'pain1_num': '63%',
    'pain1_h3': 'of after-hours calls go straight to voicemail',
    'pain1_p': "Sacramento homeowners in a heat dome don't wait for callbacks. They call three companies and book whoever picks up first.",
    'pain2_num': '$4.2k',
    'pain2_h3': 'Lost per week during Sacramento heat dome',
    'pain2_p': "Missing 3 calls a day during a Sacramento summer heat spike adds up fast. One month of Calling Matrix costs less than a single missed job.",
    'pain3_num': '2 min',
    'pain3_h3': 'Before callers move to your Sacramento competitor',
    'pain3_p': "68% of callers move on to the next HVAC company on Google if no one answers within 2 minutes.",
    'pain_link_href': 'https://callingmatrix.blog/hvac-answering-service-cost',
    'pain_link_text': 'How much does an HVAC answering service cost?',
    'feat_label': 'Features',
    'feat_title': 'Built for how Sacramento HVAC<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, pricing, and Sacramento service territory. Handles heat dome surges, emergencies, and routine bookings without missing a call.',
    'feat_html': HVAC_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Sacramento HVAC owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ("Can it handle Sacramento's summer heat dome call spikes?", "Yes. When a heat dome settles over the Central Valley and your call volume triples overnight, Calling Matrix answers every call within 2 seconds. No additional staff, no overflow to voicemail."),
      ('Can it serve the greater Sacramento area including Elk Grove, Folsom, and Roseville?', "Yes. We load your full service territory during onboarding — zip codes, cities, and suburbs — so bookings stay inside your coverage area."),
      ('Does it handle PG&E outage-related HVAC calls?', "Yes. We can configure the AI to address outage situations, explain what to do while power is out, and queue non-emergency bookings for when power is restored."),
      ('Will it book tune-ups and maintenance plans?', "Yes. The AI handles routine tune-up bookings end-to-end and is trained to mention your service agreement options — turning one-time callers into recurring customers."),
      ('How quickly can we go live?', "Most Sacramento HVAC companies are live within 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Stop losing Sacramento jobs to<br><span class="italic">voicemail.</span>',
    'final_p': "See how Sacramento HVAC companies are booking more jobs with an AI receptionist that never takes a day off — not during heat domes, not at 2 AM, not on holidays.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ("Can it handle Sacramento's summer heat dome call spikes?", "Yes. When a heat dome settles over the Central Valley and your call volume triples overnight, Calling Matrix answers every call within 2 seconds -- no additional staff, no overflow to voicemail."),
      ('Can it serve the greater Sacramento area including Elk Grove, Folsom, and Roseville?', "Yes. We load your full service territory during onboarding -- zip codes, cities, and suburbs -- so bookings stay inside your coverage area."),
      ('How quickly can we go live?', "Most Sacramento HVAC companies are live within 48 hours after a 30-minute onboarding call."),
    ],
  },
  {
    'slug': 'hvac-answering-service-houston',
    'industry': 'hvac',
    'city': 'Houston',
    'state': 'TX',
    'title': 'HVAC Answering Service in Houston, TX | Calling Matrix',
    'meta_desc': "Houston HVAC runs 12 months a year. Bilingual AI answering service — answers every call in English and Spanish, routes emergencies 24/7. Live in 48 hours.",
    'og_desc': "Houston HVAC runs year-round. Bilingual AI answering service answers every call in English and Spanish, routes emergencies 24/7.",
    'parent_name': 'HVAC AI Receptionist',
    'parent_url': 'https://callingmatrix.com/hvac',
    'local_service_desc': '24/7 bilingual AI answering service for HVAC companies in Houston, TX. Answers every call in English and Spanish, routes emergencies, and books jobs automatically.',
    'eyebrow': 'Built for Houston HVAC companies',
    'h1': 'Houston HVAC calls answered.<br>English, Spanish, <span class="italic accent">24/7.</span>',
    'hero_sub': "Houston's humidity and year-round heat mean HVAC emergencies happen every month. With a large Spanish-speaking customer base, bilingual answering isn't optional. Calling Matrix answers every call in <strong>English and Spanish</strong>, routes emergencies to your on-call tech, and books jobs automatically.",
    'stat1_num': '67%',
    'stat1_lbl': 'of HVAC calls happen after 6 PM',
    'stat2_num': '$380',
    'stat2_lbl': 'Average job value per missed call',
    'stat3_num': '<2s',
    'stat3_lbl': 'Answer time, every time',
    'pain_label': 'The problem',
    'pain_title': 'Houston callers hang up when no one answers.<br><span class="italic">Bilingual callers hang up faster.</span>',
    'pain1_num': '63%',
    'pain1_h3': 'of after-hours calls go straight to voicemail',
    'pain1_p': "Houston homeowners with broken AC don't wait for callbacks. Spanish-speaking callers who can't get a bilingual answer move on immediately.",
    'pain2_num': '$4.2k',
    'pain2_h3': 'Lost per week in Houston peak season',
    'pain2_p': "Missing just 3 calls a day during Houston summers adds up fast. One month of Calling Matrix costs less than a single missed job.",
    'pain3_num': '2 min',
    'pain3_h3': 'Before callers move to your Houston competitor',
    'pain3_p': "68% of callers move on to the next HVAC company on Google if no one answers within 2 minutes.",
    'pain_link_href': 'https://callingmatrix.blog/hvac-answering-service-cost',
    'pain_link_text': 'How much does an HVAC answering service cost?',
    'feat_label': 'Features',
    'feat_title': 'Built for how Houston HVAC<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Bilingual English/Spanish answering. Trained on your services, pricing, and Houston territory. Handles year-round emergencies and seasonal surges without missing a beat.',
    'feat_html': HVAC_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Houston HVAC owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ('Does it answer in both English and Spanish?', "Yes. Calling Matrix automatically detects the caller's preferred language and answers in English or Spanish. Your bilingual Houston customers get the same quality experience either way."),
      ('Can it handle Harris County and surrounding areas like Sugar Land and The Woodlands?', "Yes. We load your complete service territory during onboarding so the AI books calls inside your area and politely declines calls outside it."),
      ('Does it handle calls after tropical storms and extreme humidity events?', "Yes. Calling Matrix handles any call volume surge — whether from a hurricane aftermath or a heat index day above 110. Every caller gets answered within 2 seconds."),
      ('Will it integrate with our ServiceTitan account?', "Yes. Bookings sync directly to ServiceTitan, Housecall Pro, and Jobber. Jobs appear on your techs' schedules with full customer details the moment they're booked."),
      ('How quickly can a Houston HVAC company go live?', "Most Houston companies are live within 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Stop losing Houston jobs to<br><span class="italic">voicemail.</span>',
    'final_p': "See how Houston HVAC companies are booking more jobs with a bilingual AI receptionist that answers in English and Spanish — 24/7, no exceptions.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ('Does it answer in both English and Spanish?', "Yes. Calling Matrix automatically detects the caller's preferred language and answers in English or Spanish."),
      ('Can it handle Harris County and surrounding areas like Sugar Land and The Woodlands?', "Yes. We load your complete service territory during onboarding so the AI books calls inside your area and politely declines calls outside it."),
      ('How quickly can a Houston HVAC company go live?', "Most Houston companies are live within 48 hours after a 30-minute onboarding call."),
    ],
  },
  {
    'slug': 'hvac-answering-service-phoenix',
    'industry': 'hvac',
    'city': 'Phoenix',
    'state': 'AZ',
    'title': 'HVAC Answering Service in Phoenix, AZ | Calling Matrix',
    'meta_desc': "Phoenix hits 115°F. Your AC calls can't go to voicemail. Calling Matrix answers every HVAC call 24/7 — routes emergencies, books jobs, handles monsoon surge. Live in 48 hours.",
    'og_desc': "Phoenix temperatures hit 115°F. 24/7 AI answering service for Phoenix HVAC — routes emergencies, handles monsoon surge, never voicemail.",
    'parent_name': 'HVAC AI Receptionist',
    'parent_url': 'https://callingmatrix.com/hvac',
    'local_service_desc': '24/7 AI answering service for HVAC companies in Phoenix, AZ. Routes AC emergencies, handles extreme heat and monsoon surge, books jobs automatically.',
    'eyebrow': 'Built for Phoenix HVAC companies',
    'h1': 'Phoenix heat doesn\'t stop.<br>Your calls <span class="italic accent">shouldn\'t either.</span>',
    'hero_sub': "Phoenix temperatures routinely exceed 115°F. An AC failure isn't uncomfortable — it's dangerous. Homeowners call every HVAC company on the list and book whoever answers first. Calling Matrix answers every call <strong>24/7</strong> and routes emergencies to your on-call tech before the caller dials your competitor.",
    'stat1_num': '67%',
    'stat1_lbl': 'of HVAC calls happen after 6 PM',
    'stat2_num': '$380',
    'stat2_lbl': 'Average job value per missed call',
    'stat3_num': '<2s',
    'stat3_lbl': 'Answer time, every time',
    'pain_label': 'The problem',
    'pain_title': 'Phoenix homeowners can\'t wait.<br><span class="italic">Neither can your call volume.</span>',
    'pain1_num': '63%',
    'pain1_h3': 'of after-hours calls go straight to voicemail',
    'pain1_p': "In Phoenix, a broken AC is a health emergency. Homeowners call every company on Google and book the first one that picks up — not the one with the best reviews.",
    'pain2_num': '$4.2k',
    'pain2_h3': 'Lost per week in Phoenix peak season',
    'pain2_p': "Missing just 3 calls a day during Phoenix summer adds up fast. One month of Calling Matrix costs less than a single missed emergency job.",
    'pain3_num': '2 min',
    'pain3_h3': 'Before callers move to your Phoenix competitor',
    'pain3_p': "68% of callers move on to the next HVAC company on Google if no one answers within 2 minutes.",
    'pain_link_href': 'https://callingmatrix.blog/hvac-answering-service-cost',
    'pain_link_text': 'How much does an HVAC answering service cost?',
    'feat_label': 'Features',
    'feat_title': 'Built for how Phoenix HVAC<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, pricing, and Phoenix territory. Handles extreme heat emergencies, monsoon season surges, and routine bookings without missing a beat.',
    'feat_html': HVAC_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Phoenix HVAC owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ('Does it handle Phoenix emergency AC calls differently?', "Yes. When a caller reports no cooling during extreme heat, Calling Matrix treats it as an emergency and immediately texts your on-call tech with the caller's name, address, and issue description. No delays, no voicemail."),
      ('Can it handle Maricopa County including Scottsdale, Tempe, Mesa, and Gilbert?', "Yes. We load your full service territory — zip codes and cities — during onboarding so every booking stays inside your coverage area."),
      ('Does it handle monsoon season calls?', "Yes. Dust storms and monsoon flooding can knock out HVAC systems. Calling Matrix handles the spike in emergency calls without adding staff — every caller gets answered within 2 seconds."),
      ('Will it know our pricing for diagnostic calls and after-hours fees?', "Yes. We load your standard rates, diagnostic fees, and after-hours surcharges during onboarding so callers get accurate pricing without tying up your dispatcher."),
      ('How quickly can a Phoenix HVAC company go live?', "Most Phoenix companies are live in 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Stop losing Phoenix jobs to<br><span class="italic">voicemail.</span>',
    'final_p': "See how Phoenix HVAC companies are booking more jobs with an AI receptionist that answers every call — not during 115-degree heat waves, not at 2 AM, not on holidays.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ('Does it handle Phoenix emergency AC calls differently?', "Yes. When a caller reports no cooling during extreme heat, Calling Matrix treats it as an emergency and immediately texts your on-call tech with the caller's name, address, and issue description. No delays, no voicemail."),
      ('Does it handle monsoon season calls?', "Yes. Calling Matrix handles the spike in emergency calls during monsoon season without adding staff -- every caller gets answered within 2 seconds."),
      ('How quickly can a Phoenix HVAC company go live?', "Most Phoenix companies are live in 48 hours after a 30-minute onboarding call."),
    ],
  },
  # ── PLUMBING ──────────────────────────────────────────────────────────────
  {
    'slug': 'plumbing-answering-service-austin',
    'industry': 'plumbing',
    'city': 'Austin',
    'state': 'TX',
    'title': 'Plumbing Answering Service in Austin, TX | Calling Matrix',
    'meta_desc': "Austin burst pipes don't wait until morning. Calling Matrix is the 24/7 AI answering service for Austin plumbers — routes emergencies, books jobs automatically. Live in 48 hours.",
    'og_desc': "Austin burst pipes don't wait. 24/7 AI answering service for Austin plumbers — routes emergencies, books jobs, never misses a lead.",
    'parent_name': 'Plumbing AI Receptionist',
    'parent_url': 'https://callingmatrix.com/plumbing',
    'local_service_desc': '24/7 AI answering service for plumbing companies in Austin, TX. Routes plumbing emergencies, screens service areas, and books jobs automatically.',
    'eyebrow': 'Built for Austin plumbing companies',
    'h1': 'Austin burst pipes don\'t wait.<br>Every call <span class="italic accent">answered.</span>',
    'hero_sub': "Austin's rapid growth means aging pipes and high-pressure systems failing without warning. When a homeowner has a burst pipe at 11 PM, they call until someone answers. Calling Matrix routes <strong>emergencies to your on-call plumber</strong> and books every non-urgent job automatically.",
    'stat1_num': '71%',
    'stat1_lbl': 'Plumbing emergencies after hours',
    'stat2_num': '$450',
    'stat2_lbl': 'Average job value per answered call',
    'stat3_num': '24/7',
    'stat3_lbl': 'Coverage, no exceptions',
    'pain_label': 'The problem',
    'pain_title': 'Your Austin phone rings while<br><span class="italic">you\'re on a job in Round Rock.</span>',
    'pain1_num': '85%',
    'pain1_h3': 'of after-hours callers book a competitor',
    'pain1_p': "Your on-call plumber can't answer while they're on a job in Round Rock. The Austin homeowner with a burst pipe isn't waiting for a callback — they've already dialed the next plumber on the list.",
    'pain2_num': '$520',
    'pain2_h3': 'Average emergency job value missed',
    'pain2_p': "Every unanswered emergency is revenue walking out the door — straight to the Austin plumber who picked up.",
    'pain3_num': '3x',
    'pain3_h3': 'Higher booking rate with instant answer',
    'pain3_p': "Customers who get answered immediately are 3x more likely to book than those sent to voicemail.",
    'pain_link_href': 'https://callingmatrix.blog/answering-service-for-plumbers',
    'pain_link_text': 'Best answering services for plumbers — what to look for',
    'feat_label': 'Features',
    'feat_title': 'Built for how Austin plumbing<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, service area, and pricing. Routes Austin emergencies, screens callers, and books jobs without interrupting your team.',
    'feat_html': PLUMBING_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Austin plumbing owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ("Can it identify Austin flooding emergencies from heavy spring rains?", "Yes. Calling Matrix listens for urgency indicators — active flooding, water heater failure, sewage backup — and immediately dispatches your on-call plumber with the caller's name, address, and situation."),
      ('Can it serve Greater Austin including Cedar Park, Round Rock, and Pflugerville?', "Yes. We load your full service territory during onboarding so every booking stays inside your coverage area and you never dispatch a tech to an out-of-range address."),
      ('Does it handle HVAC and plumbing combo companies?', "Yes. If you offer both services, we configure the AI to route HVAC and plumbing calls separately, with different intake questions and escalation paths for each."),
      ('Will it book both emergency and non-emergency plumbing calls?', "Yes. Emergency calls are routed to your on-call plumber immediately. Non-urgent calls — clogged drains, faucet repairs, water heater quotes — are booked as scheduled appointments."),
      ('How quickly can an Austin plumbing company go live?', "Most Austin companies are live in 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Your Austin phone rings while<br><span class="italic">you\'re on the job.</span>',
    'final_p': "Let Calling Matrix handle every Austin call. You focus on the work. Every lead turns into a booked job.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ("Can it identify Austin flooding emergencies from heavy spring rains?", "Yes. Calling Matrix listens for urgency indicators -- active flooding, water heater failure, sewage backup -- and immediately dispatches your on-call plumber with the caller's name, address, and situation."),
      ('Can it serve Greater Austin including Cedar Park, Round Rock, and Pflugerville?', "Yes. We load your full service territory during onboarding so every booking stays inside your coverage area."),
      ('How quickly can an Austin plumbing company go live?', "Most Austin companies are live in 48 hours after a 30-minute onboarding call."),
    ],
  },
  {
    'slug': 'plumbing-answering-service-sacramento',
    'industry': 'plumbing',
    'city': 'Sacramento',
    'state': 'CA',
    'title': 'Plumbing Answering Service in Sacramento, CA | Calling Matrix',
    'meta_desc': "Sacramento plumbing emergencies happen at 2 AM. Calling Matrix answers every call 24/7 — routes floods, books jobs, never misses a lead. Live in 48 hours.",
    'og_desc': "Sacramento plumbing emergencies don't wait. 24/7 AI answering service for Sacramento plumbers — routes floods, books jobs, captures every after-hours lead.",
    'parent_name': 'Plumbing AI Receptionist',
    'parent_url': 'https://callingmatrix.com/plumbing',
    'local_service_desc': '24/7 AI answering service for plumbing companies in Sacramento, CA. Routes plumbing emergencies, captures after-hours leads, and books jobs automatically.',
    'eyebrow': 'Built for Sacramento plumbing companies',
    'h1': 'Burst pipes. Midnight floods.<br>Every Sacramento call <span class="italic accent">answered.</span>',
    'hero_sub': "Sacramento homeowners deal with aging infrastructure and seasonal flooding. Midnight burst pipes and slow drains don't wait for office hours. Calling Matrix routes <strong>emergencies to your on-call plumber</strong> and captures every job automatically — including the ones your competitors miss at 2 AM.",
    'stat1_num': '71%',
    'stat1_lbl': 'Plumbing emergencies after hours',
    'stat2_num': '$450',
    'stat2_lbl': 'Average job value per answered call',
    'stat3_num': '24/7',
    'stat3_lbl': 'Coverage, no exceptions',
    'pain_label': 'The problem',
    'pain_title': 'Sacramento calls come in at 2 AM.<br><span class="italic">Your voicemail is costing you jobs.</span>',
    'pain1_num': '85%',
    'pain1_h3': 'of after-hours callers book a competitor',
    'pain1_p': "Your on-call plumber can't answer while they're on a job. The Sacramento homeowner with a burst pipe isn't waiting for a callback — they've already dialed the next plumber.",
    'pain2_num': '$520',
    'pain2_h3': 'Average emergency job value missed',
    'pain2_p': "Sacramento's Pham Plumbing captured 14 after-hours jobs in their first month with Calling Matrix — jobs that had previously gone straight to voicemail.",
    'pain3_num': '3x',
    'pain3_h3': 'Higher booking rate with instant answer',
    'pain3_p': "Customers who get answered immediately are 3x more likely to book than those sent to voicemail.",
    'pain_link_href': 'https://callingmatrix.blog/answering-service-for-plumbers',
    'pain_link_text': 'Best answering services for plumbers — what to look for',
    'feat_label': 'Features',
    'feat_title': 'Built for how Sacramento plumbing<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, service area, and pricing. Routes Sacramento emergencies, screens callers, and books jobs without interrupting your team.',
    'feat_html': PLUMBING_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Sacramento plumbing owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ("Can it route Sacramento flooding emergencies after winter storms?", "Yes. Calling Matrix identifies active flooding, burst pipes, and sewage backups and immediately texts your on-call plumber with the caller's name, address, and situation."),
      ('Can it serve Sacramento including Elk Grove, Rancho Cordova, and Citrus Heights?', "Yes. We load your full service territory during onboarding so every booking stays inside your coverage area."),
      ('Do Sacramento plumbers really get that many after-hours calls?', "Yes. Sacramento's Pham Plumbing captured 14 after-hours jobs in their first month with Calling Matrix — jobs that had previously gone straight to voicemail and been lost to competitors."),
      ('Will it handle drain cleaning and water heater quotes as well as emergencies?', "Yes. The AI handles the full range of plumbing call types — emergency routing for floods and burst pipes, and scheduled booking for non-urgent repairs and quotes."),
      ('How quickly can a Sacramento plumbing company go live?', "Most Sacramento companies are live within 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Your Sacramento phone rings while<br><span class="italic">you\'re on the job.</span>',
    'final_p': "Let Calling Matrix handle every Sacramento call. Every lead turns into a booked job — including the ones that come in at 2 AM.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ("Can it route Sacramento flooding emergencies after winter storms?", "Yes. Calling Matrix identifies active flooding, burst pipes, and sewage backups and immediately texts your on-call plumber with the caller's name, address, and situation."),
      ("Do Sacramento plumbers really get that many after-hours calls?", "Yes. Sacramento's Pham Plumbing captured 14 after-hours jobs in their first month with Calling Matrix -- jobs that had previously gone straight to voicemail and been lost to competitors."),
      ('How quickly can a Sacramento plumbing company go live?', "Most Sacramento companies are live within 48 hours after a 30-minute onboarding call."),
    ],
  },
  {
    'slug': 'plumbing-answering-service-houston',
    'industry': 'plumbing',
    'city': 'Houston',
    'state': 'TX',
    'title': 'Plumbing Answering Service in Houston, TX | Calling Matrix',
    'meta_desc': "Houston floods don't wait. Bilingual AI answering service for Houston plumbers — routes emergencies in English and Spanish, books jobs 24/7. Live in 48 hours.",
    'og_desc': "Houston floods don't wait. Bilingual AI answering service for Houston plumbers — routes emergencies in English and Spanish, books jobs 24/7.",
    'parent_name': 'Plumbing AI Receptionist',
    'parent_url': 'https://callingmatrix.com/plumbing',
    'local_service_desc': '24/7 bilingual AI answering service for plumbing companies in Houston, TX. Routes emergencies in English and Spanish, books jobs automatically.',
    'eyebrow': 'Built for Houston plumbing companies',
    'h1': 'Houston floods don\'t wait.<br>Every call <span class="italic accent">answered.</span>',
    'hero_sub': "Houston flooding events — tropical storms, flash floods, heavy rains — generate emergency plumbing calls around the clock. With a large Spanish-speaking community, bilingual response is essential. Calling Matrix answers in <strong>English and Spanish</strong>, routes emergencies instantly, and books every job automatically.",
    'stat1_num': '71%',
    'stat1_lbl': 'Plumbing emergencies after hours',
    'stat2_num': '$450',
    'stat2_lbl': 'Average job value per answered call',
    'stat3_num': '24/7',
    'stat3_lbl': 'Coverage, no exceptions',
    'pain_label': 'The problem',
    'pain_title': 'Houston callers hang up after 2 rings.<br><span class="italic">Bilingual callers move faster.</span>',
    'pain1_num': '85%',
    'pain1_h3': 'of after-hours callers book a competitor',
    'pain1_p': "Your on-call plumber can't answer while they're on a job. Spanish-speaking callers who can't get a bilingual answer move on immediately.",
    'pain2_num': '$520',
    'pain2_h3': 'Average emergency job value missed',
    'pain2_p': "Every unanswered Houston flood call is revenue walking out the door — straight to the plumber who picked up.",
    'pain3_num': '3x',
    'pain3_h3': 'Higher booking rate with instant answer',
    'pain3_p': "Customers who get answered immediately are 3x more likely to book than those sent to voicemail.",
    'pain_link_href': 'https://callingmatrix.blog/answering-service-for-plumbers',
    'pain_link_text': 'Best answering services for plumbers — what to look for',
    'feat_label': 'Features',
    'feat_title': 'Built for how Houston plumbing<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Bilingual English/Spanish answering. Trained on your services, service area, and Houston territory. Routes flood emergencies and books jobs without interrupting your team.',
    'feat_html': PLUMBING_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Houston plumbing owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ('Does it answer plumbing calls in both English and Spanish?', "Yes. Calling Matrix automatically detects the caller's preferred language and responds fluently in English or Spanish — your entire Houston service area gets the help they need."),
      ('Can it handle Harris County flooding emergency surges?', "Yes. During flood events, Calling Matrix handles any volume spike — 10 calls or 500 — answering every caller within 2 seconds without adding staff."),
      ('Can it serve Greater Houston including Sugar Land, Pasadena, and Baytown?', "Yes. We load your complete service territory during onboarding so bookings stay inside your coverage area and you never dispatch to an out-of-range address."),
      ('Does it integrate with ServiceTitan for Houston commercial plumbing companies?', "Yes. Bookings sync directly to ServiceTitan, Jobber, and Housecall Pro — jobs appear on your techs' schedules with full customer details the moment they're confirmed."),
      ('How quickly can a Houston plumbing company go live?', "Most Houston companies are live in 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Your Houston phone rings while<br><span class="italic">you\'re on the job.</span>',
    'final_p': "Let Calling Matrix handle every Houston call in English and Spanish. Every lead turns into a booked job — no matter when they call.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ('Does it answer plumbing calls in both English and Spanish?', "Yes. Calling Matrix automatically detects the caller's preferred language and responds fluently in English or Spanish."),
      ('Can it handle Harris County flooding emergency surges?', "Yes. During flood events, Calling Matrix handles any volume spike -- 10 calls or 500 -- answering every caller within 2 seconds without adding staff."),
      ('How quickly can a Houston plumbing company go live?', "Most Houston companies are live in 48 hours after a 30-minute onboarding call."),
    ],
  },
  {
    'slug': 'plumbing-answering-service-phoenix',
    'industry': 'plumbing',
    'city': 'Phoenix',
    'state': 'AZ',
    'title': 'Plumbing Answering Service in Phoenix, AZ | Calling Matrix',
    'meta_desc': "Hard water destroys pipes. Monsoon floods fill your voicemail. Calling Matrix answers every Phoenix plumbing call 24/7 — routes emergencies, books jobs automatically. Live in 48 hours.",
    'og_desc': "Phoenix hard water and monsoon floods mean year-round plumbing emergencies. 24/7 AI answering service routes emergencies and books jobs automatically.",
    'parent_name': 'Plumbing AI Receptionist',
    'parent_url': 'https://callingmatrix.com/plumbing',
    'local_service_desc': '24/7 AI answering service for plumbing companies in Phoenix, AZ. Routes monsoon flooding emergencies and hard water repair calls, books jobs automatically.',
    'eyebrow': 'Built for Phoenix plumbing companies',
    'h1': 'Hard water. Monsoon floods.<br>Every call <span class="italic accent">answered.</span>',
    'hero_sub': "Phoenix hard water is relentless on pipes, water heaters, and fixtures. Add monsoon season flooding and you have plumbing emergencies year-round. Calling Matrix routes <strong>emergencies to your on-call plumber</strong> and captures every job automatically — 24/7, no voicemail.",
    'stat1_num': '71%',
    'stat1_lbl': 'Plumbing emergencies after hours',
    'stat2_num': '$450',
    'stat2_lbl': 'Average job value per answered call',
    'stat3_num': '24/7',
    'stat3_lbl': 'Coverage, no exceptions',
    'pain_label': 'The problem',
    'pain_title': 'Phoenix plumbing calls don\'t follow<br><span class="italic">a 9-to-5 schedule.</span>',
    'pain1_num': '85%',
    'pain1_h3': 'of after-hours callers book a competitor',
    'pain1_p': "Your on-call plumber can't answer while they're on a job. Phoenix homeowners dealing with a monsoon-flooded basement aren't waiting for a callback.",
    'pain2_num': '$520',
    'pain2_h3': 'Average emergency job value missed',
    'pain2_p': "Hard water damage and monsoon flood calls are high-value jobs. Every unanswered call is revenue walking straight to your competitor.",
    'pain3_num': '3x',
    'pain3_h3': 'Higher booking rate with instant answer',
    'pain3_p': "Customers who get answered immediately are 3x more likely to book than those sent to voicemail.",
    'pain_link_href': 'https://callingmatrix.blog/answering-service-for-plumbers',
    'pain_link_text': 'Best answering services for plumbers — what to look for',
    'feat_label': 'Features',
    'feat_title': 'Built for how Phoenix plumbing<br><span class="italic">businesses actually work.</span>',
    'feat_sub': 'Trained on your services, service area, and pricing. Routes monsoon emergencies, handles hard water repair calls, and books jobs without interrupting your team.',
    'feat_html': PLUMBING_FEATURES,
    'faq_label': 'FAQ',
    'faq_title': 'Questions Phoenix plumbing owners<br><span class="italic">ask us every day.</span>',
    'faqs': [
      ('Does it handle hard water and water softener calls?', "Yes. We train the AI on your service types — including water softener installation, descaling, and pipe repair from hard water damage — so it can answer questions and book the right job type."),
      ('Can it route Phoenix monsoon flooding emergencies?', "Yes. Calling Matrix identifies flooding emergencies and immediately dispatches your on-call plumber with the caller's name, address, and situation — no delays."),
      ('Can it serve Greater Phoenix including Scottsdale, Tempe, Chandler, and Mesa?', "Yes. We load your full service territory during onboarding so every booking stays inside your coverage area."),
      ('Will it handle slab leak detection calls?', "Yes. Slab leak calls require specific intake — we configure the AI to gather the relevant details so your tech arrives prepared."),
      ('How quickly can a Phoenix plumbing company go live?', "Most Phoenix companies are live in 48 hours after a 30-minute onboarding call."),
    ],
    'final_h2': 'Your Phoenix phone rings while<br><span class="italic">you\'re on the job.</span>',
    'final_p': "Let Calling Matrix handle every Phoenix call. Hard water repairs, monsoon flood emergencies, routine bookings — every lead turns into a booked job.",
    'final_cta': 'Book a free 15-min demo',
    'faq_ld': [
      ('Does it handle hard water and water softener calls?', "Yes. We train the AI on your service types -- including water softener installation, descaling, and pipe repair from hard water damage."),
      ('Can it route Phoenix monsoon flooding emergencies?', "Yes. Calling Matrix identifies flooding emergencies and immediately dispatches your on-call plumber with the caller's name, address, and situation -- no delays."),
      ('How quickly can a Phoenix plumbing company go live?', "Most Phoenix companies are live in 48 hours after a 30-minute onboarding call."),
    ],
  },
]

# ---------------------------------------------------------------------------
# Build helpers
# ---------------------------------------------------------------------------

def esc_json(s):
    """Escape a string for safe embedding in JSON."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')


def build_faq_ld(faqs):
    items = []
    for q, a in faqs:
        items.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (esc_json(q), esc_json(a))
        )
    return ','.join(items)


def build_page(p):
    slug = p['slug']
    canonical = f'https://callingmatrix.com/{slug}'
    breadcrumb_parent_name = p['parent_name']
    breadcrumb_parent_url = p['parent_url']

    schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"Organization","name":"Calling Matrix","url":"https://callingmatrix.com"},'
        '{"@type":"LocalBusiness","name":"Calling Matrix",'
        '"url":"' + canonical + '",'
        '"description":"' + esc_json(p['local_service_desc']) + '",'
        '"areaServed":{"@type":"City","name":"' + p['city'] + '","addressRegion":"' + p['state'] + '"}},'
        '{"@type":"Service","name":"' + esc_json(p['industry'].upper() + ' Answering Service ' + p['city'] + ' ' + p['state']) + '",'
        '"serviceType":"' + p['industry'].upper() + ' Answering Service",'
        '"provider":{"@type":"Organization","name":"Calling Matrix"},'
        '"description":"' + esc_json(p['local_service_desc']) + '",'
        '"areaServed":{"@type":"City","name":"' + p['city'] + '","addressRegion":"' + p['state'] + '"},'
        '"offers":{"@type":"Offer","price":"497","priceCurrency":"USD"}},'
        '{"@type":"FAQPage","mainEntity":[' + build_faq_ld(p['faq_ld']) + ']},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://callingmatrix.com"},'
        '{"@type":"ListItem","position":2,"name":"' + esc_json(breadcrumb_parent_name) + '","item":"' + breadcrumb_parent_url + '"},'
        '{"@type":"ListItem","position":3,"name":"' + esc_json(p['city'] + ' ' + p['industry'].upper()) + '","item":"' + canonical + '"}'
        ']}]}'
    )

    faq_items_html = '\n'.join(
        f'      <div class="faq-item"><div class="faq-q"><span>{q}</span><span class="faq-plus"></span></div>'
        f'<div class="faq-a">{a}</div></div>'
        for q, a in p['faqs']
    )

    html = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">

<title>{p['title']}</title>
<meta name="description" content="{p['meta_desc']}">
<meta name="robots" content="index, follow">
<meta name="author" content="Calling Matrix">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Calling Matrix">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['og_desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://callingmatrix.com/api/og?industry={p['industry']}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p['title']}">
<meta name="twitter:description" content="{p['og_desc']}">
<meta name="twitter:image" content="https://callingmatrix.com/api/og?industry={p['industry']}">

<script type="application/ld+json">{schema}</script>

<script defer src="/_vercel/insights/script.js"></script>
<script src="https://analytics.ahrefs.com/analytics.js" data-key="94z1bOhN7RVx3o2W/eEUbQ" async></script>
<link rel="stylesheet" href="/shared.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="{FONTS_URL}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{FONTS_URL}"></noscript>

</head>
<body>
<a class="skip-nav" href="#main-content">Skip to content</a>

<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="/" class="logo">
      <span class="logo-mark">{LOGO_SVG}</span>
      Calling Matrix
    </a>
    <nav class="nav-links">
      <a href="#features">Features</a>
      <a href="#faq">FAQ</a>
      <a href="/#pricing">Pricing</a>
      <a href="https://callingmatrix.blog">Blog</a>
    </nav>
    <a href="#" class="nav-cta" onclick="openCalendly();return false;">Book a demo</a>
  </div>
</nav>

<header class="hero" id="main-content">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap">
    <span class="eyebrow reveal in"><span class="dot"></span><span>{p['eyebrow']}</span></span>
    <h1 class="hero-title reveal in d1">{p['h1']}</h1>
    <p class="hero-sub reveal in d2">{p['hero_sub']}</p>
    <div class="cta-row reveal in d3">
      <a href="#" class="btn btn-primary" onclick="openCalendly();return false;">
        <span>Book a free 15-min demo</span>
        {ARROW_SVG}
      </a>
      <a href="#features" class="btn btn-ghost">See how it works &rarr;</a>
    </div>
    <div class="hero-stats reveal in d3">
      <div><div class="s-num">{p['stat1_num']}</div><div class="s-lbl">{p['stat1_lbl']}</div></div>
      <div><div class="s-num">{p['stat2_num']}</div><div class="s-lbl">{p['stat2_lbl']}</div></div>
      <div><div class="s-num">{p['stat3_num']}</div><div class="s-lbl">{p['stat3_lbl']}</div></div>
    </div>
  </div>
</header>

<section class="pain">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">{p['pain_label']}</div>
      <h2 class="sec-title">{p['pain_title']}</h2>
    </div>
    <div class="pain-grid">
      <div class="pain-cell reveal in"><div class="big-num">{p['pain1_num']}</div><h3>{p['pain1_h3']}</h3><p>{p['pain1_p']}</p></div>
      <div class="pain-cell reveal in d1"><div class="big-num">{p['pain2_num']}</div><h3>{p['pain2_h3']}</h3><p>{p['pain2_p']}</p></div>
      <div class="pain-cell reveal in d2"><div class="big-num">{p['pain3_num']}</div><h3>{p['pain3_h3']}</h3><p>{p['pain3_p']}</p></div>
    </div>
    <p style="margin-top:28px;font-family:var(--mono);font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:var(--fg-mute);">Further reading &rarr; <a href="{p['pain_link_href']}" style="color:var(--accent);text-decoration:none;transition:opacity .2s;" onmouseover="this.style.opacity='.7'" onmouseout="this.style.opacity='1'">{p['pain_link_text']}</a></p>
  </div>
</section>

<section class="features" id="features">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">{p['feat_label']}</div>
      <h2 class="sec-title">{p['feat_title']}</h2>
      <p class="sec-sub">{p['feat_sub']}</p>
    </div>
    {p['feat_html']}
  </div>
</section>

<section class="faq" id="faq">
  <div class="wrap">
    <div class="sec-head reveal in">
      <div class="sec-label">{p['faq_label']}</div>
      <h2 class="sec-title">{p['faq_title']}</h2>
    </div>
    <div class="faq-list">
{faq_items_html}
    </div>
  </div>
</section>

<section class="final">
  <div class="wrap inner">
    <h2 class="reveal in">{p['final_h2']}</h2>
    <p class="reveal in d1">{p['final_p']}</p>
    <a href="#" class="btn btn-primary reveal in d2" onclick="openCalendly();return false;">
      <span>{p['final_cta']}</span>
      {ARROW_SVG}
    </a>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="foot-inner">
      <div class="foot-brand">
        <a href="/" class="logo" style="font-family:var(--serif);font-size:20px;display:flex;align-items:center;gap:8px;">
          <span class="logo-mark">{LOGO_SVG}</span>
          Calling Matrix
        </a>
        <p>24/7 AI receptionist for home service businesses. Answer every call. Book every job.</p>
      </div>
      <div class="foot-col">
        <h6>Industries</h6>
        <a href="/hvac">HVAC</a>
        <a href="/plumbing">Plumbing</a>
        <a href="/electrical">Electrical</a>
        <a href="/roofing">Roofing</a>
        <a href="/cleaning">Cleaning</a>
      </div>
      <div class="foot-col">
        <h6>Product</h6>
        <a href="/#features">Features</a>
        <a href="/#pricing">Pricing</a>
        <a href="/#faq">FAQ</a>
        <a href="/#how">How it works</a>
        <a href="https://callingmatrix.blog">Blog</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 2026 Calling Matrix. All rights reserved.</span>
      <span>callingmatrix.com</span>
    </div>
  </div>
</footer>

{SCRIPTS}
</body></html>'''

    return html


# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

for p in PAGES:
    path = os.path.join(OUT, p['slug'] + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(build_page(p))
    print(f"wrote {p['slug']}.html")

print('\nDone.')
